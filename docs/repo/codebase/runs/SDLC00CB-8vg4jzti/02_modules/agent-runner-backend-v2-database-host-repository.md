---
title: "Module Documentation: agent_runner_backend_v2.database.host_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/host_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-host-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-8vg4jzti / 2026-08-05T23:33:46+08:00"
created: "2026-08-05T23:33:46+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.host_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for host machine persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.models.host` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_host()

**Signature**: `get_host(db: Session, host_id: str)`

**Purpose**: Fetch a host by its primary key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host_id` | `str` | -- | -- |

**Returns**: `Host | None`

---

#### get_host_by_identity()

**Signature**: `get_host_by_identity(db: Session, *, hostname: str, ip_address: str | None = None)`

**Purpose**: Fetch a host by hostname + ip_address combination.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `hostname` | `str` | -- | -- |
| `ip_address` | `str | None` | `None` | -- |

**Returns**: `Host | None`

---

#### list_hosts()

**Signature**: `list_hosts(db: Session)`

**Purpose**: List all registered hosts, ordered by hostname.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |

**Returns**: `list[Host]`

---

#### create_host()

**Signature**: `create_host(db: Session, host: Host)`

**Purpose**: Insert a new host.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host` | `Host` | -- | -- |

**Returns**: `Host`

---

#### update_host()

**Signature**: `update_host(db: Session, host: Host, **kwargs)`

**Purpose**: Update host fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host` | `Host` | -- | -- |
| `**kwargs` | -- | -- | -- |

**Returns**: `Host`

---

#### delete_host()

**Signature**: `delete_host(db: Session, host: Host)`

**Purpose**: Delete a host.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `host` | `Host` | -- | -- |

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
