---
title: "Module Documentation: agent_runner_backend_v2.api.routes"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/routes.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-routes.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-grpxyiln / 2026-08-05T13:01:30+08:00"
created: "2026-08-05T13:01:30+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.routes

## 1. Module Overview

### 1.1 Purpose

API router aggregation.

### 1.2 Responsibility

This module belongs to the `api` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.api.auth_routes` | internal module | repository dependency |
| `agent_runner_backend_v2.api.host_routes` | internal module | repository dependency |
| `agent_runner_backend_v2.api.repo_routes` | internal module | repository dependency |
| `agent_runner_backend_v2.api.run_routes` | internal module | repository dependency |
| `agent_runner_backend_v2.api.worker_routes` | internal module | repository dependency |
| `agent_runner_backend_v2.api.workflow_routes` | internal module | repository dependency |
| `fastapi` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### health()

**Decorators**: `@router.get`

**Signature**: `health()`

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
