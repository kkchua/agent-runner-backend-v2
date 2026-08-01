"""Integration test fixtures."""
from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from agent_runner_backend_v2.database import get_db
from tests.conftest import SessionLocal


def _test_get_db() -> Generator[Session, None, None]:
    """DB dependency override that auto-commits."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture
def api_client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with DB override."""
    from agent_runner_backend_v2.main import create_app

    app = create_app()
    app.dependency_overrides[get_db] = _test_get_db
    with TestClient(app) as client:
        yield client
