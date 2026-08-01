"""Worker service — orchestration for worker lifecycle."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import worker_repository
from agent_runner_backend_v2.models.worker import WorkerRegistry


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def register_worker(
    db: Session,
    *,
    worker_id: str,
    worker_label: str = "live",
    capabilities: dict | None = None,
    host_id: str | None = None,
) -> WorkerRegistry:
    """Register or update a worker."""
    worker = WorkerRegistry(
        worker_id=worker_id,
        host_id=host_id,
        status="active",
        worker_label=worker_label,
        capabilities=capabilities or {},
    )
    return worker_repository.upsert_worker(db, worker)


def heartbeat(
    db: Session,
    *,
    worker_id: str,
    status: str = "idle",
    current_run_id: str | None = None,
    current_step_run_id: str | None = None,
) -> WorkerRegistry | None:
    """Update worker heartbeat."""
    worker = worker_repository.get_worker(db, worker_id)
    if not worker:
        return None

    return worker_repository.update_heartbeat(
        db, worker,
        status=status,
        current_run_id=current_run_id,
        current_step_run_id=current_step_run_id,
        heartbeat_time=utcnow(),
    )


def stop_worker(db: Session, *, worker_id: str) -> bool:
    """Mark a worker as stopped."""
    worker = worker_repository.get_worker(db, worker_id)
    if not worker:
        return False
    worker.status = "stopped"
    db.flush()
    return True
