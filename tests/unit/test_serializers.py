"""Tests for API serializers."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.serializers import serialize_workflow
from agent_runner_backend_v2.services import workflow_service


class TestSerializeWorkflow:
    def test_init_input_keys_from_artifacts(self, db_session: Session):
        """Extracts required_inputs from init step's artifacts section."""
        workflow_service.sync_workflow(
            db_session,
            workflow_name="init_keys_test",
            definition={
                "job_prefix": "T",
                "init_step": "generate",
                "steps": {
                    "generate": {
                        "artifacts": {"required_inputs": ["DRAFT_INIT_FILE"]},
                    },
                    "review": {
                        "artifacts": {"required_inputs": ["GENERATED_FILE"]},
                    },
                },
            },
        )

        from agent_runner_backend_v2.database import workflow_repository
        wf = workflow_repository.get_workflow_by_name(db_session, "init_keys_test")
        result = serialize_workflow(wf)

        assert result.init_input_keys == ["DRAFT_INIT_FILE"]

    def test_init_input_keys_from_flattened(self, db_session: Session):
        """Falls back to top-level required_inputs when no artifacts key."""
        workflow_service.sync_workflow(
            db_session,
            workflow_name="flat_test",
            definition={
                "job_prefix": "T",
                "init_step": "generate",
                "steps": {
                    "generate": {
                        "required_inputs": ["WORKFLOW_SPEC"],
                    },
                },
            },
        )

        from agent_runner_backend_v2.database import workflow_repository
        wf = workflow_repository.get_workflow_by_name(db_session, "flat_test")
        result = serialize_workflow(wf)

        assert result.init_input_keys == ["WORKFLOW_SPEC"]

    def test_init_input_keys_empty_when_no_inputs(self, db_session: Session):
        """Returns empty list when init step has no required inputs."""
        workflow_service.sync_workflow(
            db_session,
            workflow_name="no_inputs_test",
            definition={
                "job_prefix": "T",
                "init_step": "generate",
                "steps": {
                    "generate": {},
                },
            },
        )

        from agent_runner_backend_v2.database import workflow_repository
        wf = workflow_repository.get_workflow_by_name(db_session, "no_inputs_test")
        result = serialize_workflow(wf)

        assert result.init_input_keys == []

    def test_init_input_keys_multiple(self, db_session: Session):
        """Returns all required inputs for the init step."""
        workflow_service.sync_workflow(
            db_session,
            workflow_name="multi_test",
            definition={
                "job_prefix": "T",
                "init_step": "generate",
                "steps": {
                    "generate": {
                        "artifacts": {"required_inputs": ["INPUT_A", "INPUT_B", "INPUT_C"]},
                    },
                },
            },
        )

        from agent_runner_backend_v2.database import workflow_repository
        wf = workflow_repository.get_workflow_by_name(db_session, "multi_test")
        result = serialize_workflow(wf)

        assert result.init_input_keys == ["INPUT_A", "INPUT_B", "INPUT_C"]

    def test_basic_fields(self, db_session: Session):
        """Serializes basic workflow fields correctly."""
        workflow_service.sync_workflow(
            db_session,
            workflow_name="basic_test",
            definition={
                "job_prefix": "BSC",
                "init_step": "step_a",
                "default_max_rejects": 2,
                "steps": {
                    "step_a": {"onsuccess": "step_b"},
                    "step_b": {},
                },
            },
        )

        from agent_runner_backend_v2.database import workflow_repository
        wf = workflow_repository.get_workflow_by_name(db_session, "basic_test")
        result = serialize_workflow(wf)

        assert result.workflow_name == "basic_test"
        assert result.job_prefix == "BSC"
        assert result.init_step == "step_a"
        assert result.is_active is True
        assert result.step_count == 2
        assert result.steps == ["step_a", "step_b"]
