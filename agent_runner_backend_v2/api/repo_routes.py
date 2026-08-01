"""Repo management API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from agent_runner_backend_v2.api.schemas import (
    AssignWorkflowRequest,
    CreateRepoRequest,
    RepoResponse,
    RepoWorkflowResponse,
    UpdateRepoRequest,
)
from agent_runner_backend_v2.api.serializers import serialize_repo, serialize_repo_workflow
from agent_runner_backend_v2.database import get_db
from agent_runner_backend_v2.services import repo_service

router = APIRouter(prefix="/api/repos", tags=["repos"])


@router.get("")
def list_repos(db: Session = Depends(get_db)) -> list[RepoResponse]:
    """List all registered repos with their workflow assignments."""
    repos = repo_service.list_repos(db)
    return [serialize_repo(r) for r in repos]


@router.post("", status_code=201)
def create_repo(req: CreateRepoRequest, db: Session = Depends(get_db)) -> RepoResponse:
    """Register a new repo."""
    repo = repo_service.create_repo(
        db, name=req.name, path=req.path, worker_id=req.worker_id,
    )
    return serialize_repo(repo)


@router.get("/{repo_id}")
def get_repo(repo_id: str, db: Session = Depends(get_db)) -> RepoResponse:
    """Get repo detail with workflow assignments."""
    repo = repo_service.get_repo(db, repo_id)
    return serialize_repo(repo)


@router.put("/{repo_id}")
def update_repo(
    repo_id: str, req: UpdateRepoRequest, db: Session = Depends(get_db),
) -> RepoResponse:
    """Update a repo's fields."""
    updates = req.model_dump(exclude_unset=True)
    repo = repo_service.update_repo(db, repo_id, **updates)
    return serialize_repo(repo)


@router.delete("/{repo_id}")
def delete_repo(repo_id: str, db: Session = Depends(get_db)) -> dict:
    """Delete a repo and its workflow assignments."""
    repo_service.delete_repo(db, repo_id)
    return {"status": "ok", "message": f"Repo {repo_id} deleted"}


@router.get("/{repo_id}/workflows")
def list_repo_workflows(
    repo_id: str, db: Session = Depends(get_db),
) -> list[RepoWorkflowResponse]:
    """List workflow assignments for a repo."""
    assignments = repo_service.list_repo_workflows(db, repo_id)
    return [serialize_repo_workflow(a) for a in assignments]


@router.post("/{repo_id}/workflows", status_code=201)
def assign_workflow(
    repo_id: str, req: AssignWorkflowRequest, db: Session = Depends(get_db),
) -> RepoWorkflowResponse:
    """Assign a workflow to a repo."""
    assignment = repo_service.assign_workflow(
        db,
        repo_id=repo_id,
        workflow_name=req.workflow_name,
        display_name=req.display_name,
    )
    return serialize_repo_workflow(assignment)


@router.delete("/{repo_id}/workflows/{workflow_name}")
def unassign_workflow(
    repo_id: str, workflow_name: str, db: Session = Depends(get_db),
) -> dict:
    """Remove a workflow assignment from a repo."""
    repo_service.unassign_workflow(db, repo_id=repo_id, workflow_name=workflow_name)
    return {"status": "ok", "message": f"Workflow '{workflow_name}' removed from repo {repo_id}"}
