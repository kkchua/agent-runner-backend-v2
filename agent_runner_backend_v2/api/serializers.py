"""ORM model → JSON serialization."""
from __future__ import annotations

from agent_runner_backend_v2.api.schemas import RunResponse, WorkerResponse, WorkflowResponse
from agent_runner_backend_v2.models.run import WorkflowRun
from agent_runner_backend_v2.models.worker import WorkerRegistry
from agent_runner_backend_v2.models.workflow import WorkflowDefinition
from agent_runner_backend_v2.services.state_machine import get_valid_actions


def serialize_run(run: WorkflowRun, valid_actions: list[str] | None = None) -> RunResponse:
    """Serialize a WorkflowRun to a RunResponse."""
    wf_name = ""
    if run.workflow_definition:
        wf_name = run.workflow_definition.name

    return RunResponse(
        run_id=run.id,
        run_code=run.run_code,
        workflow_name=wf_name,
        run_status=run.run_status,
        action_requested=run.action_requested,
        current_step=run.current_step_name,
        current_step_run_id=run.current_step_run_id,
        worker_id=run.claimed_by_worker or run.target_worker_id,
        created_at=run.created_at.isoformat() if run.created_at else "",
        updated_at=run.updated_at.isoformat() if run.updated_at else "",
        valid_actions=valid_actions or get_valid_actions(run),
    )


def serialize_worker(worker: WorkerRegistry) -> WorkerResponse:
    """Serialize a WorkerRegistry to a WorkerResponse."""
    return WorkerResponse(
        worker_id=worker.worker_id,
        status=worker.status,
        worker_label=worker.worker_label,
        last_heartbeat=worker.last_heartbeat.isoformat() if worker.last_heartbeat else None,
        current_run_id=worker.current_run_id,
    )


def serialize_workflow(wf: WorkflowDefinition) -> WorkflowResponse:
    """Serialize a WorkflowDefinition to a WorkflowResponse."""
    return WorkflowResponse(
        workflow_name=wf.name,
        job_prefix=wf.job_prefix,
        init_step=wf.init_step,
        is_active=wf.is_active,
        step_count=len(wf.steps),
    )
