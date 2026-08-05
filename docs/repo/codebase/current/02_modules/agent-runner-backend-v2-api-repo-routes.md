---
title: "Module Documentation: agent_runner_backend_v2.api.repo_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/repo_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-repo-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-1q5sbtkm / 2026-08-05T16:37:47+08:00"
created: "2026-08-05T16:37:47+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.repo_routes

## 1. Module Overview

### 1.1 Purpose

Repo management API routes.

### 1.2 Responsibility

This module belongs to the `api` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.api.schemas` | internal module | repository dependency |
| `agent_runner_backend_v2.api.serializers` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.rbac` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.supabase_auth` | internal module | repository dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.services` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### list_repos()

**Decorators**: `@router.get`

**Signature**: `list_repos(db: Session = , user: UserContext = )`

**Purpose**: List all registered repos with their workflow assignments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[RepoResponse]`

---

#### create_repo()

**Decorators**: `@router.post`

**Signature**: `create_repo(req: CreateRepoRequest, db: Session = , user: UserContext = )`

**Purpose**: Register a new repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `req` | `CreateRepoRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RepoResponse`

---

#### get_repo()

**Decorators**: `@router.get`

**Signature**: `get_repo(repo_id: str, db: Session = , user: UserContext = )`

**Purpose**: Get repo detail with workflow assignments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RepoResponse`

---

#### update_repo()

**Decorators**: `@router.put`

**Signature**: `update_repo(repo_id: str, req: UpdateRepoRequest, db: Session = , user: UserContext = )`

**Purpose**: Update a repo's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `req` | `UpdateRepoRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RepoResponse`

---

#### delete_repo()

**Decorators**: `@router.delete`

**Signature**: `delete_repo(repo_id: str, db: Session = , user: UserContext = )`

**Purpose**: Delete a repo and its workflow assignments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `dict`

---

#### list_repo_workflows()

**Decorators**: `@router.get`

**Signature**: `list_repo_workflows(repo_id: str, db: Session = , user: UserContext = )`

**Purpose**: List workflow assignments for a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[RepoWorkflowResponse]`

---

#### assign_workflow()

**Decorators**: `@router.post`

**Signature**: `assign_workflow(repo_id: str, req: AssignWorkflowRequest, db: Session = , user: UserContext = )`

**Purpose**: Assign a workflow to a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `req` | `AssignWorkflowRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RepoWorkflowResponse`

---

#### unassign_workflow()

**Decorators**: `@router.delete`

**Signature**: `unassign_workflow(repo_id: str, workflow_name: str, db: Session = , user: UserContext = )`

**Purpose**: Remove a workflow assignment from a repo.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `repo_id` | `str` | -- | -- |
| `workflow_name` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `dict`

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
