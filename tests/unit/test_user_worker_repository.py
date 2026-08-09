"""Unit tests for user_worker_repository CRUD operations."""
from __future__ import annotations

import pytest

from agent_runner_backend_v2.auth.user_role_model import UserRole
from agent_runner_backend_v2.database.user_role_repository import (
    delete_user,
    get_or_create_user,
    is_system_user,
    list_users,
)
from agent_runner_backend_v2.database.user_worker_repository import (
    assign_worker,
    get_user_worker_ids,
    set_user_workers,
    unassign_worker,
)


class TestAssignWorker:
    def test_assigns_worker_to_user(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assignment = assign_worker(db_session, "user-1", "worker-1")
        db_session.commit()
        assert assignment.user_id == "user-1"
        assert assignment.worker_id == "worker-1"

    def test_idempotent_assign(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        assign_worker(db_session, "user-1", "worker-1")
        db_session.commit()
        ids = get_user_worker_ids(db_session, "user-1")
        assert ids == ["worker-1"]


class TestUnassignWorker:
    def test_removes_assignment(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        db_session.commit()
        assert unassign_worker(db_session, "user-1", "worker-1") is True
        db_session.commit()
        assert get_user_worker_ids(db_session, "user-1") == []

    def test_returns_false_for_nonexistent(self, db_session):
        assert unassign_worker(db_session, "user-1", "worker-1") is False


class TestGetUserWorkerIds:
    def test_empty_when_no_assignments(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert get_user_worker_ids(db_session, "user-1") == []

    def test_returns_all_assigned_workers(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        assign_worker(db_session, "user-1", "worker-2")
        db_session.commit()
        ids = get_user_worker_ids(db_session, "user-1")
        assert sorted(ids) == ["worker-1", "worker-2"]


class TestSetUserWorkers:
    def test_replaces_all_assignments(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        assign_worker(db_session, "user-1", "worker-2")
        db_session.commit()
        set_user_workers(db_session, "user-1", ["worker-3", "worker-4"])
        db_session.commit()
        ids = get_user_worker_ids(db_session, "user-1")
        assert sorted(ids) == ["worker-3", "worker-4"]

    def test_clears_when_empty_list(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        db_session.commit()
        set_user_workers(db_session, "user-1", [])
        db_session.commit()
        assert get_user_worker_ids(db_session, "user-1") == []


class TestSystemUserProtection:
    def test_system_user_cannot_be_deleted(self, db_session):
        user = get_or_create_user(db_session, "system-1", "system@test.com")
        user.is_system = True
        db_session.commit()
        assert delete_user(db_session, "system-1") is False
        db_session.commit()
        assert len(list_users(db_session)) == 1

    def test_non_system_user_can_be_deleted(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert delete_user(db_session, "user-1") is True
        db_session.commit()
        assert len(list_users(db_session)) == 0

    def test_is_system_user_returns_true_for_system(self, db_session):
        user = get_or_create_user(db_session, "system-1", "system@test.com")
        user.is_system = True
        db_session.commit()
        assert is_system_user(db_session, "system-1") is True

    def test_is_system_user_returns_false_for_normal(self, db_session):
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assert is_system_user(db_session, "user-1") is False

    def test_is_system_user_returns_false_for_unknown(self, db_session):
        assert is_system_user(db_session, "nonexistent") is False

    def test_cascade_deletes_worker_assignments(self, db_session):
        """When a user is deleted, their worker assignments should be cascade-deleted."""
        get_or_create_user(db_session, "user-1", "alice@test.com")
        db_session.commit()
        assign_worker(db_session, "user-1", "worker-1")
        assign_worker(db_session, "user-1", "worker-2")
        db_session.commit()
        delete_user(db_session, "user-1")
        db_session.commit()
        assert get_user_worker_ids(db_session, "user-1") == []
