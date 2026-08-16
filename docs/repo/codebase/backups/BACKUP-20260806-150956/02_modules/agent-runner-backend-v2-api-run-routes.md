---
title: "Module Documentation: agent_runner_backend_v2.api.run_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/run_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-run-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-8vg4jzti / 2026-08-05T23:33:46+08:00"
created: "2026-08-05T23:33:46+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.run_routes

## 1. Module Overview

### 1.1 Purpose

Run management API routes.

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
| `structlog` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### submit_run()

**Decorators**: `@router.post`

**Signature**: `submit_run(req: SubmitRunRequest, db: Session = , user: UserContext = )`

**Purpose**: Submit a new workflow run.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `req` | `SubmitRunRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RunResponse`

---

#### list_runs()

**Decorators**: `@router.get`

**Signature**: `list_runs(status: str | None = None, worker_id: str | None = None, workflow_name: str | None = None, limit: int = 100, offset: int = 0, db: Session = , user: UserContext = )`

**Purpose**: List workflow runs with optional filters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `status` | `str | None` | `None` | -- |
| `worker_id` | `str | None` | `None` | -- |
| `workflow_name` | `str | None` | `None` | -- |
| `limit` | `int` | `100` | -- |
| `offset` | `int` | `0` | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RunListResponse`

---

#### get_run()

**Decorators**: `@router.get`

**Signature**: `get_run(run_id: str, db: Session = , user: UserContext = )`

**Purpose**: Get run detail with valid actions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `run_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RunResponse`

---

#### request_action()

**Decorators**: `@router.post`

**Signature**: `request_action(run_id: str, req: ActionRequest, db: Session = , user: UserContext = )`

**Purpose**: Request an action on a run (approve, reject, resume, retry, cancel).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `run_id` | `str` | -- | -- |
| `req` | `ActionRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RunResponse`

---

#### reset_step()

**Decorators**: `@router.post`

**Signature**: `reset_step(run_id: str, req: ResetStepRequest, db: Session = , user: UserContext = )`

**Purpose**: Reset a run's current step.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `run_id` | `str` | -- | -- |
| `req` | `ResetStepRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `RunResponse`

---

#### report_outcome()

**Decorators**: `@router.post`

**Signature**: `report_outcome(step_run_id: str, req: OutcomeRequest, db: Session = , user: UserContext = )`

**Purpose**: Report a step outcome -- backend computes next state.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `step_run_id` | `str` | -- | -- |
| `req` | `OutcomeRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `OutcomeResponse`

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
