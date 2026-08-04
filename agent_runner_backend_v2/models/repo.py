"""Repository and workflow assignment models."""
from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import utcnow


class RepoRegistry(Base):
    """A project repository registered for workflow execution."""

    __tablename__ = "repos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False, unique=True, index=True)
    path = Column(Text, nullable=False)
    worker_id = Column(String(80), nullable=False, index=True)
    worker_uuid = Column(String(36), ForeignKey("worker_registry.id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    worker = relationship("WorkerRegistry", lazy="select", foreign_keys=[worker_uuid])
    workflow_assignments = relationship(
        "RepoWorkflowAssignment",
        back_populates="repo",
        cascade="all, delete-orphan",
        order_by="RepoWorkflowAssignment.created_at",
    )


class RepoWorkflowAssignment(Base):
    """Binding between a repo and a workflow definition."""

    __tablename__ = "repo_workflow_assignments"
    __table_args__ = (
        UniqueConstraint("repo_id", "workflow_name", name="uq_repo_workflow"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repo_id = Column(String(36), ForeignKey("repos.id", ondelete="CASCADE"), nullable=False, index=True)
    workflow_name = Column(String(120), nullable=False)
    display_name = Column(String(200), nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    repo = relationship("RepoRegistry", back_populates="workflow_assignments")
