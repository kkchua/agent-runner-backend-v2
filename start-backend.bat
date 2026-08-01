@echo off
setlocal

rem Start agent-runner-backend-v2 on Windows.
if not defined AGENT_RUNNER_DATABASE_URL (
    set "AGENT_RUNNER_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/agentrunnerv2"
)
if not defined DATABASE_URL (
    set "DATABASE_URL=%AGENT_RUNNER_DATABASE_URL%"
)
if not defined API_HOST (
    set "API_HOST=0.0.0.0"
)
if not defined API_PORT (
    set "API_PORT=8200"
)

set "ROOT_DIR=%~dp0"
pushd "%ROOT_DIR%"

echo Starting backend V2 with:
echo   DATABASE_URL: %DATABASE_URL%
echo   API_HOST: %API_HOST%
echo   API_PORT: %API_PORT%

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn agent_runner_backend_v2.main:create_app --factory --host %API_HOST% --port %API_PORT%
) else (
    python -m uvicorn agent_runner_backend_v2.main:create_app --factory --host %API_HOST% --port %API_PORT%
)

popd
endlocal
