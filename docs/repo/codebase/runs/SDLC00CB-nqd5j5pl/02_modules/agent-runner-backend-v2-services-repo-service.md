---
title: "Module Documentation: agent_runner_backend_v2.services.repo_service"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/repo_service.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-repo-service.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-nqd5j5pl / 2026-08-06T14:58:43+08:00"
created: "2026-08-06T14:58:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.repo_service

## 1. Module Overview

### 1.1 Purpose

Repo service -- repo registration and workflow assignment.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.repo` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### create_repo()

**Signature**: `create_repo(db: Session, *, name: str, path: str, worker_id: str)`

**Purpose**: Create a new repo registration.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `name` | `str` | -- | -- |
| `path` | `str` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `RepoRegistry`

---

#### get_repo()

**Signature**: `get_repo(db: Session, repo_id: str)`

**Purpose**: Get a repo by ID, raising 404 if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |

**Returns**: `RepoRegistry`

---

#### list_repos()

**Signature**: `list_repos(db: Session)`

**Purpose**: List all registered repos.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |

**Returns**: `list[RepoRegistry]`

---

#### update_repo()

**Signature**: `update_repo(db: Session, repo_id: str, **kwargs)`

**Purpose**: Update a repo's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `RepoRegistry`

---

#### delete_repo()

**Signature**: `delete_repo(db: Session, repo_id: str)`

**Purpose**: Delete a repo and its workflow assignments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |

**Returns**: `None`

---

#### assign_workflow()

**Signature**: `assign_workflow(db: Session, *, repo_id: str, workflow_name: str, display_name: str | None = None)`

**Purpose**: Assign a workflow to a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |
| `workflow_name` | `str` | -- | -- |
| `display_name` | `str | None` | `None` | -- |

**Returns**: `RepoWorkflowAssignment`

---

#### unassign_workflow()

**Signature**: `unassign_workflow(db: Session, *, repo_id: str, workflow_name: str)`

**Purpose**: Remove a workflow assignment from a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |
| `workflow_name` | `str` | -- | -- |

**Returns**: `None`

---

#### list_repo_workflows()

**Signature**: `list_repo_workflows(db: Session, repo_id: str)`

**Purpose**: List workflow assignments for a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |

**Returns**: `list[RepoWorkflowAssignment]`

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
| 2026-08-06 | Initial baseline generated from repository scan | sdlc_00_codebase_v1 |
