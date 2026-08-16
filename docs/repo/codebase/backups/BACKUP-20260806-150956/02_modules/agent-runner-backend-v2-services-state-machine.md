---
title: "Module Documentation: agent_runner_backend_v2.services.state_machine"
template_id: "CB-02"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
module_path: "agent_runner_backend_v2/services/state_machine.py"
module_area: "services"
documentation_mode: "full"
owner_doc_path: "docs/repo/codebase/current/02_modules/agent-runner-backend-v2-services-state-machine.md"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-8vg4jzti / 2026-08-05T23:33:46+08:00"
created: "2026-08-05T23:33:46+08:00"
owner: "sdlc_00_codebase_v1"
---

# Module Documentation: agent_runner_backend_v2.services.state_machine

## 1. Module Overview

### 1.1 Purpose

V2 State Machine Engine -- the single authority for run state transitions.

### 1.2 Responsibility

This module belongs to the `services` area and is documented as `full`.

### 1.3 Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `__future__` | stdlib module | imported dependency |
| `dataclasses` | stdlib module | imported dependency |
| `enum` | stdlib module | imported dependency |
| `typing` | stdlib module | imported dependency |
| `agent_runner_backend_v2.database` | internal module | repository dependency |
| `agent_runner_backend_v2.models.run` | internal module | repository dependency |
| `agent_runner_backend_v2.models.workflow` | internal module | repository dependency |
| `sqlalchemy.orm` | external module | repository dependency |

## 2. Public API

### 2.1 Classes

#### RunStatus

**Inherits from**: `str`, `Enum`

**Purpose**: Public class

#### Action

**Inherits from**: `str`, `Enum`

**Purpose**: Public class

#### FailureClass

**Inherits from**: `str`, `Enum`

**Purpose**: Public class

#### EventType

**Inherits from**: `str`, `Enum`

**Purpose**: Public class

#### TransitionEvent

**Decorators**: `@dataclass`

**Purpose**: An event that triggers a state transition.

#### TransitionResult

**Decorators**: `@dataclass`

**Purpose**: The outcome of a state transition.

**Methods**:

- `is_error()` -> `bool` -- method


### 2.2 Functions

#### transition()

**Signature**: `transition(db: Session, run: WorkflowRun, event: TransitionEvent, workflow: WorkflowDefinition)`

**Purpose**: Compute the next state given (current_state, event, workflow_rules).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Session` | -- | -- |
| `run` | `WorkflowRun` | -- | -- |
| `event` | `TransitionEvent` | -- | -- |
| `workflow` | `WorkflowDefinition` | -- | -- |

**Returns**: `TransitionResult`

---

#### get_valid_actions()

**Signature**: `get_valid_actions(run: WorkflowRun)`

**Purpose**: Return the list of valid actions for a run's current status.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `run` | `WorkflowRun` | -- | -- |

**Returns**: `list[str]`

---


### 2.3 Constants / Configuration

| Name | Purpose |
|------|--------|
| `TERMINAL_STATUSES` | module configuration |
| `NON_TERMINAL_STATUSES` | module configuration |
| `CLAIMABLE_STATUSES` | module configuration |
| `USER_ACTION_STATUSES` | module configuration |


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
