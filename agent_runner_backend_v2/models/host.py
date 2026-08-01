"""Host machine model — top-level identity for worker machines."""
from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, String, UniqueConstraint

from agent_runner_backend_v2.database import Base
from agent_runner_backend_v2.models.run import utcnow


class Host(Base):
    """A physical or virtual machine that runs daemon workers."""

    __tablename__ = "hosts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = Column(String(200), nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    os_type = Column(String(20), nullable=False, default="windows")
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint("hostname", "ip_address", name="uq_host_identity"),
    )
