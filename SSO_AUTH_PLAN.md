# SSO Authentication Implementation Plan

## Overview

Add Supabase-based SSO authentication to agent-runner-backend-v2 with support for:
- Browser-based users (React operator console) via OIDC/JWT
- Script/machine authentication via API keys
- Role-based access control (RBAC) for navigation and endpoint protection
- Multi-service SSO for future backend consolidation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Supabase (Auth + User DB)                  │
│  - User authentication (email/password, OAuth, magic link) │
│  - JWT token issuance (ES256)                               │
│  - User management dashboard                                │
│  - Role metadata in JWT claims                              │
└─────────────────────────────────────────────────────────────┘
                            ↓ issues JWT
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
┌──────────────────┐                  ┌──────────────────┐
│  React Console   │                  │  Scripts/Machines│
│  (@supabase/sdk) │                  │  (X-API-Key)     │
│  Browser-based   │                  │  Server-to-server│
└──────────────────┘                  └──────────────────┘
        ↓ Bearer JWT                          ↓ X-API-Key
        └───────────────────┬─────────────────┘
                            ↓
              ┌─────────────────────────────┐
              │  agent-runner-backend-v2    │
              │  (Resource Server)          │
              │  - Validates Supabase JWT   │
              │  - Validates API keys       │
              │  - Checks roles/permissions │
              │  - Exposes navigation API   │
              └─────────────────────────────┘
                    Railway (one service)
```

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| IdP | Supabase Auth | Free at 5-10 users, PostgreSQL-native, open-source, Railway-friendly |
| Script auth | API keys (bcrypt hashed, stored in app DB) | Simple, no OAuth flow needed for scripts |
| RBAC location | In Supabase user metadata | Roles passed via JWT claims, no extra lookup |
| Navigation config | Hardcoded in backend | Simple, version-controlled, sufficient for current scale |
| Auth module location | Same repo (`auth/` package) | Single backend, cost savings, can extract later if needed |
| JWT algorithm | ES256 via JWKS | Supabase default, public key validation (no shared secret) |

## Supabase Project

- **URL:** `https://<YOUR_PROJECT>.supabase.co`
- **Keys:** Legacy anon/service_role keys (JWT format `eyJ...`) — NOT the new `sb_publishable_...` format
- **JWT Secret:** Configured in `.env`
- **Data API:** Auto-expose disabled (security)

## Role Model

| Role | Access |
|------|--------|
| `admin` | Full access — all endpoints, API key management, user management |
| `operator` | Runs, workers, workflows — day-to-day operations |
| `viewer` | Read-only dashboard access |
| `service-account` | Daemon API — register, heartbeat, claim, outcome |

## Phase Status

### Phase 1: Backend Auth Module ✅ COMPLETED (2026-08-04)

**Commit:** `0e0814f`

**What was built:**
- `auth/supabase_auth.py` — JWT validation using JWKS public keys (ES256), preloaded at startup
- `auth/api_key_auth.py` — API key generation (bcrypt hashed), verification
- `auth/rbac.py` — `require_jwt_or_api_key()` dependency factory
- `auth/navigation.py` — Role-filtered navigation menu config
- `auth/models.py` — `APIKey` ORM model
- `database/api_key_repository.py` — API key CRUD
- `api/auth_routes.py` — `/api/auth/me`, `/navigation`, `/api-keys` CRUD
- CORS middleware in `main.py`
- Alembic migration `85a4f77176f3` for `api_keys` table
- 24 unit tests (all passing)

**Route protection applied:**
- `/api/runs/*` → admin, operator (outcome also allows service-account)
- `/api/workers/*` daemon endpoints → admin, operator, service-account
- `/api/workers/*` management endpoints → admin, operator
- `/api/workflows/*` → admin, operator
- `/api/hosts/*` → admin only
- `/api/repos/*` → admin only

**Verified working:**
- JWT login via Supabase → `/api/auth/me` returns correct user info
- Role extraction from Supabase user metadata
- Test user: `andychua7401@gmail.com` with role `admin`

---

### Phase 2: React Frontend Integration (operator-console-v2)

**Goal:** Add login flow to the React operator console using `@supabase/supabase-js`

**Tasks:**
- [ ] Install `@supabase/supabase-js` in operator-console-v2
- [ ] Create auth context/provider with login state management
- [ ] Build login page (email/password form)
- [ ] Add protected route wrapper — redirect to login if not authenticated
- [ ] Store JWT in memory (not localStorage for security)
- [ ] Send `Authorization: Bearer <token>` on all API calls
- [ ] Handle token refresh (Supabase auto-refreshes)
- [ ] Read user role from JWT claims
- [ ] Use `/api/auth/navigation` endpoint to build sidebar/menu
- [ ] Add logout functionality

**Files to create/modify:**
- `src/lib/supabase.ts` — Supabase client initialization
- `src/contexts/AuthContext.tsx` — Auth state provider
- `src/components/LoginPage.tsx` — Login form
- `src/components/ProtectedRoute.tsx` — Route guard
- `src/hooks/useAuth.ts` — Auth hook
- Update `src/App.tsx` — Wrap with auth provider

---

### Phase 3: Daemon/Script API Key Setup

**Goal:** Configure daemon workers to authenticate via API keys

**Tasks:**
- [ ] Create API keys for each daemon worker via `/api/auth/api-keys`
- [ ] Update daemon `backend_client.py` to send `X-API-Key` header
- [ ] Update daemon `sync.py` to send `X-API-Key` header
- [ ] Store API keys in daemon config (encrypted)
- [ ] Test daemon registration, heartbeat, claim, outcome with API key auth
- [ ] Document API key rotation process

**Daemon config example:**
```json
{
  "backend_url": "https://agent-runner.up.railway.app",
  "api_key": "arb_xxxxxxxxxxxxxxxxxxxxx"
}
```

---

### Phase 4: Railway Deployment

**Goal:** Deploy the authenticated backend to Railway

**Tasks:**
- [ ] Add Supabase env vars to Railway dashboard:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `SUPABASE_JWT_SECRET`
- [ ] Add `CORS_ORIGINS` with production frontend URL
- [ ] Run Alembic migration on Railway PostgreSQL
- [ ] Test auth flow end-to-end on Railway
- [ ] Create initial admin API key for daemon

**Railway env vars:**
```
SUPABASE_URL=https://<YOUR_PROJECT>.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_JWT_SECRET=...
CORS_ORIGINS=["https://operator-console.up.railway.app"]
```

---

### Phase 5: Backend Consolidation (Future)

**Goal:** Consolidate multiple Python/FastAPI backends into one platform

**Tasks:**
- [ ] Create `agent-runner-platform` repo (or rename current)
- [ ] Move agent-runner-backend-v2 as `agent_runner/` module
- [ ] Move other backends as separate modules
- [ ] Share auth module across all modules
- [ ] Share database connection
- [ ] Unified API under one domain
- [ ] Deploy as single Railway service

**Target structure:**
```
agent-runner-platform/
├── auth/              # Shared auth module (current auth/)
├── agent_runner/      # Agent runner module (current backend v2)
├── workflow_builder/  # Workflow builder module
├── other_service/     # Other backend modules
├── shared/            # Shared utilities, models
└── main.py            # Single FastAPI app
```

---

## API Key Management

### Storage Locations

**Backend database** (`api_keys` table):
- Stores bcrypt hash of the key (never the plain text)
- Fields: `id`, `key_hash`, `key_prefix` (first 11 chars for identification), `name`, `role`, `created_by`, `expires_at`, `is_active`, `created_at`, `last_used_at`
- The plain key is only returned once when created — store it securely!

**Daemon config** (`~/.ukbe-runner/config.json`):
- Stores the plain text API key in the `v2_api_key` field
- Example:
  ```json
  {
    "v2_backend_url": "http://192.168.0.200:8200",
    "v2_api_key": "arb_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
  ```
- Alternative: Set environment variable `AGENT_RUNNER_V2_API_KEY` (takes priority over config)

### API Key Rotation

To rotate/change an API key:

```bash
# 1. List existing API keys to get the key ID
curl http://127.0.0.1:8200/api/auth/api-keys \
  -H "Authorization: Bearer <JWT_TOKEN>"

# 2. Revoke the old key
curl -X DELETE http://127.0.0.1:8200/api/auth/api-keys/<KEY_ID> \
  -H "Authorization: Bearer <JWT_TOKEN>"

# 3. Create a new key
curl -X POST http://127.0.0.1:8200/api/auth/api-keys \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "chua-worker-01", "role": "service-account"}'
# Save the returned "key" value — it won't be shown again!

# 4. Update daemon config
# Edit ~/.ukbe-runner/config.json and update the "v2_api_key" field
# Or set environment variable: export AGENT_RUNNER_V2_API_KEY="arb_..."

# 5. Restart the daemon
```

### Current API Keys

| Name | Role | Key ID | Created |
|------|------|--------|---------|
| chua-worker-01 | service-account | 600a2300-ce2e-4527-99a7-bca37574de6b | 2026-08-04 |

---

## Operational Commands

### Create an API key
```bash
# Login and get token first, then:
curl -X POST http://127.0.0.1:8200/api/auth/api-keys \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-daemon", "role": "service-account"}'
```

### Set user role in Supabase
```sql
UPDATE auth.users 
SET raw_user_meta_data = '{"email_verified": true, "role": "admin"}'::jsonb
WHERE email = 'user@example.com';
```

### Get JWT token (for testing)
```bash
curl -X POST "https://<YOUR_PROJECT>.supabase.co/auth/v1/token?grant_type=password" \
  -H "apikey: <ANON_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

## Notes

- **Windows localhost issue:** On Windows, `localhost` resolves to `::1` (IPv6). Use `127.0.0.1` explicitly in HTTP clients.
- **JWKS preloading:** Keys are fetched at startup to avoid blocking the async event loop on first request.
- **Supabase free tier:** 50k MAU, 500MB database — well within limits for 5-10 users.
- **Token expiry:** Supabase JWTs expire after 1 hour. Frontend should handle refresh automatically.
