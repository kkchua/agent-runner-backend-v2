"""Tests for V2 database models — schema, defaults, constraints, relationships."""
from __future__ import annotations

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import (
    WorkflowArtifact,
    WorkflowEvent,
    WorkflowReview,
    WorkflowRun,
    WorkflowStepRun,
)
from agent_runner_backend_v2.models.worker import WorkerRegistry
from agent_runner_backend_v2.models.workflow import (
    WorkflowDefinition,
    WorkflowStepArtifactBinding,
    WorkflowStepCoderPolicy,
    WorkflowStepDefinition,
    WorkflowStepTransition,
)


class TestTableCreation:
    """Verify all tables are created with correct columns."""

    def test_all_tables_created(self, db_session):
        Base.metadata.create_all(db_session.get_bind())
        inspector = inspect(db_session.get_bind())
        tables = inspector.get_table_names()
        expected = [
            "workflow_runs",
            "workflow_step_runs",
            "workflow_artifacts",
            "workflow_events",
            "workflow_reviews",
            "worker_registry",
            "workflow_definitions",
            "workflow_step_definitions",
            "workflow_step_transitions",
            "workflow_step_coder_policies",
            "workflow_step_artifact_bindings",
        ]
        for table in expected:
            assert table in tables, f"Table {table} not created"

    def test_workflow_run_has_v2_state_fields(self, db_session):
        Base.metadata.create_all(db_session.get_bind())
        inspector = inspect(db_session.get_bind())
        columns = {c["name"] for c in inspector.get_columns("workflow_runs")}
        assert "run_status" in columns
        assert "action_requested" in columns
        assert "action_feedback" in columns
        assert "refine_iterations" in columns

    def test_step_run_has_split_status_outcome(self, db_session):
        Base.metadata.create_all(db_session.get_bind())
        inspector = inspect(db_session.get_bind())
        columns = {c["name"] for c in inspector.get_columns("workflow_step_runs")}
        assert "step_status" in columns
        assert "step_outcome" in columns


class TestWorkflowRunDefaults:
    """Verify V2 state machine defaults."""

    def test_new_run_defaults_to_submitted(self, db_session):
        wf = WorkflowDefinition(
            name="test_wf", job_prefix="TST", source_hash="abc123",
        )
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-001", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        assert run.run_status == "SUBMITTED"
        assert run.action_requested is None
        assert run.action_feedback is None
        assert run.refine_iterations == {}

    def test_action_requested_is_nullable(self, db_session):
        wf = WorkflowDefinition(
            name="test_wf2", job_prefix="TST", source_hash="abc123",
        )
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(
            run_code="JOB-002",
            workflow_definition_id=wf.id,
            run_status="WAITING_FOR_HUMAN_APPROVAL",
            action_requested=None,
        )
        db_session.add(run)
        db_session.flush()

        assert run.action_requested is None

    def test_action_requested_accepts_valid_values(self, db_session):
        wf = WorkflowDefinition(
            name="test_wf3", job_prefix="TST", source_hash="abc123",
        )
        db_session.add(wf)
        db_session.flush()

        for action in ["APPROVE", "REJECT", "RESUME", "RETRY", "CANCEL"]:
            run = WorkflowRun(
                run_code=f"JOB-{action}",
                workflow_definition_id=wf.id,
                run_status="WAITING_FOR_HUMAN_APPROVAL",
                action_requested=action,
            )
            db_session.add(run)
            db_session.flush()
            assert run.action_requested == action


class TestStepRunDefaults:
    """Verify split step_status / step_outcome."""

    def test_new_step_run_defaults(self, db_session):
        wf = WorkflowDefinition(
            name="test_wf_sr", job_prefix="TST", source_hash="abc",
        )
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-SR", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        step = WorkflowStepRun(
            workflow_run_id=run.id,
            step_name="generate",
            sequence_no=1,
        )
        db_session.add(step)
        db_session.flush()

        assert step.step_status == "pending"
        assert step.step_outcome is None


class TestRunCodeUniqueness:
    """Verify run_code unique constraint."""

    def test_duplicate_run_code_rejected(self, db_session):
        wf = WorkflowDefinition(
            name="test_wf_dup", job_prefix="TST", source_hash="abc",
        )
        db_session.add(wf)
        db_session.flush()

        run1 = WorkflowRun(run_code="JOB-DUP", workflow_definition_id=wf.id)
        db_session.add(run1)
        db_session.flush()

        run2 = WorkflowRun(run_code="JOB-DUP", workflow_definition_id=wf.id)
        db_session.add(run2)
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestWorkflowDefinitionDefaults:
    """Verify workflow definition defaults."""

    def test_defaults(self, db_session):
        wf = WorkflowDefinition(
            name="test_defaults", job_prefix="DEF", source_hash="xyz",
        )
        db_session.add(wf)
        db_session.flush()

        assert wf.is_active is True
        assert wf.default_max_rejects == 0
        assert wf.raw_definition == {}

    def test_name_unique(self, db_session):
        wf1 = WorkflowDefinition(name="unique_wf", job_prefix="U", source_hash="a")
        db_session.add(wf1)
        db_session.flush()

        wf2 = WorkflowDefinition(name="unique_wf", job_prefix="U", source_hash="b")
        db_session.add(wf2)
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestRelationships:
    """Verify ORM relationships work correctly."""

    def test_run_to_step_runs(self, db_session):
        wf = WorkflowDefinition(name="rel_wf", job_prefix="R", source_hash="r")
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-REL", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        s1 = WorkflowStepRun(workflow_run_id=run.id, step_name="step1", sequence_no=1)
        s2 = WorkflowStepRun(workflow_run_id=run.id, step_name="step2", sequence_no=2)
        db_session.add_all([s1, s2])
        db_session.flush()

        assert len(run.step_runs) == 2

    def test_run_to_artifacts(self, db_session):
        wf = WorkflowDefinition(name="art_wf", job_prefix="A", source_hash="a")
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-ART", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        art = WorkflowArtifact(
            workflow_run_id=run.id,
            artifact_key="REVIEW_FILE",
            file_path="/tmp/review.md",
        )
        db_session.add(art)
        db_session.flush()

        assert len(run.artifacts) == 1
        assert run.artifacts[0].artifact_key == "REVIEW_FILE"

    def test_run_to_events(self, db_session):
        wf = WorkflowDefinition(name="evt_wf", job_prefix="E", source_hash="e")
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-EVT", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        evt = WorkflowEvent(
            workflow_run_id=run.id,
            event_type="RUN_CREATED",
            message="Run submitted",
        )
        db_session.add(evt)
        db_session.flush()

        assert len(run.events) == 1

    def test_workflow_to_steps_ordered(self, db_session):
        wf = WorkflowDefinition(name="ord_wf", job_prefix="O", source_hash="o")
        db_session.add(wf)
        db_session.flush()

        s3 = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="third", step_order=3,
        )
        s1 = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="first", step_order=1,
        )
        s2 = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="second", step_order=2,
        )
        db_session.add_all([s3, s1, s2])
        db_session.flush()

        names = [s.step_name for s in wf.steps]
        assert names == ["first", "second", "third"]

    def test_step_to_transitions(self, db_session):
        wf = WorkflowDefinition(name="tr_wf", job_prefix="T", source_hash="t")
        db_session.add(wf)
        db_session.flush()

        step = WorkflowStepDefinition(
            workflow_definition_id=wf.id, step_name="review", step_order=1,
        )
        db_session.add(step)
        db_session.flush()

        trans = WorkflowStepTransition(
            step_definition_id=step.id,
            transition_type="onsuccess",
            outcome="approved",
            target_step_name="generate",
        )
        db_session.add(trans)
        db_session.flush()

        assert len(step.transitions) == 1
        assert step.transitions[0].target_step_name == "generate"

    def test_cascade_delete_run_deletes_steps(self, db_session):
        wf = WorkflowDefinition(name="cas_wf", job_prefix="C", source_hash="c")
        db_session.add(wf)
        db_session.flush()

        run = WorkflowRun(run_code="JOB-CAS", workflow_definition_id=wf.id)
        db_session.add(run)
        db_session.flush()

        step = WorkflowStepRun(workflow_run_id=run.id, step_name="s1", sequence_no=1)
        db_session.add(step)
        db_session.flush()
        step_id = step.id

        db_session.delete(run)
        db_session.flush()

        result = db_session.query(WorkflowStepRun).filter_by(id=step_id).first()
        assert result is None


class TestWorkerRegistry:
    """Verify worker model."""

    def test_worker_defaults(self, db_session):
        w = WorkerRegistry(worker_id="w1")
        db_session.add(w)
        db_session.flush()

        assert w.status == "active"
        assert w.worker_label == "live"
        assert w.capabilities == {}
        assert w.current_run_id is None
        assert w.last_heartbeat is None
