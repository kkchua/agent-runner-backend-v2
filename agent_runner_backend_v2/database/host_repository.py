"""Repository layer for host machine persistence."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.models.host import Host


def get_host(db: Session, host_id: str) -> Host | None:
    """Fetch a host by its primary key."""
    return db.query(Host).filter(Host.id == host_id).first()


def get_host_by_identity(db: Session, *, hostname: str, ip_address: str | None = None) -> Host | None:
    """Fetch a host by hostname + ip_address combination."""
    query = db.query(Host).filter(Host.hostname == hostname)
    if ip_address:
        query = query.filter(Host.ip_address == ip_address)
    else:
        query = query.filter(Host.ip_address.is_(None))
    return query.first()


def list_hosts(db: Session) -> list[Host]:
    """List all registered hosts, ordered by hostname."""
    return db.query(Host).order_by(Host.hostname).all()


def create_host(db: Session, host: Host) -> Host:
    """Insert a new host."""
    db.add(host)
    db.flush()
    return host


def update_host(db: Session, host: Host, **kwargs) -> Host:
    """Update host fields."""
    for key, value in kwargs.items():
        if hasattr(host, key):
            setattr(host, key, value)
    db.flush()
    return host


def delete_host(db: Session, host: Host) -> None:
    """Delete a host."""
    db.delete(host)
    db.flush()
