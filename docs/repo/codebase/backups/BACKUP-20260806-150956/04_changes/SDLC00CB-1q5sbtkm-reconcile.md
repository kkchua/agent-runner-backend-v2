---
title: "Change Impact: agent-runner-backend-v2 codebase reconcile"
template_id: "CB-04"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
change_id: "SDLC00CB-1q5sbtkm"
task_id: "sdlc_00_codebase_v1"
initiative_id: "codebase-doc-bootstrap"
created: "2026-08-05T16:37:47+08:00"
author: "sdlc_00_codebase_v1"
---

# Change Impact: agent-runner-backend-v2 codebase reconcile

## 1. Change Summary

### 1.1 Description

Repository scan bootstrap/reconcile generated or refreshed the codebase documentation baseline.

### 1.2 Rationale

Keep `/docs/repo/codebase/current` synchronized with the current repository state even when code changes occurred outside the normal workflow SOP.

## 2. Changed Files

### 2.1 Source Code Changes

| File | Change Type | Description | Impact |
|------|-------------|-------------|--------|
| `.env.example` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/auth_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/host_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/repo_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/run_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/schemas.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/serializers.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/worker_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/api/workflow_routes.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/api_key_auth.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/models.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/navigation.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/rbac.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/auth/supabase_auth.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/config.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/api_key_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/host_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/repo_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/run_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/worker_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/database/workflow_repository.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/logging_config.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/main.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/host.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/repo.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/run.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/worker.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/models/workflow.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/__init__.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/host_service.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/repo_service.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/run_service.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/state_machine.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/worker_service.py` | modify | part of repository scan baseline | medium |
| `agent_runner_backend_v2/services/workflow_service.py` | modify | part of repository scan baseline | medium |
| `AGENTS.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/01_inventory/codebase_inventory.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-auth-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-host-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-repo-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-run-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-schemas.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-serializers.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-worker-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-models.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-navigation.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-rbac.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-host-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-repo-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-run-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-worker-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-logging-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-main.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-host.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-repo.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-run.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-worker.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-workflow.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-host-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-repo-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-run-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-state-machine.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-worker-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-workflow-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/actions-package.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/codebase-governance.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/config-and-data.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/scripts-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/tests-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/workflow-families.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile-validation.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SDLC00CB-cgiwv6ic-review.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SDLC00CB-cgiwv6ic-review.meta.json` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SYNC-SDLC00CB-cgiwv6ic.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/01_inventory/codebase_inventory.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/01_inventory/codebase_inventory.meta.json` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-auth-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-host-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-repo-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-run-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-schemas.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-serializers.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-worker-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-models.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-navigation.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-rbac.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-host-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-repo-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-run-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-worker-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-logging-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-main.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-host.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-repo.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-run.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-worker.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-workflow.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-host-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-repo-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-run-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-state-machine.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-worker-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-workflow-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/actions-package.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/codebase-governance.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/config-and-data.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/scripts-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/tests-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/workflow-families.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/04_changes/SDLC00CB-fvfhkqhj-reconcile.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SDLC00CB-fvfhkqhj-review.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SDLC00CB-fvfhkqhj-review.meta.json` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SYNC-SDLC00CB-fvfhkqhj.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/01_inventory/codebase_inventory.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/01_inventory/codebase_inventory.meta.json` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-auth-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-host-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-repo-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-run-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-schemas.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-serializers.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-worker-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-models.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-navigation.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-rbac.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-host-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-repo-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-run-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-worker-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-logging-config.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-main.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-host.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-repo.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-run.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-worker.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-workflow.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-host-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-init.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-repo-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-run-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-state-machine.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-worker-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-workflow-service.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/actions-package.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/codebase-governance.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/config-and-data.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/scripts-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/tests-suite.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/workflow-families.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile-validation.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SDLC00CB-grpxyiln-review.md` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SDLC00CB-grpxyiln-review.meta.json` | modify | part of repository scan baseline | medium |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SYNC-SDLC00CB-grpxyiln.md` | modify | part of repository scan baseline | medium |
| `How-Do.md` | modify | part of repository scan baseline | medium |
| `pyproject.toml` | modify | part of repository scan baseline | medium |
| `SSO_AUTH_PLAN.md` | modify | part of repository scan baseline | medium |
| `start-backend.bat` | modify | part of repository scan baseline | medium |
| `start-backend.sh` | modify | part of repository scan baseline | medium |
| `tests/__init__.py` | modify | part of repository scan baseline | medium |
| `tests/conftest.py` | modify | part of repository scan baseline | medium |
| `tests/integration/__init__.py` | modify | part of repository scan baseline | medium |
| `tests/integration/conftest.py` | modify | part of repository scan baseline | medium |
| `tests/integration/test_api_routes.py` | modify | part of repository scan baseline | medium |
| `tests/unit/__init__.py` | modify | part of repository scan baseline | medium |
| `tests/unit/test_auth.py` | modify | part of repository scan baseline | medium |
| `tests/unit/test_models.py` | modify | part of repository scan baseline | medium |
| `tests/unit/test_run_repository.py` | modify | part of repository scan baseline | medium |
| `tests/unit/test_run_service.py` | modify | part of repository scan baseline | medium |
| `tests/unit/test_state_machine.py` | modify | part of repository scan baseline | medium |

### 2.2 Configuration Changes

| File | Change Type | Description | Impact |
|------|-------------|-------------|--------|
| | | | |

### 2.3 Test Changes

| File | Change Type | Description |
|------|-------------|-------------|
| | | |

## 3. Updated Documentation

### 3.1 Documentation Created

| Document | Path | Type | Status |
|----------|------|------|--------|
| `codebase_inventory.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/01_inventory/codebase_inventory.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-auth-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-auth-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-host-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-host-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-repo-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-repo-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-run-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-run-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-schemas.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-schemas.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-serializers.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-serializers.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-worker-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-worker-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-api-workflow-routes.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-api-key-auth.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-models.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-models.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-navigation.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-navigation.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-rbac.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-rbac.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-auth-supabase-auth.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-config.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-config.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-api-key-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-host-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-host-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-repo-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-repo-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-run-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-run-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-worker-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-worker-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-database-workflow-repository.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-logging-config.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-logging-config.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-main.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-main.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-host.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-host.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-repo.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-repo.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-run.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-run.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-worker.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-worker.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-models-workflow.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-models-workflow.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-init.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-init.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-host-service.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-host-service.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-repo-service.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-repo-service.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-run-service.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-run-service.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-state-machine.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-state-machine.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-worker-service.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-worker-service.md` | module/component/inventory | draft |
| `agent-runner-backend-v2-services-workflow-service.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-services-workflow-service.md` | module/component/inventory | draft |
| `workflow-families.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/workflow-families.md` | module/component/inventory | draft |
| `actions-package.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/actions-package.md` | module/component/inventory | draft |
| `tests-suite.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/tests-suite.md` | module/component/inventory | draft |
| `scripts-suite.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/scripts-suite.md` | module/component/inventory | draft |
| `config-and-data.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/config-and-data.md` | module/component/inventory | draft |
| `codebase-governance.md` | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/03_components/codebase-governance.md` | module/component/inventory | draft |

### 3.2 Documentation Updated

| Document | Path | Section Updated | Reason |
|----------|------|-----------------|--------|

### 3.3 Inventory Updates

| Module | Previous Status | New Status | Owner Doc Path |
|--------|----------------|------------|----------------|
| `codebase_inventory.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/01_inventory/codebase_inventory.md` |
| `agent-runner-backend-v2-init.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-init.md` |
| `agent-runner-backend-v2-api-init.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-init.md` |
| `agent-runner-backend-v2-api-auth-routes.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-auth-routes.md` |
| `agent-runner-backend-v2-api-host-routes.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-host-routes.md` |
| `agent-runner-backend-v2-api-repo-routes.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-repo-routes.md` |
| `agent-runner-backend-v2-api-routes.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-routes.md` |
| `agent-runner-backend-v2-api-run-routes.md` | undocumented | current | `docs/repo/codebase/runs/SDLC00CB-1q5sbtkm/02_modules/agent-runner-backend-v2-api-run-routes.md` |

## 4. Stale Documentation Removal

### 4.1 Stale Documents Identified

| Document | Path | Reason for Staleness | Action |
|----------|------|---------------------|--------|
| | | | |

### 4.2 Removal Log

| Document | Path | Removed By | Date | Reason |
|----------|------|-----------|------|--------|
| | | | | |

## 5. Impact Assessment

### 5.1 Affected Components

| Component | Impact | Documentation Status |
|-----------|--------|---------------------|
| codebase documentation baseline | high | current |

### 5.2 Affected Workflows

| Workflow | Impact | Notes |
|----------|--------|-------|
| `sdlc_00_codebase_v1` | high | repository scan baseline |

### 5.3 Backward Compatibility

| Aspect | Compatible | Notes |
|--------|-----------|-------|
| API | yes | documentation only |
| Configuration | yes | no code changes |
| Sidecar contract | yes | action writes standard v2 meta.json |

## 6. Documentation Debt

| Item | Reason for Deferral | Owner | Due Date |
|------|-------------------|-------|----------|
| | | | |

## 7. Verification

| Check | Status | Notes |
|-------|--------|-------|
| All changed files listed | pass | repository scan summary |
| All updated docs listed | pass | generated docs |
| Stale docs identified and handled | pass | regenerated baseline |
| Inventory updated | pass | current scan |
