"""Shared test fixtures."""
from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

TEST_DATABASE_URL = (
    os.environ.get("AGENT_RUNNER_TEST_DATABASE_URL")
    or os.environ.get("TEST_DATABASE_URL")
    or "postgresql+psycopg2://postgres:postgres@localhost:5432/agentrunnerv2_test"
)

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["AGENT_RUNNER_DATABASE_URL"] = TEST_DATABASE_URL

from agent_runner_backend_v2.database import Base  # noqa: E402

# Import all models so Base.metadata knows about every table
from agent_runner_backend_v2.auth.models import APIKey  # noqa: F401, E402
from agent_runner_backend_v2.models import host, repo, run, worker, workflow  # noqa: F401, E402

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    """Ensure all tables exist, clean up data between tests."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide a database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
