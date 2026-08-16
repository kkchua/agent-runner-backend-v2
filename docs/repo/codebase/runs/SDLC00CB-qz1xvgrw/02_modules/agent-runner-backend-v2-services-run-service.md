---
title: "Module Documentation: agent_runner_backend_v2.services.run_service"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/run_service.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-run-service.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-qz1xvgrw / 2026-08-05T23:20:00+08:00"
created: "2026-08-05T23:20:00+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.run_service

## 1. Module Overview

### 1.1 Purpose

Run service -- orchestration layer for workflow run lifecycle.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.run` | internal module | repository dependency |
| `agent_runner_backend_v2.models.workflow` | internal module | repository dependency |
| `agent_runner_backend_v2.services.state_machine` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### utcnow()

**Signature**: `utcnow()`

**Purpose**: Return the current UTC time as a naive datetime.

**Returns**: `datetime`

---

#### submit_run()

**Signature**: `submit_run(db: Session, *, workflow_name: str, worker_id: str | None = None, project_root: str | None = None, workspace_path: str | None = None, input_payload: dict | None = None, start_step: str | None = None)`

**Purpose**: Submit a new workflow run.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow_name` | `str` | -- | -- |
| `worker_id` | `str | None` | `None` | -- |
| `project_root` | `str | None` | `None` | -- |
| `workspace_path` | `str | None` | `None` | -- |
| `input_payload` | `dict | None` | `None` | -- |
| `start_step` | `str | None` | `None` | -- |

**Returns**: `WorkflowRun`

---

#### claim_work()

**Signature**: `claim_work(db: Session, *, worker_id: str)`

**Purpose**: Claim the next available work for a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `dict | None`

---

#### report_outcome()

**Signature**: `report_outcome(db: Session, *, step_run_id: str, outcome: str, failure_class: str | None = None, artifacts: dict | None = None, review: dict | None = None, error_message: str | None = None, usage_summary: dict | None = None, job_dir: str | None = None)`

**Purpose**: Report a step outcome and compute the next state via the state machine.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `step_run_id` | `str` | -- | -- |
| `outcome` | `str` | -- | -- |
| `failure_class` | `str | None` | `None` | -- |
| `artifacts` | `dict | None` | `None` | -- |
| `review` | `dict | None` | `None` | -- |
| `error_message` | `str | None` | `None` | -- |
| `usage_summary` | `dict | None` | `None` | -- |
| `job_dir` | `str | None` | `None` | -- |

**Returns**: `WorkflowRun`

---

#### request_action()

**Signature**: `request_action(db: Session, *, run_id: str, action: str, feedback: str | None = None)`

**Purpose**: Request an action on a run (approve, reject, resume, retry, cancel).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_id` | `str` | -- | -- |
| `action` | `str` | -- | -- |
| `feedback` | `str | None` | `None` | -- |

**Returns**: `WorkflowRun`

---

#### reset_step()

**Signature**: `reset_step(db: Session, *, run_id: str, step_name: str)`

**Purpose**: Reset a run's current step.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_id` | `str` | -- | -- |
| `step_name` | `str` | -- | -- |

**Returns**: `WorkflowRun`

---

#### get_force_cancelled_runs()

**Signature**: `get_force_cancelled_runs(db: Session, *, worker_id: str)`

**Purpose**: Get runs claimed by this worker that have force-cancel pending.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `list[WorkflowRun]`

---

#### get_run_detail()

**Signature**: `get_run_detail(db: Session, run_id: str)`

**Purpose**: Get run detail with computed valid_actions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_id` | `str` | -- | -- |

**Returns**: `dict | None`

---


### 2.3 Constants / Configuration

No public constants.


## 3. Error Handling

No documented exceptions.


## 4. Testing

### 4.1 Test Coverage

| Test File | Coverage Area |
|-----------|---------------|
| (none) | No test references found |


## 5. Change Log

| Date | Change | Verified By |
|------|--------|-------------|
| 2026-08-05 | Initial baseline generated from repository scan | sdlc_00_codebase_v1 |
