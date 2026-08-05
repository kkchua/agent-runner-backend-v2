---
title: "Module Documentation: agent_runner_backend_v2.database.worker_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/worker_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-worker-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-fvfhkqhj / 2026-08-05T15:35:19+08:00"
created: "2026-08-05T15:35:19+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.worker_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for worker persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.models.worker` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |
| `sqlalchemy.orm.attributes` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_worker()

**Signature**: `get_worker(db: Session, worker_id: str)`

**Purpose**: Fetch a worker by ID.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `WorkerRegistry | None`

---

#### list_workers()

**Signature**: `list_workers(db: Session)`

**Purpose**: List all registered workers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |

**Returns**: `list[WorkerRegistry]`

---

#### upsert_worker()

**Signature**: `upsert_worker(db: Session, worker: WorkerRegistry)`

**Purpose**: Insert or update a worker registration.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker` | `WorkerRegistry` | -- | -- |

**Returns**: `WorkerRegistry`

---

#### update_heartbeat()

**Signature**: `update_heartbeat(db: Session, worker: WorkerRegistry, *, status: str, current_run_id: str | None = None, current_step_run_id: str | None = None, heartbeat_time: datetime | None = None)`

**Purpose**: Update worker heartbeat and current assignment.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker` | `WorkerRegistry` | -- | -- |
| `status` | `str` | -- | -- |
| `current_run_id` | `str | None` | `None` | -- |
| `current_step_run_id` | `str | None` | `None` | -- |
| `heartbeat_time` | `datetime | None` | `None` | -- |

**Returns**: `WorkerRegistry`

---

#### update_worker()

**Signature**: `update_worker(db: Session, worker: WorkerRegistry, **kwargs)`

**Purpose**: Update arbitrary fields on a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker` | `WorkerRegistry` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `WorkerRegistry`

---

#### delete_worker()

**Signature**: `delete_worker(db: Session, worker: WorkerRegistry)`

**Purpose**: Delete a worker from the registry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker` | `WorkerRegistry` | -- | -- |

**Returns**: `None`

---

#### list_stale_workers()

**Signature**: `list_stale_workers(db: Session, *, timeout_seconds: int)`

**Purpose**: List workers whose last heartbeat exceeds the timeout.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `timeout_seconds` | `int` | -- | -- |

**Returns**: `list[WorkerRegistry]`

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
