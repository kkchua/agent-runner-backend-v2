---
title: "Module Documentation: agent_runner_backend_v2.services.host_service"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/host_service.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-host-service.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-fvfhkqhj / 2026-08-05T15:35:19+08:00"
created: "2026-08-05T15:35:19+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.host_service

## 1. Module Overview

### 1.1 Purpose

Host service -- host machine registration and lookup.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.host` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### register_host()

**Signature**: `register_host(db: Session, *, hostname: str, ip_address: str | None = None, os_type: str = 'windows')`

**Purpose**: Register or return existing host by identity (hostname + ip_address).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `hostname` | `str` | -- | -- |
| `ip_address` | `str | None` | `None` | -- |
| `os_type` | `str` | `'windows'` | -- |

**Returns**: `Host`

---

#### get_host()

**Signature**: `get_host(db: Session, host_id: str)`

**Purpose**: Get a host by ID, raising 404 if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host_id` | `str` | -- | -- |

**Returns**: `Host`

---

#### list_hosts()

**Signature**: `list_hosts(db: Session)`

**Purpose**: List all registered hosts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |

**Returns**: `list[Host]`

---

#### update_host()

**Signature**: `update_host(db: Session, host_id: str, **kwargs)`

**Purpose**: Update a host's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host_id` | `str` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `Host`

---

#### delete_host()

**Signature**: `delete_host(db: Session, host_id: str)`

**Purpose**: Delete a host.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host_id` | `str` | -- | -- |

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
