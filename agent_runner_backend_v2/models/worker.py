"""Worker registry model."""
from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import utcnow


class WorkerRegistry(Base):
    """A registered daemon worker that claims and executes workflow steps."""

    __tablename__ = "worker_registry"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_id = Column(String(80), unique=True, nullable=False, index=True)
    host_id = Column(String(36), ForeignKey("hosts.id"), nullable=True, index=True)
    status = Column(String(30), nullable=False, default="active", index=True)
    worker_label = Column(String(40), nullable=False, default="live", index=True)
    is_enabled = Column(Boolean, nullable=False, default=True)
    capabilities = Column(JSONB, nullable=False, default=dict)
    current_run_id = Column(String(36), nullable=True, index=True)
    current_step_run_id = Column(String(36), nullable=True, index=True)
    last_heartbeat = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    host = relationship("Host", lazy="select")
