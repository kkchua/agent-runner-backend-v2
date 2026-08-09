"""Repository layer for user-worker assignment persistence."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.auth.user_role_model import UserWorker


def assign_worker(db: Session, user_id: str, worker_id: str) -> UserWorker:
    """Assign a worker to a user. Idempotent — skips if already assigned."""
    existing = (
        db.query(UserWorker)
        .filter(UserWorker.user_id == user_id, UserWorker.worker_id == worker_id)
        .first()
    )
    if existing:
        return existing
    assignment = UserWorker(user_id=user_id, worker_id=worker_id)
    db.add(assignment)
    db.flush()
    return assignment


def unassign_worker(db: Session, user_id: str, worker_id: str) -> bool:
    """Remove a worker assignment. Returns True if deleted, False if not found."""
    rows = (
        db.query(UserWorker)
        .filter(UserWorker.user_id == user_id, UserWorker.worker_id == worker_id)
        .delete()
    )
    db.flush()
    return rows > 0


def get_user_worker_ids(db: Session, user_id: str) -> list[str]:
    """Get all worker IDs assigned to a user."""
    rows = db.query(UserWorker.worker_id).filter(UserWorker.user_id == user_id).all()
    return [r[0] for r in rows]


def set_user_workers(db: Session, user_id: str, worker_ids: list[str]) -> list[str]:
    """Replace all worker assignments for a user. Returns the final list of worker IDs."""
    db.query(UserWorker).filter(UserWorker.user_id == user_id).delete()
    for wid in worker_ids:
        db.add(UserWorker(user_id=user_id, worker_id=wid))
    db.flush()
    return worker_ids
