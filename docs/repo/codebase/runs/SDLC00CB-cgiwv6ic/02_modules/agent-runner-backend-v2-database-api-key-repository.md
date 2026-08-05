---
title: "Module Documentation: agent_runner_backend_v2.database.api_key_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/api_key_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-api-key-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-cgiwv6ic / 2026-08-05T10:13:53+08:00"
created: "2026-08-05T10:13:53+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.api_key_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for API key persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.auth.models` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_api_key_by_id()

**Signature**: `get_api_key_by_id(db: Session, key_id: str)`

**Purpose**: Fetch an API key by its primary key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `key_id` | `str` | -- | -- |

**Returns**: `APIKey | None`

---

#### get_api_key_by_prefix()

**Signature**: `get_api_key_by_prefix(db: Session, prefix: str)`

**Purpose**: Fetch API keys matching a key prefix (for lookup optimization).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `prefix` | `str` | -- | -- |

**Returns**: `list[APIKey]`

---

#### list_api_keys()

**Signature**: `list_api_keys(db: Session, *, active_only: bool = False)`

**Purpose**: List all API keys, optionally filtering to active only.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `active_only` | `bool` | `False` | -- |

**Returns**: `list[APIKey]`

---

#### create_api_key()

**Signature**: `create_api_key(db: Session, *, key_hash: str, key_prefix: str, name: str, role: str, created_by: str, expires_at: datetime | None = None)`

**Purpose**: Insert a new API key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `key_hash` | `str` | -- | -- |
| `key_prefix` | `str` | -- | -- |
| `name` | `str` | -- | -- |
| `role` | `str` | -- | -- |
| `created_by` | `str` | -- | -- |
| `expires_at` | `datetime | None` | `None` | -- |

**Returns**: `APIKey`

---

#### revoke_api_key()

**Signature**: `revoke_api_key(db: Session, api_key: APIKey)`

**Purpose**: Soft-delete an API key by marking it inactive.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `api_key` | `APIKey` | -- | -- |

**Returns**: `None`

---

#### update_last_used()

**Signature**: `update_last_used(db: Session, api_key: APIKey)`

**Purpose**: Update the last_used_at timestamp.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `api_key` | `APIKey` | -- | -- |

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
