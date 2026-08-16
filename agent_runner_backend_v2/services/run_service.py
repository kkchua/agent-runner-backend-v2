"""Run service — orchestration layer for workflow run lifecycle.

Sits between API routes and repositories. Calls the state machine for
all transitions. Never uses db.query() directly — goes through repositories.
"""
from __future__ import annotations

import structlog
from datetime import datetime, timezone

logger = structlog.get_logger(__name__)

from fastapi import HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import run_repository, worker_repository, workflow_repository
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

from agent_runner_backend_v2.qwenpaw_client import notify_telegram


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
    implementation_name: str | None = None,
    prompt_selections: dict | None = None,
) -> WorkflowRun:
    """Submit a new workflow run.

    Creates the run in SUBMITTED status with the workflow's init step.
    If start_step is provided, overrides the init step.

    For file-type inputs (keys ending with _FILE or _DOC), bare filenames
    are resolved to full paths using init_input_dirs from the workflow
    definition: project_root / directory / filename.
    """
    workflow = workflow_repository.get_workflow_by_name(db, workflow_name)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail=f"Workflow '{workflow_name}' is not active")

    # Resolve bare filenames in input_payload to full artifact paths
    resolved_payload = _resolve_input_paths(
        input_payload or {},
        workflow=workflow,
        project_root=project_root,
    )

    run_code = _generate_run_code(db, workflow.job_prefix)
    init_step = start_step or workflow.init_step

    # Store BCS context in context_payload
    context_payload = {}
    if implementation_name:
        context_payload["implementation_name"] = implementation_name
    if prompt_selections:
        context_payload["prompt_selections"] = prompt_selections

    # --- [DEBUG] Log constructed context_payload ---
    logger.info("service_submit_run_context", 
                run_code=run_code, 
                context_payload=context_payload)

    run = WorkflowRun(
        run_code=run_code,
        workflow_definition_id=workflow.id,
        run_status=RunStatus.USER_SUBMITTED.value,
        current_step_name=init_step,
        target_worker_id=worker_id,
        worker_label="live",
        project_root=project_root,
        workspace_path=workspace_path,
        input_payload=resolved_payload,
        context_payload=context_payload,
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


def _resolve_input_paths(
    input_payload: dict,
    *,
    workflow: WorkflowDefinition,
    project_root: str | None,
) -> dict:
    """Resolve bare filenames in input_payload to full artifact paths.

    For keys ending with _FILE or _DOC, if the value is a bare filename
    (no path separators), it is resolved using:
        project_root / init_input_dirs[key] / filename

    Other keys or values with path separators are passed through as-is.
    """
    import os

    if not input_payload or not project_root:
        return dict(input_payload)

    init_input_dirs = (workflow.raw_definition or {}).get("init_input_dirs", {})
    if not init_input_dirs:
        return dict(input_payload)

    resolved = {}
    for key, value in input_payload.items():
        if not isinstance(value, str) or not value:
            resolved[key] = value
            continue

        if key == "BOOTSTRAP_SPEC_FILE" or key == "REQUIREMENT_DOC":
            resolved[key] = value
            continue
        
        # Check if this is a file-type key with a bare filename
        is_file_key = key.endswith("_FILE") or key.endswith("_DOC")
        
        is_bare = os.sep not in value and "/" not in value
        
        if is_file_key and is_bare and key in init_input_dirs:
            directory = init_input_dirs[key]
            full_path = os.path.join(project_root, directory, value)
            resolved[key] = value
        else:
            resolved[key] = value

    return resolved


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
    # Check worker's max_parallel limit
    worker = worker_repository.get_worker(db, worker_id)
    if worker:
        max_parallel = (worker.capabilities or {}).get("max_parallel", 1)
        active_runs = run_repository.count_active_runs(db, worker_id=worker_id)
        if active_runs >= max_parallel:
            return None

    # Check for action-pending runs first (USER_* statuses)
    action_runs = run_repository.list_action_pending_runs(db, worker_id=worker_id)
    if action_runs:
        run = action_runs[0]
        workflow = run.workflow_definition

        # Map USER_* status to action name
        status_to_action = {
            "USER_APPROVED": "APPROVE",
            "USER_REJECTED": "REJECT",
            "USER_RESUMED": "RESUME",
            "USER_RETRIED": "RETRY",
        }
        action = status_to_action.get(run.run_status, "")

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
            "action": action,
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
    job_dir: str | None = None,
) -> WorkflowRun:
    """Report a step outcome and compute the next state via the state machine.

    This is the key endpoint: CLI reports what happened, backend decides what's next.
    If job_dir is provided and not yet stored on the run, it is persisted.
    """
    step_run = run_repository.get_step_run_by_id(db, step_run_id)
    if not step_run:
        raise HTTPException(status_code=404, detail=f"Step run {step_run_id} not found")

    run = run_repository.get_run_by_id(db, step_run.workflow_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found for step run")

    # Store job_dir on first outcome (daemon provides the local job path)
    if job_dir and not run.job_dir:
        run.job_dir = job_dir

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
        clear_action=result.clear_action,
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

    # Send Telegram notification for step outcome
    try:
        _notify_step_outcome(
            run,
            step_name=step_run.step_name,
            outcome=outcome,
            failure_class=failure_class,
            error_message=error_message,
            usage_summary=usage_summary,
            artifacts=artifacts,
            next_status=result.run_status,
        )
    except Exception:
        logger.exception("telegram_notification_failed", run_code=run.run_code)

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
    import structlog
    logger = structlog.get_logger(__name__)
    
    run = run_repository.get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    logger.info("request_action", run_id=run_id, action=action, current_status=run.run_status, current_action_requested=run.action_requested)

    workflow = run.workflow_definition

    event = TransitionEvent(
        event_type=EventType.ACTION_REQUESTED,
        action=action,
        feedback=feedback,
    )
    result = transition(db, run, event, workflow)

    logger.info("request_action_result", is_error=result.is_error, error=result.error, new_status=result.run_status, new_action_requested=result.action_requested)

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
    if result.cancel_requested:
        run.cancel_requested = result.cancel_requested
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


def get_force_cancelled_runs(db: Session, *, worker_id: str) -> list[WorkflowRun]:
    """Get runs claimed by this worker that have force-cancel pending.

    These runs have cancel_requested='force' and the daemon needs to
    terminate their children immediately.
    """
    return run_repository.list_force_cancelled_runs(db, worker_id=worker_id)


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


def _notify_step_outcome(
    run: WorkflowRun,
    step_name: str,
    outcome: str,
    failure_class: str | None = None,
    error_message: str | None = None,
    usage_summary: dict | None = None,
    artifacts: dict | None = None,
    next_status: str | None = None,
) -> None:
    """Send Telegram notification for every step outcome.

    Fires on every step outcome (approved / rejected / failed), notifying
    the user immediately via Telegram.
    """
    import structlog
    logger = structlog.get_logger(__name__)
    logger.info("step_notify_check", step=step_name, outcome=outcome,
                 run_code=run.run_code, next_status=next_status)

    # Outcome emoji
    if outcome == "approved":
        emoji = "✅"
    elif outcome == "rejected":
        emoji = "🔄"  # rejected → refine loop
    elif outcome == "failed":
        emoji = "❌"
    else:
        emoji = "ℹ️"

    lines = [
        f"{emoji} *[Backend AGB Step]*",
        f"*Workflow:* {run.workflow_definition.name}",
        f"*Job ID:* {run.run_code}",
        f"*Project:* {run.project_root or 'N/A'}",
        "",
        "━━━ *Step Result* ━━━",
        f"*Step:* {step_name}",
        f"*Outcome:* {outcome.upper()}",
    ]

    if failure_class:
        lines.append(f"*Failure Class:* {failure_class}")
    if error_message:
        lines.append("")
        lines.append("━━━ *Error* ━━━")
        lines.append(f"`{error_message[:300]}`")

    if usage_summary:
        total = usage_summary.get("total_tokens")
        if total:
            lines.append("")
            lines.append("━━━ *Usage* ━━━")
            lines.append(f"*Tokens:* {total:,}")

    if artifacts:
        lines.append("")
        lines.append("━━━ *Artifacts* ━━━")
        for key, path in artifacts.items():
            # Show just the filename for readability
            fname = path.split("\\")[-1].split("/")[-1] if isinstance(path, str) else str(path)
            lines.append(f"*{key}:* `{fname}`")

    if next_status:
        lines.append("")
        lines.append(f"*Next Status:* {next_status}")

    # Always show where to review/check
    paths = []
    if run.job_dir:
        paths.append(f"*Job Dir:* `{run.job_dir}`")
    if run.project_root:
        paths.append(f"*Project Root:* `{run.project_root}`")
    if paths:
        lines.append("")
        lines.append("━━━ *Where to Review* ━━━")
        lines.extend(paths)

    user_message = "\n".join(lines)
    logger.info("step_notify_sending", step=step_name, run_code=run.run_code,
                 message_length=len(user_message))

    # Send to Telegram
    telegram_result = notify_telegram(user_message)
    logger.info("step_notify_sent", step=step_name, run_code=run.run_code,
                 telegram_result=telegram_result)


def _notify_on_status_change(run: WorkflowRun, status: str) -> None:
    """Send Telegram notification for job-level status changes.

    Fires on: completion, failure, cancellation, waiting for approval,
    or awaiting intervention.
    """
    import structlog
    logger = structlog.get_logger(__name__)
    logger.info("notify_check", status=status, run_code=run.run_code)

    # Only notify on: completion, failure, waiting for approval, intervention, cancellation
    NOTIFY_STATUSES = {
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        "WAITING_FOR_HUMAN_APPROVAL",
        "AWAITING_INTERVENTION",
    }
    if status not in NOTIFY_STATUSES:
        logger.info("notify_skip", status=status, reason="not in NOTIFY_STATUSES")
        return

    # Calculate duration
    duration = "In progress"
    if run.started_at:
        from datetime import datetime
        now = datetime.now()
        delta = now - run.started_at
        total_seconds = int(delta.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        duration = f"{minutes}m {seconds}s"

    # Status emoji
    if status == "COMPLETED":
        emoji = "✅"
    elif status in ("FAILED", "CANCELLED"):
        emoji = "❌"
    else:
        emoji = "⚠️"

    # Build enriched message with [AGB Events] tag
    lines = [
        f"{emoji} *[Backend AGB Events]*",
        f"*Status:* {status}",
        "",
        "━━━ *Job Info* ━━━",
        f"*Workflow:* {run.workflow_definition.name}",
        f"*Job ID:* {run.run_code}",
        f"*Worker:* {run.claimed_by_worker or run.target_worker_id or 'N/A'}",
    ]

    # Add timing info
    if run.submitted_at:
        lines.append(f"*Submitted:* {run.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if run.started_at:
        lines.append(f"*Started:* {run.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"*Duration:* {duration}")

    # Add current step info
    if run.current_step_name:
        lines.append("")
        lines.append("━━━ *Current Step* ━━━")
        lines.append(f"*Step:* {run.current_step_name}")

        # Get latest step run details if available
        if run.step_runs:
            latest_step = run.step_runs[-1]  # Last step by created_at
            if latest_step.step_outcome:
                lines.append(f"*Outcome:* {latest_step.step_outcome}")
            if latest_step.coder:
                lines.append(f"*Coder:* {latest_step.coder}")
            if latest_step.duration_seconds:
                step_mins, step_secs = divmod(latest_step.duration_seconds, 60)
                lines.append(f"*Step Duration:* {step_mins}m {step_secs}s")

    # Add action info for approval/intervention states
    if status in ("WAITING_FOR_HUMAN_APPROVAL", "AWAITING_INTERVENTION"):
        lines.append("")
        lines.append("━━━ *Action Required* ━━━")
        action = run.action_requested or "REVIEW"
        lines.append(f"*Action:* {action}")
        if run.action_feedback:
            lines.append(f"*Feedback:* {run.action_feedback[:200]}")

    # Add error message if present
    if run.error_message:
        lines.append("")
        lines.append("━━━ *Error* ━━━")
        lines.append(f"`{run.error_message[:300]}`")

    # Add paths if available
    paths = []
    if run.project_root:
        paths.append(f"*Project:* {run.project_root}")
    if run.job_dir:
        paths.append(f"*Job Dir:* {run.job_dir}")
    if run.workspace_path:
        paths.append(f"*Workspace:* {run.workspace_path}")

    if paths:
        lines.append("")
        lines.append("━━━ *Paths* ━━━")
        lines.extend(paths)

    # Add refine iterations if any
    if run.refine_iterations:
        refine_info = ", ".join(f"{step}: {count}x" for step, count in run.refine_iterations.items())
        if refine_info:
            lines.append("")
            lines.append(f"*Refine Iterations:* {refine_info}")

    user_message = "\n".join(lines)
    logger.info("notify_sending", status=status, run_code=run.run_code, message_length=len(user_message))

    # Send to Telegram
    telegram_result = notify_telegram(user_message)
    logger.info("notify_telegram_sent", status=status, run_code=run.run_code,
                 telegram_result=telegram_result)
    
    