"""Repository layer for API key persistence."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from agent_runner_backend_v2.auth.models import APIKey


def get_api_key_by_id(db: Session, key_id: str) -> APIKey | None:
    """Fetch an API key by its primary key."""
    return db.query(APIKey).filter(APIKey.id == key_id).first()


def get_api_key_by_prefix(db: Session, prefix: str) -> list[APIKey]:
    """Fetch API keys matching a key prefix (for lookup optimization)."""
    return db.query(APIKey).filter(APIKey.key_prefix == prefix).all()


def list_api_keys(db: Session, *, active_only: bool = False) -> list[APIKey]:
    """List all API keys, optionally filtering to active only."""
    query = db.query(APIKey)
    if active_only:
        query = query.filter(APIKey.is_active == True)  # noqa: E712
    return query.order_by(APIKey.created_at.desc()).all()


def create_api_key(
    db: Session,
    *,
    key_hash: str,
    key_prefix: str,
    name: str,
    role: str,
    created_by: str,
    expires_at: datetime | None = None,
) -> APIKey:
    """Insert a new API key."""
    api_key = APIKey(
        key_hash=key_hash,
        key_prefix=key_prefix,
        name=name,
        role=role,
        created_by=created_by,
        expires_at=expires_at,
    )
    db.add(api_key)
    db.flush()
    return api_key


def revoke_api_key(db: Session, api_key: APIKey) -> None:
    """Soft-delete an API key by marking it inactive."""
    api_key.is_active = False
    db.flush()


def update_last_used(db: Session, api_key: APIKey) -> None:
    """Update the last_used_at timestamp."""
    api_key.last_used_at = datetime.now(timezone.utc)
    db.flush()
