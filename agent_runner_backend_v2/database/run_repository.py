"""Repository layer for workflow run and step-run persistence."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.models.run import (
    WorkflowArtifact,
    WorkflowEvent,
    WorkflowRun,
    WorkflowStepRun,
)


def get_run_by_id(db: Session, run_id: str) -> WorkflowRun | None:
    """Fetch a workflow run by its primary key."""
    return db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()


def get_run_by_code(db: Session, run_code: str) -> WorkflowRun | None:
    """Fetch a workflow run by its run_code."""
    return db.query(WorkflowRun).filter(WorkflowRun.run_code == run_code).first()


def list_runs(
    db: Session,
    *,
    run_status: str | None = None,
    statuses: list[str] | None = None,
    worker_id: str | None = None,
    workflow_name: str | None = None,
) -> list[WorkflowRun]:
    """List workflow runs with optional filters, ordered by creation date descending."""
    query = db.query(WorkflowRun)
    if run_status:
        query = query.filter(WorkflowRun.run_status == run_status)
    if statuses:
        query = query.filter(WorkflowRun.run_status.in_(statuses))
    if worker_id:
        query = query.filter(
            (WorkflowRun.target_worker_id == worker_id)
            | (WorkflowRun.claimed_by_worker == worker_id)
        )
    if workflow_name:
        query = query.join(WorkflowRun.workflow_definition).filter(
            WorkflowRun.workflow_definition.has(name=workflow_name)
        )
    return query.order_by(WorkflowRun.created_at.desc()).all()


def list_claimable_runs(db: Session, *, worker_id: str) -> list[WorkflowRun]:
    """List runs available for claim by a worker as EXECUTE_STEP.

    Returns runs where run_status IN (USER_SUBMITTED, PENDING) AND action_requested IS NULL
    AND cancel_requested IS NULL (cancelled runs are not claimable).
    """
    return (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.run_status.in_(["USER_SUBMITTED", "PENDING"]),
            WorkflowRun.action_requested.is_(None),
            WorkflowRun.cancel_requested.is_(None),
        )
        .order_by(WorkflowRun.created_at.asc())
        .all()
    )


def list_action_pending_runs(db: Session, *, worker_id: str | None = None) -> list[WorkflowRun]:
    """List runs with a pending user action (PROCESS_ACTION).

    These are runs where the user has requested an action (approve, reject, etc.)
    and the status has been set to USER_* to signal the daemon to process it.

    Returns runs where run_status IN (USER_APPROVED, USER_REJECTED, USER_RESUMED, USER_RETRIED).
    """
    return (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.run_status.in_(["USER_APPROVED", "USER_REJECTED", "USER_RESUMED", "USER_RETRIED"]),
        )
        .order_by(WorkflowRun.created_at.asc())
        .all()
    )


def list_force_cancelled_runs(db: Session, *, worker_id: str) -> list[WorkflowRun]:
    """List runs with force-cancel pending, claimed by this worker."""
    return (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.cancel_requested == "force",
            WorkflowRun.claimed_by_worker == worker_id,
        )
        .all()
    )


def create_run(db: Session, run: WorkflowRun) -> WorkflowRun:
    """Insert a new workflow run."""
    db.add(run)
    db.flush()
    return run


def update_run_status(
    db: Session,
    run: WorkflowRun,
    *,
    run_status: str,
    current_step_name: str | None = None,
    current_step_run_id: str | None = None,
    action_requested: str | None = None,
    clear_action: bool = False,
) -> WorkflowRun:
    """Update a run's state machine fields."""
    run.run_status = run_status
    if current_step_name is not None and current_step_name != run.current_step_name:
        run.current_step_name = current_step_name
        run.current_step_run_id = None  # Clear stale step_run reference on step change
    if current_step_run_id is not None:
        run.current_step_run_id = current_step_run_id
    if clear_action:
        run.action_requested = None
        run.action_feedback = None
    elif action_requested is not None:
        run.action_requested = action_requested
    db.flush()
    return run


def get_step_run_by_id(db: Session, step_run_id: str) -> WorkflowStepRun | None:
    """Fetch a step run by its primary key."""
    return db.query(WorkflowStepRun).filter(WorkflowStepRun.id == step_run_id).first()


def create_step_run(db: Session, step_run: WorkflowStepRun) -> WorkflowStepRun:
    """Insert a new step run."""
    db.add(step_run)
    db.flush()
    return step_run


def update_step_run(
    db: Session,
    step_run: WorkflowStepRun,
    *,
    step_status: str | None = None,
    step_outcome: str | None = None,
    error_message: str | None = None,
) -> WorkflowStepRun:
    """Update step run fields."""
    if step_status is not None:
        step_run.step_status = step_status
    if step_outcome is not None:
        step_run.step_outcome = step_outcome
    if error_message is not None:
        step_run.error_message = error_message
    db.flush()
    return step_run


def create_artifact(db: Session, artifact: WorkflowArtifact) -> WorkflowArtifact:
    """Insert a new artifact."""
    db.add(artifact)
    db.flush()
    return artifact


def create_event(db: Session, event: WorkflowEvent) -> WorkflowEvent:
    """Insert a new event."""
    db.add(event)
    db.flush()
    return event
