"""Tests for the V2 state machine engine — all transitions, validation, invariants."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import run_repository, workflow_repository
from agent_runner_backend_v2.models.run import WorkflowRun, WorkflowStepRun
from agent_runner_backend_v2.models.workflow import (
    WorkflowDefinition,
    WorkflowStepDefinition,
    WorkflowStepTransition,
)
from agent_runner_backend_v2.services.state_machine import (
    Action,
    EventType,
    FailureClass,
    RunStatus,
    TransitionEvent,
    TransitionResult,
    get_valid_actions,
    transition,
)


def _make_workflow_with_steps(
    db: Session,
    name: str = "sm_test_wf",
    steps: list[dict] | None = None,
) -> WorkflowDefinition:
    """Create a workflow with steps and transitions for testing.

    Default: generate → review → complete
    """
    wf = WorkflowDefinition(name=name, job_prefix="SM", source_hash="sm_hash", init_step="generate")
    workflow_repository.create_workflow(db, wf)

    if steps is None:
        steps = [
            {"step_name": "generate", "step_order": 1, "requires_human_approval": False},
            {"step_name": "review", "step_order": 2, "requires_human_approval": True},
            {"step_name": "complete", "step_order": 3, "requires_human_approval": False},
        ]

    step_defs = []
    for s in steps:
        sd = WorkflowStepDefinition(
            workflow_definition_id=wf.id,
            step_name=s["step_name"],
            step_order=s["step_order"],
            requires_human_approval=s.get("requires_human_approval", False),
            raw_config=s.get("raw_config", {}),
        )
        workflow_repository.create_step_definition(db, sd)
        step_defs.append(sd)

    # Add onsuccess transitions (each step → next step)
    for i, sd in enumerate(step_defs):
        if i + 1 < len(step_defs):
            t = WorkflowStepTransition(
                step_definition_id=sd.id,
                transition_type="onsuccess",
                outcome="approved",
                target_step_name=step_defs[i + 1].step_name,
            )
            workflow_repository.create_transition(db, t)

    return wf


def _make_run(
    db: Session,
    wf: WorkflowDefinition,
    *,
    run_code: str = "SM-JOB-001",
    run_status: str = "SUBMITTED",
    current_step: str = "generate",
    action_requested: str | None = None,
    refine_iterations: dict | None = None,
) -> WorkflowRun:
    run = WorkflowRun(
        run_code=run_code,
        workflow_definition_id=wf.id,
        run_status=run_status,
        current_step_name=current_step,
        action_requested=action_requested,
        refine_iterations=refine_iterations or {},
    )
    return run_repository.create_run(db, run)


# ===========================================================================
# Normal Flow
# ===========================================================================

class TestNormalFlow:
    def test_submitted_to_running_on_claim(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="SUBMITTED")

        result = transition(db_session, run, TransitionEvent(event_type=EventType.STEP_CLAIMED), wf)

        assert result.run_status == "RUNNING"
        assert not result.is_error

    def test_pending_to_running_on_claim(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="PENDING")

        result = transition(db_session, run, TransitionEvent(event_type=EventType.STEP_CLAIMED), wf)

        assert result.run_status == "RUNNING"

    def test_running_to_pending_on_approved_with_next_step(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="generate")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="approved",
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "review"

    def test_running_to_completed_on_approved_no_next_step(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="complete")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="approved",
        ), wf)

        assert result.run_status == "COMPLETED"

    def test_running_to_WAITING_FOR_HUMAN_APPROVAL_on_review_gate(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="review")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="approved",
        ), wf)

        assert result.run_status == "WAITING_FOR_HUMAN_APPROVAL"
        assert result.current_step_name == "review"

    def test_running_to_pending_on_auto_retryable_failure(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="generate")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME,
            outcome="rejected",
            failure_class="AUTO_RETRYABLE",
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "generate"

    def test_running_to_awaiting_intervention_on_human_retry(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="generate")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME,
            outcome="rejected",
            failure_class="HUMAN_RETRY_REQUIRED",
        ), wf)

        assert result.run_status == "AWAITING_INTERVENTION"

    def test_running_to_failed_on_fatal(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="generate")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME,
            outcome="rejected",
            failure_class="FATAL",
        ), wf)

        assert result.run_status == "FAILED"

    def test_running_to_failed_on_step_failed(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="generate")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="failed",
        ), wf)

        assert result.run_status == "FAILED"


# ===========================================================================
# Refine Loop
# ===========================================================================

class TestRefineLoop:
    def _make_refine_workflow(self, db: Session) -> WorkflowDefinition:
        wf = WorkflowDefinition(name="refine_wf", job_prefix="RF", source_hash="rf", default_max_rejects=3)
        workflow_repository.create_workflow(db, wf)

        review = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="review", step_order=1,
            raw_config={"on_reject_refine": {"refine_step": "refine", "max_iterations": 2}},
        )
        workflow_repository.create_step_definition(db, review)

        refine = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="refine", step_order=2,
        )
        workflow_repository.create_step_definition(db, refine)

        # refine → review (loop back)
        t = WorkflowStepTransition(
            step_definition_id=refine.id, transition_type="onsuccess",
            outcome="approved", target_step_name="review",
        )
        workflow_repository.create_transition(db, t)

        return wf

    def test_rejected_with_refine_available(self, db_session: Session):
        wf = self._make_refine_workflow(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING", current_step="review")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="rejected",
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "refine"
        assert result.refine_iterations.get("review") == 1

    def test_rejected_refine_exhausted_to_awaiting_maxretried(self, db_session: Session):
        wf = self._make_refine_workflow(db_session)
        run = _make_run(
            db_session, wf, run_status="RUNNING", current_step="review",
            refine_iterations={"review": 2},  # already at max
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="rejected",
        ), wf)

        assert result.run_status == "AWAITING_MAXRETRIED"


# ===========================================================================
# Human Actions
# ===========================================================================

class TestHumanActions:
    def test_approve_from_WAITING_FOR_HUMAN_APPROVAL(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL",
            current_step="review", action_requested="APPROVE",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_CONSUMED,
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "complete"
        assert result.clear_action is True

    def test_reject_from_WAITING_FOR_HUMAN_APPROVAL(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL",
            current_step="review", action_requested="REJECT",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_CONSUMED,
            outcome="rejected",
            failure_class="HUMAN_RETRY_REQUIRED",
        ), wf)

        assert result.run_status == "AWAITING_INTERVENTION"

    def test_resume_from_awaiting_intervention(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="AWAITING_INTERVENTION",
            current_step="generate", action_requested="RESUME",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_CONSUMED,
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "review"
        assert result.clear_action is True

    def test_retry_from_awaiting_intervention(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="AWAITING_INTERVENTION",
            current_step="generate", action_requested="RETRY",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_CONSUMED,
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "generate"
        assert result.clear_action is True

    def test_cancel_from_WAITING_FOR_HUMAN_APPROVAL(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="CANCEL",
        ), wf)

        assert result.run_status == "CANCELLED"
        assert result.cancel_requested == "graceful"


# ===========================================================================
# Validation
# ===========================================================================

class TestValidation:
    def test_reject_approve_when_not_WAITING_FOR_HUMAN_APPROVAL(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="APPROVE",
        ), wf)

        assert result.is_error
        assert "not valid" in result.error

    def test_reject_action_when_another_action_pending(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL",
            action_requested="APPROVE",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="REJECT",
        ), wf)

        assert result.is_error
        assert "already pending" in result.error

    def test_reject_any_action_on_terminal_status(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="COMPLETED")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="CANCEL",
        ), wf)

        assert result.is_error

    def test_reject_unknown_action(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="RUNNING")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="FLIP",
        ), wf)

        assert result.is_error
        assert "Unknown action" in result.error

    def test_reject_claim_when_action_pending(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="SUBMITTED",
            action_requested="CANCEL",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_CLAIMED,
        ), wf)

        assert result.is_error
        assert "action_requested" in result.error

    def test_reject_outcome_when_not_running(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="PENDING")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_OUTCOME, outcome="approved",
        ), wf)

        assert result.is_error
        assert "expected RUNNING" in result.error

    def test_reject_reset_on_terminal(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="FAILED")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_RESET, target_step="generate",
        ), wf)

        assert result.is_error
        assert "terminal" in result.error


# ===========================================================================
# Invariants
# ===========================================================================

class TestInvariants:
    def test_single_action_enforced(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL",
            action_requested="APPROVE",
        )

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="REJECT",
        ), wf)

        assert result.is_error

    def test_terminal_is_terminal(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)

        for status in ["COMPLETED", "FAILED"]:
            run = _make_run(db_session, wf, run_code=f"TERM-{status}", run_status=status)
            result = transition(db_session, run, TransitionEvent(
                event_type=EventType.STEP_CLAIMED,
            ), wf)
            assert result.is_error

    def test_claim_filter_excludes_action_pending(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(
            db_session, wf, run_code="CLAIM-ACT",
            run_status="SUBMITTED", action_requested="CANCEL",
        )

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 0

    def test_action_requested_preserves_status(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.ACTION_REQUESTED, action="APPROVE",
        ), wf)

        assert result.run_status == "WAITING_FOR_HUMAN_APPROVAL"
        assert result.action_requested == "APPROVE"


# ===========================================================================
# Valid Actions Helper
# ===========================================================================

class TestValidActions:
    def test_submitted_cancel_actions(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="SUBMITTED")
        assert get_valid_actions(run) == ["CANCEL", "FORCE_CANCEL"]

    def test_WAITING_FOR_HUMAN_APPROVAL_actions(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="WAITING_FOR_HUMAN_APPROVAL")
        actions = get_valid_actions(run)
        assert "APPROVE" in actions
        assert "REJECT" in actions
        assert "CANCEL" in actions
        assert "RESUME" not in actions

    def test_awaiting_intervention_actions(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="AWAITING_INTERVENTION")
        actions = get_valid_actions(run)
        assert "RESUME" in actions
        assert "RETRY" in actions
        assert "CANCEL" in actions
        assert "APPROVE" not in actions

    def test_completed_no_actions(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="COMPLETED")
        assert get_valid_actions(run) == []


# ===========================================================================
# Step Reset
# ===========================================================================

class TestStepReset:
    def test_reset_to_different_step(self, db_session: Session):
        wf = _make_workflow_with_steps(db_session)
        run = _make_run(db_session, wf, run_status="AWAITING_INTERVENTION", current_step="review")

        result = transition(db_session, run, TransitionEvent(
            event_type=EventType.STEP_RESET, target_step="generate",
        ), wf)

        assert result.run_status == "PENDING"
        assert result.current_step_name == "generate"
        assert result.clear_action is True
