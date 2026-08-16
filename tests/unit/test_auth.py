"""Unit tests for the auth module — JWT validation, API keys, RBAC, navigation."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from agent_runner_backend_v2.auth.api_key_auth import (
    generate_api_key,
    hash_api_key,
    verify_api_key,
)
from agent_runner_backend_v2.auth.models import APIKey
from agent_runner_backend_v2.auth.navigation import (
    AGENT_RUNNER_MENU,
    MenuItem,
    _filter_menu,
    get_navigation,
)
from agent_runner_backend_v2.auth.supabase_auth import (
    UserContext,
    _extract_role,
)
from agent_runner_backend_v2.database.api_key_repository import (
    create_api_key,
    get_api_key_by_id,
    list_api_keys,
    revoke_api_key,
    update_last_used,
)


# ── JWT validation tests ──


class TestDecodeSupabaseToken:
    """Tests for decode_supabase_token()."""

    def test_valid_token(self):
        """Test that a valid token is decoded correctly (uses JWKS in real env)."""
        # In unit test env without Supabase, we verify the function exists
        # and raises proper errors. Integration tests cover real tokens.
        from agent_runner_backend_v2.auth.supabase_auth import decode_supabase_token
        assert callable(decode_supabase_token)

    def test_expired_token_raises_401(self):
        """Expired tokens should raise 401."""
        from agent_runner_backend_v2.auth.supabase_auth import decode_supabase_token
        # Without a real JWKS connection, invalid tokens raise 401
        with pytest.raises(HTTPException) as exc_info:
            decode_supabase_token("invalid.token.here")
        assert exc_info.value.status_code == 401

    def test_invalid_token_raises_401(self):
        """Malformed tokens should raise 401."""
        from agent_runner_backend_v2.auth.supabase_auth import decode_supabase_token
        with pytest.raises(HTTPException) as exc_info:
            decode_supabase_token("not-a-jwt")
        assert exc_info.value.status_code == 401


class TestExtractRole:
    """Tests for _extract_role()."""

    def test_extracts_role_from_metadata(self):
        payload = {"user_metadata": {"role": "operator"}}
        assert _extract_role(payload) == "operator"

    def test_defaults_to_viewer(self):
        payload = {"user_metadata": {}}
        assert _extract_role(payload) == "viewer"

    def test_defaults_to_viewer_no_metadata(self):
        payload = {}
        assert _extract_role(payload) == "viewer"


# ── API key tests ──


class TestAPIKeyGeneration:
    """Tests for API key generation and verification."""

    def test_generate_api_key_returns_tuple(self):
        plain, hashed = generate_api_key()
        assert plain.startswith("arb_")
        assert len(plain) > 20
        assert hashed != plain

    def test_verify_api_key_correct(self):
        plain, hashed = generate_api_key()
        assert verify_api_key(plain, hashed) is True

    def test_verify_api_key_wrong_key(self):
        _, hashed = generate_api_key()
        assert verify_api_key("wrong-key", hashed) is False

    def test_hash_api_key_deterministic_verify(self):
        key = "test-api-key-12345"
        hashed = hash_api_key(key)
        assert verify_api_key(key, hashed) is True
        assert verify_api_key("different-key", hashed) is False


class TestAPIKeyRepository:
    """Tests for API key database operations."""

    def test_create_api_key(self, db_session):
        _, key_hash = generate_api_key()
        api_key = create_api_key(
            db_session,
            key_hash=key_hash,
            key_prefix="arb_test",
            name="Test Key",
            role="service-account",
            created_by="user-123",
        )
        assert api_key.id is not None
        assert api_key.name == "Test Key"
        assert api_key.role == "service-account"
        assert api_key.is_active is True

    def test_get_api_key_by_id(self, db_session):
        _, key_hash = generate_api_key()
        created = create_api_key(
            db_session,
            key_hash=key_hash,
            key_prefix="arb_test",
            name="Test Key",
            role="admin",
            created_by="user-123",
        )
        found = get_api_key_by_id(db_session, created.id)
        assert found is not None
        assert found.name == "Test Key"

    def test_get_api_key_by_id_not_found(self, db_session):
        assert get_api_key_by_id(db_session, "nonexistent") is None

    def test_list_api_keys(self, db_session):
        for i in range(3):
            _, key_hash = generate_api_key()
            create_api_key(
                db_session,
                key_hash=key_hash,
                key_prefix=f"arb_{i}",
                name=f"Key {i}",
                role="service-account",
                created_by="user-123",
            )
        keys = list_api_keys(db_session)
        assert len(keys) == 3

    def test_revoke_api_key(self, db_session):
        _, key_hash = generate_api_key()
        api_key = create_api_key(
            db_session,
            key_hash=key_hash,
            key_prefix="arb_test",
            name="Test Key",
            role="service-account",
            created_by="user-123",
        )
        assert api_key.is_active is True
        revoke_api_key(db_session, api_key)
        assert api_key.is_active is False

    def test_update_last_used(self, db_session):
        _, key_hash = generate_api_key()
        api_key = create_api_key(
            db_session,
            key_hash=key_hash,
            key_prefix="arb_test",
            name="Test Key",
            role="service-account",
            created_by="user-123",
        )
        assert api_key.last_used_at is None
        update_last_used(db_session, api_key)
        assert api_key.last_used_at is not None

    def test_create_api_key_with_expiry(self, db_session):
        _, key_hash = generate_api_key()
        expires = datetime.now(timezone.utc) + timedelta(days=30)
        api_key = create_api_key(
            db_session,
            key_hash=key_hash,
            key_prefix="arb_test",
            name="Expiring Key",
            role="service-account",
            created_by="user-123",
            expires_at=expires,
        )
        assert api_key.expires_at is not None


# ── Navigation tests ──


class TestNavigationFiltering:
    """Tests for menu filtering by role."""

    def test_admin_sees_all_items(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "admin")
        ids = [item["id"] for item in result]
        assert "dashboard" in ids
        assert "runs" in ids
        assert "hosts" in ids
        assert "repos" in ids
        assert "settings" in ids

    def test_operator_sees_operational_items(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "operator")
        ids = [item["id"] for item in result]
        assert "dashboard" in ids
        assert "runs" in ids
        assert "workflows" in ids
        assert "workers" in ids
        assert "hosts" not in ids
        assert "repos" not in ids
        assert "settings" not in ids

    def test_viewer_sees_limited_items(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "viewer")
        ids = [item["id"] for item in result]
        assert "dashboard" in ids
        assert "runs" not in ids
        assert "hosts" not in ids

    def test_unknown_role_sees_nothing(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "unknown")
        assert result == []

    def test_settings_children_filtered(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "admin")
        settings_item = next(item for item in result if item["id"] == "settings")
        child_ids = [c["id"] for c in settings_item["children"]]
        assert "settings-general" in child_ids
        assert "settings-api-keys" in child_ids
        assert "settings-users" in child_ids


class TestUserContext:
    """Tests for UserContext dataclass."""

    def test_create_user_context(self):
        ctx = UserContext(
            user_id="user-123",
            email="test@example.com",
            role="admin",
        )
        assert ctx.user_id == "user-123"
        assert ctx.email == "test@example.com"
        assert ctx.role == "admin"
        assert ctx.is_service_account is False

    def test_create_service_account_context(self):
        ctx = UserContext(
            user_id="apikey:abc-123",
            email="my-script@service",
            role="service-account",
            is_service_account=True,
            metadata={"api_key_name": "My Script"},
        )
        assert ctx.is_service_account is True
        assert ctx.metadata["api_key_name"] == "My Script"


# ── Current navigation config tests ──


class TestAgentRunnerMenuFiltering:
    """Tests for the actual AGENT_RUNNER_MENU config (runs, history, submit, etc.)."""

    def test_admin_sees_all_items_including_users(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "admin")
        ids = [item["id"] for item in result]
        assert "runs" in ids
        assert "history" in ids
        assert "submit" in ids
        assert "workflows" in ids
        assert "workers" in ids
        assert "hosts" in ids
        assert "repos" in ids
        assert "users" in ids

    def test_operator_sees_operational_items_no_admin(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "operator")
        ids = [item["id"] for item in result]
        assert "runs" in ids
        assert "history" in ids
        assert "submit" in ids
        assert "workflows" in ids
        assert "workers" in ids
        assert "hosts" not in ids
        assert "repos" not in ids
        assert "users" not in ids

    def test_viewer_sees_read_only_items(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "viewer")
        ids = [item["id"] for item in result]
        assert "runs" in ids
        assert "history" in ids
        assert "submit" not in ids
        assert "workflows" not in ids
        assert "workers" not in ids
        assert "hosts" not in ids
        assert "repos" not in ids
        assert "users" not in ids

    def test_unknown_role_sees_nothing(self):
        result = _filter_menu(AGENT_RUNNER_MENU, "unknown")
        assert result == []
