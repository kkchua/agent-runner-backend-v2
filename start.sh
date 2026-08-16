#!/usr/bin/env bash
set -euo pipefail

echo "Running database migrations..."
python -m alembic upgrade head

echo "Starting uvicorn on 0.0.0.0:${PORT:-8000}..."
exec python -m uvicorn agent_runner_backend_v2.main:create_app \
    --factory \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"
