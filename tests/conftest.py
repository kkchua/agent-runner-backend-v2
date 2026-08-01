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
    or "postgresql+psycopg2://postgres:postgres@localhost:5432/agentrunnerv2"
)

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["AGENT_RUNNER_DATABASE_URL"] = TEST_DATABASE_URL

from agent_runner_backend_v2.database import Base  # noqa: E402

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    """Truncate all tables between tests for isolation."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide a database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
