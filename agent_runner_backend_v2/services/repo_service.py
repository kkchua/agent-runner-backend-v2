"""Repo service — repo registration and workflow assignment."""
from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import repo_repository, worker_repository, workflow_repository
from agent_runner_backend_v2.models.repo import RepoRegistry, RepoWorkflowAssignment


def create_repo(
    db: Session,
    *,
    name: str,
    path: str,
    worker_id: str,
) -> RepoRegistry:
    """Create a new repo registration."""
    existing = repo_repository.get_repo_by_name(db, name)
    if existing:
        raise HTTPException(status_code=409, detail=f"Repo '{name}' already exists")

    # Look up worker to get UUID
    worker = worker_repository.get_worker(db, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker '{worker_id}' not found")

    repo = RepoRegistry(name=name, path=path, worker_id=worker_id, worker_uuid=worker.id)
    return repo_repository.create_repo(db, repo)


def get_repo(db: Session, repo_id: str) -> RepoRegistry:
    """Get a repo by ID, raising 404 if not found."""
    repo = repo_repository.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repo {repo_id} not found")
    return repo


def list_repos(db: Session) -> list[RepoRegistry]:
    """List all registered repos."""
    return repo_repository.list_repos(db)


def update_repo(db: Session, repo_id: str, **kwargs) -> RepoRegistry:
    """Update a repo's fields."""
    repo = get_repo(db, repo_id)
    if "name" in kwargs and kwargs["name"] != repo.name:
        conflict = repo_repository.get_repo_by_name(db, kwargs["name"])
        if conflict:
            raise HTTPException(status_code=409, detail=f"Repo name '{kwargs['name']}' already exists")
    # If worker_id is being changed, resolve to worker_uuid
    if "worker_id" in kwargs:
        worker = worker_repository.get_worker(db, kwargs["worker_id"])
        if not worker:
            raise HTTPException(status_code=404, detail=f"Worker '{kwargs['worker_id']}' not found")
        kwargs["worker_uuid"] = worker.id
    return repo_repository.update_repo(db, repo, **kwargs)


def delete_repo(db: Session, repo_id: str) -> None:
    """Delete a repo and its workflow assignments."""
    repo = get_repo(db, repo_id)
    repo_repository.delete_repo(db, repo)


def assign_workflow(
    db: Session,
    *,
    repo_id: str,
    workflow_name: str,
    display_name: str | None = None,
) -> RepoWorkflowAssignment:
    """Assign a workflow to a repo."""
    repo = get_repo(db, repo_id)

    existing = repo_repository.get_repo_workflow(
        db, repo_id=repo_id, workflow_name=workflow_name,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Workflow '{workflow_name}' already assigned to repo '{repo.name}'",
        )

    assignment = RepoWorkflowAssignment(
        repo_id=repo_id,
        workflow_name=workflow_name,
        display_name=display_name,
    )
    return repo_repository.create_workflow_assignment(db, assignment)


def unassign_workflow(db: Session, *, repo_id: str, workflow_name: str) -> None:
    """Remove a workflow assignment from a repo."""
    assignment = repo_repository.get_repo_workflow(
        db, repo_id=repo_id, workflow_name=workflow_name,
    )
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{workflow_name}' not assigned to repo {repo_id}",
        )
    repo_repository.delete_workflow_assignment(db, assignment)


def list_repo_workflows(db: Session, repo_id: str) -> list[RepoWorkflowAssignment]:
    """List workflow assignments for a repo."""
    get_repo(db, repo_id)
    return repo_repository.list_repo_workflows(db, repo_id)
