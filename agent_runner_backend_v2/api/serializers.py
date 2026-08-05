"""ORM model → JSON serialization."""
from __future__ import annotations

from agent_runner_backend_v2.api.schemas import (
    HostResponse,
    RepoResponse,
    RepoWorkflowResponse,
    RunResponse,
    WorkerResponse,
    WorkflowResponse,
)
from agent_runner_backend_v2.models.host import Host
from agent_runner_backend_v2.models.repo import RepoRegistry, RepoWorkflowAssignment
from agent_runner_backend_v2.models.run import WorkflowRun
from agent_runner_backend_v2.models.worker import WorkerRegistry
from agent_runner_backend_v2.models.workflow import WorkflowDefinition
from agent_runner_backend_v2.services.state_machine import get_valid_actions


def serialize_run(run: WorkflowRun, valid_actions: list[str] | None = None) -> RunResponse:
    """Serialize a WorkflowRun to a RunResponse."""
    wf_name = ""
    wf_def_id = ""
    if run.workflow_definition:
        wf_name = run.workflow_definition.name
        wf_def_id = run.workflow_definition.id

    return RunResponse(
        run_id=run.id,
        run_code=run.run_code,
        workflow_definition_id=wf_def_id,
        workflow_name=wf_name,
        run_status=run.run_status,
        action_requested=run.action_requested,
        action_feedback=run.action_feedback,
        cancel_requested=run.cancel_requested,
        current_step=run.current_step_name,
        current_step_run_id=run.current_step_run_id,
        target_worker_id=run.target_worker_id,
        worker_id=run.claimed_by_worker or run.target_worker_id,
        worker_label=run.worker_label,
        project_root=run.project_root,
        workspace_path=run.workspace_path,
        job_dir=run.job_dir,
        input_payload=run.input_payload,
        context_payload=run.context_payload,
        error_message=run.error_message,
        refine_iterations=run.refine_iterations,
        submitted_at=run.submitted_at.isoformat() if run.submitted_at else None,
        started_at=run.started_at.isoformat() if run.started_at else None,
        completed_at=run.completed_at.isoformat() if run.completed_at else None,
        created_at=run.created_at.isoformat() if run.created_at else "",
        updated_at=run.updated_at.isoformat() if run.updated_at else "",
        valid_actions=valid_actions or get_valid_actions(run),
    )


def serialize_host(host: Host) -> HostResponse:
    """Serialize a Host to a HostResponse."""
    return HostResponse(
        id=host.id,
        hostname=host.hostname,
        ip_address=host.ip_address,
        os_type=host.os_type,
        created_at=host.created_at.isoformat() if host.created_at else "",
        updated_at=host.updated_at.isoformat() if host.updated_at else "",
    )


def serialize_worker(worker: WorkerRegistry) -> WorkerResponse:
    """Serialize a WorkerRegistry to a WorkerResponse."""
    hostname = None
    if worker.host:
        hostname = worker.host.hostname

    return WorkerResponse(
        worker_id=worker.worker_id,
        host_id=worker.host_id,
        hostname=hostname,
        status=worker.status,
        worker_label=worker.worker_label,
        is_enabled=worker.is_enabled,
        capabilities=worker.capabilities or {},
        last_heartbeat=worker.last_heartbeat.isoformat() if worker.last_heartbeat else None,
        current_run_id=worker.current_run_id,
    )


def serialize_workflow(wf: WorkflowDefinition) -> WorkflowResponse:
    """Serialize a WorkflowDefinition to a WorkflowResponse."""
    step_names = [s.step_name for s in sorted(wf.steps, key=lambda s: s.step_order)]
    return WorkflowResponse(
        workflow_name=wf.name,
        job_prefix=wf.job_prefix,
        init_step=wf.init_step,
        is_active=wf.is_active,
        step_count=len(wf.steps),
        steps=step_names,
    )


def serialize_repo_workflow(assignment: RepoWorkflowAssignment) -> RepoWorkflowResponse:
    """Serialize a RepoWorkflowAssignment."""
    return RepoWorkflowResponse(
        id=assignment.id,
        workflow_name=assignment.workflow_name,
        display_name=assignment.display_name,
        created_at=assignment.created_at.isoformat() if assignment.created_at else "",
    )


def serialize_repo(repo: RepoRegistry) -> RepoResponse:
    """Serialize a RepoRegistry to a RepoResponse, including host and workflow info."""
    hostname = None
    os_type = None
    if repo.worker and repo.worker.host:
        hostname = repo.worker.host.hostname
        os_type = repo.worker.host.os_type

    workflows = [serialize_repo_workflow(a) for a in repo.workflow_assignments]

    return RepoResponse(
        id=repo.id,
        name=repo.name,
        path=repo.path,
        worker_id=repo.worker_id,
        worker_uuid=repo.worker_uuid,
        host_id=repo.worker.host_id if repo.worker else None,
        hostname=hostname,
        os_type=os_type,
        workflows=workflows,
        created_at=repo.created_at.isoformat() if repo.created_at else "",
        updated_at=repo.updated_at.isoformat() if repo.updated_at else "",
    )
