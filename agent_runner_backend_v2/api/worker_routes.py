"""Worker management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import (
    ClaimResponse,
    HeartbeatRequest,
    HeartbeatResponse,
    RegisterWorkerRequest,
    UpdateWorkerRequest,
    WorkerResponse,
)
from agent_runner_backend_v2.api.serializers import serialize_worker, serialize_run
from agent_runner_backend_v2.auth.rbac import require_jwt_or_api_key
from agent_runner_backend_v2.auth.supabase_auth import UserContext
from agent_runner_backend_v2.database import get_db, worker_repository
from agent_runner_backend_v2.services import run_service, worker_service

router = APIRouter(prefix="/api/workers", tags=["workers"])


@router.post("/register", status_code=201)
def register_worker(
    req: RegisterWorkerRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> WorkerResponse:
    """Register or update a worker."""
    w = worker_service.register_worker(
        db, worker_id=req.worker_id, worker_label=req.worker_label,
        capabilities=req.capabilities, host_id=req.host_id,
    )
    return serialize_worker(w)


@router.post("/{worker_id}/heartbeat")
def heartbeat(
    worker_id: str,
    req: HeartbeatRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> HeartbeatResponse:
    """Update worker heartbeat."""
    w = worker_service.heartbeat(
        db, worker_id=worker_id, status=req.status,
        current_run_id=req.current_run_id,
        current_step_run_id=req.current_step_run_id,
    )
    if not w:
        raise HTTPException(status_code=404, detail="Worker not found")

    commands: list[str] = []

    # If worker is disabled, tell daemon to shut down
    if not w.is_enabled:
        commands.append("shutdown")
        return HeartbeatResponse(commands=commands, detail={"reason": "worker_disabled"})

    # Check for force-cancelled runs claimed by this worker — daemon must
    # terminate their children immediately.
    force_cancel_runs = run_service.get_force_cancelled_runs(db, worker_id=worker_id)
    if force_cancel_runs:
        commands.append("terminate_children")

    return HeartbeatResponse(
        commands=commands,
        detail={"force_cancel_run_ids": [r.id for r in force_cancel_runs]} if force_cancel_runs else None,
    )


@router.post("/{worker_id}/claim")
def claim_work(
    worker_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> ClaimResponse:
    """Claim the next available work for a worker."""
    # Reject if worker is disabled
    worker = worker_repository.get_worker(db, worker_id)
    if worker and not worker.is_enabled:
        return ClaimResponse(work_type="IDLE")

    work = run_service.claim_work(db, worker_id=worker_id)
    if not work:
        return ClaimResponse(work_type="IDLE")

    # Commit BEFORE responding: the daemon acts on the claim response
    # immediately (fetches run state, spawns a child whose outcome POST is
    # keyed on this step run). FastAPI's get_db dependency commits in its
    # teardown, which runs AFTER the response is sent — so without an
    # explicit commit the claim (step run INSERT + run UPDATE) could still
    # be uncommitted when the child reports its outcome, yielding a
    # "Step run not found" 404 and a permanently stalled run.
    db.commit()

    run = work["run"]
    step_run = work["step_run"]

    run_data = {
        "run_id": run.id,
        "run_code": run.run_code,
        "workflow_name": run.workflow_definition.name if run.workflow_definition else "",
        "project_root": run.project_root,
        "job_dir": run.job_dir,
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
def stop_worker(
    worker_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> dict:
    """Stop a worker."""
    ok = worker_service.stop_worker(db, worker_id=worker_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"status": "ok", "message": f"Worker {worker_id} stopped"}


@router.put("/{worker_id}")
def update_worker(
    worker_id: str,
    req: UpdateWorkerRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> WorkerResponse:
    """Update a worker's fields."""
    updates = req.model_dump(exclude_unset=True)
    w = worker_service.update_worker(db, worker_id, **updates)
    return serialize_worker(w)


@router.delete("/{worker_id}")
def delete_worker(
    worker_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> dict:
    """Delete a worker from the registry."""
    worker_service.delete_worker(db, worker_id)
    return {"status": "ok", "message": f"Worker {worker_id} deleted"}


@router.get("/{worker_id}")
def get_worker(
    worker_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> WorkerResponse:
    """Get a single worker by ID."""
    w = worker_service.get_worker(db, worker_id)
    return serialize_worker(w)


@router.get("")
def list_workers(
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> list[WorkerResponse]:
    """List all registered workers."""
    workers = worker_repository.list_workers(db)
    return [serialize_worker(w) for w in workers]
