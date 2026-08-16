---
title: "Module Documentation: agent_runner_backend_v2.api.workflow_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/workflow_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-workflow-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-a8mugds1 / 2026-08-05T22:16:43+08:00"
created: "2026-08-05T22:16:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.workflow_routes

## 1. Module Overview

### 1.1 Purpose

Workflow management API routes.

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

#### sync_workflow()

**Decorators**: `@router.post`

**Signature**: `sync_workflow(req: SyncWorkflowRequest, db: Session = , user: UserContext = )`

**Purpose**: Sync a workflow definition from the runner.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `req` | `SyncWorkflowRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `WorkflowResponse`

---

#### list_workflows()

**Decorators**: `@router.get`

**Signature**: `list_workflows(db: Session = , user: UserContext = )`

**Purpose**: List all active workflow definitions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[WorkflowResponse]`

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
