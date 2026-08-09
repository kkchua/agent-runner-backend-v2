"""Database session management."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from agent_runner_backend_v2.config import settings


def _normalize_database_url(raw_url: str) -> str:
    """Normalize a database URL to use the psycopg2 driver."""
    url = make_url(raw_url)
    if url.drivername.startswith("postgresql") and url.drivername != "postgresql+psycopg2":
        url = url.set(drivername="postgresql+psycopg2")
    return url.render_as_string(hide_password=False)


engine = create_engine(
    _normalize_database_url(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=settings.is_development,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session with auto-commit/rollback and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Provide a transactional database scope with auto-commit/rollback."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Import all ORM models and create tables if they don't exist."""
    from agent_runner_backend_v2.auth import models as auth_models  # noqa: F401
    from agent_runner_backend_v2.auth import user_role_model as user_role_model  # noqa: F401
    from agent_runner_backend_v2.models import host, repo, run, worker, workflow  # noqa: F401
    Base.metadata.create_all(bind=engine)
