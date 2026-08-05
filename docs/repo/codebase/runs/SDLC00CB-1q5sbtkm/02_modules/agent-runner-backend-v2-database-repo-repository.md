---
title: "Module Documentation: agent_runner_backend_v2.database.repo_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/repo_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-repo-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-1q5sbtkm / 2026-08-05T16:37:47+08:00"
created: "2026-08-05T16:37:47+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.repo_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for repo and workflow assignment persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.models.repo` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_repo()

**Signature**: `get_repo(db: Session, repo_id: str)`

**Purpose**: Fetch a repo by its primary key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |

**Returns**: `RepoRegistry | None`

---

#### get_repo_by_name()

**Signature**: `get_repo_by_name(db: Session, name: str, worker_uuid: str)`

**Purpose**: Fetch a repo by name scoped to a specific worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `name` | `str` | -- | -- |
| `worker_uuid` | `str` | -- | -- |

**Returns**: `RepoRegistry | None`

---

#### list_repos()

**Signature**: `list_repos(db: Session)`

**Purpose**: List all registered repos, ordered by name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |

**Returns**: `list[RepoRegistry]`

---

#### list_repos_by_worker()

**Signature**: `list_repos_by_worker(db: Session, worker_uuid: str)`

**Purpose**: List repos assigned to a specific worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_uuid` | `str` | -- | -- |

**Returns**: `list[RepoRegistry]`

---

#### create_repo()

**Signature**: `create_repo(db: Session, repo: RepoRegistry)`

**Purpose**: Insert a new repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo` | `RepoRegistry` | -- | -- |

**Returns**: `RepoRegistry`

---

#### update_repo()

**Signature**: `update_repo(db: Session, repo: RepoRegistry, **kwargs)`

**Purpose**: Update repo fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo` | `RepoRegistry` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `RepoRegistry`

---

#### delete_repo()

**Signature**: `delete_repo(db: Session, repo: RepoRegistry)`

**Purpose**: Delete a repo and its workflow assignments (cascade).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo` | `RepoRegistry` | -- | -- |

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

#### get_repo_workflow()

**Signature**: `get_repo_workflow(db: Session, *, repo_id: str, workflow_name: str)`

**Purpose**: Fetch a specific workflow assignment for a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `repo_id` | `str` | -- | -- |
| `workflow_name` | `str` | -- | -- |

**Returns**: `RepoWorkflowAssignment | None`

---

#### create_workflow_assignment()

**Signature**: `create_workflow_assignment(db: Session, assignment: RepoWorkflowAssignment)`

**Purpose**: Insert a new workflow assignment.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `assignment` | `RepoWorkflowAssignment` | -- | -- |

**Returns**: `RepoWorkflowAssignment`

---

#### delete_workflow_assignment()

**Signature**: `delete_workflow_assignment(db: Session, assignment: RepoWorkflowAssignment)`

**Purpose**: Delete a workflow assignment.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `assignment` | `RepoWorkflowAssignment` | -- | -- |

**Returns**: `None`

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
