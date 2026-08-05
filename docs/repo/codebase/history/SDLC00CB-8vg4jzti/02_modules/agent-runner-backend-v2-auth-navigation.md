---
title: "Module Documentation: agent_runner_backend_v2.auth.navigation"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/auth/navigation.py"
module_area: "support"
documentation_mode: "summary"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-auth-navigation.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-1q5sbtkm / 2026-08-05T16:37:47+08:00"
created: "2026-08-05T16:37:47+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.auth.navigation

## 1. Module Overview

### 1.1 Purpose

Navigation/menu configuration and endpoint.

### 1.2 Responsibility

This module belongs to the `support` area and is documented as `summary`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `dataclasses` | stdlib module | imported dependency |
| `agent_runner_backend_v2.auth.supabase_auth` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### MenuItem

**Decorators**: `@dataclass`

**Purpose**: A single navigation menu item.

**Methods**:

- `to_dict()` -> `dict` -- Convert to dict, recursively converting children.


### 2.2 Functions

#### get_navigation()

**Signature**: `get_navigation(app_id: str = 'agent-runner', user: UserContext = )`

**Purpose**: Return the navigation menu filtered by the user's role.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `app_id` | `str` | `'agent-runner'` | -- |
| `user` | `UserContext` | -- | -- |

**Returns**: `list[dict]`

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
