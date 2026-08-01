"""Worker management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import (
    ClaimResponse,
    HeartbeatRequest,
    HeartbeatResponse,
    RegisterWorkerRequest,
    WorkerResponse,
)
from agent_runner_backend_v2.api.serializers import serialize_worker, serialize_run
from agent_runner_backend_v2.database import get_db, worker_repository
from agent_runner_backend_v2.services import run_service, worker_service

router = APIRouter(prefix="/api/workers", tags=["workers"])


@router.post("/register", status_code=201)
def register_worker(req: RegisterWorkerRequest, db: Session = Depends(get_db)) -> WorkerResponse:
    """Register or update a worker."""
    w = worker_service.register_worker(
        db, worker_id=req.worker_id, worker_label=req.worker_label,
        capabilities=req.capabilities,
    )
    return serialize_worker(w)


@router.post("/{worker_id}/heartbeat")
def heartbeat(
    worker_id: str, req: HeartbeatRequest, db: Session = Depends(get_db),
) -> HeartbeatResponse:
    """Update worker heartbeat."""
    w = worker_service.heartbeat(
        db, worker_id=worker_id, status=req.status,
        current_run_id=req.current_run_id,
        current_step_run_id=req.current_step_run_id,
    )
    if not w:
        raise HTTPException(status_code=404, detail="Worker not found")
    return HeartbeatResponse(commands=[])


@router.post("/{worker_id}/claim")
def claim_work(worker_id: str, db: Session = Depends(get_db)) -> ClaimResponse:
    """Claim the next available work for a worker."""
    work = run_service.claim_work(db, worker_id=worker_id)
    if not work:
        return ClaimResponse(work_type="IDLE")

    run = work["run"]
    step_run = work["step_run"]

    run_data = {
        "run_id": run.id,
        "run_code": run.run_code,
        "workflow_name": run.workflow_definition.name if run.workflow_definition else "",
        "project_root": run.project_root,
    }
    step_data = {
        "step_run_id": step_run.id,
        "step_name": step_run.step_name,
    }

    return ClaimResponse(
        work_type=work["work_type"],
        run=run_data,
        step_run=step_data,
        action=work.get("action"),
        feedback=work.get("feedback"),
    )


@router.post("/{worker_id}/stop")
def stop_worker(worker_id: str, db: Session = Depends(get_db)) -> dict:
    """Stop a worker."""
    ok = worker_service.stop_worker(db, worker_id=worker_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"status": "ok", "message": f"Worker {worker_id} stopped"}


@router.get("")
def list_workers(db: Session = Depends(get_db)) -> list[WorkerResponse]:
    """List all registered workers."""
    workers = worker_repository.list_workers(db)
    return [serialize_worker(w) for w in workers]
