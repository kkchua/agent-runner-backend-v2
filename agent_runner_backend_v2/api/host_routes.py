"""Host management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import CreateHostRequest, HostResponse, UpdateHostRequest
from agent_runner_backend_v2.api.serializers import serialize_host
from agent_runner_backend_v2.database import get_db
from agent_runner_backend_v2.services import host_service

router = APIRouter(prefix="/api/hosts", tags=["hosts"])


@router.get("")
def list_hosts(db: Session = Depends(get_db)) -> list[HostResponse]:
    """List all registered hosts."""
    hosts = host_service.list_hosts(db)
    return [serialize_host(h) for h in hosts]


@router.post("", status_code=201)
def create_host(req: CreateHostRequest, db: Session = Depends(get_db)) -> HostResponse:
    """Register a new host machine."""
    host = host_service.register_host(
        db,
        hostname=req.hostname,
        ip_address=req.ip_address,
        os_type=req.os_type,
    )
    return serialize_host(host)


@router.get("/{host_id}")
def get_host(host_id: str, db: Session = Depends(get_db)) -> HostResponse:
    """Get host detail."""
    host = host_service.get_host(db, host_id)
    return serialize_host(host)


@router.put("/{host_id}")
def update_host(host_id: str, req: UpdateHostRequest, db: Session = Depends(get_db)) -> HostResponse:
    """Update a host's fields."""
    updates = req.model_dump(exclude_unset=True)
    host = host_service.update_host(db, host_id, **updates)
    return serialize_host(host)


@router.delete("/{host_id}")
def delete_host(host_id: str, db: Session = Depends(get_db)) -> dict:
    """Delete a host."""
    host_service.delete_host(db, host_id)
    return {"status": "ok", "message": f"Host {host_id} deleted"}
