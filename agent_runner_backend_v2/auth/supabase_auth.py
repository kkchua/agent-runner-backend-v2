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
    """
    global _public_keys
    jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
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
                # Convert JWK to a public key object using PyJWT
                jwk = PyJWK(key_data)
                _public_keys[kid] = jwk.key

        logger.info("jwks_preloaded", num_keys=len(_public_keys))
    except Exception as exc:
        logger.error("jwks_preload_failed", error=str(exc))


def decode_supabase_token(token: str) -> dict:
    """Decode and validate a Supabase JWT token using cached public keys."""
    # Extract kid from token header
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token header: {exc}",
        )

    kid = header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'kid' header",
        )

    public_key = _public_keys.get(kid)
    if not public_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unknown key ID: {kid}. Restart server to refresh keys.",
        )

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["ES256"],
            options={
                "verify_aud": False,
                "leeway": 30,
            },
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    payload = decode_supabase_token(credentials.credentials)
    user_id = payload.get("sub", "")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
    return UserContext(
        user_id=user_id,
        email=payload.get("email", ""),
        role=_extract_role(payload),
        metadata=payload.get("user_metadata", {}),
    )
