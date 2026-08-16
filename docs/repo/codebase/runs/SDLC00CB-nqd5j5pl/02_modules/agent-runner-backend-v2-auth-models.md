---
title: "Module Documentation: agent_runner_backend_v2.auth.models"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/auth/models.py"
module_area: "support"
documentation_mode: "summary"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-auth-models.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-nqd5j5pl / 2026-08-06T14:58:43+08:00"
created: "2026-08-06T14:58:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.auth.models

## 1. Module Overview

### 1.1 Purpose

API key model for script/machine authentication.

### 1.2 Responsibility

This module belongs to the `support` area and is documented as `summary`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `datetime` | stdlib module | imported dependency |
| `uuid` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `sqlalchemy` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### APIKey

**Inherits from**: `Base`

**Purpose**: An API key for script/machine authentication.


### 2.2 Functions

No public functions.


### 2.3 Constants / Configuration

No public constants.


## 3. Error Handling

No documented exceptions.


## 4. Testing

### 4.1 Test Coverage

| Test File | Coverage Area |
|-----------|---------------|
| `tests/conftest.py` | `agent_runner_backend_v2.auth.models` |


## 5. Change Log

| Date | Change | Verified By |
|------|--------|-------------|
| 2026-08-06 | Initial baseline generated from repository scan | sdlc_00_codebase_v1 |
