"""Workflow service — workflow definition sync and query."""
from __future__ import annotations

import hashlib
import json

from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import workflow_repository
from agent_runner_backend_v2.models.workflow import (
    WorkflowDefinition,
    WorkflowStepArtifactBinding,
    WorkflowStepCoderPolicy,
    WorkflowStepDefinition,
    WorkflowStepTransition,
)


def sync_workflow(
    db: Session,
    *,
    workflow_name: str,
    definition: dict,
) -> WorkflowDefinition:
    """Sync a workflow definition from the runner.

    Creates or updates the workflow, its steps, transitions, coder policies,
    and artifact bindings.
    """
    source_hash = hashlib.sha256(
        json.dumps(definition, sort_keys=True).encode()
    ).hexdigest()

    existing = workflow_repository.get_workflow_by_name(db, workflow_name)

    if existing:
        # Update existing
        existing.job_prefix = definition.get("job_prefix", "JOB")
        existing.init_step = definition.get("init_step") or definition.get("job_init_step")
        existing.default_max_rejects = definition.get("default_max_rejects", 0)
        existing.raw_definition = definition
        existing.source_hash = source_hash
        existing.is_active = True
        _sync_steps(db, existing, definition)
        return existing

    # Create new
    wf = WorkflowDefinition(
        name=workflow_name,
        job_prefix=definition.get("job_prefix", "JOB"),
        init_step=definition.get("init_step") or definition.get("job_init_step"),
        default_max_rejects=definition.get("default_max_rejects", 0),
        raw_definition=definition,
        source_hash=source_hash,
    )
    workflow_repository.create_workflow(db, wf)
    _sync_steps(db, wf, definition)
    return wf


def _sync_steps(db: Session, wf: WorkflowDefinition, definition: dict) -> None:
    """Sync step definitions, transitions, coder policies, and artifact bindings."""
    steps_config = definition.get("steps", {})
    if isinstance(steps_config, list):
        # Legacy format: list of step names
        for i, step_name in enumerate(steps_config):
            _ensure_step(db, wf, step_name, i + 1, {})
        return

    # Dict format: {step_name: step_config}
    for i, (step_name, step_cfg) in enumerate(steps_config.items()):
        _ensure_step(db, wf, step_name, i + 1, step_cfg)


def _ensure_step(
    db: Session,
    wf: WorkflowDefinition,
    step_name: str,
    step_order: int,
    step_cfg: dict,
) -> WorkflowStepDefinition:
    """Ensure a step definition exists with its transitions and policies."""
    existing = workflow_repository.get_step_by_name(db, workflow_id=wf.id, step_name=step_name)

    if existing:
        existing.step_order = step_order
        existing.raw_config = step_cfg
        existing.requires_human_approval = step_cfg.get("requires_human_approval_after", False)
        existing.execution_kind = "action" if step_cfg.get("action") else "coder"
        existing.prompt_file = step_cfg.get("prompt_file")
        existing.action = step_cfg.get("action")
        db.flush()
        step = existing
    else:
        step = WorkflowStepDefinition(
            workflow_definition_id=wf.id,
            step_name=step_name,
            step_order=step_order,
            execution_kind="action" if step_cfg.get("action") else "coder",
            prompt_file=step_cfg.get("prompt_file"),
            action=step_cfg.get("action"),
            requires_human_approval=step_cfg.get("requires_human_approval_after", False),
            raw_config=step_cfg,
        )
        workflow_repository.create_step_definition(db, step)

    # Sync transitions
    _sync_transitions(db, step, step_cfg)

    # Sync coder policy
    _sync_coder_policy(db, step, step_cfg.get("coder", {}))

    # Sync artifact bindings
    _sync_artifact_bindings(db, step, step_cfg)

    return step


def _sync_transitions(db: Session, step: WorkflowStepDefinition, step_cfg: dict) -> None:
    """Sync onsuccess transition."""
    onsuccess = step_cfg.get("onsuccess")
    if onsuccess:
        existing = next(
            (t for t in step.transitions
             if t.transition_type == "onsuccess" and t.outcome == "approved"),
            None,
        )
        if existing:
            existing.target_step_name = onsuccess
        else:
            t = WorkflowStepTransition(
                step_definition_id=step.id,
                transition_type="onsuccess",
                outcome="approved",
                target_step_name=onsuccess,
            )
            workflow_repository.create_transition(db, t)


def _sync_coder_policy(db: Session, step: WorkflowStepDefinition, coder_cfg: dict) -> None:
    """Sync coder policy for a step."""
    if not coder_cfg:
        return

    if step.coder_policy:
        step.coder_policy.default_coder = coder_cfg.get("role_policy")
        step.coder_policy.allowed_coders = coder_cfg.get("allowed", [])
        step.coder_policy.must_differ = coder_cfg.get("must_differ", False)
    else:
        policy = WorkflowStepCoderPolicy(
            step_definition_id=step.id,
            default_coder=coder_cfg.get("role_policy"),
            allowed_coders=coder_cfg.get("allowed", []),
            must_differ=coder_cfg.get("must_differ", False),
        )
        workflow_repository.create_coder_policy(db, policy)


def _sync_artifact_bindings(db: Session, step: WorkflowStepDefinition, step_cfg: dict) -> None:
    """Sync artifact bindings (produces, required_inputs) for a step."""
    artifacts_cfg = step_cfg.get("artifacts", {})
    if not artifacts_cfg:
        return

    produces = artifacts_cfg.get("produces", [])
    required_inputs = artifacts_cfg.get("required_inputs", [])

    existing_keys = {b.artifact_key for b in step.artifact_bindings}

    for key in produces:
        if key not in existing_keys:
            binding = WorkflowStepArtifactBinding(
                step_definition_id=step.id,
                artifact_key=key,
                binding_type="produces",
            )
            workflow_repository.create_artifact_binding(db, binding)

    for key in required_inputs:
        if key not in existing_keys:
            binding = WorkflowStepArtifactBinding(
                step_definition_id=step.id,
                artifact_key=key,
                binding_type="required_input",
            )
            workflow_repository.create_artifact_binding(db, binding)
