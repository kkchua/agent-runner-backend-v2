"""Run management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import (
    ActionRequest,
    OutcomeRequest,
    OutcomeResponse,
    ResetStepRequest,
    RunListResponse,
    RunResponse,
    SubmitRunRequest,
)
from agent_runner_backend_v2.api.serializers import serialize_run
from agent_runner_backend_v2.database import get_db, run_repository
from agent_runner_backend_v2.services import run_service

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("", status_code=201)
def submit_run(req: SubmitRunRequest, db: Session = Depends(get_db)) -> RunResponse:
    """Submit a new workflow run."""
    run = run_service.submit_run(
        db,
        workflow_name=req.workflow_name,
        worker_id=req.worker_id,
        project_root=req.project_root,
        workspace_path=req.workspace_path,
        input_payload=req.input_payload,
        start_step=req.start_step,
    )
    return serialize_run(run)


@router.get("")
def list_runs(
    status: str | None = None,
    worker_id: str | None = None,
    workflow_name: str | None = None,
    db: Session = Depends(get_db),
) -> RunListResponse:
    """List workflow runs with optional filters."""
    statuses = None
    if status == "active":
        statuses = ["SUBMITTED", "PENDING", "RUNNING", "AWAITING_APPROVAL",
                     "AWAITING_INTERVENTION", "AWAITING_MAXRETRIED"]
    elif status == "terminal":
        statuses = ["COMPLETED", "FAILED"]

    runs = run_repository.list_runs(
        db,
        statuses=statuses,
        run_status=status if status not in ("active", "terminal") else None,
        worker_id=worker_id,
        workflow_name=workflow_name,
    )
    return RunListResponse(runs=[serialize_run(r) for r in runs])


@router.get("/{run_id}")
def get_run(run_id: str, db: Session = Depends(get_db)) -> RunResponse:
    """Get run detail with valid actions."""
    detail = run_service.get_run_detail(db, run_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Run not found")
    return serialize_run(detail["run"], detail["valid_actions"])


@router.post("/{run_id}/action")
def request_action(
    run_id: str, req: ActionRequest, db: Session = Depends(get_db),
) -> RunResponse:
    """Request an action on a run (approve, reject, resume, retry, cancel)."""
    run = run_service.request_action(
        db, run_id=run_id, action=req.action, feedback=req.feedback,
    )
    return serialize_run(run)


@router.post("/{run_id}/reset-step")
def reset_step(
    run_id: str, req: ResetStepRequest, db: Session = Depends(get_db),
) -> RunResponse:
    """Reset a run's current step."""
    run = run_service.reset_step(db, run_id=run_id, step_name=req.step_name)
    return serialize_run(run)


@router.post("/step-runs/{step_run_id}/outcome")
def report_outcome(
    step_run_id: str, req: OutcomeRequest, db: Session = Depends(get_db),
) -> OutcomeResponse:
    """Report a step outcome — backend computes next state."""
    run = run_service.report_outcome(
        db,
        step_run_id=step_run_id,
        outcome=req.outcome,
        failure_class=req.failure_class,
        artifacts=req.artifacts,
        review=req.review,
        error_message=req.error_message,
        usage_summary=req.usage_summary,
    )
    return OutcomeResponse(
        run_id=run.id,
        run_status=run.run_status,
        current_step=run.current_step_name,
        action_requested=run.action_requested,
        message=f"Transitioned to {run.run_status}",
    )
