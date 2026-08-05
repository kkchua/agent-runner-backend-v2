"""Role-based access control dependencies."""
from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from agent_runner_backend_v2.auth.supabase_auth import (
    UserContext,
    _extract_role,
    decode_supabase_token,
)

_bearer_scheme = HTTPBearer(auto_error=False)
_api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def _user_from_bearer(bearer: HTTPAuthorizationCredentials) -> UserContext:
    """Extract user context from a Bearer JWT token."""
    payload = decode_supabase_token(bearer.credentials)
    user_id = payload.get("sub", "")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )
    return UserContext(
        user_id=user_id,
        email=payload.get("email", ""),
        role=_extract_role(payload),
        is_service_account=False,
        metadata=payload.get("user_metadata", {}),
    )


def _user_from_api_key(api_key: str) -> UserContext | None:
    """Validate an API key and return user context, or None if invalid."""
    from datetime import datetime, timezone

    from agent_runner_backend_v2.auth.api_key_auth import verify_api_key
    from agent_runner_backend_v2.auth.models import APIKey
    from agent_runner_backend_v2.database import SessionLocal
    from agent_runner_backend_v2.database.api_key_repository import update_last_used

    db = SessionLocal()
    try:
        for candidate in db.query(APIKey).filter(APIKey.is_active == True).all():  # noqa: E712
            if verify_api_key(api_key, candidate.key_hash):
                if candidate.expires_at and candidate.expires_at < datetime.now(timezone.utc):
                    return None
                update_last_used(db, candidate)
                db.commit()
                return UserContext(
                    user_id=f"apikey:{candidate.id}",
                    email=f"{candidate.name}@service",
                    role=candidate.role,
                    is_service_account=True,
                    metadata={"api_key_id": candidate.id, "api_key_name": candidate.name},
                )
        return None
    finally:
        db.close()


def require_role(*allowed_roles: str) -> Callable:
    """FastAPI dependency factory: require the user to have one of the specified roles.

    Usage:
        @router.get("/admin-only")
        def admin_endpoint(user: UserContext = Depends(require_role("admin"))):
            ...
    """
    allowed = set(allowed_roles)

    def _check_role(
        bearer: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    ) -> UserContext:
        if bearer is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        user = _user_from_bearer(bearer)
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' is not authorized. Required: {allowed_roles}",
            )
        return user

    return _check_role


def require_jwt_or_api_key(*allowed_roles: str) -> Callable:
    """FastAPI dependency factory: accept either JWT or API key, then check role.

    This is the main dependency for endpoints that should support both
    browser users (JWT) and scripts (API key).
    """
    allowed = set(allowed_roles)

    def _check(
        bearer: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
        api_key: str | None = Depends(_api_key_scheme),
    ) -> UserContext:
        user: UserContext | None = None

        if bearer is not None:
            try:
                user = _user_from_bearer(bearer)
            except HTTPException as exc:
                import structlog
                structlog.get_logger().warning("auth_bearer_failed", status=exc.status_code, detail=exc.detail)
                raise
        elif api_key is not None:
            user = _user_from_api_key(api_key)

        if user is None:
            import structlog
            structlog.get_logger().warning("auth_no_credentials", has_bearer=bearer is not None, has_api_key=api_key is not None)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated. Provide Bearer token or X-API-Key header.",
            )

        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' is not authorized. Required: {allowed_roles}",
            )

        return user

    return _check
