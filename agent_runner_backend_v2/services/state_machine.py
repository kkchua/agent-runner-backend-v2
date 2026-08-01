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
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    AWAITING_INTERVENTION = "AWAITING_INTERVENTION"
    AWAITING_MAXRETRIED = "AWAITING_MAXRETRIED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


TERMINAL_STATUSES = {RunStatus.COMPLETED, RunStatus.FAILED}
NON_TERMINAL_STATUSES = {s for s in RunStatus if s not in TERMINAL_STATUSES}
CLAIMABLE_STATUSES = {RunStatus.SUBMITTED, RunStatus.PENDING}


# ---------------------------------------------------------------------------
# Action constants
# ---------------------------------------------------------------------------

class Action(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RESUME = "RESUME"
    RETRY = "RETRY"
    CANCEL = "CANCEL"


# Valid actions per status
VALID_ACTIONS: dict[RunStatus, set[Action]] = {
    RunStatus.SUBMITTED: {Action.CANCEL},
    RunStatus.PENDING: {Action.CANCEL},
    RunStatus.RUNNING: {Action.CANCEL},
    RunStatus.AWAITING_APPROVAL: {Action.APPROVE, Action.REJECT, Action.CANCEL},
    RunStatus.AWAITING_INTERVENTION: {Action.RESUME, Action.RETRY, Action.CANCEL},
    RunStatus.AWAITING_MAXRETRIED: {Action.RESUME, Action.RETRY, Action.CANCEL},
    RunStatus.COMPLETED: set(),
    RunStatus.FAILED: set(),
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
        return _handle_action_requested(status, run, event)

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
            error=f"Cannot claim: run_status is {status.value}, expected SUBMITTED or PENDING",
        )
    if run.action_requested is not None:
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
        return TransitionResult(run_status=RunStatus.FAILED.value)

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
            run_status=RunStatus.AWAITING_APPROVAL.value,
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
        refine_step = refine_config.get("refine_step")

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

            # Refine exhausted — check replan
            replan_config = current_step.raw_config.get("on_exhaust_replan") or {}
            replan_step = replan_config.get("replan_step")
            if replan_step:
                return TransitionResult(
                    run_status=RunStatus.PENDING.value,
                    current_step_name=replan_step,
                )

            # All exhausted
            return TransitionResult(
                run_status=RunStatus.AWAITING_MAXRETRIED.value,
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

    # FATAL or unknown
    return TransitionResult(run_status=RunStatus.FAILED.value)


def _handle_action_requested(
    status: RunStatus,
    run: WorkflowRun,
    event: TransitionEvent,
) -> TransitionResult:
    """Console requests an action — validate and set action_requested."""
    action = event.action

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
        return TransitionResult(
            run_status=run.run_status,
            error=f"Action {action} is not valid for status {status.value}",
        )

    # Check no existing pending action
    if run.action_requested is not None:
        return TransitionResult(
            run_status=run.run_status,
            error=f"Action {run.action_requested} already pending",
        )

    # Cancel is immediate
    if action_enum == Action.CANCEL:
        return TransitionResult(
            run_status=RunStatus.FAILED.value,
            clear_action=True,
        )

    # Other actions: set action_requested, status unchanged
    return TransitionResult(
        run_status=run.run_status,
        action_requested=action,
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
