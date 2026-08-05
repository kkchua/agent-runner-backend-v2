---
title: "Module Documentation: agent_runner_backend_v2.api.schemas"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/api/schemas.py"
module_area: "api"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-api-schemas.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-grpxyiln / 2026-08-05T13:01:30+08:00"
created: "2026-08-05T13:01:30+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.api.schemas

## 1. Module Overview

### 1.1 Purpose

Pydantic request/response schemas for the API.

### 1.2 Responsibility

This module belongs to the `api` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `pydantic` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### SubmitRunRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### RunResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### RunListResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### ActionRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### ResetStepRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### ErrorResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### RegisterWorkerRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### HeartbeatRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### HeartbeatResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### UpdateWorkerRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### WorkerResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### ClaimResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### OutcomeRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### OutcomeResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### SyncWorkflowRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### WorkflowResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### CreateHostRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### UpdateHostRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### HostResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### CreateRepoRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### UpdateRepoRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### AssignWorkflowRequest

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### RepoWorkflowResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class

#### RepoResponse

**Inherits from**: `BaseModel`

**Purpose**: Public class


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
| (none) | No test references found |


## 5. Change Log

| Date | Change | Verified By |
|------|--------|-------------|
| 2026-08-05 | Initial baseline generated from repository scan | sdlc_00_codebase_v1 |
