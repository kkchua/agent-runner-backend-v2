"""Run management API routes."""
from __future__ import annotations

import structlog
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
from agent_runner_backend_v2.auth.rbac import require_jwt_or_api_key
from agent_runner_backend_v2.auth.supabase_auth import UserContext
from agent_runner_backend_v2.database import get_db, run_repository
from agent_runner_backend_v2.services import run_service

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("", status_code=201)
def submit_run(
    req: SubmitRunRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> RunResponse:
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
    db.commit()
    return serialize_run(run)


@router.get("")
def list_runs(
    status: str | None = None,
    worker_id: str | None = None,
    workflow_name: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> RunListResponse:
    """List workflow runs with optional filters."""
    statuses = None
    if status == "active":
        statuses = ["USER_SUBMITTED", "USER_APPROVED", "USER_REJECTED", "USER_RESUMED", "USER_RETRIED",
                     "PENDING", "RUNNING", "WAITING_FOR_HUMAN_APPROVAL",
                     "AWAITING_INTERVENTION", "AWAITING_MAXRETRIED"]
    elif status == "terminal":
        statuses = ["COMPLETED", "FAILED", "CANCELLED", "USER_CANCELLED"]

    runs, total = run_repository.list_runs(
        db,
        statuses=statuses,
        run_status=status if status not in ("active", "terminal") else None,
        worker_id=worker_id,
        workflow_name=workflow_name,
        limit=limit,
        offset=offset,
    )
    return RunListResponse(runs=[serialize_run(r) for r in runs], total=total)


@router.get("/{run_id}")
def get_run(
    run_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> RunResponse:
    """Get run detail with valid actions."""
    detail = run_service.get_run_detail(db, run_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Run not found")
    return serialize_run(detail["run"], detail["valid_actions"])


@router.post("/{run_id}/action")
def request_action(
    run_id: str,
    req: ActionRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> RunResponse:
    """Request an action on a run (approve, reject, resume, retry, cancel).

    For CANCEL action: set force=True to immediately kill children (force cancel),
    or force=False to let the current step finish naturally (graceful cancel).
    """
    logger.info("api_request_action", run_id=run_id, action=req.action, force=req.force)
    try:
        # Map CANCEL + force=True → FORCE_CANCEL internally
        action = req.action
        if action == "CANCEL" and req.force:
            action = "FORCE_CANCEL"
        run = run_service.request_action(
            db, run_id=run_id, action=action, feedback=req.feedback,
        )
        # Commit before responding so the daemon's next claim sees the
        # USER_* status (see claim_work for the same rationale).
        db.commit()
        logger.info("api_request_action_success", run_id=run_id, new_status=run.run_status)
        return serialize_run(run)
    except HTTPException:
        logger.error("api_request_action_http_error", run_id=run_id, action=req.action)
        raise
    except Exception as e:
        logger.error("api_request_action_unexpected_error", run_id=run_id, action=req.action, error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/{run_id}/reset-step")
def reset_step(
    run_id: str,
    req: ResetStepRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> RunResponse:
    """Reset a run's current step."""
    run = run_service.reset_step(db, run_id=run_id, step_name=req.step_name)
    db.commit()
    return serialize_run(run)


@router.post("/step-runs/{step_run_id}/outcome")
def report_outcome(
    step_run_id: str,
    req: OutcomeRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "service-account")),
) -> OutcomeResponse:
    """Report a step outcome — backend computes next state."""
    logger.info("api_report_outcome", step_run_id=step_run_id, outcome=req.outcome, failure_class=req.failure_class)
    try:
        run = run_service.report_outcome(
            db,
            step_run_id=step_run_id,
            outcome=req.outcome,
            failure_class=req.failure_class,
            artifacts=req.artifacts,
            review=req.review,
            error_message=req.error_message,
            usage_summary=req.usage_summary,
            job_dir=req.job_dir,
        )
        # Commit before responding so the next claim (which keys on the
        # transitioned run state) sees a durable outcome.
        db.commit()
        logger.info("api_report_outcome_success", step_run_id=step_run_id, new_status=run.run_status, action_requested=run.action_requested)
        return OutcomeResponse(
            run_id=run.id,
            run_status=run.run_status,
            current_step=run.current_step_name,
            action_requested=run.action_requested,
            message=f"Transitioned to {run.run_status}",
        )
    except HTTPException:
        logger.error("api_report_outcome_http_error", step_run_id=step_run_id, outcome=req.outcome)
        raise
    except Exception as e:
        logger.error("api_report_outcome_unexpected_error", step_run_id=step_run_id, outcome=req.outcome, error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
