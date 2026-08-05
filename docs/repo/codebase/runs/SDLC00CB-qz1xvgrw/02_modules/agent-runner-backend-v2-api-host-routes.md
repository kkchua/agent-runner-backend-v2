---
title: "Module Documentation: agent_runner_backend_v2.api.host_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/host_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-host-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-qz1xvgrw / 2026-08-05T23:20:00+08:00"
created: "2026-08-05T23:20:00+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.host_routes

## 1. Module Overview

### 1.1 Purpose

Host management API routes.

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

#### list_hosts()

**Decorators**: `@router.get`

**Signature**: `list_hosts(db: Session = , user: UserContext = )`

**Purpose**: List all registered hosts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[HostResponse]`

---

#### create_host()

**Decorators**: `@router.post`

**Signature**: `create_host(req: CreateHostRequest, db: Session = , user: UserContext = )`

**Purpose**: Register a new host machine.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `req` | `CreateHostRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `HostResponse`

---

#### get_host()

**Decorators**: `@router.get`

**Signature**: `get_host(host_id: str, db: Session = , user: UserContext = )`

**Purpose**: Get host detail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `host_id` | `str` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `HostResponse`

---

#### update_host()

**Decorators**: `@router.put`

**Signature**: `update_host(host_id: str, req: UpdateHostRequest, db: Session = , user: UserContext = )`

**Purpose**: Update a host's fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `host_id` | `str` | -- | -- |
| `req` | `UpdateHostRequest` | -- | -- |
| `db` | `Session` | -- | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `HostResponse`

---

#### delete_host()

**Decorators**: `@router.delete`

**Signature**: `delete_host(host_id: str, db: Session = , user: UserContext = )`

**Purpose**: Delete a host.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `host_id` | `str` | -- | -- |
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
