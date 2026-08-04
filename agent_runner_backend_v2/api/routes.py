"""API router aggregation."""
from __future__ import annotations

from fastapi import APIRouter

from agent_runner_backend_v2.api.auth_routes import router as auth_router
from agent_runner_backend_v2.api.host_routes import router as host_router
from agent_runner_backend_v2.api.repo_routes import router as repo_router
from agent_runner_backend_v2.api.run_routes import router as run_router
from agent_runner_backend_v2.api.worker_routes import router as worker_router
from agent_runner_backend_v2.api.workflow_routes import router as workflow_router

router = APIRouter()


# Simple health check — no auth
@router.get("/health")
def health():
    return {"status": "ok"}


router.include_router(auth_router)
router.include_router(host_router)
router.include_router(repo_router)
router.include_router(run_router)
router.include_router(worker_router)
router.include_router(workflow_router)
