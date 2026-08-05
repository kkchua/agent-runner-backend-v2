# Agent Runner Backend V2 — Agent Instructions

This file provides context for AI agents working on this codebase.

## Project Overview

FastAPI backend for the agent-runner-v2 workflow platform. Manages workflow definitions, runs, workers, and provides a state machine for orchestrating multi-step agent workflows with human-in-the-loop approval gates.

**Tech Stack:**
- Python 3.12+
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy 2.0 ORM
- Alembic for migrations
- Pydantic v2 for validation
- structlog for structured logging
- pytest for testing

## Architecture

### Core Components

```
agent_runner_backend_v2/
├── main.py              # FastAPI app entrypoint, uvicorn server
├── config.py            # Settings from environment variables
├── database/            # SQLAlchemy session management, repositories
├── models/              # ORM models (host, repo, run, worker, workflow)
├── services/            # Business logic layer
│   ├── state_machine.py # THE authority for run state transitions
│   ├── run_service.py   # Run lifecycle management
│   ├── worker_service.py
│   ├── workflow_service.py
│   ├── host_service.py
│   └── repo_service.py
└── api/                 # FastAPI routes and schemas
    ├── routes.py        # Router aggregation
    ├── run_routes.py    # /api/runs endpoints
    ├── worker_routes.py # /api/workers endpoints
    ├── workflow_routes.py
    ├── host_routes.py
    ├── repo_routes.py
    ├── schemas.py       # Pydantic request/response models
    └── serializers.py   # ORM → API response conversion
```

### State Machine

**Critical:** `services/state_machine.py` is the single authority for all run state transitions. Never bypass it.

**Key concepts:**
- **RunStatus**: Actor-prefixed statuses (USER_SUBMITTED, USER_APPROVED, etc.) + internal statuses (PENDING, RUNNING, WAITING_FOR_HUMAN_APPROVAL, etc.)
- **Action**: APPROVE, REJECT, RESUME, RETRY, CANCEL, FORCE_CANCEL
- **Transition events**: STEP_CLAIMED, STEP_OUTCOME, ACTION_REQUESTED, ACTION_CONSUMED, STEP_RESET
- **Pair action principle**: Backend sets USER_* status, daemon processes it and reports outcome

**Flow:**
1. Console/worker submits run → USER_SUBMITTED
2. Daemon claims work → RUNNING
3. CLI reports step outcome → backend computes next state via state machine
4. If approval gate → WAITING_FOR_HUMAN_APPROVAL
5. Console requests action (APPROVE/REJECT) → USER_APPROVED/USER_REJECTED
6. Daemon consumes action → backend computes next state

### Database Layer

- **Models** (`models/`): SQLAlchemy ORM models with relationships
- **Repositories** (`database/*_repository.py`): Data access layer, called by services
- **Session management**: `database/__init__.py` provides `get_db()` dependency

**Pattern:** Routes → Services → Repositories → Models

## Development Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Git

### Initial Setup

```bash
# Clone and enter directory
cd agent-runner-backend-v2

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env
# Edit .env with your database credentials
```

### Database Setup

```bash
# Create database (PostgreSQL)
createdb agentrunnerv2

# Run migrations
python -m alembic upgrade head

# Check current version
python -m alembic current
```

### Running the Server

```bash
# Option 1: Using start script (Windows)
start-backend.bat

# Option 2: Using start script (Linux/Mac)
./start-backend.sh

# Option 3: Direct uvicorn
python -m uvicorn agent_runner_backend_v2.main:create_app --factory --host 0.0.0.0 --port 8200

# Option 4: Using installed command
arb-v2-server
```

Server runs at `http://localhost:8200`

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run specific test file
pytest tests/unit/test_state_machine.py

# Run with verbose output
pytest -v
```

**Test database:** Tests use `AGENT_RUNNER_TEST_DATABASE_URL` env var (defaults to `agentrunnerv2_test` database).

## Development Approach: Test-Driven Development (TDD)

**All development must follow TDD practices.** Write tests before implementation.

### TDD Workflow

1. **Red** — Write a failing test that describes the desired behavior
2. **Green** — Write the minimal code to make the test pass
3. **Refactor** — Clean up code while keeping tests green

### Rules

- **Never write implementation code without a failing test first**
- Tests define the specification — if you can't test it, don't build it
- Run tests frequently (after every small change)
- Keep tests fast — slow tests don't get run
- Refactor with confidence: tests are your safety net

### Practical Example

```python
# Step 1: Write failing test
def test_submit_run_creates_pending_run(db_session):
    run = run_service.submit_run(db_session, workflow_name="test_wf", ...)
    assert run.run_status == "USER_SUBMITTED"

# Step 2: Run test — it fails (function doesn't exist or returns wrong status)
# pytest tests/unit/test_run_service.py::test_submit_run_creates_pending_run

# Step 3: Implement minimal code to pass
def submit_run(db, workflow_name, ...):
    run = WorkflowRun(run_status="USER_SUBMITTED", ...)
    db.add(run)
    return run

# Step 4: Run test — it passes
# Step 5: Refactor if needed, run tests again
```

### What to Test

- **State machine transitions** — every status change, every edge case
- **Service methods** — business logic, error handling
- **Repository methods** — database queries, filters
- **API endpoints** — request validation, response format, status codes

### TDD Benefits for This Codebase

- State machine is critical — tests catch transition bugs before they corrupt runs
- Service layer is complex — tests document expected behavior
- Refactoring is safe — comprehensive tests catch regressions

## Code Conventions

### Python Style

- Use type hints everywhere
- Use `from __future__ import annotations` at top of files
- Prefer dataclasses for structured data
- Use Pydantic v2 for API schemas
- Use structlog for logging (not standard logging)
- Keep functions focused and small
- Prefer explicit over implicit

### Naming

- **Files**: snake_case (e.g., `run_service.py`)
- **Classes**: PascalCase (e.g., `WorkflowRun`)
- **Functions/variables**: snake_case (e.g., `get_run_detail`)
- **Constants**: UPPER_CASE (e.g., `TERMINAL_STATUSES`)
- **Enums**: PascalCase class, UPPER_CASE values (e.g., `RunStatus.COMPLETED`)

### API Design

- RESTful endpoints under `/api/` prefix
- Use Pydantic schemas for request/response validation
- Serialize ORM models in `serializers.py`, not in routes
- Return appropriate HTTP status codes (201 for creation, 404 for not found, etc.)
- Use `HTTPException` for errors

### Database

- All models in `models/` directory
- Use SQLAlchemy relationships, not manual joins
- Repository pattern for data access
- Never query models directly from routes — go through services/repositories

### State Machine

- **Never** mutate `run_status` directly — always go through `state_machine.transition()`
- All state transitions must be explicit events
- Keep transition logic in `state_machine.py`, not in services
- Services orchestrate; state machine decides

## Git Workflow

**Branch strategy:**
- `master` — stable, production-ready (locked for development)
- `dev` — active development branch

**Rules:**
- **Always work in `dev` branch**, never commit directly to `master`
- Verify you're on `dev` before starting work
- Merge `dev` → `master` for releases (not the other way around)

**Commit messages:**
- Clear, concise, focused on "why" not "what"
- Use conventional commits when applicable: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- Reference issues/tickets if relevant

## Testing Strategy

### Test Types

- **Unit tests** (`tests/unit/`): Pure logic with real test database
- **Integration tests** (`tests/integration/`): Require database and/or running services

### Test Structure

```python
def test_descriptive_name(db_session):
    # Arrange
    # ... setup test data ...
    
    # Act
    result = service_function(db_session, ...)
    
    # Assert
    assert result.expected_field == expected_value
```

**Fixtures:**
- `db_session`: Provides clean database session
- `reset_db` (autouse): Drops and recreates tables between tests

**Guidelines:**
- Test behavior, not implementation
- Use descriptive test names
- Keep tests independent
- Mock external services, not database
- Test edge cases and error paths

## Common Tasks

### Adding a New API Endpoint

1. Define schema in `api/schemas.py`
2. Add route in appropriate `api/*_routes.py`
3. Implement logic in corresponding `services/*_service.py`
4. Add repository methods in `database/*_repository.py` if needed
5. Update serializer in `api/serializers.py` if returning new model
6. Write tests

### Adding a New Model

1. Create model in `models/` directory
2. Import in `models/__init__.py`
3. Create Alembic migration: `alembic revision --autogenerate -m "description"`
4. Review generated migration in `alembic/versions/`
5. Apply migration: `alembic upgrade head`
6. Add repository methods in `database/`
7. Write tests

### Modifying State Machine

**⚠️ Critical: State machine changes affect all workflow runs**

1. Understand current flow by reading `services/state_machine.py`
2. Add new status/action/event to appropriate enum
3. Implement handler function (`_handle_*`)
4. Update `VALID_ACTIONS` mapping
5. Add comprehensive tests in `tests/unit/test_state_machine.py`
6. Document the change in commit message

### Database Migrations

```bash
# Create migration after model changes
python -m alembic revision --autogenerate -m "add new field to workflow"

# Review the generated migration file
# Edit if needed (autogenerate isn't perfect)

# Apply migration
python -m alembic upgrade head

# Rollback one step
python -m alembic downgrade -1

# Check current version
python -m alembic current
```

## Environment Variables

See `.env.example` for all available settings:

- `APP_ENV`: development/production
- `DATABASE_URL`: PostgreSQL connection string
- `API_HOST`: Server bind address (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8200)
- `WORKER_HEARTBEAT_INTERVAL`: Seconds between heartbeats (default: 20)
- `WORKER_TIMEOUT`: Seconds before worker considered dead (default: 60)

## Key Patterns

### Dependency Injection

FastAPI's `Depends()` for database sessions:

```python
@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    return service.list_items(db)
```

### Service Layer

Services orchestrate business logic, call repositories and state machine:

```python
def submit_run(db, workflow_name, ...):
    workflow = workflow_repository.get_by_name(db, workflow_name)
    run = Run(...)
    db.add(run)
    db.flush()
    
    result = state_machine.transition(db, run, event, workflow)
    run.run_status = result.run_status
    
    return run
```

### Repository Pattern

Repositories handle database queries:

```python
def get_by_id(db: Session, id: str) -> Model | None:
    return db.query(Model).filter(Model.id == id).first()
```

## Troubleshooting

### Database Connection Errors

- Check `DATABASE_URL` in `.env`
- Verify PostgreSQL is running: `pg_isready`
- Ensure database exists: `createdb agentrunnerv2`
- Check credentials have proper permissions

### Migration Errors

- If autogenerate misses changes, edit migration manually
- Always review generated migrations before applying
- Use `alembic current` to check state
- Use `alembic history` to see migration chain

### Test Failures

- Ensure test database exists: `createdb agentrunnerv2_test`
- Check `AGENT_RUNNER_TEST_DATABASE_URL` env var
- Tests drop and recreate tables — don't use production database
- Run with `-v` for verbose output

## Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
- Alembic: https://alembic.sqlalchemy.org/
- Pydantic v2: https://docs.pydantic.dev/latest/
- structlog: https://www.structlog.org/
