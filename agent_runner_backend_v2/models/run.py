"""Workflow run and step-run execution models."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from agent_runner_backend_v2.database import Base


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class WorkflowRun(Base):
    """A single execution of a workflow with V2 two-field state machine."""

    __tablename__ = "workflow_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_code = Column(String(80), nullable=False, unique=True, index=True)

    workflow_definition_id = Column(
        String(36),
        ForeignKey("workflow_definitions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # V2 two-field state machine
    run_status = Column(String(40), nullable=False, default="USER_SUBMITTED", index=True)
    action_requested = Column(String(40), nullable=True, index=True)
    action_feedback = Column(Text, nullable=True)

    # Cancel tracking — normal cancel sets this flag so claim_work stops
    # serving the run while letting the current child finish naturally.
    cancel_requested = Column(String(20), nullable=True)  # "graceful" or "force"

    # Step tracking
    current_step_name = Column(String(120), nullable=True)
    current_step_run_id = Column(String(36), nullable=True)

    # Worker assignment
    target_worker_id = Column(String(80), nullable=True, index=True)
    claimed_by_worker = Column(String(80), nullable=True, index=True)
    worker_label = Column(String(40), nullable=False, default="live", index=True)

    # Execution context
    project_root = Column(Text, nullable=True)
    workspace_path = Column(Text, nullable=True)
    input_payload = Column(JSONB, nullable=False, default=dict)
    context_payload = Column(JSONB, nullable=False, default=dict)
    error_message = Column(Text, nullable=True)

    # Refine loop tracking: {"step_name": iteration_count, ...}
    refine_iterations = Column(JSONB, nullable=False, default=dict)

    # Timestamps
    submitted_at = Column(DateTime, nullable=False, default=utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    # Relationships
    workflow_definition = relationship("WorkflowDefinition")
    step_runs = relationship(
        "WorkflowStepRun",
        back_populates="workflow_run",
        cascade="all, delete-orphan",
        order_by="WorkflowStepRun.created_at",
    )
    artifacts = relationship(
        "WorkflowArtifact",
        back_populates="workflow_run",
        cascade="all, delete-orphan",
    )
    events = relationship(
        "WorkflowEvent",
        back_populates="workflow_run",
        cascade="all, delete-orphan",
        order_by="WorkflowEvent.created_at",
    )


class WorkflowStepRun(Base):
    """A single step execution within a workflow run."""

    __tablename__ = "workflow_step_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(
        String(36),
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    step_name = Column(String(120), nullable=False, index=True)
    sequence_no = Column(Integer, nullable=False)
    attempt_no = Column(Integer, nullable=False, default=1)

    # V2 split: lifecycle vs outcome
    step_status = Column(String(40), nullable=False, default="pending", index=True)
    step_outcome = Column(String(50), nullable=True)

    coder = Column(String(50), nullable=True)
    assigned_worker_id = Column(String(80), nullable=True, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    output_payload = Column(JSONB, nullable=True)
    usage_summary = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    # Relationships
    workflow_run = relationship("WorkflowRun", back_populates="step_runs")
    reviews = relationship(
        "WorkflowReview",
        back_populates="step_run",
        cascade="all, delete-orphan",
    )


class WorkflowArtifact(Base):
    """An output artifact produced by a workflow run or step."""

    __tablename__ = "workflow_artifacts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(
        String(36),
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    workflow_step_run_id = Column(
        String(36),
        ForeignKey("workflow_step_runs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    artifact_key = Column(String(100), nullable=False, index=True)
    role = Column(String(30), nullable=False, default="output")
    file_path = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    workflow_run = relationship("WorkflowRun", back_populates="artifacts")


class WorkflowEvent(Base):
    """An immutable event logged during a workflow run lifecycle."""

    __tablename__ = "workflow_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(
        String(36),
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    workflow_step_run_id = Column(
        String(36),
        ForeignKey("workflow_step_runs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type = Column(String(60), nullable=False, index=True)
    message = Column(Text, nullable=True)
    payload = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    workflow_run = relationship("WorkflowRun", back_populates="events")


class WorkflowReview(Base):
    """A human or automated review decision recorded against a step run."""

    __tablename__ = "workflow_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(
        String(36),
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    workflow_step_run_id = Column(
        String(36),
        ForeignKey("workflow_step_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    review_type = Column(String(50), nullable=False, default="step_review")
    decision = Column(String(30), nullable=False, index=True)
    remark = Column(Text, nullable=True)
    findings = Column(JSONB, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    step_run = relationship("WorkflowStepRun", back_populates="reviews")
