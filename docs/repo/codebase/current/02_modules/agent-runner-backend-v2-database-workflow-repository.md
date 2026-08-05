---
title: "Module Documentation: agent_runner_backend_v2.database.workflow_repository"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/database/workflow_repository.py"
module_area: "database"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-database-workflow-repository.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-1q5sbtkm / 2026-08-05T16:37:47+08:00"
created: "2026-08-05T16:37:47+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.database.workflow_repository

## 1. Module Overview

### 1.1 Purpose

Repository layer for workflow definition persistence.

### 1.2 Responsibility

This module belongs to the `database` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `agent_runner_backend_v2.models.workflow` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

No public classes.


### 2.2 Functions

#### get_workflow_by_name()

**Signature**: `get_workflow_by_name(db: Session, name: str)`

**Purpose**: Fetch a workflow definition by name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `name` | `str` | -- | -- |

**Returns**: `WorkflowDefinition | None`

---

#### list_workflows()

**Signature**: `list_workflows(db: Session, *, active_only: bool = True)`

**Purpose**: List workflow definitions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `active_only` | `bool` | `True` | -- |

**Returns**: `list[WorkflowDefinition]`

---

#### create_workflow()

**Signature**: `create_workflow(db: Session, workflow: WorkflowDefinition)`

**Purpose**: Insert a new workflow definition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow` | `WorkflowDefinition` | -- | -- |

**Returns**: `WorkflowDefinition`

---

#### update_workflow()

**Signature**: `update_workflow(db: Session, workflow: WorkflowDefinition)`

**Purpose**: Update an existing workflow definition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow` | `WorkflowDefinition` | -- | -- |

**Returns**: `WorkflowDefinition`

---

#### get_step_by_name()

**Signature**: `get_step_by_name(db: Session, *, workflow_id: str, step_name: str)`

**Purpose**: Fetch a step definition by workflow ID and step name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow_id` | `str` | -- | -- |
| `step_name` | `str` | -- | -- |

**Returns**: `WorkflowStepDefinition | None`

---

#### get_next_step_name()

**Signature**: `get_next_step_name(db: Session, *, workflow_id: str, current_step_name: str)`

**Purpose**: Get the next step name after the current step based on onsuccess transition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `workflow_id` | `str` | -- | -- |
| `current_step_name` | `str` | -- | -- |

**Returns**: `str | None`

---

#### create_step_definition()

**Signature**: `create_step_definition(db: Session, step: WorkflowStepDefinition)`

**Purpose**: Insert a new step definition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `step` | `WorkflowStepDefinition` | -- | -- |

**Returns**: `WorkflowStepDefinition`

---

#### create_transition()

**Signature**: `create_transition(db: Session, transition: WorkflowStepTransition)`

**Purpose**: Insert a new step transition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `transition` | `WorkflowStepTransition` | -- | -- |

**Returns**: `WorkflowStepTransition`

---

#### create_coder_policy()

**Signature**: `create_coder_policy(db: Session, policy: WorkflowStepCoderPolicy)`

**Purpose**: Insert a new coder policy.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `policy` | `WorkflowStepCoderPolicy` | -- | -- |

**Returns**: `WorkflowStepCoderPolicy`

---

#### create_artifact_binding()

**Signature**: `create_artifact_binding(db: Session, binding: WorkflowStepArtifactBinding)`

**Purpose**: Insert a new artifact binding.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `binding` | `WorkflowStepArtifactBinding` | -- | -- |

**Returns**: `WorkflowStepArtifactBinding`

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
