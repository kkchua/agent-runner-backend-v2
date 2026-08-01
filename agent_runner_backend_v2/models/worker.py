"""Worker registry model."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import utcnow


class WorkerRegistry(Base):
    """A registered daemon worker that claims and executes workflow steps."""

    __tablename__ = "worker_registry"

    worker_id = Column(String(80), primary_key=True)
    status = Column(String(30), nullable=False, default="active", index=True)
    worker_label = Column(String(40), nullable=False, default="live", index=True)
    capabilities = Column(JSONB, nullable=False, default=dict)
    current_run_id = Column(String(36), nullable=True, index=True)
    current_step_run_id = Column(String(36), nullable=True, index=True)
    last_heartbeat = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)
