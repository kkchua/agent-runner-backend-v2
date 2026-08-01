"""Integration test fixtures."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from agent_runner_backend_v2.database import get_db
from tests.conftest import SessionLocal


@pytest.fixture
def api_client() -> TestClient:
    """Provide a FastAPI test client with DB override."""
    from agent_runner_backend_v2.main import create_app

    app = create_app()

    def _override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client
