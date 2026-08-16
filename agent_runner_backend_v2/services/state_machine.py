"""V2 State Machine Engine — the single authority for run state transitions.

Every state mutation in the backend goes through this module. It computes
the next (run_status, current_step, action_requested) given the current
state, an event, and the workflow definition.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import workflow_repository
from agent_runner_backend_v2.models.run import WorkflowRun
from agent_runner_backend_v2.models.workflow import WorkflowDefinition


# ---------------------------------------------------------------------------
# Run status constants
# ---------------------------------------------------------------------------

class RunStatus(str, Enum):
    # Actor-prefixed statuses — track who/what initiated the action
    USER_SUBMITTED = "USER_SUBMITTED"
    USER_APPROVED = "USER_APPROVED"
    USER_REJECTED = "USER_REJECTED"
    USER_RESUMED = "USER_RESUMED"
    USER_RETRIED = "USER_RETRIED"
    USER_CANCELLED = "USER_CANCELLED"
    # Internal workflow statuses
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_FOR_HUMAN_APPROVAL = "WAITING_FOR_HUMAN_APPROVAL"
    AWAITING_INTERVENTION = "AWAITING_INTERVENTION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


TERMINAL_STATUSES = {RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELLED}
NON_TERMINAL_STATUSES = {s for s in RunStatus if s not in TERMINAL_STATUSES}
# Claimable by daemon as EXECUTE_STEP: USER_SUBMITTED (new jobs) + PENDING (next step)
CLAIMABLE_STATUSES = {
    RunStatus.USER_SUBMITTED,
    RunStatus.PENDING,
}
# User action statuses that daemon should process as PROCESS_ACTION
USER_ACTION_STATUSES = {
    RunStatus.USER_APPROVED,
    RunStatus.USER_REJECTED,
    RunStatus.USER_RESUMED,
    RunStatus.USER_RETRIED,
}


# ---------------------------------------------------------------------------
# Action constants
# ---------------------------------------------------------------------------

class Action(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RESUME = "RESUME"
    RETRY = "RETRY"
    CANCEL = "CANCEL"
    FORCE_CANCEL = "FORCE_CANCEL"


# Valid actions per status
VALID_ACTIONS: dict[RunStatus, set[Action]] = {
    RunStatus.USER_SUBMITTED: {Action.CANCEL, Action.FORCE_CANCEL},
    RunStatus.USER_APPROVED: set(),  # Daemon processes this, no further actions
    RunStatus.USER_REJECTED: set(),  # Daemon processes this, no further actions
    RunStatus.USER_RESUMED: set(),  # Daemon processes this, no further actions
    RunStatus.USER_RETRIED: set(),  # Daemon processes this, no further actions
    RunStatus.USER_CANCELLED: set(),  # Terminal-like, no actions
    RunStatus.PENDING: {Action.CANCEL, Action.FORCE_CANCEL},
    RunStatus.RUNNING: {Action.CANCEL, Action.FORCE_CANCEL},
    RunStatus.WAITING_FOR_HUMAN_APPROVAL: {Action.APPROVE, Action.REJECT, Action.CANCEL, Action.FORCE_CANCEL},
    RunStatus.AWAITING_INTERVENTION: {Action.RESUME, Action.RETRY, Action.CANCEL, Action.FORCE_CANCEL},
    RunStatus.COMPLETED: set(),
    RunStatus.FAILED: set(),
    RunStatus.CANCELLED: set(),
}


# ---------------------------------------------------------------------------
# Failure classification (from CLI)
# ---------------------------------------------------------------------------

class FailureClass(str, Enum):
    AUTO_RETRYABLE = "AUTO_RETRYABLE"
    HUMAN_RETRY_REQUIRED = "HUMAN_RETRY_REQUIRED"
    FATAL = "FATAL"


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class EventType(str, Enum):
    STEP_CLAIMED = "STEP_CLAIMED"
    STEP_OUTCOME = "STEP_OUTCOME"
    ACTION_REQUESTED = "ACTION_REQUESTED"
    ACTION_CONSUMED = "ACTION_CONSUMED"
    STEP_RESET = "STEP_RESET"


@dataclass
class TransitionEvent:
    """An event that triggers a state transition."""
    event_type: EventType
    # For STEP_OUTCOME:
    outcome: str | None = None          # "approved" | "rejected" | "failed"
    failure_class: str | None = None    # FailureClass value or None
    # For ACTION_REQUESTED:
    action: str | None = None           # Action value
    feedback: str | None = None
    # For STEP_RESET:
    target_step: str | None = None


# ---------------------------------------------------------------------------
# Transition result
# ---------------------------------------------------------------------------

@dataclass
class TransitionResult:
    """The outcome of a state transition."""
    run_status: str
    current_step_name: str | None = None
    current_step_run_id: str | None = None
    action_requested: str | None = None
    clear_action: bool = False
    cancel_requested: str | None = None  # "graceful" or "force"
    refine_iterations: dict[str, int] = field(default_factory=dict)
    error: str | None = None

    @property
    def is_error(self) -> bool:
        return self.error is not None


# ---------------------------------------------------------------------------
# Core transition function
# ---------------------------------------------------------------------------

def transition(
    db: Session,
    run: WorkflowRun,
    event: TransitionEvent,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """Compute the next state given (current_state, event, workflow_rules).

    This is the ONLY function that determines state transitions.
    All service methods call this function.
    """
    status = RunStatus(run.run_status)

    if event.event_type == EventType.STEP_CLAIMED:
        return _handle_claim(status, run)

    if event.event_type == EventType.STEP_OUTCOME:
        return _handle_outcome(db, status, run, event, workflow)

    if event.event_type == EventType.ACTION_REQUESTED:
        return _handle_action_requested(db, status, run, event, workflow)

    if event.event_type == EventType.ACTION_CONSUMED:
        return _handle_action_consumed(db, status, run, event, workflow)

    if event.event_type == EventType.STEP_RESET:
        return _handle_step_reset(status, run, event)

    return TransitionResult(
        run_status=run.run_status,
        error=f"Unknown event type: {event.event_type}",
    )


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------

def _handle_claim(status: RunStatus, run: WorkflowRun) -> TransitionResult:
    """Daemon claims a run → set RUNNING."""
    if status not in CLAIMABLE_STATUSES:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Cannot claim: run_status is {status.value}, expected USER_SUBMITTED or PENDING",
        )
    # For USER_SUBMITTED and PENDING, action_requested should not be set
    pending_action = run.action_requested or None
    if pending_action is not None:
        return TransitionResult(
            run_status=run.run_status,
            error="Cannot claim: action_requested is set",
        )
    return TransitionResult(run_status=RunStatus.RUNNING.value)


def _handle_outcome(
    db: Session,
    status: RunStatus,
    run: WorkflowRun,
    event: TransitionEvent,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """CLI reports step outcome → backend computes next state."""
    if status != RunStatus.RUNNING:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Cannot report outcome: run_status is {status.value}, expected RUNNING",
        )

    outcome = (event.outcome or "").lower()

    if outcome == "approved":
        return _handle_approved(db, run, workflow)

    if outcome == "rejected":
        return _handle_rejected(db, run, event, workflow)

    if outcome == "failed":
        return TransitionResult(
            run_status=RunStatus.AWAITING_INTERVENTION.value,
            current_step_name=run.current_step_name,
        )

    return TransitionResult(
        run_status=run.run_status,
        error=f"Unknown outcome: {event.outcome}",
    )


def _handle_approved(
    db: Session,
    run: WorkflowRun,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """Step approved — check review gate, then advance or complete."""
    current_step = workflow_repository.get_step_by_name(
        db, workflow_id=workflow.id, step_name=run.current_step_name,
    )

    # Check if this step has a review gate
    if current_step and current_step.requires_human_approval:
        return TransitionResult(
            run_status=RunStatus.WAITING_FOR_HUMAN_APPROVAL.value,
            current_step_name=run.current_step_name,
        )

    # Advance to next step
    return _advance_to_next_step(db, run, workflow)


def _handle_rejected(
    db: Session,
    run: WorkflowRun,
    event: TransitionEvent,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """Step rejected — check refine loop, then classify failure."""
    current_step = workflow_repository.get_step_by_name(
        db, workflow_id=workflow.id, step_name=run.current_step_name,
    )

    # Check refine loop
    if current_step:
        refine_config = current_step.raw_config.get("on_reject_refine") or {}
        max_iterations = refine_config.get("max_iterations", 0)
        refine_step = refine_config.get("step")  # Key is "step" in workflow.toml

        if refine_step and max_iterations > 0:
            iterations = run.refine_iterations.get(run.current_step_name, 0)
            if iterations < max_iterations:
                new_iterations = dict(run.refine_iterations)
                new_iterations[run.current_step_name] = iterations + 1
                return TransitionResult(
                    run_status=RunStatus.PENDING.value,
                    current_step_name=refine_step,
                    refine_iterations=new_iterations,
                )

            # Refine exhausted — human intervention required
            return TransitionResult(
                run_status=RunStatus.AWAITING_INTERVENTION.value,
                current_step_name=run.current_step_name,
            )

    # No refine loop — classify by failure_class
    fc = event.failure_class
    if fc == FailureClass.AUTO_RETRYABLE or fc == "AUTO_RETRYABLE":
        return TransitionResult(
            run_status=RunStatus.PENDING.value,
            current_step_name=run.current_step_name,
        )

    if fc == FailureClass.HUMAN_RETRY_REQUIRED or fc == "HUMAN_RETRY_REQUIRED":
        return TransitionResult(
            run_status=RunStatus.AWAITING_INTERVENTION.value,
            current_step_name=run.current_step_name,
        )

    # FATAL or unknown — human intervention required (never auto-FAILED)
    return TransitionResult(
        run_status=RunStatus.AWAITING_INTERVENTION.value,
        current_step_name=run.current_step_name,
    )


def _handle_action_requested(
    db: Session,
    status: RunStatus,
    run: WorkflowRun,
    event: TransitionEvent,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """Console requests an action — validate and set action_requested."""
    import structlog
    logger = structlog.get_logger(__name__)
    
    action = event.action
    logger.info("handle_action_requested", action=action, status=status.value, run_action_requested=run.action_requested)

    # Validate action is a known value
    try:
        action_enum = Action(action)
    except ValueError:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Unknown action: {action}",
        )

    # Validate action is valid for current status
    valid = VALID_ACTIONS.get(status, set())
    if action_enum not in valid:
        logger.info("handle_action_requested_invalid", action=action, status=status.value, valid=list(valid))
        return TransitionResult(
            run_status=run.run_status,
            error=f"Action {action} is not valid for status {status.value}",
        )

    # Check no existing pending action (unless it's the same action being confirmed)
    # Treat empty string same as None (both mean "no pending action")
    pending_action = run.action_requested or None
    if pending_action is not None:
        if pending_action == action:
            logger.info("handle_action_requested_same_action", action=action)
            # Same action being confirmed — allow it (consume the action)
            pass
        else:
            logger.info("handle_action_requested_different_pending", pending=pending_action, requested=action)
            return TransitionResult(
                run_status=run.run_status,
                error=f"Action {pending_action} already pending",
            )

    # Cancel is immediate — both types go to CANCELLED, but the flag
    # tells the daemon how to handle running children.
    if action_enum == Action.CANCEL:
        return TransitionResult(
            run_status=RunStatus.USER_CANCELLED.value,
            clear_action=True,
            cancel_requested="graceful",
        )

    if action_enum == Action.FORCE_CANCEL:
        return TransitionResult(
            run_status=RunStatus.USER_CANCELLED.value,
            clear_action=True,
            cancel_requested="force",
        )

    # Map actions to USER_* statuses — daemon will pick these up and process them
    # This implements the "pair action" principle: backend sets status, daemon updates job.json
    # Keep action_requested set so report_outcome knows it's an action consumption
    action_to_status = {
        Action.APPROVE: RunStatus.USER_APPROVED,
        Action.REJECT: RunStatus.USER_REJECTED,
        Action.RESUME: RunStatus.USER_RESUMED,
        Action.RETRY: RunStatus.USER_RETRIED,
    }

    if action_enum in action_to_status:
        new_status = action_to_status[action_enum]
        logger.info("handle_action_requested_set_user_status", action=action, new_status=new_status.value)
        return TransitionResult(
            run_status=new_status.value,
            action_requested=action,  # Keep action_requested for report_outcome to detect
        )

    logger.info("handle_action_requested_unknown_action", action=action)
    return TransitionResult(
        run_status=run.run_status,
        error=f"Unhandled action: {action}",
    )


def _handle_action_consumed(
    db: Session,
    status: RunStatus,
    run: WorkflowRun,
    event: TransitionEvent,
    workflow: WorkflowDefinition,
) -> TransitionResult:
    """Daemon processed the action — compute next state."""
    action = run.action_requested
    if not action:
        return TransitionResult(
            run_status=run.run_status,
            error="No action to consume",
        )

    try:
        action_enum = Action(action)
    except ValueError:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Unknown action: {action}",
        )

    if action_enum == Action.APPROVE:
        return _advance_to_next_step(db, run, workflow, clear_action=True)

    if action_enum == Action.REJECT:
        return _handle_rejected(db, run, event, workflow)

    if action_enum == Action.RESUME:
        return _advance_to_next_step(db, run, workflow, clear_action=True)

    if action_enum == Action.RETRY:
        new_iterations = dict(run.refine_iterations)
        new_iterations.pop(run.current_step_name, None)
        return TransitionResult(
            run_status=RunStatus.PENDING.value,
            current_step_name=run.current_step_name,
            clear_action=True,
            refine_iterations=new_iterations,
        )

    return TransitionResult(
        run_status=run.run_status,
        error=f"Unhandled action: {action}",
    )


def _handle_step_reset(
    status: RunStatus,
    run: WorkflowRun,
    event: TransitionEvent,
) -> TransitionResult:
    """Console resets the current step."""
    if status in TERMINAL_STATUSES:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Cannot reset: run is terminal ({status.value})",
        )

    return TransitionResult(
        run_status=RunStatus.PENDING.value,
        current_step_name=event.target_step,
        clear_action=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _advance_to_next_step(
    db: Session,
    run: WorkflowRun,
    workflow: WorkflowDefinition,
    *,
    clear_action: bool = False,
) -> TransitionResult:
    """Advance to the next step, or complete if no next step."""
    next_step = workflow_repository.get_next_step_name(
        db, workflow_id=workflow.id, current_step_name=run.current_step_name,
    )

    if next_step:
        return TransitionResult(
            run_status=RunStatus.PENDING.value,
            current_step_name=next_step,
            clear_action=clear_action,
        )

    return TransitionResult(
        run_status=RunStatus.COMPLETED.value,
        clear_action=clear_action,
    )


def get_valid_actions(run: WorkflowRun) -> list[str]:
    """Return the list of valid actions for a run's current status."""
    status = RunStatus(run.run_status)
    valid = VALID_ACTIONS.get(status, set())
    return sorted(a.value for a in valid)
