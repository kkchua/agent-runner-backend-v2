---
title: "Module Documentation: agent_runner_backend_v2.auth.api_key_auth"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/auth/api_key_auth.py"
module_area: "support"
documentation_mode: "summary"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-auth-api-key-auth.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-fvfhkqhj / 2026-08-05T15:35:19+08:00"
created: "2026-08-05T15:35:19+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.auth.api_key_auth

## 1. Module Overview

### 1.1 Purpose

API key authentication for scripts and machines.

### 1.2 Responsibility

This module belongs to the `support` area and is documented as `summary`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.auth.models` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.supabase_auth` | internal module | repository dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.database.api_key_repository` | internal module | repository dependency |
| `bcrypt` | external module | repository dependency |
| `fastapi` | external module | repository dependency |
| `fastapi.security` | external module | repository dependency |
| `structlog` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### hash_api_key()

**Signature**: `hash_api_key(key: str)`

**Purpose**: Hash an API key using bcrypt.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `key` | `str` | -- | -- |

**Returns**: `str`

---

#### verify_api_key()

**Signature**: `verify_api_key(plain_key: str, key_hash: str)`

**Purpose**: Verify a plain API key against a bcrypt hash.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `plain_key` | `str` | -- | -- |
| `key_hash` | `str` | -- | -- |

**Returns**: `bool`

---

#### generate_api_key()

**Signature**: `generate_api_key()`

**Purpose**: Generate a new API key and return (plain_key, key_hash).

**Returns**: `tuple[str, str]`

---

#### get_api_key_user()

**Signature**: `get_api_key_user(api_key: str | None = , db = )`

**Purpose**: FastAPI dependency: authenticate via X-API-Key header.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `api_key` | `str | None` | -- | -- |
| `db` | -- | -- | -- |

**Returns**: `UserContext`

---


### 2.3 Constants / Configuration

| Name | Purpose |
|------|--------|
| `API_KEY_HEADER` | module configuration |


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
