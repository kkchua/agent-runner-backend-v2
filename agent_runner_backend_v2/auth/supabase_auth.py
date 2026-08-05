"""Supabase JWT validation and user context."""
from __future__ import annotations

from dataclasses import dataclass, field

import httpx
import jwt
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWK

from agent_runner_backend_v2.config import settings

logger = structlog.get_logger()

security = HTTPBearer(auto_error=False)

# Cached public keys: kid -> public key object
_public_keys: dict[str, object] = {}


def preload_jwks() -> None:
    """Fetch and cache Supabase JWKS public keys at startup.

    This avoids blocking the async event loop during request handling.
    Retries up to 3 times on failure.
    """
    global _public_keys
    jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            resp = httpx.get(
                jwks_url,
                headers={"apikey": settings.SUPABASE_ANON_KEY},
                timeout=10,
            )
            resp.raise_for_status()
            jwks = resp.json()

            for key_data in jwks.get("keys", []):
                kid = key_data.get("kid")
                if kid:
                    jwk = PyJWK(key_data)
                    _public_keys[kid] = jwk.key

            logger.info("jwks_preloaded", num_keys=len(_public_keys), attempt=attempt)
            return
        except Exception as exc:
            last_error = exc
            logger.warning("jwks_preload_attempt_failed", attempt=attempt, error=str(exc))
            if attempt < 3:
                import time
                time.sleep(2 * attempt)

    logger.error("jwks_preload_failed_all_retries", error=str(last_error))


def decode_supabase_token(token: str) -> dict:
    """Decode and validate a Supabase JWT token using cached public keys or JWT secret fallback."""
    # Extract kid from token header
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token header: {exc}",
        )

    kid = header.get("kid")
    alg = header.get("alg", "ES256")

    # Try JWKS public key first (ES256)
    if kid and alg == "ES256":
        # Lazy-load JWKS keys if not cached yet
        if not _public_keys:
            logger.info("jwks_lazy_reload_triggered")
            preload_jwks()

        public_key = _public_keys.get(kid)
        if public_key:
            try:
                payload = jwt.decode(
                    token,
                    public_key,
                    algorithms=["ES256"],
                    options={"verify_aud": False, "verify_iat": False, "leeway": 300},
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
            except jwt.InvalidTokenError as exc:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {exc}")

    # Fallback: HS256 with SUPABASE_JWT_SECRET
    if settings.SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False, "verify_iat": False, "leeway": 300},
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            pass  # Fall through to error below

    # No validation method succeeded
    if kid and not _public_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWKS keys not loaded (key ID: {kid}). Restart server to refresh keys.",
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate token with available keys.",
    )


def _extract_role(payload: dict) -> str:
    """Extract the user role from JWT payload metadata."""
    user_metadata = payload.get("user_metadata", {})
    return user_metadata.get("role", "viewer")


@dataclass
class UserContext:
    """Authenticated user context extracted from JWT or API key."""

    user_id: str
    email: str
    role: str
    is_service_account: bool = False
    metadata: dict = field(default_factory=dict)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserContext:
    """FastAPI dependency: extract user from Bearer JWT."""
    if credentials is None:
        logger.warning("auth_no_bearer_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    token = credentials.credentials
    # Diagnostic: log token header (without exposing the full token)
    try:
        header = jwt.get_unverified_header(token)
        logger.info("auth_token_header", kid=header.get("kid"), alg=header.get("alg"), cached_kids=list(_public_keys.keys()))
    except Exception:
        pass
    payload = decode_supabase_token(token)
    user_id = payload.get("sub", "")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
    return UserContext(
        user_id=user_id,
        email=payload.get("email", ""),
        role=_extract_role(payload),
        metadata=payload.get("user_metadata", {}),
    )
