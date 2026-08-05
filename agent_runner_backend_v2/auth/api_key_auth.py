"""API key authentication for scripts and machines."""
from __future__ import annotations

from datetime import datetime, timezone

import bcrypt
import structlog
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from agent_runner_backend_v2.auth.models import APIKey
from agent_runner_backend_v2.auth.supabase_auth import UserContext
from agent_runner_backend_v2.database import get_db
from agent_runner_backend_v2.database.api_key_repository import update_last_used

logger = structlog.get_logger()

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_api_key(key: str) -> str:
    """Hash an API key using bcrypt."""
    return bcrypt.hashpw(key.encode(), bcrypt.gensalt()).decode()


def verify_api_key(plain_key: str, key_hash: str) -> bool:
    """Verify a plain API key against a bcrypt hash."""
    return bcrypt.checkpw(plain_key.encode(), key_hash.encode())


def generate_api_key() -> tuple[str, str]:
    """Generate a new API key and return (plain_key, key_hash).

    The plain key should be shown to the user once, then discarded.
    Only the hash is stored in the database.
    """
    import secrets
    plain_key = f"arb_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(plain_key)
    return plain_key, key_hash


def get_api_key_user(
    api_key: str | None = Security(API_KEY_HEADER),
    db=Depends(get_db),
) -> UserContext:
    """FastAPI dependency: authenticate via X-API-Key header.

    Returns a UserContext with the service account's role.
    Raises 401 if the key is missing, invalid, inactive, or expired.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )

    key_prefix = api_key[:11] if len(api_key) >= 11 else api_key[:4]

    from sqlalchemy.orm import Session
    stored_key: APIKey | None = db.query(APIKey).filter(
        APIKey.is_active == True,  # noqa: E712
    ).first()

    found_key: APIKey | None = None
    for candidate in db.query(APIKey).filter(APIKey.is_active == True).all():  # noqa: E712
        if verify_api_key(api_key, candidate.key_hash):
            found_key = candidate
            break

    if found_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    if found_key.expires_at and found_key.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key has expired",
        )

    update_last_used(db, found_key)

    return UserContext(
        user_id=f"apikey:{found_key.id}",
        email=f"{found_key.name}@service",
        role=found_key.role,
        is_service_account=True,
        metadata={"api_key_id": found_key.id, "api_key_name": found_key.name},
    )
