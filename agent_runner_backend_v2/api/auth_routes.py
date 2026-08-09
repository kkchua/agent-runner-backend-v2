"""Auth API routes — user info, navigation, API key management."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agent_runner_backend_v2.auth.api_key_auth import generate_api_key
from agent_runner_backend_v2.auth.navigation import get_navigation
from agent_runner_backend_v2.auth.rbac import require_jwt_or_api_key
from agent_runner_backend_v2.auth.supabase_auth import UserContext
from agent_runner_backend_v2.database import get_db
from agent_runner_backend_v2.database.api_key_repository import (
    create_api_key,
    list_api_keys,
    revoke_api_key,
)
from agent_runner_backend_v2.database.user_role_repository import (
    delete_user,
    list_users,
    update_user_role,
)
from agent_runner_backend_v2.database.user_worker_repository import (
    get_user_worker_ids,
    set_user_workers,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Schemas ──


class UserInfoResponse(BaseModel):
    """Current user information from JWT or API key."""

    user_id: str
    email: str
    role: str
    is_service_account: bool


class NavigationResponse(BaseModel):
    """Navigation menu item."""

    id: str
    label: str
    icon: str
    path: str
    required_roles: list[str]
    children: list[dict] | None = None


class CreateAPIKeyRequest(BaseModel):
    """Request body for creating a new API key."""

    name: str
    role: str = "service-account"
    expires_at: datetime | None = None


class CreateAPIKeyResponse(BaseModel):
    """Response after creating an API key — includes the plain key (shown once)."""

    id: str
    key: str  # plain key — only returned here, never again
    name: str
    role: str
    expires_at: datetime | None


class APIKeyInfo(BaseModel):
    """API key info for listing (no secret)."""

    id: str
    key_prefix: str
    name: str
    role: str
    is_active: bool
    expires_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None


class UserRoleResponse(BaseModel):
    """User role info for listing."""

    user_id: str
    email: str
    role: str
    is_system: bool
    created_at: datetime
    updated_at: datetime


class SetUserWorkersRequest(BaseModel):
    """Request body for setting a user's assigned workers."""

    worker_ids: list[str]


class UpdateUserRoleRequest(BaseModel):
    """Request body for updating a user's role."""

    role: str


# ── Endpoints ──


@router.get("/me", response_model=UserInfoResponse)
def get_me(
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "viewer", "service-account")),
):
    """Return the current authenticated user's info."""
    return UserInfoResponse(
        user_id=user.user_id,
        email=user.email,
        role=user.role,
        is_service_account=user.is_service_account,
    )


@router.get("/navigation")
def get_nav(
    app_id: str = "agent-runner",
    user: UserContext = Depends(require_jwt_or_api_key("admin", "operator", "viewer", "service-account")),
):
    """Return the navigation menu filtered by the user's role."""
    return get_navigation(app_id=app_id, user=user)


@router.post("/api-keys", response_model=CreateAPIKeyResponse, status_code=status.HTTP_201_CREATED)
def create_key(
    body: CreateAPIKeyRequest,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Create a new API key. Admin only. The plain key is returned once — store it securely."""
    plain_key, key_hash = generate_api_key()
    key_prefix = plain_key[:11]

    api_key = create_api_key(
        db,
        key_hash=key_hash,
        key_prefix=key_prefix,
        name=body.name,
        role=body.role,
        created_by=user.user_id,
        expires_at=body.expires_at,
    )

    return CreateAPIKeyResponse(
        id=api_key.id,
        key=plain_key,
        name=api_key.name,
        role=api_key.role,
        expires_at=api_key.expires_at,
    )


@router.get("/api-keys", response_model=list[APIKeyInfo])
def list_keys(
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """List all API keys. Admin only. Secrets are never returned."""
    keys = list_api_keys(db)
    return [
        APIKeyInfo(
            id=k.id,
            key_prefix=k.key_prefix,
            name=k.name,
            role=k.role,
            is_active=k.is_active,
            expires_at=k.expires_at,
            created_at=k.created_at,
            last_used_at=k.last_used_at,
        )
        for k in keys
    ]


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_key(
    key_id: str,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Revoke an API key. Admin only."""
    from agent_runner_backend_v2.database.api_key_repository import get_api_key_by_id

    api_key = get_api_key_by_id(db, key_id)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")

    revoke_api_key(db, api_key)


# ── User Management (admin only) ──


VALID_ROLES = {"admin", "operator", "viewer"}


@router.get("/users", response_model=list[UserRoleResponse])
def list_all_users(
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """List all users with their roles. Admin only."""
    users = list_users(db)
    return [
        UserRoleResponse(
            user_id=u.user_id,
            email=u.email,
            role=u.role,
            is_system=u.is_system,
            created_at=u.created_at,
            updated_at=u.updated_at,
        )
        for u in users
    ]


@router.put("/users/{user_id}/role", response_model=UserRoleResponse)
def change_user_role(
    user_id: str,
    body: UpdateUserRoleRequest,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Update a user's role. Admin only."""
    if body.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{body.role}'. Must be one of: {sorted(VALID_ROLES)}",
        )
    updated = update_user_role(db, user_id, body.role)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return UserRoleResponse(
        user_id=updated.user_id,
        email=updated.email,
        role=updated.role,
        is_system=updated.is_system,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: str,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Remove a user from the user_roles table. Admin only. Does not delete the Supabase auth account.

    System accounts cannot be deleted.
    """
    from agent_runner_backend_v2.database.user_role_repository import is_system_user

    if is_system_user(db, user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete a system account")
    if not delete_user(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()


# ── User-Worker Assignment (admin only) ──


@router.get("/users/{user_id}/workers", response_model=list[str])
def get_user_workers(
    user_id: str,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Get the list of worker IDs assigned to a user. Admin only."""
    return get_user_worker_ids(db, user_id)


@router.put("/users/{user_id}/workers")
def set_user_workers_endpoint(
    user_id: str,
    body: SetUserWorkersRequest,
    user: UserContext = Depends(require_jwt_or_api_key("admin")),
    db: Session = Depends(get_db),
):
    """Set the list of worker IDs assigned to a user (replaces existing). Admin only."""
    result = set_user_workers(db, user_id, body.worker_ids)
    db.commit()
    return {"user_id": user_id, "worker_ids": result}
