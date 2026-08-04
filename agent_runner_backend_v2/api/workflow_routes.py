"""Workflow management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import SyncWorkflowRequest, WorkflowResponse
from agent_runner_backend_v2.api.serializers import serialize_workflow
from agent_runner_backend_v2.auth.rbac import require_jwt_or_api_key
from agent_runner_backend_v2.auth.supabase_auth import UserContext
from agent_runner_backend_v2.database import get_db, workflow_repository
from agent_runner_backend_v2.services import workflow_service

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.post("/sync")
def sync_workflow(
    req: SyncWorkflowRequest,
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> WorkflowResponse:
    """Sync a workflow definition from the runner."""
    wf = workflow_service.sync_workflow(
        db, workflow_name=req.workflow_name, definition=req.definition,
    )
    return serialize_workflow(wf)


@router.get("")
def list_workflows(
    db: Session = Depends(get_db),
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator")),
) -> list[WorkflowResponse]:
    """List all active workflow definitions."""
    workflows = workflow_repository.list_workflows(db)
    return [serialize_workflow(wf) for wf in workflows]
