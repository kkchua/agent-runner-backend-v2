#!/usr/bin/env bash
set -euo pipefail

echo "Initializing database schema..."
python -c "from agent_runner_backend_v2.database import init_db; init_db()"

echo "Stamping Alembic migrations as applied..."
python -m alembic stamp head

echo "Starting uvicorn on 0.0.0.0:${PORT:-8000}..."
exec python -m uvicorn agent_runner_backend_v2.main:create_app \
    --factory \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"
