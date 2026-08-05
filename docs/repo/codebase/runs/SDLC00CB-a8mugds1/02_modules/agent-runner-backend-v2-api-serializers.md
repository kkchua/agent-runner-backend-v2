---
title: "Module Documentation: agent_runner_backend_v2.api.serializers"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/serializers.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-serializers.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-a8mugds1 / 2026-08-05T22:16:43+08:00"
created: "2026-08-05T22:16:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.serializers

## 1. Module Overview

### 1.1 Purpose

ORM model -> JSON serialization.

### 1.2 Responsibility

This module belongs to the `api` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.api.schemas` | internal module | repository dependency |
| `agent_runner_backend_v2.models.host` | internal module | repository dependency |
| `agent_runner_backend_v2.models.repo` | internal module | repository dependency |
| `agent_runner_backend_v2.models.run` | internal module | repository dependency |
| `agent_runner_backend_v2.models.worker` | internal module | repository dependency |
| `agent_runner_backend_v2.models.workflow` | internal module | repository dependency |
| `agent_runner_backend_v2.services.state_machine` | internal module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### serialize_run()

**Signature**: `serialize_run(run: WorkflowRun, valid_actions: list[str] | None = None)`

**Purpose**: Serialize a WorkflowRun to a RunResponse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `run` | `WorkflowRun` | -- | -- |
| `valid_actions` | `list[str] | None` | `None` | -- |

**Returns**: `RunResponse`

---

#### serialize_host()

**Signature**: `serialize_host(host: Host)`

**Purpose**: Serialize a Host to a HostResponse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `host` | `Host` | -- | -- |

**Returns**: `HostResponse`

---

#### serialize_worker()

**Signature**: `serialize_worker(worker: WorkerRegistry)`

**Purpose**: Serialize a WorkerRegistry to a WorkerResponse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker` | `WorkerRegistry` | -- | -- |

**Returns**: `WorkerResponse`

---

#### serialize_workflow()

**Signature**: `serialize_workflow(wf: WorkflowDefinition)`

**Purpose**: Serialize a WorkflowDefinition to a WorkflowResponse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `wf` | `WorkflowDefinition` | -- | -- |

**Returns**: `WorkflowResponse`

---

#### serialize_repo_workflow()

**Signature**: `serialize_repo_workflow(assignment: RepoWorkflowAssignment)`

**Purpose**: Serialize a RepoWorkflowAssignment.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `assignment` | `RepoWorkflowAssignment` | -- | -- |

**Returns**: `RepoWorkflowResponse`

---

#### serialize_repo()

**Signature**: `serialize_repo(repo: RepoRegistry)`

**Purpose**: Serialize a RepoRegistry to a RepoResponse, including host and workflow info.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo` | `RepoRegistry` | -- | -- |

**Returns**: `RepoResponse`

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
