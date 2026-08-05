---
title: "Module Documentation: agent_runner_backend_v2.api.auth_routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/auth_routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-auth-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-fvfhkqhj / 2026-08-05T15:35:19+08:00"
created: "2026-08-05T15:35:19+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.auth_routes

## 1. Module Overview

### 1.1 Purpose

Auth API routes -- user info, navigation, API key management.

### 1.2 Responsibility

This module belongs to the `api` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `agent_runner_backend_v2.auth.api_key_auth` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.navigation` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.rbac` | internal module | repository dependency |
| `agent_runner_backend_v2.auth.supabase_auth` | internal module | repository dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.database.api_key_repository` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `pydantic` | external module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### UserInfoResponse

**Inherits from**: `BaseModel`

**Purpose**: Current user information from JWT or API key.

#### NavigationResponse

**Inherits from**: `BaseModel`

**Purpose**: Navigation menu item.

#### CreateAPIKeyRequest

**Inherits from**: `BaseModel`

**Purpose**: Request body for creating a new API key.

#### CreateAPIKeyResponse

**Inherits from**: `BaseModel`

**Purpose**: Response after creating an API key -- includes the plain key (shown once).

#### APIKeyInfo

**Inherits from**: `BaseModel`

**Purpose**: API key info for listing (no secret).


### 2.2 Functions

#### get_me()

**Decorators**: `@router.get`

**Signature**: `get_me(user: UserContext = )`

**Purpose**: Return the current authenticated user's info.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `user` | `UserContext` | -- | -- |

---

#### get_nav()

**Decorators**: `@router.get`

**Signature**: `get_nav(app_id: str = 'agent-runner', user: UserContext = )`

**Purpose**: Return the navigation menu filtered by the user's role.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `app_id` | `str` | `'agent-runner'` | -- |
| `user` | `UserContext` | -- | -- |

---

#### create_key()

**Decorators**: `@router.post`

**Signature**: `create_key(body: CreateAPIKeyRequest, user: UserContext = , db: Session = )`

**Purpose**: Create a new API key. Admin only. The plain key is returned once -- store it securely.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `body` | `CreateAPIKeyRequest` | -- | -- |
| `user` | `UserContext` | -- | -- |
| `db` | `Session` | -- | -- |

---

#### list_keys()

**Decorators**: `@router.get`

**Signature**: `list_keys(user: UserContext = , db: Session = )`

**Purpose**: List all API keys. Admin only. Secrets are never returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `user` | `UserContext` | -- | -- |
| `db` | `Session` | -- | -- |

---

#### delete_key()

**Decorators**: `@router.delete`

**Signature**: `delete_key(key_id: str, user: UserContext = , db: Session = )`

**Purpose**: Revoke an API key. Admin only.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `key_id` | `str` | -- | -- |
| `user` | `UserContext` | -- | -- |
| `db` | `Session` | -- | -- |

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
