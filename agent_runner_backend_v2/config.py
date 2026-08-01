"""Application settings loaded from environment variables."""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Agent Runner Backend V2"
    APP_ENV: str = "development"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agentrunnerv2"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8200

    WORKER_HEARTBEAT_INTERVAL: int = 20
    WORKER_TIMEOUT: int = 60

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def is_development(self) -> bool:
        """Return True if running in development mode."""
        return self.APP_ENV == "development"


settings = Settings()
