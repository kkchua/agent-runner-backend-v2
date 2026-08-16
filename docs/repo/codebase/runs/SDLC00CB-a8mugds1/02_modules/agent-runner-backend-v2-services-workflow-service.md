---
title: "Module Documentation: agent_runner_backend_v2.services.workflow_service"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/workflow_service.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-workflow-service.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-a8mugds1 / 2026-08-05T22:16:43+08:00"
created: "2026-08-05T22:16:43+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.workflow_service

## 1. Module Overview

### 1.1 Purpose

Workflow service -- workflow definition sync and query.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `hashlib` | stdlib module | imported dependency |
| `json` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.workflow` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### sync_workflow()

**Signature**: `sync_workflow(db: Session, *, workflow_name: str, definition: dict)`

**Purpose**: Sync a workflow definition from the runner.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow_name` | `str` | -- | -- |
| `definition` | `dict` | -- | -- |

**Returns**: `WorkflowDefinition`

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
