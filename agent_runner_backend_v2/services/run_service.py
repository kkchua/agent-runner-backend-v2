"""Run service — orchestration layer for workflow run lifecycle.

Sits between API routes and repositories. Calls the state machine for
all transitions. Never uses db.query() directly — goes through repositories.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import run_repository, workflow_repository
from agent_runner_backend_v2.models.run import (
    WorkflowArtifact,
    WorkflowEvent,
    WorkflowRun,
    WorkflowStepRun,
)
from agent_runner_backend_v2.models.workflow import WorkflowDefinition
from agent_runner_backend_v2.services.state_machine import (
    EventType,
    RunStatus,
    TransitionEvent,
    get_valid_actions,
    transition,
)


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _generate_run_code(db: Session, prefix: str) -> str:
    """Generate a unique run code with the given prefix."""
    import random
    import string
    for _ in range(100):
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        code = f"{prefix}-{suffix}"
        if not run_repository.get_run_by_code(db, code):
            return code
    raise RuntimeError("Failed to generate unique run code after 100 attempts")


def submit_run(
    db: Session,
    *,
    workflow_name: str,
    worker_id: str | None = None,
    project_root: str | None = None,
    workspace_path: str | None = None,
    input_payload: dict | None = None,
    start_step: str | None = None,
) -> WorkflowRun:
    """Submit a new workflow run.

    Creates the run in SUBMITTED status with the workflow's init step.
    If start_step is provided, overrides the init step.
    """
    workflow = workflow_repository.get_workflow_by_name(db, workflow_name)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail=f"Workflow '{workflow_name}' is not active")

    run_code = _generate_run_code(db, workflow.job_prefix)
    init_step = start_step or workflow.init_step

    run = WorkflowRun(
        run_code=run_code,
        workflow_definition_id=workflow.id,
        run_status=RunStatus.SUBMITTED.value,
        current_step_name=init_step,
        target_worker_id=worker_id,
        worker_label="live",
        project_root=project_root,
        workspace_path=workspace_path,
        input_payload=input_payload or {},
    )
    run_repository.create_run(db, run)

    # Create initial event
    event = WorkflowEvent(
        workflow_run_id=run.id,
        event_type="RUN_SUBMITTED",
        message=f"Run submitted for workflow {workflow_name}",
    )
    run_repository.create_event(db, event)

    return run


def claim_work(
    db: Session,
    *,
    worker_id: str,
) -> dict | None:
    """Claim the next available work for a worker.

    Returns a dict with work_type, run, step_run, and execution_spec.
    Returns None if no work is available.

    Checks for:
    1. Action-pending runs (PROCESS_ACTION)
    2. Claimable runs (EXECUTE_STEP)
    """
    # Check for action-pending runs first
    action_runs = run_repository.list_action_pending_runs(db, worker_id=worker_id)
    if action_runs:
        run = action_runs[0]
        workflow = run.workflow_definition

        # Transition to RUNNING for action processing
        run_repository.update_run_status(db, run, run_status="RUNNING")
        run.claimed_by_worker = worker_id
        run.started_at = utcnow()

        step_run = _get_or_create_step_run(db, run, workflow)

        return {
            "work_type": "PROCESS_ACTION",
            "run": run,
            "step_run": step_run,
            "workflow": workflow,
            "action": run.action_requested,
            "feedback": run.action_feedback,
        }

    # Check for claimable runs
    claimable = run_repository.list_claimable_runs(db, worker_id=worker_id)
    if not claimable:
        return None

    run = claimable[0]
    workflow = run.workflow_definition

    # Transition to RUNNING
    result = transition(db, run, TransitionEvent(event_type=EventType.STEP_CLAIMED), workflow)
    if result.is_error:
        return None

    run_repository.update_run_status(
        db, run,
        run_status=result.run_status,
        current_step_name=result.current_step_name or run.current_step_name,
    )
    run.claimed_by_worker = worker_id
    run.started_at = utcnow()

    step_run = _get_or_create_step_run(db, run, workflow)

    return {
        "work_type": "EXECUTE_STEP",
        "run": run,
        "step_run": step_run,
        "workflow": workflow,
    }


def report_outcome(
    db: Session,
    *,
    step_run_id: str,
    outcome: str,
    failure_class: str | None = None,
    artifacts: dict | None = None,
    review: dict | None = None,
    error_message: str | None = None,
    usage_summary: dict | None = None,
) -> WorkflowRun:
    """Report a step outcome and compute the next state via the state machine.

    This is the key endpoint: CLI reports what happened, backend decides what's next.
    """
    step_run = run_repository.get_step_run_by_id(db, step_run_id)
    if not step_run:
        raise HTTPException(status_code=404, detail=f"Step run {step_run_id} not found")

    run = run_repository.get_run_by_id(db, step_run.workflow_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found for step run")

    workflow = run.workflow_definition

    # Update step run
    run_repository.update_step_run(
        db, step_run,
        step_status="completed" if outcome != "failed" else "failed",
        step_outcome=outcome,
        error_message=error_message,
    )
    step_run.completed_at = utcnow()
    if usage_summary:
        step_run.usage_summary = usage_summary

    # Create artifacts
    if artifacts:
        for key, path in artifacts.items():
            art = WorkflowArtifact(
                workflow_run_id=run.id,
                workflow_step_run_id=step_run.id,
                artifact_key=key,
                file_path=path,
            )
            run_repository.create_artifact(db, art)

    # Transition via state machine
    # If action_requested is set, this is an action consumption, not a step outcome
    if run.action_requested:
        event = TransitionEvent(
            event_type=EventType.ACTION_CONSUMED,
            outcome=outcome,
            failure_class=failure_class,
        )
    else:
        event = TransitionEvent(
            event_type=EventType.STEP_OUTCOME,
            outcome=outcome,
            failure_class=failure_class,
        )
    result = transition(db, run, event, workflow)

    if result.is_error:
        raise HTTPException(status_code=409, detail=result.error)

    # Apply transition result
    run_repository.update_run_status(
        db, run,
        run_status=result.run_status,
        current_step_name=result.current_step_name,
    )
    if result.refine_iterations:
        run.refine_iterations = result.refine_iterations

    # Create event
    evt = WorkflowEvent(
        workflow_run_id=run.id,
        workflow_step_run_id=step_run.id,
        event_type="STEP_OUTCOME",
        message=f"Step {step_run.step_name} outcome: {outcome}",
        payload={"outcome": outcome, "failure_class": failure_class, "next_status": result.run_status},
    )
    run_repository.create_event(db, evt)

    return run


def request_action(
    db: Session,
    *,
    run_id: str,
    action: str,
    feedback: str | None = None,
) -> WorkflowRun:
    """Request an action on a run (approve, reject, resume, retry, cancel).

    Validates the action against the state machine and sets action_requested.
    """
    run = run_repository.get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    workflow = run.workflow_definition

    event = TransitionEvent(
        event_type=EventType.ACTION_REQUESTED,
        action=action,
        feedback=feedback,
    )
    result = transition(db, run, event, workflow)

    if result.is_error:
        if "not valid" in result.error:
            raise HTTPException(status_code=422, detail=result.error)
        if "already pending" in result.error:
            raise HTTPException(status_code=409, detail=result.error)
        raise HTTPException(status_code=400, detail=result.error)

    run_repository.update_run_status(
        db, run,
        run_status=result.run_status,
        action_requested=result.action_requested,
        clear_action=result.clear_action,
    )
    if feedback:
        run.action_feedback = feedback

    # Create event
    evt = WorkflowEvent(
        workflow_run_id=run.id,
        event_type=f"ACTION_{action}",
        message=f"Action {action} requested" + (f": {feedback}" if feedback else ""),
    )
    run_repository.create_event(db, evt)

    return run


def reset_step(
    db: Session,
    *,
    run_id: str,
    step_name: str,
) -> WorkflowRun:
    """Reset a run's current step."""
    run = run_repository.get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    workflow = run.workflow_definition

    event = TransitionEvent(
        event_type=EventType.STEP_RESET,
        target_step=step_name,
    )
    result = transition(db, run, event, workflow)

    if result.is_error:
        raise HTTPException(status_code=400, detail=result.error)

    run_repository.update_run_status(
        db, run,
        run_status=result.run_status,
        current_step_name=result.current_step_name,
        clear_action=result.clear_action,
    )

    return run


def get_run_detail(db: Session, run_id: str) -> dict | None:
    """Get run detail with computed valid_actions."""
    run = run_repository.get_run_by_id(db, run_id)
    if not run:
        return None

    return {
        "run": run,
        "valid_actions": get_valid_actions(run),
    }


def _get_or_create_step_run(
    db: Session,
    run: WorkflowRun,
    workflow: WorkflowDefinition,
) -> WorkflowStepRun:
    """Get the current step run or create a new one."""
    if run.current_step_run_id:
        existing = run_repository.get_step_run_by_id(db, run.current_step_run_id)
        if existing:
            return existing

    # Determine sequence number
    seq = len(run.step_runs) + 1

    step_run = WorkflowStepRun(
        workflow_run_id=run.id,
        step_name=run.current_step_name,
        sequence_no=seq,
        step_status="running",
    )
    run_repository.create_step_run(db, step_run)
    run.current_step_run_id = step_run.id

    return step_run
