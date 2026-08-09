"""Unit tests for user_role_repository CRUD operations."""
from __future__ import annotations

import pytest

from agent_runner_backend_v2.auth.user_role_model import UserRole
from agent_runner_backend_v2.database.user_role_repository import (
    delete_user,
    get_or_create_user,
    get_user_role,
    list_users,
    update_user_email,
    update_user_role,
)


class TestGetOrCreateUser:
    def test_creates_new_user_with_default_viewer_role(self, db_session):
        user = get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert user.user_id == "user-1"
        assert user.email == "alice@test.com"
        assert user.role == "viewer"

    def test_returns_existing_user_without_duplicate(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        user2 = get_or_create_user(db_session, "user-1", "alice@test.com")
        assert user2.user_id == "user-1"
        assert len(list_users(db_session)) == 1

    def test_preserves_existing_role_on_retrieve(self, db_session):
        user = get_or_create_user(db_session, "user-1", "alice@test.com")
        user.role = "admin"
        db_session.commit()
        retrieved = get_or_create_user(db_session, "user-1", "alice@test.com")
        assert retrieved.role == "admin"


class TestGetUserRole:
    def test_returns_role_for_existing_user(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert get_user_role(db_session, "user-1") == "viewer"

    def test_returns_none_for_unknown_user(self, db_session):
        assert get_user_role(db_session, "nonexistent") is None


class TestListUsers:
    def test_empty_when_no_users(self, db_session):
        assert list_users(db_session) == []

    def test_returns_all_users_ordered_by_email(self, db_session):
        get_or_create_user(db_session, "u1", "charlie@test.com")
        get_or_create_user(db_session, "u2", "alice@test.com")
        get_or_create_user(db_session, "u3", "bob@test.com")
        db_session.commit()
        users = list_users(db_session)
        assert len(users) == 3
        assert [u.email for u in users] == ["alice@test.com", "bob@test.com", "charlie@test.com"]


class TestUpdateUserRole:
    def test_updates_role(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        updated = update_user_role(db_session, "user-1", "operator")
        db_session.commit()
        assert updated is not None
        assert updated.role == "operator"

    def test_returns_none_for_unknown_user(self, db_session):
        assert update_user_role(db_session, "nonexistent", "admin") is None


class TestUpdateUserEmail:
    def test_updates_email(self, db_session):
        get_or_create_user(db_session, "user-1", "old@test.com")
        db_session.commit()
        updated = update_user_email(db_session, "user-1", "new@test.com")
        db_session.commit()
        assert updated is not None
        assert updated.email == "new@test.com"

    def test_returns_none_for_unknown_user(self, db_session):
        assert update_user_email(db_session, "nonexistent", "x@test.com") is None


class TestDeleteUser:
    def test_deletes_existing_user(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert delete_user(db_session, "user-1") is True
        db_session.commit()
        assert len(list_users(db_session)) == 0

    def test_returns_false_for_unknown_user(self, db_session):
        assert delete_user(db_session, "nonexistent") is False
