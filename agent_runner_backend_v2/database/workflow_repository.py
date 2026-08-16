"""Repository layer for workflow definition persistence."""
from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from agent_runner_backend_v2.models.workflow import (
    WorkflowDefinition,
    WorkflowStepArtifactBinding,
    WorkflowStepCoderPolicy,
    WorkflowStepDefinition,
    WorkflowStepTransition,
)


def get_workflow_by_name(db: Session, name: str) -> WorkflowDefinition | None:
    """Fetch a workflow definition by name."""
    return db.query(WorkflowDefinition).filter(WorkflowDefinition.name == name).first()


def list_workflows(db: Session, *, active_only: bool = True) -> list[WorkflowDefinition]:
    """List workflow definitions with steps and artifact bindings eagerly loaded."""
    query = db.query(WorkflowDefinition).options(
        joinedload(WorkflowDefinition.steps)
        .joinedload(WorkflowStepDefinition.artifact_bindings),
    )
    if active_only:
        query = query.filter(WorkflowDefinition.is_active.is_(True))
    return query.order_by(WorkflowDefinition.name).all()


def create_workflow(db: Session, workflow: WorkflowDefinition) -> WorkflowDefinition:
    """Insert a new workflow definition."""
    db.add(workflow)
    db.flush()
    return workflow


def update_workflow(db: Session, workflow: WorkflowDefinition) -> WorkflowDefinition:
    """Update an existing workflow definition."""
    db.flush()
    return workflow


def get_step_by_name(
    db: Session, *, workflow_id: str, step_name: str,
) -> WorkflowStepDefinition | None:
    """Fetch a step definition by workflow ID and step name."""
    return (
        db.query(WorkflowStepDefinition)
        .filter(
            WorkflowStepDefinition.workflow_definition_id == workflow_id,
            WorkflowStepDefinition.step_name == step_name,
        )
        .first()
    )


def get_next_step_name(
    db: Session, *, workflow_id: str, current_step_name: str,
) -> str | None:
    """Get the next step name after the current step based on onsuccess transition."""
    current_step = get_step_by_name(db, workflow_id=workflow_id, step_name=current_step_name)
    if not current_step:
        return None

    for transition in current_step.transitions:
        if transition.transition_type == "onsuccess" and transition.outcome == "approved":
            return transition.target_step_name
    return None


def create_step_definition(
    db: Session, step: WorkflowStepDefinition,
) -> WorkflowStepDefinition:
    """Insert a new step definition."""
    db.add(step)
    db.flush()
    return step


def create_transition(
    db: Session, transition: WorkflowStepTransition,
) -> WorkflowStepTransition:
    """Insert a new step transition."""
    db.add(transition)
    db.flush()
    return transition


def create_coder_policy(
    db: Session, policy: WorkflowStepCoderPolicy,
) -> WorkflowStepCoderPolicy:
    """Insert a new coder policy."""
    db.add(policy)
    db.flush()
    return policy


def create_artifact_binding(
    db: Session, binding: WorkflowStepArtifactBinding,
) -> WorkflowStepArtifactBinding:
    """Insert a new artifact binding."""
    db.add(binding)
    db.flush()
    return binding
