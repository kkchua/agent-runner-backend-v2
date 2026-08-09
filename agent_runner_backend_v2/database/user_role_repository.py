"""CRUD operations for the user_roles table."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from agent_runner_backend_v2.auth.user_role_model import UserRole


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_or_create_user(db: Session, user_id: str, email: str) -> UserRole:
    """Return the existing user_roles row, or auto-provision one with default role 'viewer'."""
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    if user is None:
        user = UserRole(user_id=user_id, email=email, role="viewer", created_at=_utcnow(), updated_at=_utcnow())
        db.add(user)
        db.flush()
    return user


def get_user_role(db: Session, user_id: str) -> str | None:
    """Return the role string for a user, or None if not found."""
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    return user.role if user else None


def list_users(db: Session) -> list[UserRole]:
    """Return all user_roles entries ordered by email."""
    return db.query(UserRole).order_by(UserRole.email).all()


def update_user_role(db: Session, user_id: str, new_role: str) -> UserRole | None:
    """Update a user's role. Returns the updated row, or None if not found."""
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    if user is None:
        return None
    user.role = new_role
    user.updated_at = _utcnow()
    db.flush()
    return user


def update_user_email(db: Session, user_id: str, email: str) -> UserRole | None:
    """Update a user's email. Returns the updated row, or None if not found."""
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    if user is None:
        return None
    user.email = email
    user.updated_at = _utcnow()
    db.flush()
    return user


def delete_user(db: Session, user_id: str) -> bool:
    """Delete a user_roles entry. Returns True if deleted, False if not found.

    System accounts cannot be deleted — returns False for them.
    """
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    if user is None:
        return False
    if user.is_system:
        return False
    db.delete(user)
    db.flush()
    return True


def is_system_user(db: Session, user_id: str) -> bool:
    """Return True if the user is marked as a system account."""
    user = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    return user.is_system if user else False
