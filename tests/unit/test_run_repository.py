"""Tests for run repository — CRUD, claim queries, state updates."""
from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import run_repository, worker_repository
from agent_runner_backend_v2.database.workflow_repository import create_workflow
from agent_runner_backend_v2.models.run import (
    WorkflowArtifact,
    WorkflowEvent,
    WorkflowRun,
    WorkflowStepRun,
)
from agent_runner_backend_v2.models.worker import WorkerRegistry
from agent_runner_backend_v2.models.workflow import WorkflowDefinition


def _make_workflow(db: Session, name: str = "test_wf") -> WorkflowDefinition:
    wf = WorkflowDefinition(name=name, job_prefix="TST", source_hash="abc")
    return create_workflow(db, wf)


def _make_run(
    db: Session,
    wf: WorkflowDefinition,
    *,
    run_code: str = "JOB-001",
    run_status: str = "SUBMITTED",
    action_requested: str | None = None,
    worker_id: str | None = None,
) -> WorkflowRun:
    run = WorkflowRun(
        run_code=run_code,
        workflow_definition_id=wf.id,
        run_status=run_status,
        action_requested=action_requested,
        target_worker_id=worker_id,
        claimed_by_worker=worker_id,
    )
    return run_repository.create_run(db, run)


class TestRunCRUD:
    def test_create_and_get_by_id(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        fetched = run_repository.get_run_by_id(db_session, run.id)
        assert fetched is not None
        assert fetched.run_code == "JOB-001"
        assert fetched.run_status == "SUBMITTED"

    def test_get_by_code(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="JOB-CODE")

        fetched = run_repository.get_run_by_code(db_session, "JOB-CODE")
        assert fetched is not None
        assert fetched.run_code == "JOB-CODE"

    def test_get_nonexistent_returns_none(self, db_session: Session):
        assert run_repository.get_run_by_id(db_session, "nonexistent") is None
        assert run_repository.get_run_by_code(db_session, "nonexistent") is None

    def test_list_runs_no_filter(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1")
        _make_run(db_session, wf, run_code="J2")

        runs = run_repository.list_runs(db_session)
        assert len(runs) == 2

    def test_list_runs_by_status(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="SUBMITTED")
        _make_run(db_session, wf, run_code="J2", run_status="PENDING")
        _make_run(db_session, wf, run_code="J3", run_status="SUBMITTED")

        runs = run_repository.list_runs(db_session, run_status="SUBMITTED")
        assert len(runs) == 2

    def test_list_runs_by_multiple_statuses(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="SUBMITTED")
        _make_run(db_session, wf, run_code="J2", run_status="RUNNING")
        _make_run(db_session, wf, run_code="J3", run_status="COMPLETED")

        runs = run_repository.list_runs(db_session, statuses=["SUBMITTED", "RUNNING"])
        assert len(runs) == 2


class TestClaimQuery:
    """Verify the claim filter: status IN (SUBMITTED, PENDING) AND action_requested IS NULL."""

    def test_claimable_includes_submitted(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="SUBMITTED")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 1

    def test_claimable_includes_pending(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="PENDING")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 1

    def test_claimable_excludes_running(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="RUNNING")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 0

    def test_claimable_excludes_awaiting(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="AWAITING_APPROVAL")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 0

    def test_claimable_excludes_action_pending(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(
            db_session, wf, run_code="J1",
            run_status="SUBMITTED", action_requested="CANCEL",
        )

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 0

    def test_claimable_excludes_terminal(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="COMPLETED")
        _make_run(db_session, wf, run_code="J2", run_status="FAILED")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 0

    def test_claimable_ordered_by_created(self, db_session: Session):
        wf = _make_workflow(db_session)
        r1 = _make_run(db_session, wf, run_code="J1", run_status="SUBMITTED")
        r2 = _make_run(db_session, wf, run_code="J2", run_status="PENDING")

        claimable = run_repository.list_claimable_runs(db_session, worker_id="w1")
        assert len(claimable) == 2
        assert claimable[0].id == r1.id
        assert claimable[1].id == r2.id


class TestActionPendingQuery:
    def test_lists_runs_with_action(self, db_session: Session):
        wf = _make_workflow(db_session)
        _make_run(db_session, wf, run_code="J1", run_status="AWAITING_APPROVAL", action_requested="APPROVE")
        _make_run(db_session, wf, run_code="J2", run_status="AWAITING_APPROVAL")

        pending = run_repository.list_action_pending_runs(db_session)
        assert len(pending) == 1
        assert pending[0].action_requested == "APPROVE"


class TestUpdateRunStatus:
    def test_update_status(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        run_repository.update_run_status(db_session, run, run_status="RUNNING")
        assert run.run_status == "RUNNING"

    def test_update_with_step(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        run_repository.update_run_status(
            db_session, run,
            run_status="PENDING",
            current_step_name="generate",
            current_step_run_id="step-123",
        )
        assert run.current_step_name == "generate"
        assert run.current_step_run_id == "step-123"

    def test_set_and_clear_action(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf, run_status="AWAITING_APPROVAL")

        run_repository.update_run_status(
            db_session, run,
            run_status="AWAITING_APPROVAL",
            action_requested="APPROVE",
        )
        assert run.action_requested == "APPROVE"

        run_repository.update_run_status(
            db_session, run,
            run_status="PENDING",
            clear_action=True,
        )
        assert run.action_requested is None
        assert run.action_feedback is None


class TestStepRunCRUD:
    def test_create_and_get(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        step = WorkflowStepRun(
            workflow_run_id=run.id, step_name="generate", sequence_no=1,
        )
        run_repository.create_step_run(db_session, step)

        fetched = run_repository.get_step_run_by_id(db_session, step.id)
        assert fetched is not None
        assert fetched.step_name == "generate"
        assert fetched.step_status == "pending"

    def test_update_step(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)
        step = WorkflowStepRun(
            workflow_run_id=run.id, step_name="generate", sequence_no=1,
        )
        run_repository.create_step_run(db_session, step)

        run_repository.update_step_run(
            db_session, step,
            step_status="completed",
            step_outcome="approved",
        )
        assert step.step_status == "completed"
        assert step.step_outcome == "approved"


class TestArtifactAndEvent:
    def test_create_artifact(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        art = WorkflowArtifact(
            workflow_run_id=run.id,
            artifact_key="REVIEW_FILE",
            file_path="/tmp/review.md",
        )
        run_repository.create_artifact(db_session, art)
        assert art.id is not None

    def test_create_event(self, db_session: Session):
        wf = _make_workflow(db_session)
        run = _make_run(db_session, wf)

        evt = WorkflowEvent(
            workflow_run_id=run.id,
            event_type="RUN_CREATED",
            message="submitted",
        )
        run_repository.create_event(db_session, evt)
        assert evt.id is not None


class TestWorkerRepository:
    def test_upsert_new_worker(self, db_session: Session):
        w = WorkerRegistry(worker_id="w1", worker_label="live")
        result = worker_repository.upsert_worker(db_session, w)
        assert result.worker_id == "w1"
        assert result.status == "active"

    def test_upsert_existing_worker(self, db_session: Session):
        w1 = WorkerRegistry(worker_id="w1")
        worker_repository.upsert_worker(db_session, w1)

        w2 = WorkerRegistry(worker_id="w1", status="idle", worker_label="dev")
        result = worker_repository.upsert_worker(db_session, w2)
        assert result.status == "idle"
        assert result.worker_label == "dev"

    def test_update_heartbeat(self, db_session: Session):
        w = WorkerRegistry(worker_id="w1")
        worker_repository.upsert_worker(db_session, w)

        now = datetime(2026, 8, 1, 12, 0, 0)
        worker_repository.update_heartbeat(
            db_session, w,
            status="busy",
            current_run_id="run-123",
            heartbeat_time=now,
        )
        assert w.last_heartbeat == now
        assert w.status == "busy"
        assert w.current_run_id == "run-123"

    def test_list_workers(self, db_session: Session):
        worker_repository.upsert_worker(db_session, WorkerRegistry(worker_id="w1"))
        worker_repository.upsert_worker(db_session, WorkerRegistry(worker_id="w2"))

        workers = worker_repository.list_workers(db_session)
        assert len(workers) == 2


class TestWorkflowRepository:
    def test_create_and_get(self, db_session: Session):
        wf = _make_workflow(db_session, name="my_workflow")
        fetched = run_repository  # just verify it exists
        from agent_runner_backend_v2.database import workflow_repository
        result = workflow_repository.get_workflow_by_name(db_session, "my_workflow")
        assert result is not None
        assert result.name == "my_workflow"

    def test_list_active_only(self, db_session: Session):
        from agent_runner_backend_v2.database import workflow_repository
        wf1 = WorkflowDefinition(name="active_wf", job_prefix="A", source_hash="a", is_active=True)
        wf2 = WorkflowDefinition(name="inactive_wf", job_prefix="I", source_hash="b", is_active=False)
        workflow_repository.create_workflow(db_session, wf1)
        workflow_repository.create_workflow(db_session, wf2)

        active = workflow_repository.list_workflows(db_session, active_only=True)
        assert len(active) == 1
        assert active[0].name == "active_wf"

        all_wfs = workflow_repository.list_workflows(db_session, active_only=False)
        assert len(all_wfs) == 2
