"""Repository layer for worker persistence."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from agent_runner_backend_v2.models.worker import WorkerRegistry


def get_worker(db: Session, worker_id: str) -> WorkerRegistry | None:
    """Fetch a worker by ID."""
    return db.query(WorkerRegistry).filter(WorkerRegistry.worker_id == worker_id).first()


def list_workers(db: Session) -> list[WorkerRegistry]:
    """List all registered workers."""
    return db.query(WorkerRegistry).all()


def upsert_worker(db: Session, worker: WorkerRegistry) -> WorkerRegistry:
    """Insert or update a worker registration."""
    existing = get_worker(db, worker.worker_id)
    if existing:
        existing.status = worker.status
        existing.worker_label = worker.worker_label
        existing.capabilities = worker.capabilities
        db.flush()
        return existing
    db.add(worker)
    db.flush()
    return worker


def update_heartbeat(
    db: Session,
    worker: WorkerRegistry,
    *,
    status: str,
    current_run_id: str | None = None,
    current_step_run_id: str | None = None,
    heartbeat_time: datetime | None = None,
) -> WorkerRegistry:
    """Update worker heartbeat and current assignment."""
    worker.last_heartbeat = heartbeat_time or datetime.utcnow()
    worker.status = status
    worker.current_run_id = current_run_id
    worker.current_step_run_id = current_step_run_id
    db.flush()
    return worker


def list_stale_workers(db: Session, *, timeout_seconds: int) -> list[WorkerRegistry]:
    """List workers whose last heartbeat exceeds the timeout."""
    from sqlalchemy import text

    cutoff = text(f"NOW() - INTERVAL '{timeout_seconds} seconds'")
    return (
        db.query(WorkerRegistry)
        .filter(
            WorkerRegistry.status == "active",
            WorkerRegistry.last_heartbeat.isnot(None),
            WorkerRegistry.last_heartbeat < cutoff,
        )
        .all()
    )
