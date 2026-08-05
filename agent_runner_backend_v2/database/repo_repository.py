"""Repository layer for repo and workflow assignment persistence."""
from __future__ import annotations

from sqlalchemy.orm import Session

from agent_runner_backend_v2.models.repo import RepoRegistry, RepoWorkflowAssignment


def get_repo(db: Session, repo_id: str) -> RepoRegistry | None:
    """Fetch a repo by its primary key."""
    return db.query(RepoRegistry).filter(RepoRegistry.id == repo_id).first()


def get_repo_by_name(db: Session, name: str, worker_uuid: str) -> RepoRegistry | None:
    """Fetch a repo by name scoped to a specific worker."""
    return (
        db.query(RepoRegistry)
        .filter(RepoRegistry.name == name, RepoRegistry.worker_uuid == worker_uuid)
        .first()
    )


def list_repos(db: Session) -> list[RepoRegistry]:
    """List all registered repos, ordered by name."""
    return db.query(RepoRegistry).order_by(RepoRegistry.name).all()


def list_repos_by_worker(db: Session, worker_uuid: str) -> list[RepoRegistry]:
    """List repos assigned to a specific worker."""
    return (
        db.query(RepoRegistry)
        .filter(RepoRegistry.worker_uuid == worker_uuid)
        .order_by(RepoRegistry.name)
        .all()
    )


def create_repo(db: Session, repo: RepoRegistry) -> RepoRegistry:
    """Insert a new repo."""
    db.add(repo)
    db.flush()
    return repo


def update_repo(db: Session, repo: RepoRegistry, **kwargs) -> RepoRegistry:
    """Update repo fields."""
    for key, value in kwargs.items():
        if hasattr(repo, key):
            setattr(repo, key, value)
    db.flush()
    return repo


def delete_repo(db: Session, repo: RepoRegistry) -> None:
    """Delete a repo and its workflow assignments (cascade)."""
    db.delete(repo)
    db.flush()


def list_repo_workflows(db: Session, repo_id: str) -> list[RepoWorkflowAssignment]:
    """List workflow assignments for a repo."""
    return (
        db.query(RepoWorkflowAssignment)
        .filter(RepoWorkflowAssignment.repo_id == repo_id)
        .order_by(RepoWorkflowAssignment.created_at)
        .all()
    )


def get_repo_workflow(
    db: Session, *, repo_id: str, workflow_name: str,
) -> RepoWorkflowAssignment | None:
    """Fetch a specific workflow assignment for a repo."""
    return (
        db.query(RepoWorkflowAssignment)
        .filter(
            RepoWorkflowAssignment.repo_id == repo_id,
            RepoWorkflowAssignment.workflow_name == workflow_name,
        )
        .first()
    )


def create_workflow_assignment(
    db: Session, assignment: RepoWorkflowAssignment,
) -> RepoWorkflowAssignment:
    """Insert a new workflow assignment."""
    db.add(assignment)
    db.flush()
    return assignment


def delete_workflow_assignment(db: Session, assignment: RepoWorkflowAssignment) -> None:
    """Delete a workflow assignment."""
    db.delete(assignment)
    db.flush()
