"""Pydantic request/response schemas for the API."""
from __future__ import annotations

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Run schemas
# ---------------------------------------------------------------------------

class SubmitRunRequest(BaseModel):
    workflow_name: str
    worker_id: str | None = None
    project_root: str | None = None
    workspace_path: str | None = None
    input_payload: dict = Field(default_factory=dict)
    start_step: str | None = None


class RunResponse(BaseModel):
    run_id: str
    run_code: str
    workflow_definition_id: str
    workflow_name: str
    run_status: str
    action_requested: str | None = None
    action_feedback: str | None = None
    cancel_requested: str | None = None
    current_step: str | None = None
    current_step_run_id: str | None = None
    target_worker_id: str | None = None
    worker_id: str | None = None
    worker_label: str | None = None
    project_root: str | None = None
    workspace_path: str | None = None
    job_dir: str | None = None
    input_payload: dict | None = None
    context_payload: dict | None = None
    error_message: str | None = None
    refine_iterations: dict | None = None
    submitted_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    created_at: str
    updated_at: str
    valid_actions: list[str] = Field(default_factory=list)


class RunListResponse(BaseModel):
    runs: list[RunResponse]
    total: int = 0


class ActionRequest(BaseModel):
    action: str
    feedback: str | None = None
    force: bool = False  # For CANCEL: True=force cancel (kill children immediately)


class ResetStepRequest(BaseModel):
    step_name: str


class ErrorResponse(BaseModel):
    detail: str


# ---------------------------------------------------------------------------
# Worker schemas
# ---------------------------------------------------------------------------

class RegisterWorkerRequest(BaseModel):
    worker_id: str
    worker_label: str = "live"
    capabilities: dict = Field(default_factory=dict)
    host_id: str | None = None


class HeartbeatRequest(BaseModel):
    status: str = "idle"
    current_run_id: str | None = None
    current_step_run_id: str | None = None


class HeartbeatResponse(BaseModel):
    commands: list[str] = Field(default_factory=list)
    detail: dict | None = None


class UpdateWorkerRequest(BaseModel):
    worker_label: str | None = None
    status: str | None = None
    is_enabled: bool | None = None
    capabilities: dict | None = None
    host_id: str | None = None


class WorkerResponse(BaseModel):
    worker_id: str
    host_id: str | None = None
    hostname: str | None = None
    status: str
    worker_label: str
    is_enabled: bool = True
    capabilities: dict = Field(default_factory=dict)
    last_heartbeat: str | None = None
    current_run_id: str | None = None


# ---------------------------------------------------------------------------
# Claim schemas
# ---------------------------------------------------------------------------

class ClaimResponse(BaseModel):
    work_type: str  # EXECUTE_STEP | PROCESS_ACTION | IDLE
    run: dict | None = None
    step_run: dict | None = None
    action: str | None = None
    feedback: str | None = None
    execution_spec: dict | None = None


# ---------------------------------------------------------------------------
# Outcome schemas
# ---------------------------------------------------------------------------

class OutcomeRequest(BaseModel):
    outcome: str
    failure_class: str | None = None
    artifacts: dict = Field(default_factory=dict)
    review: dict | None = None
    error_message: str | None = None
    usage_summary: dict | None = None
    job_dir: str | None = None  # Full path to local job folder (set on first outcome)


class OutcomeResponse(BaseModel):
    run_id: str
    run_status: str
    current_step: str | None = None
    action_requested: str | None = None
    message: str


# ---------------------------------------------------------------------------
# Workflow schemas
# ---------------------------------------------------------------------------

class SyncWorkflowRequest(BaseModel):
    workflow_name: str
    definition: dict


class WorkflowResponse(BaseModel):
    workflow_name: str
    job_prefix: str
    init_step: str | None = None
    is_active: bool
    step_count: int
    steps: list[str] = Field(default_factory=list)
    init_input_keys: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Host schemas
# ---------------------------------------------------------------------------

class CreateHostRequest(BaseModel):
    hostname: str
    ip_address: str | None = None
    os_type: str = "windows"


class UpdateHostRequest(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    os_type: str | None = None


class HostResponse(BaseModel):
    id: str
    hostname: str
    ip_address: str | None = None
    os_type: str
    created_at: str
    updated_at: str


# ---------------------------------------------------------------------------
# Repo schemas
# ---------------------------------------------------------------------------

class CreateRepoRequest(BaseModel):
    name: str
    path: str
    worker_id: str


class UpdateRepoRequest(BaseModel):
    name: str | None = None
    path: str | None = None
    worker_id: str | None = None


class AssignWorkflowRequest(BaseModel):
    workflow_name: str
    display_name: str | None = None


class RepoWorkflowResponse(BaseModel):
    id: str
    workflow_name: str
    display_name: str | None = None
    created_at: str


class RepoResponse(BaseModel):
    id: str
    name: str
    path: str
    worker_id: str
    worker_uuid: str | None = None
    host_id: str | None = None
    hostname: str | None = None
    os_type: str | None = None
    workflows: list[RepoWorkflowResponse] = Field(default_factory=list)
    created_at: str
    updated_at: str
