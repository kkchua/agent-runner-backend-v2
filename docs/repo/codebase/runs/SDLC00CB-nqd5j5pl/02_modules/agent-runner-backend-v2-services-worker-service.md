---
title: "Module Documentation: agent_runner_backend_v2.services.worker_service"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/worker_service.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-worker-service.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-nqd5j5pl / 2026-08-06T14:58:43+08:00"
created: "2026-08-06T14:58:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.worker_service

## 1. Module Overview

### 1.1 Purpose

Worker service -- orchestration for worker lifecycle.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.worker` | internal module | repository dependency |
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

#### register_worker()

**Signature**: `register_worker(db: Session, *, worker_id: str, worker_label: str = 'live', capabilities: dict | None = None, host_id: str | None = None)`

**Purpose**: Register or update a worker.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |
| `worker_label` | `str` | `'live'` | -- |
| `capabilities` | `dict | None` | `None` | -- |
| `host_id` | `str | None` | `None` | -- |

**Returns**: `WorkerRegistry`

---

#### heartbeat()

**Signature**: `heartbeat(db: Session, *, worker_id: str, status: str = 'idle', current_run_id: str | None = None, current_step_run_id: str | None = None)`

**Purpose**: Update worker heartbeat.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |
| `status` | `str` | `'idle'` | -- |
| `current_run_id` | `str | None` | `None` | -- |
| `current_step_run_id` | `str | None` | `None` | -- |

**Returns**: `WorkerRegistry | None`

---

#### stop_worker()

**Signature**: `stop_worker(db: Session, *, worker_id: str)`

**Purpose**: Mark a worker as stopped.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `bool`

---

#### get_worker()

**Signature**: `get_worker(db: Session, worker_id: str)`

**Purpose**: Get a worker by ID, raising 404 if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

**Returns**: `WorkerRegistry`

---

#### update_worker()

**Signature**: `update_worker(db: Session, worker_id: str, **kwargs)`

**Purpose**: Update a worker's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `WorkerRegistry`

---

#### delete_worker()

**Signature**: `delete_worker(db: Session, worker_id: str)`

**Purpose**: Delete a worker from the registry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `worker_id` | `str` | -- | -- |

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
| 2026-08-06 | Initial baseline generated from repository scan | sdlc_00_codebase_v1 |
