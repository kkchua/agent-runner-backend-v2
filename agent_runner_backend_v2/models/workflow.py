"""Workflow definition models."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import utcnow


class WorkflowDefinition(Base):
    """A named workflow with its step sequence, configuration, and routing rules."""

    __tablename__ = "workflow_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False, unique=True)
    job_prefix = Column(String(50), nullable=False)
    init_step = Column(String(120), nullable=True)
    default_max_rejects = Column(Integer, nullable=False, default=0)
    raw_definition = Column(JSONB, nullable=False, default=dict)
    source_hash = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    steps = relationship(
        "WorkflowStepDefinition",
        back_populates="workflow_definition",
        cascade="all, delete-orphan",
        order_by="WorkflowStepDefinition.step_order",
    )


class WorkflowStepDefinition(Base):
    """A single step within a workflow definition."""

    __tablename__ = "workflow_step_definitions"
    __table_args__ = (
        UniqueConstraint("workflow_definition_id", "step_name", name="uq_workflow_step_name"),
        UniqueConstraint("workflow_definition_id", "step_order", name="uq_workflow_step_order"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_definition_id = Column(
        String(36),
        ForeignKey("workflow_definitions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    step_name = Column(String(120), nullable=False)
    step_order = Column(Integer, nullable=False)
    execution_kind = Column(String(30), nullable=False, default="coder")
    prompt_file = Column(Text, nullable=True)
    action = Column(String(100), nullable=True)
    requires_human_approval = Column(Boolean, nullable=False, default=False)
    raw_config = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    workflow_definition = relationship("WorkflowDefinition", back_populates="steps")
    transitions = relationship(
        "WorkflowStepTransition",
        back_populates="step_definition",
        cascade="all, delete-orphan",
    )
    coder_policy = relationship(
        "WorkflowStepCoderPolicy",
        back_populates="step_definition",
        cascade="all, delete-orphan",
        uselist=False,
    )
    artifact_bindings = relationship(
        "WorkflowStepArtifactBinding",
        back_populates="step_definition",
        cascade="all, delete-orphan",
    )


class WorkflowStepTransition(Base):
    """A transition rule from a step to another step based on outcome."""

    __tablename__ = "workflow_step_transitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    step_definition_id = Column(
        String(36),
        ForeignKey("workflow_step_definitions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    transition_type = Column(String(50), nullable=False)
    outcome = Column(String(50), nullable=False)
    target_step_name = Column(String(120), nullable=False)
    config = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    step_definition = relationship("WorkflowStepDefinition", back_populates="transitions")


class WorkflowStepCoderPolicy(Base):
    """Coder assignment policy for a step definition."""

    __tablename__ = "workflow_step_coder_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    step_definition_id = Column(
        String(36),
        ForeignKey("workflow_step_definitions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    default_coder = Column(String(50), nullable=True)
    allowed_coders = Column(JSONB, nullable=False, default=list)
    must_differ = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    step_definition = relationship("WorkflowStepDefinition", back_populates="coder_policy")


class WorkflowStepArtifactBinding(Base):
    """Binding between a step definition and an artifact key with a role."""

    __tablename__ = "workflow_step_artifact_bindings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    step_definition_id = Column(
        String(36),
        ForeignKey("workflow_step_definitions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    artifact_key = Column(String(100), nullable=False)
    binding_type = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    step_definition = relationship("WorkflowStepDefinition", back_populates="artifact_bindings")
