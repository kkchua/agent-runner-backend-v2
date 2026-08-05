---
title: "Module Documentation: agent_runner_backend_v2.database.run_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/run_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-run-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-grpxyiln / 2026-08-05T13:01:30+08:00"
created: "2026-08-05T13:01:30+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.run_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for workflow run and step-run persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.models.run` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_run_by_id()

**Signature**: `get_run_by_id(db: Session, run_id: str)`

**Purpose**: Fetch a workflow run by its primary key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_id` | `str` | -- | -- |

**Returns**: `WorkflowRun | None`

---

#### get_run_by_code()

**Signature**: `get_run_by_code(db: Session, run_code: str)`

**Purpose**: Fetch a workflow run by its run_code.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_code` | `str` | -- | -- |

**Returns**: `WorkflowRun | None`

---

#### list_runs()

**Signature**: `list_runs(db: Session, *, run_status: str | None = None, statuses: list[str] | None = None, worker_id: str | None = None, workflow_name: str | None = None, limit: int | None = None, offset: int = 0)`

**Purpose**: List workflow runs with optional filters, ordered by creation date descending.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run_status` | `str | None` | `None` | -- |
| `statuses` | `list[str] | None` | `None` | -- |
| `worker_id` | `str | None` | `None` | -- |
| `workflow_name` | `str | None` | `None` | -- |
| `limit` | `int | None` | `None` | -- |
| `offset` | `int` | `0` | -- |

**Returns**: `tuple[list[WorkflowRun], int]`

---

#### list_claimable_runs()

**Signature**: `list_claimable_runs(db: Session, *, worker_id: str)`

**Purpose**: List runs available for claim by a worker as EXECUTE_STEP.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `list[WorkflowRun]`

---

#### list_action_pending_runs()

**Signature**: `list_action_pending_runs(db: Session, *, worker_id: str | None = None)`

**Purpose**: List runs with a pending user action (PROCESS_ACTION).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str | None` | `None` | -- |

**Returns**: `list[WorkflowRun]`

---

#### list_force_cancelled_runs()

**Signature**: `list_force_cancelled_runs(db: Session, *, worker_id: str)`

**Purpose**: List runs with force-cancel pending, claimed by this worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `list[WorkflowRun]`

---

#### create_run()

**Signature**: `create_run(db: Session, run: WorkflowRun)`

**Purpose**: Insert a new workflow run.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run` | `WorkflowRun` | -- | -- |

**Returns**: `WorkflowRun`

---

#### update_run_status()

**Signature**: `update_run_status(db: Session, run: WorkflowRun, *, run_status: str, current_step_name: str | None = None, current_step_run_id: str | None = None, action_requested: str | None = None, clear_action: bool = False)`

**Purpose**: Update a run's state machine fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run` | `WorkflowRun` | -- | -- |
| `run_status` | `str` | -- | -- |
| `current_step_name` | `str | None` | `None` | -- |
| `current_step_run_id` | `str | None` | `None` | -- |
| `action_requested` | `str | None` | `None` | -- |
| `clear_action` | `bool` | `False` | -- |

**Returns**: `WorkflowRun`

---

#### get_step_run_by_id()

**Signature**: `get_step_run_by_id(db: Session, step_run_id: str)`

**Purpose**: Fetch a step run by its primary key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `step_run_id` | `str` | -- | -- |

**Returns**: `WorkflowStepRun | None`

---

#### create_step_run()

**Signature**: `create_step_run(db: Session, step_run: WorkflowStepRun)`

**Purpose**: Insert a new step run.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `step_run` | `WorkflowStepRun` | -- | -- |

**Returns**: `WorkflowStepRun`

---

#### update_step_run()

**Signature**: `update_step_run(db: Session, step_run: WorkflowStepRun, *, step_status: str | None = None, step_outcome: str | None = None, error_message: str | None = None)`

**Purpose**: Update step run fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `step_run` | `WorkflowStepRun` | -- | -- |
| `step_status` | `str | None` | `None` | -- |
| `step_outcome` | `str | None` | `None` | -- |
| `error_message` | `str | None` | `None` | -- |

**Returns**: `WorkflowStepRun`

---

#### create_artifact()

**Signature**: `create_artifact(db: Session, artifact: WorkflowArtifact)`

**Purpose**: Insert a new artifact.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `artifact` | `WorkflowArtifact` | -- | -- |

**Returns**: `WorkflowArtifact`

---

#### create_event()

**Signature**: `create_event(db: Session, event: WorkflowEvent)`

**Purpose**: Insert a new event.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `event` | `WorkflowEvent` | -- | -- |

**Returns**: `WorkflowEvent`

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
