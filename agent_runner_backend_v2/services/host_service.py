"""Host service — host machine registration and lookup."""
from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import host_repository
from agent_runner_backend_v2.models.host import Host


def register_host(
    db: Session,
    *,
    hostname: str,
    ip_address: str | None = None,
    os_type: str = "windows",
) -> Host:
    """Register or return existing host by identity (hostname + ip_address)."""
    existing = host_repository.get_host_by_identity(
        db, hostname=hostname, ip_address=ip_address,
    )
    if existing:
        return existing

    host = Host(
        hostname=hostname,
        ip_address=ip_address,
        os_type=os_type,
    )
    return host_repository.create_host(db, host)


def get_host(db: Session, host_id: str) -> Host:
    """Get a host by ID, raising 404 if not found."""
    host = host_repository.get_host(db, host_id)
    if not host:
        raise HTTPException(status_code=404, detail=f"Host {host_id} not found")
    return host


def list_hosts(db: Session) -> list[Host]:
    """List all registered hosts."""
    return host_repository.list_hosts(db)


def update_host(db: Session, host_id: str, **kwargs) -> Host:
    """Update a host's fields."""
    host = get_host(db, host_id)
    return host_repository.update_host(db, host, **kwargs)


def delete_host(db: Session, host_id: str) -> None:
    """Delete a host."""
    host = get_host(db, host_id)
    host_repository.delete_host(db, host)
