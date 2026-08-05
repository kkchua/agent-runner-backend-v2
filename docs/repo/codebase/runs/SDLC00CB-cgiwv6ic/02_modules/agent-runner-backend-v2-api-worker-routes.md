---
title: "Module Documentation: agent_runner_backend_v2.api.worker_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/worker_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-worker-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-cgiwv6ic / 2026-08-05T10:13:53+08:00"
created: "2026-08-05T10:13:53+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.worker_routes

## 1. Module Overview

### 1.1 Purpose

Worker management API routes.

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

#### register_worker()

**Decorators**: `@router.post`

**Signature**: `register_worker(req: RegisterWorkerRequest, db: Session = , user: UserContext = )`

**Purpose**: Register or update a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `req` | `RegisterWorkerRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `WorkerResponse`

---

#### heartbeat()

**Decorators**: `@router.post`

**Signature**: `heartbeat(worker_id: str, req: HeartbeatRequest, db: Session = , user: UserContext = )`

**Purpose**: Update worker heartbeat.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `req` | `HeartbeatRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `HeartbeatResponse`

---

#### claim_work()

**Decorators**: `@router.post`

**Signature**: `claim_work(worker_id: str, db: Session = , user: UserContext = )`

**Purpose**: Claim the next available work for a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `ClaimResponse`

---

#### stop_worker()

**Decorators**: `@router.post`

**Signature**: `stop_worker(worker_id: str, db: Session = , user: UserContext = )`

**Purpose**: Stop a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `dict`

---

#### update_worker()

**Decorators**: `@router.put`

**Signature**: `update_worker(worker_id: str, req: UpdateWorkerRequest, db: Session = , user: UserContext = )`

**Purpose**: Update a worker's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `req` | `UpdateWorkerRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `WorkerResponse`

---

#### delete_worker()

**Decorators**: `@router.delete`

**Signature**: `delete_worker(worker_id: str, db: Session = , user: UserContext = )`

**Purpose**: Delete a worker from the registry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `dict`

---

#### get_worker()

**Decorators**: `@router.get`

**Signature**: `get_worker(worker_id: str, db: Session = , user: UserContext = )`

**Purpose**: Get a single worker by ID.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `worker_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `WorkerResponse`

---

#### list_workers()

**Decorators**: `@router.get`

**Signature**: `list_workers(db: Session = , user: UserContext = )`

**Purpose**: List all registered workers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[WorkerResponse]`

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
