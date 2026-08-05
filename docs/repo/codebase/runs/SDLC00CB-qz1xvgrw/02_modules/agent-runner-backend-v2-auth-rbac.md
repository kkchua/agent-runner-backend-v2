---
title: "Module Documentation: agent_runner_backend_v2.auth.rbac"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/auth/rbac.py"
module_area: "support"
documentation_mode: "summary"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-auth-rbac.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-qz1xvgrw / 2026-08-05T23:20:00+08:00"
created: "2026-08-05T23:20:00+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.auth.rbac

## 1. Module Overview

### 1.1 Purpose

Role-based access control dependencies.

### 1.2 Responsibility

This module belongs to the `support` area and is documented as `summary`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `collections.abc` | stdlib module | imported dependency |
| `agent_runner_backend_v2.auth.supabase_auth` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |
| `fastapi.security` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### require_role()

**Signature**: `require_role(*allowed_roles: str)`

**Purpose**: FastAPI dependency factory: require the user to have one of the specified roles.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `*allowed_roles` | `str` | -- | -- |

**Returns**: `Callable`

---

#### require_jwt_or_api_key()

**Signature**: `require_jwt_or_api_key(*allowed_roles: str)`

**Purpose**: FastAPI dependency factory: accept either JWT or API key, then check role.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `*allowed_roles` | `str` | -- | -- |

**Returns**: `Callable`

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
