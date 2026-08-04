"""API key model for script/machine authentication."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, Text

from agent_runner_backend_v2.database import Base


def _utcnow() -> datetime:
    """Return current UTC time as a naive datetime (for SQLAlchemy default)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class APIKey(Base):
    """An API key for script/machine authentication."""

    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key_hash = Column(Text, nullable=False, unique=True)
    key_prefix = Column(String(8), nullable=False)
    name = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False, default="service-account")
    created_by = Column(String(200), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=_utcnow)
    last_used_at = Column(DateTime, nullable=True)
