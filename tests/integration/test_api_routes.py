"""Integration tests for API endpoints — full HTTP request/response cycle."""
from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from agent_runner_backend_v2.services import workflow_service


def _seed_workflow(db_session: Session, name: str = "api_test_wf") -> None:
    """Seed a workflow for testing."""
    definition = {
        "job_prefix": "API",
        "init_step": "generate",
        "steps": {
            "generate": {"onsuccess": "review"},
            "review": {"requires_human_approval_after": True, "onsuccess": "complete"},
            "complete": {},
        },
    }
    workflow_service.sync_workflow(db_session, workflow_name=name, definition=definition)


class TestRunEndpoints:
    def test_submit_run(self, api_client: TestClient):
        # Seed workflow via direct DB access through the app
        with api_client:
            # First sync a workflow
            resp = api_client.post("/api/workflows/sync", json={
                "workflow_name": "api_test_wf",
                "definition": {
                    "job_prefix": "API",
                    "init_step": "generate",
                    "steps": {
                        "generate": {"onsuccess": "review"},
                        "review": {"requires_human_approval_after": True},
                    },
                },
            })
            assert resp.status_code == 200

            # Submit a run
            resp = api_client.post("/api/runs", json={
                "workflow_name": "api_test_wf",
                "project_root": "/workspace",
            })
            assert resp.status_code == 201
            data = resp.json()
            assert data["run_status"] == "SUBMITTED"
            assert data["current_step"] == "generate"
            assert data["run_code"].startswith("API-")

    def test_list_runs(self, api_client: TestClient):
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "list_test",
            "definition": {"job_prefix": "L", "init_step": "s1", "steps": {"s1": {}}},
        })
        api_client.post("/api/runs", json={"workflow_name": "list_test"})
        api_client.post("/api/runs", json={"workflow_name": "list_test"})

        resp = api_client.get("/api/runs")
        assert resp.status_code == 200
        assert len(resp.json()["runs"]) == 2

    def test_get_run_detail(self, api_client: TestClient):
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "detail_test",
            "definition": {"job_prefix": "D", "init_step": "s1", "steps": {"s1": {}}},
        })
        submit_resp = api_client.post("/api/runs", json={"workflow_name": "detail_test"})
        run_id = submit_resp.json()["run_id"]

        resp = api_client.get(f"/api/runs/{run_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["run_id"] == run_id
        assert "CANCEL" in data["valid_actions"]

    def test_get_nonexistent_run_returns_404(self, api_client: TestClient):
        resp = api_client.get("/api/runs/nonexistent")
        assert resp.status_code == 404

    def test_request_action(self, api_client: TestClient):
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "action_test",
            "definition": {"job_prefix": "A", "init_step": "s1", "steps": {"s1": {}}},
        })
        submit_resp = api_client.post("/api/runs", json={"workflow_name": "action_test"})
        run_id = submit_resp.json()["run_id"]

        resp = api_client.post(f"/api/runs/{run_id}/action", json={
            "action": "CANCEL",
        })
        assert resp.status_code == 200
        assert resp.json()["run_status"] == "CANCELLED"

    def test_invalid_action_returns_422(self, api_client: TestClient):
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "invalid_action_test",
            "definition": {"job_prefix": "IA", "init_step": "s1", "steps": {"s1": {}}},
        })
        submit_resp = api_client.post("/api/runs", json={"workflow_name": "invalid_action_test"})
        run_id = submit_resp.json()["run_id"]

        resp = api_client.post(f"/api/runs/{run_id}/action", json={
            "action": "APPROVE",  # Not valid for SUBMITTED status
        })
        assert resp.status_code == 422

    def test_submit_unknown_workflow_returns_404(self, api_client: TestClient):
        resp = api_client.post("/api/runs", json={"workflow_name": "nonexistent"})
        assert resp.status_code == 404


class TestWorkerEndpoints:
    def test_register_worker(self, api_client: TestClient):
        resp = api_client.post("/api/workers/register", json={
            "worker_id": "w1",
            "worker_label": "live",
        })
        assert resp.status_code == 201
        assert resp.json()["worker_id"] == "w1"
        assert resp.json()["status"] == "active"

    def test_heartbeat(self, api_client: TestClient):
        api_client.post("/api/workers/register", json={"worker_id": "w1"})

        resp = api_client.post("/api/workers/w1/heartbeat", json={
            "status": "busy",
            "current_run_id": "run-123",
        })
        assert resp.status_code == 200
        assert resp.json()["commands"] == []

    def test_heartbeat_unknown_worker_returns_404(self, api_client: TestClient):
        resp = api_client.post("/api/workers/unknown/heartbeat", json={"status": "idle"})
        assert resp.status_code == 404

    def test_claim_returns_idle_when_no_work(self, api_client: TestClient):
        api_client.post("/api/workers/register", json={"worker_id": "w1"})

        resp = api_client.post("/api/workers/w1/claim")
        assert resp.status_code == 200
        assert resp.json()["work_type"] == "IDLE"

    def test_claim_returns_execute_step(self, api_client: TestClient):
        api_client.post("/api/workers/register", json={"worker_id": "w1"})
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "claim_test",
            "definition": {"job_prefix": "C", "init_step": "s1", "steps": {"s1": {}}},
        })
        api_client.post("/api/runs", json={"workflow_name": "claim_test"})

        resp = api_client.post("/api/workers/w1/claim")
        assert resp.status_code == 200
        data = resp.json()
        assert data["work_type"] == "EXECUTE_STEP"
        assert data["run"]["workflow_name"] == "claim_test"
        assert data["step_run"]["step_name"] == "s1"

    def test_list_workers(self, api_client: TestClient):
        api_client.post("/api/workers/register", json={"worker_id": "w1"})
        api_client.post("/api/workers/register", json={"worker_id": "w2"})

        resp = api_client.get("/api/workers")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_stop_worker(self, api_client: TestClient):
        api_client.post("/api/workers/register", json={"worker_id": "w1"})

        resp = api_client.post("/api/workers/w1/stop")
        assert resp.status_code == 200


class TestWorkflowEndpoints:
    def test_sync_workflow(self, api_client: TestClient):
        resp = api_client.post("/api/workflows/sync", json={
            "workflow_name": "sync_test",
            "definition": {
                "job_prefix": "S",
                "init_step": "s1",
                "steps": {"s1": {"onsuccess": "s2"}, "s2": {}},
            },
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["workflow_name"] == "sync_test"
        assert data["step_count"] == 2

    def test_list_workflows(self, api_client: TestClient):
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "wf1",
            "definition": {"job_prefix": "A", "init_step": "s1", "steps": {"s1": {}}},
        })
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "wf2",
            "definition": {"job_prefix": "B", "init_step": "s1", "steps": {"s1": {}}},
        })

        resp = api_client.get("/api/workflows")
        assert resp.status_code == 200
        assert len(resp.json()) == 2


class TestFullWorkflowCycle:
    """End-to-end: submit → claim → outcome → action → complete."""

    def test_full_lifecycle(self, api_client: TestClient):
        # Setup
        api_client.post("/api/workers/register", json={"worker_id": "w1"})
        api_client.post("/api/workflows/sync", json={
            "workflow_name": "lifecycle_test",
            "definition": {
                "job_prefix": "LC",
                "init_step": "generate",
                "steps": {
                    "generate": {"onsuccess": "review"},
                    "review": {"requires_human_approval_after": True, "onsuccess": "done"},
                    "done": {},
                },
            },
        })

        # 1. Submit
        resp = api_client.post("/api/runs", json={"workflow_name": "lifecycle_test"})
        body = resp.json()
        assert resp.status_code == 201, f"Submit failed: {resp.status_code} {body}"
        assert "run_status" in body, f"Missing run_status in: {body}"
        assert body["run_status"] == "SUBMITTED"
        run_id = resp.json()["run_id"]

        # 2. Claim (generate step)
        resp = api_client.post("/api/workers/w1/claim")
        assert resp.json()["work_type"] == "EXECUTE_STEP"
        step_run_id = resp.json()["step_run"]["step_run_id"]

        # 3. Report outcome (approved → advance to review)
        resp = api_client.post(f"/api/runs/step-runs/{step_run_id}/outcome", json={
            "outcome": "approved",
        })
        assert resp.json()["run_status"] == "PENDING"

        # 4. Claim (review step)
        resp = api_client.post("/api/workers/w1/claim")
        step_run_id = resp.json()["step_run"]["step_run_id"]

        # 5. Report outcome (approved at review gate → WAITING_FOR_HUMAN_APPROVAL)
        resp = api_client.post(f"/api/runs/step-runs/{step_run_id}/outcome", json={
            "outcome": "approved",
        })
        assert resp.json()["run_status"] == "WAITING_FOR_HUMAN_APPROVAL"

        # 6. Request approve action
        resp = api_client.post(f"/api/runs/{run_id}/action", json={
            "action": "APPROVE", "feedback": "looks good",
        })
        assert resp.json()["action_requested"] == "APPROVE"

        # 7. Claim (process action)
        resp = api_client.post("/api/workers/w1/claim")
        assert resp.json()["work_type"] == "PROCESS_ACTION"

        # 8. Report outcome (action consumed → advance to done)
        step_run_id = resp.json()["step_run"]["step_run_id"]
        resp = api_client.post(f"/api/runs/step-runs/{step_run_id}/outcome", json={
            "outcome": "approved",
        })
        body = resp.json()
        assert resp.status_code == 200, f"Outcome failed: {resp.status_code} {body}"
        assert body["run_status"] == "PENDING"

        # 9. Claim (done step)
        resp = api_client.post("/api/workers/w1/claim")
        step_run_id = resp.json()["step_run"]["step_run_id"]

        # 10. Report outcome (approved → COMPLETED)
        resp = api_client.post(f"/api/runs/step-runs/{step_run_id}/outcome", json={
            "outcome": "approved",
        })
        assert resp.json()["run_status"] == "COMPLETED"

        # Verify final state
        resp = api_client.get(f"/api/runs/{run_id}")
        assert resp.json()["run_status"] == "COMPLETED"
        assert resp.json()["valid_actions"] == []
