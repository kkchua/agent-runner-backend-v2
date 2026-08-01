"""Tests for service layer — run_service, worker_service, workflow_service."""
from __future__ import annotations

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import run_repository, worker_repository, workflow_repository
from agent_runner_backend_v2.models.run import WorkflowRun
from agent_runner_backend_v2.models.worker import WorkerRegistry
from agent_runner_backend_v2.services import run_service, worker_service, workflow_service


def _seed_workflow(db: Session, name: str = "svc_test_wf") -> dict:
    """Seed a workflow definition via the service."""
    definition = {
        "job_prefix": "SVC",
        "init_step": "generate",
        "default_max_rejects": 3,
        "steps": {
            "generate": {
                "step_order": 1,
                "onsuccess": "review",
            },
            "review": {
                "step_order": 2,
                "requires_human_approval_after": True,
                "onsuccess": "complete",
            },
            "complete": {
                "step_order": 3,
            },
        },
    }
    workflow_service.sync_workflow(db, workflow_name=name, definition=definition)
    return definition


# ===========================================================================
# Run Service
# ===========================================================================

class TestSubmitRun:
    def test_submit_creates_run_in_submitted(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")

        assert run.run_status == "SUBMITTED"
        assert run.current_step_name == "generate"
        assert run.run_code.startswith("SVC-")

    def test_submit_with_start_step_override(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(
            db_session, workflow_name="svc_test_wf", start_step="review",
        )

        assert run.current_step_name == "review"

    def test_submit_unknown_workflow_raises(self, db_session: Session):
        with pytest.raises(HTTPException) as exc_info:
            run_service.submit_run(db_session, workflow_name="nonexistent")
        assert exc_info.value.status_code == 404

    def test_submit_with_worker_and_project(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(
            db_session,
            workflow_name="svc_test_wf",
            worker_id="w1",
            project_root="/workspace",
        )

        assert run.target_worker_id == "w1"
        assert run.project_root == "/workspace"


class TestClaimWork:
    def test_claim_returns_execute_step(self, db_session: Session):
        _seed_workflow(db_session)
        run_service.submit_run(db_session, workflow_name="svc_test_wf")

        work = run_service.claim_work(db_session, worker_id="w1")

        assert work is not None
        assert work["work_type"] == "EXECUTE_STEP"
        assert work["run"].run_status == "RUNNING"
        assert work["run"].claimed_by_worker == "w1"

    def test_claim_returns_none_when_no_work(self, db_session: Session):
        work = run_service.claim_work(db_session, worker_id="w1")
        assert work is None

    def test_claim_skips_action_pending(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        # Simulate: run is awaiting approval with action
        run_repository.update_run_status(
            db_session, run,
            run_status="AWAITING_APPROVAL",
            action_requested="APPROVE",
        )

        work = run_service.claim_work(db_session, worker_id="w1")

        # Should return PROCESS_ACTION, not EXECUTE_STEP
        assert work is not None
        assert work["work_type"] == "PROCESS_ACTION"
        assert work["action"] == "APPROVE"


class TestReportOutcome:
    def test_approved_advances_step(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        work = run_service.claim_work(db_session, worker_id="w1")

        result_run = run_service.report_outcome(
            db_session,
            step_run_id=work["step_run"].id,
            outcome="approved",
        )

        assert result_run.run_status == "PENDING"
        assert result_run.current_step_name == "review"

    def test_approved_at_review_gate_goes_to_awaiting(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        # Claim and complete first step
        work = run_service.claim_work(db_session, worker_id="w1")
        run_service.report_outcome(db_session, step_run_id=work["step_run"].id, outcome="approved")
        # Claim second step (review)
        work2 = run_service.claim_work(db_session, worker_id="w1")

        result_run = run_service.report_outcome(
            db_session,
            step_run_id=work2["step_run"].id,
            outcome="approved",
        )

        assert result_run.run_status == "AWAITING_APPROVAL"

    def test_completed_when_last_step_approved(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        # Advance to complete step
        run_repository.update_run_status(
            db_session, run, run_status="RUNNING", current_step_name="complete",
        )
        step_run = run_service._get_or_create_step_run(db_session, run, run.workflow_definition)

        result_run = run_service.report_outcome(
            db_session,
            step_run_id=step_run.id,
            outcome="approved",
        )

        assert result_run.run_status == "COMPLETED"

    def test_auto_retryable_stays_pending(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        work = run_service.claim_work(db_session, worker_id="w1")

        result_run = run_service.report_outcome(
            db_session,
            step_run_id=work["step_run"].id,
            outcome="rejected",
            failure_class="AUTO_RETRYABLE",
        )

        assert result_run.run_status == "PENDING"
        assert result_run.current_step_name == "generate"

    def test_fatal_goes_to_failed(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        work = run_service.claim_work(db_session, worker_id="w1")

        result_run = run_service.report_outcome(
            db_session,
            step_run_id=work["step_run"].id,
            outcome="rejected",
            failure_class="FATAL",
        )

        assert result_run.run_status == "FAILED"

    def test_artifacts_created(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        work = run_service.claim_work(db_session, worker_id="w1")

        run_service.report_outcome(
            db_session,
            step_run_id=work["step_run"].id,
            outcome="approved",
            artifacts={"DOC_A": "/tmp/doc_a.md"},
        )

        fetched = run_repository.get_run_by_id(db_session, run.id)
        assert len(fetched.artifacts) == 1
        assert fetched.artifacts[0].artifact_key == "DOC_A"


class TestRequestAction:
    def test_approve_sets_action_requested(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(
            db_session, run, run_status="AWAITING_APPROVAL",
        )

        result = run_service.request_action(
            db_session, run_id=run.id, action="APPROVE", feedback="looks good",
        )

        assert result.action_requested == "APPROVE"
        assert result.action_feedback == "looks good"

    def test_cancel_sets_failed(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")

        result = run_service.request_action(
            db_session, run_id=run.id, action="CANCEL",
        )

        assert result.run_status == "FAILED"

    def test_invalid_action_raises_422(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(db_session, run, run_status="RUNNING")

        with pytest.raises(HTTPException) as exc_info:
            run_service.request_action(db_session, run_id=run.id, action="APPROVE")
        assert exc_info.value.status_code == 422

    def test_duplicate_action_raises_409(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(
            db_session, run, run_status="AWAITING_APPROVAL", action_requested="APPROVE",
        )

        with pytest.raises(HTTPException) as exc_info:
            run_service.request_action(db_session, run_id=run.id, action="REJECT")
        assert exc_info.value.status_code == 409


class TestResetStep:
    def test_reset_changes_step(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(
            db_session, run, run_status="AWAITING_INTERVENTION", current_step_name="review",
        )

        result = run_service.reset_step(
            db_session, run_id=run.id, step_name="generate",
        )

        assert result.run_status == "PENDING"
        assert result.current_step_name == "generate"

    def test_reset_on_terminal_raises(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(db_session, run, run_status="FAILED")

        with pytest.raises(HTTPException):
            run_service.reset_step(db_session, run_id=run.id, step_name="generate")


class TestGetRunDetail:
    def test_returns_valid_actions(self, db_session: Session):
        _seed_workflow(db_session)
        run = run_service.submit_run(db_session, workflow_name="svc_test_wf")
        run_repository.update_run_status(
            db_session, run, run_status="AWAITING_APPROVAL",
        )

        detail = run_service.get_run_detail(db_session, run.id)

        assert detail is not None
        assert "APPROVE" in detail["valid_actions"]
        assert "REJECT" in detail["valid_actions"]
        assert "CANCEL" in detail["valid_actions"]

    def test_returns_none_for_missing(self, db_session: Session):
        assert run_service.get_run_detail(db_session, "nonexistent") is None


# ===========================================================================
# Worker Service
# ===========================================================================

class TestWorkerService:
    def test_register_creates_worker(self, db_session: Session):
        w = worker_service.register_worker(db_session, worker_id="w1")
        assert w.worker_id == "w1"
        assert w.status == "active"

    def test_heartbeat_updates(self, db_session: Session):
        worker_service.register_worker(db_session, worker_id="w1")
        w = worker_service.heartbeat(
            db_session, worker_id="w1", status="busy", current_run_id="r1",
        )
        assert w.status == "busy"
        assert w.current_run_id == "r1"
        assert w.last_heartbeat is not None

    def test_heartbeat_unknown_worker_returns_none(self, db_session: Session):
        assert worker_service.heartbeat(db_session, worker_id="unknown") is None

    def test_stop_worker(self, db_session: Session):
        worker_service.register_worker(db_session, worker_id="w1")
        assert worker_service.stop_worker(db_session, worker_id="w1") is True
        w = worker_repository.get_worker(db_session, "w1")
        assert w.status == "stopped"


# ===========================================================================
# Workflow Service
# ===========================================================================

class TestWorkflowService:
    def test_sync_creates_workflow(self, db_session: Session):
        definition = _seed_workflow(db_session, "sync_test")
        wf = workflow_service.sync_workflow(
            db_session, workflow_name="sync_test", definition=definition,
        )
        assert wf.name == "sync_test"
        assert wf.job_prefix == "SVC"
        assert len(wf.steps) == 3

    def test_sync_updates_existing(self, db_session: Session):
        _seed_workflow(db_session, "update_test")
        definition = _seed_workflow(db_session, "update_test")
        definition["default_max_rejects"] = 5
        wf = workflow_service.sync_workflow(
            db_session, workflow_name="update_test", definition=definition,
        )
        assert wf.default_max_rejects == 5

    def test_sync_creates_transitions(self, db_session: Session):
        wf = workflow_service.sync_workflow(
            db_session,
            workflow_name="trans_test",
            definition={
                "job_prefix": "T",
                "init_step": "a",
                "steps": {
                    "a": {"onsuccess": "b"},
                    "b": {},
                },
            },
        )
        step_a = workflow_repository.get_step_by_name(db_session, workflow_id=wf.id, step_name="a")
        assert len(step_a.transitions) == 1
        assert step_a.transitions[0].target_step_name == "b"

    def test_sync_creates_coder_policy(self, db_session: Session):
        wf = workflow_service.sync_workflow(
            db_session,
            workflow_name="coder_test",
            definition={
                "job_prefix": "C",
                "init_step": "s1",
                "steps": {
                    "s1": {"coder": {"role_policy": "architect_standard", "allowed": ["opencode"]}},
                },
            },
        )
        step = workflow_repository.get_step_by_name(db_session, workflow_id=wf.id, step_name="s1")
        assert step.coder_policy is not None
        assert step.coder_policy.default_coder == "architect_standard"
