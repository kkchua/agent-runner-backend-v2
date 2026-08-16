---
title: "Component Documentation: codebase governance"
template_id: "CB-03"
version: "1.0.0"
doc_type: "system"
authority: "workflow-generated"
scan_policy: "include"
lifecycle_status: "approved"
component_id: "codebase-governance"
created: "2026-08-05T16:37:47+08:00"
owner: "sdlc_00_codebase_v1"
last_verified_by_change: "sdlc_00_codebase_v1 / SDLC00CB-1q5sbtkm / 2026-08-05T16:37:47+08:00"
modules: ["AGENTS.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/01_inventory/codebase_inventory.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-auth-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-host-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-repo-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-run-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-schemas.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-serializers.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-worker-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-workflow-routes.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-api-key-auth.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-models.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-navigation.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-rbac.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-supabase-auth.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-config.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-api-key-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-host-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-repo-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-run-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-worker-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-workflow-repository.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-logging-config.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-main.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-host.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-repo.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-run.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-worker.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-workflow.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-host-service.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-init.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-repo-service.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-run-service.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-state-machine.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-worker-service.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-workflow-service.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/actions-package.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/codebase-governance.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/config-and-data.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/scripts-suite.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/tests-suite.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/workflow-families.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile-validation.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SDLC00CB-cgiwv6ic-review.md", "docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SYNC-SDLC00CB-cgiwv6ic.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/01_inventory/codebase_inventory.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-auth-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-host-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-repo-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-run-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-schemas.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-serializers.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-worker-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-workflow-routes.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-api-key-auth.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-models.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-navigation.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-rbac.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-supabase-auth.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-config.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-api-key-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-host-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-repo-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-run-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-worker-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-workflow-repository.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-logging-config.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-main.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-host.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-repo.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-run.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-worker.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-workflow.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-host-service.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-init.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-repo-service.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-run-service.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-state-machine.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-worker-service.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-workflow-service.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/actions-package.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/codebase-governance.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/config-and-data.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/scripts-suite.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/tests-suite.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/workflow-families.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/04_changes/SDLC00CB-fvfhkqhj-reconcile.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SDLC00CB-fvfhkqhj-review.md", "docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SYNC-SDLC00CB-fvfhkqhj.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/01_inventory/codebase_inventory.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-auth-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-host-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-repo-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-run-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-schemas.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-serializers.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-worker-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-workflow-routes.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-api-key-auth.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-models.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-navigation.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-rbac.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-supabase-auth.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-config.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-api-key-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-host-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-repo-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-run-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-worker-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-workflow-repository.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-logging-config.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-main.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-host.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-repo.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-run.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-worker.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-workflow.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-host-service.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-init.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-repo-service.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-run-service.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-state-machine.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-worker-service.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-workflow-service.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/actions-package.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/codebase-governance.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/config-and-data.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/scripts-suite.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/tests-suite.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/workflow-families.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile-validation.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SDLC00CB-grpxyiln-review.md", "docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SYNC-SDLC00CB-grpxyiln.md", "How-Do.md", "SSO_AUTH_PLAN.md"]
---

# Component Documentation: codebase governance

## 1. Component Overview

### 1.1 Purpose

The codebase documentation standards, templates, inventory, and validation rules that govern `/docs/codebase`.

### 1.2 Scope

| Module | Role in Component |
|--------|-------------------|
| `AGENTS.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/01_inventory/codebase_inventory.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-auth-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-host-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-repo-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-run-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-schemas.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-serializers.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-worker-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-models.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-navigation.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-rbac.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-host-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-repo-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-run-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-worker-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-logging-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-main.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-host.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-repo.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-run.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-worker.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-workflow.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-host-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-repo-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-run-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-state-machine.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-worker-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-workflow-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/actions-package.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/codebase-governance.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/config-and-data.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/scripts-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/tests-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/workflow-families.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile-validation.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SDLC00CB-cgiwv6ic-review.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SYNC-SDLC00CB-cgiwv6ic.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/01_inventory/codebase_inventory.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-auth-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-host-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-repo-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-run-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-schemas.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-serializers.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-worker-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-models.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-navigation.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-rbac.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-host-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-repo-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-run-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-worker-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-logging-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-main.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-host.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-repo.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-run.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-worker.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-workflow.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-host-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-repo-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-run-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-state-machine.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-worker-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-workflow-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/actions-package.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/codebase-governance.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/config-and-data.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/scripts-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/tests-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/workflow-families.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/04_changes/SDLC00CB-fvfhkqhj-reconcile.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SDLC00CB-fvfhkqhj-review.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SYNC-SDLC00CB-fvfhkqhj.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/01_inventory/codebase_inventory.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-auth-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-host-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-repo-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-run-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-schemas.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-serializers.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-worker-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-models.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-navigation.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-rbac.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-host-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-repo-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-run-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-worker-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-logging-config.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-main.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-host.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-repo.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-run.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-worker.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-workflow.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-host-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-init.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-repo-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-run-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-state-machine.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-worker-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-workflow-service.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/actions-package.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/codebase-governance.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/config-and-data.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/scripts-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/tests-suite.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/workflow-families.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile-validation.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SDLC00CB-grpxyiln-review.md` | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SYNC-SDLC00CB-grpxyiln.md` | documentation artifact |
| `How-Do.md` | documentation artifact |
| `SSO_AUTH_PLAN.md` | documentation artifact |

## 2. Architecture

### 2.1 Component Diagram

Generated from repository scan baseline.

### 2.2 Data Flow

Repository files are scanned, normalized into inventory rows, and rendered into codebase documentation artifacts.

### 2.3 External Interfaces

| Interface | Direction | Protocol | Description |
|-----------|-----------|----------|-------------|
| `AGENTS.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/01_inventory/codebase_inventory.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-auth-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-host-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-repo-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-run-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-schemas.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-serializers.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-worker-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-models.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-navigation.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-rbac.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-host-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-repo-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-run-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-worker-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-logging-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-main.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-host.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-repo.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-run.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-worker.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-models-workflow.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-host-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-repo-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-run-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-state-machine.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-worker-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/02_modules/agent-runner-backend-v2-services-workflow-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/actions-package.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/codebase-governance.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/config-and-data.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/scripts-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/tests-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/03_components/workflow-families.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile-validation.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/04_changes/SDLC00CB-cgiwv6ic-reconcile.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SDLC00CB-cgiwv6ic-review.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-cgiwv6ic/sync_logs/SYNC-SDLC00CB-cgiwv6ic.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/01_inventory/codebase_inventory.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-auth-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-host-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-repo-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-run-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-schemas.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-serializers.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-worker-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-models.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-navigation.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-rbac.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-host-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-repo-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-run-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-worker-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-logging-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-main.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-host.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-repo.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-run.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-worker.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-models-workflow.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-host-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-repo-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-run-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-state-machine.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-worker-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/02_modules/agent-runner-backend-v2-services-workflow-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/actions-package.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/codebase-governance.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/config-and-data.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/scripts-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/tests-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/03_components/workflow-families.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/04_changes/SDLC00CB-fvfhkqhj-reconcile.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SDLC00CB-fvfhkqhj-review.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-fvfhkqhj/sync_logs/SYNC-SDLC00CB-fvfhkqhj.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/01_inventory/codebase_inventory.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-auth-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-host-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-repo-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-run-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-schemas.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-serializers.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-worker-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-api-workflow-routes.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-api-key-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-models.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-navigation.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-rbac.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-auth-supabase-auth.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-api-key-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-host-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-repo-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-run-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-worker-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-database-workflow-repository.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-logging-config.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-main.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-host.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-repo.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-run.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-worker.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-models-workflow.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-host-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-init.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-repo-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-run-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-state-machine.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-worker-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/02_modules/agent-runner-backend-v2-services-workflow-service.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/actions-package.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/codebase-governance.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/config-and-data.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/scripts-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/tests-suite.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/03_components/workflow-families.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile-validation.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/04_changes/SDLC00CB-grpxyiln-reconcile.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SDLC00CB-grpxyiln-review.md` | outbound | markdown | documentation artifact |
| `docs/repo/codebase/runs/SDLC00CB-grpxyiln/sync_logs/SYNC-SDLC00CB-grpxyiln.md` | outbound | markdown | documentation artifact |
| `How-Do.md` | outbound | markdown | documentation artifact |
| `SSO_AUTH_PLAN.md` | outbound | markdown | documentation artifact |

## 3. Behavior

### 3.1 Lifecycle

Created during codebase bootstrap or reconcile runs and refreshed when repository structure changes.

### 3.2 State Management

State is represented by the generated inventory and per-module/component documents.

### 3.3 Error Propagation

Documentation drift is treated as a validation failure and reraised to the workflow runner.

## 4. Configuration

| Parameter | Source | Default | Description |
|-----------|--------|---------|-------------|
| | | | |

## 5. Constraints

| Constraint | Rationale | Enforcement |
|------------|-----------|-------------|
| Zero mutation of source code | Documentation bootstrap must not alter code | Workflow writes docs only |

## 6. Testing

### 6.1 Integration Tests

| Test | Coverage |
|------|----------|
| | |

### 6.2 Known Gaps

Auto-generated baseline; extend with component-specific checks as needed.

## 7. Change Log

| Date | Change | Modules Affected | Verified By |
|------|--------|-----------------|-------------|
| 2026-08-05 | Initial baseline generated from repository scan | 155 modules/files | sdlc_00_codebase_v1 |
