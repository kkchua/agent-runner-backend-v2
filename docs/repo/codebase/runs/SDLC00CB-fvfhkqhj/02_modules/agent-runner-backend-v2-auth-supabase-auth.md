---
title: "Module Documentation: agent_runner_backend_v2.auth.supabase_auth"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/auth/supabase_auth.py"
module_area: "support"
documentation_mode: "summary"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-auth-supabase-auth.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-fvfhkqhj / 2026-08-05T15:35:19+08:00"
created: "2026-08-05T15:35:19+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.auth.supabase_auth

## 1. Module Overview

### 1.1 Purpose

Supabase JWT validation and user context.

### 1.2 Responsibility

This module belongs to the `support` area and is documented as `summary`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `dataclasses` | stdlib module | imported dependency |
| `agent_runner_backend_v2.config` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `fastapi.security` | external module | repository dependency |
| `httpx` | external module | repository dependency |
| `jwt` | external module | repository dependency |
| `structlog` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### UserContext

**Decorators**: `@dataclass`

**Purpose**: Authenticated user context extracted from JWT or API key.


### 2.2 Functions

#### preload_jwks()

**Signature**: `preload_jwks()`

**Purpose**: Fetch and cache Supabase JWKS public keys at startup.

**Returns**: `None`

---

#### decode_supabase_token()

**Signature**: `decode_supabase_token(token: str)`

**Purpose**: Decode and validate a Supabase JWT token using cached public keys or JWT secret fallback.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `token` | `str` | -- | -- |

**Returns**: `dict`

---

#### get_current_user()

**Signature**: `get_current_user(credentials: HTTPAuthorizationCredentials | None = )`

**Purpose**: FastAPI dependency: extract user from Bearer JWT.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `credentials` | `HTTPAuthorizationCredentials | None` | -- | -- |

**Returns**: `UserContext`

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
