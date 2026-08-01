#!/usr/bin/env bash
set -euo pipefail

# Start agent-runner-backend-v2 on Linux/macOS.
export AGENT_RUNNER_DATABASE_URL="${AGENT_RUNNER_DATABASE_URL:-postgresql+psycopg2://postgres:postgres@localhost:5432/agentrunnerv2}"
export DATABASE_URL="${DATABASE_URL:-$AGENT_RUNNER_DATABASE_URL}"
export API_HOST="${API_HOST:-0.0.0.0}"
export API_PORT="${API_PORT:-8200}"

cd "$(dirname "$0")"

echo "Starting backend V2 with:"
echo "  DATABASE_URL: $DATABASE_URL"
echo "  API_HOST: $API_HOST"
echo "  API_PORT: $API_PORT"

if [ -f ".venv/bin/python" ]; then
    .venv/bin/python -m uvicorn agent_runner_backend_v2.main:create_app --factory --host "$API_HOST" --port "$API_PORT"
else
    python3 -m uvicorn agent_runner_backend_v2.main:create_app --factory --host "$API_HOST" --port "$API_PORT"
fi
