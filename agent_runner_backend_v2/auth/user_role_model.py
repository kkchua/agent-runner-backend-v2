"""User role model for DB-backed role management."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String

from agent_runner_backend_v2.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class UserRole(Base):
    """Maps a Supabase auth user to an application role."""

    __tablename__ = "user_roles"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(300), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default="viewer")
    is_system = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=_utcnow)
    updated_at = Column(DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)


class UserWorker(Base):
    """Many-to-many assignment of workers to users."""

    __tablename__ = "user_workers"

    user_id = Column(String(36), ForeignKey("user_roles.user_id", ondelete="CASCADE"), primary_key=True)
    worker_id = Column(String(80), primary_key=True)
