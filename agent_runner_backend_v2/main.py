"""FastAPI application entrypoint."""
from __future__ import annotations

import signal
import threading
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from agent_runner_backend_v2.api.routes import router
from agent_runner_backend_v2.config import settings
from agent_runner_backend_v2.database import SessionLocal, engine, init_db

logger = structlog.get_logger(__name__)

_FORCE_EXIT_TIMEOUT_SECONDS = 5.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    logger.info("starting", database_url=settings.DATABASE_URL, port=settings.API_PORT)
    init_db()

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("database connected")
    except Exception as exc:
        logger.error("startup failed", error=str(exc))
        raise

    yield

    engine.dispose()
    logger.info("database pool closed")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Agent Runner Backend V2",
        description="Platform V2 backend with state machine for agent-runner-v2 workflows",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


class _WindowsFriendlyServer(uvicorn.Server):
    """Uvicorn server with Windows-friendly signal handling."""

    def __init__(self, config: uvicorn.Config):
        super().__init__(config)
        self._force_exit_timer_started = False
        self._force_exit_lock = threading.Lock()

    def handle_exit(self, sig: int, frame) -> None:
        super().handle_exit(sig, frame)
        if self.force_exit or sig != signal.SIGINT:
            return
        with self._force_exit_lock:
            if self._force_exit_timer_started:
                return
            self._force_exit_timer_started = True
        timer = threading.Timer(_FORCE_EXIT_TIMEOUT_SECONDS, self._force_shutdown)
        timer.daemon = True
        timer.start()

    def _force_shutdown(self) -> None:
        if not self.should_exit or self.force_exit:
            return
        logger.warning("graceful shutdown deadline exceeded, forcing exit")
        self.force_exit = True


def main() -> None:
    """Run the application as a uvicorn server."""
    config = uvicorn.Config(
        app=create_app(),
        host=settings.API_HOST,
        port=settings.API_PORT,
        timeout_keep_alive=1,
        timeout_graceful_shutdown=3,
    )
    server = _WindowsFriendlyServer(config)
    try:
        server.run()
    except KeyboardInterrupt:
        logger.warning("shutdown interrupted", port=settings.API_PORT)
        server.should_exit = True
        server.force_exit = True


if __name__ == "__main__":
    main()
