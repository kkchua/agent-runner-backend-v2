"""Navigation/menu configuration and endpoint.

Menu structure is hardcoded per application. Each menu item specifies which roles
can see it. The /api/auth/navigation endpoint returns the filtered menu tree
based on the current user's role.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from fastapi import Depends

from agent_runner_backend_v2.auth.supabase_auth import UserContext, get_current_user


@dataclass
class MenuItem:
    """A single navigation menu item."""

    id: str
    label: str
    icon: str
    path: str
    required_roles: list[str]
    children: list[MenuItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict, recursively converting children."""
        result = {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "path": self.path,
            "required_roles": self.required_roles,
        }
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result


# ── Menu configuration for agent-runner-platform ──

AGENT_RUNNER_MENU: list[MenuItem] = [
    MenuItem(
        id="runs",
        label="Active Runs",
        icon="Play",
        path="/",
        required_roles=["admin", "operator", "viewer"],
    ),
    MenuItem(
        id="history",
        label="History",
        icon="LayoutDashboard",
        path="/history",
        required_roles=["admin", "operator", "viewer"],
    ),
    MenuItem(
        id="submit",
        label="Submit Job",
        icon="Play",
        path="/submit",
        required_roles=["admin", "operator"],
    ),
    MenuItem(
        id="workflows",
        label="Workflows",
        icon="GitBranch",
        path="/workflows",
        required_roles=["admin", "operator"],
    ),
    MenuItem(
        id="workers",
        label="Workers",
        icon="Server",
        path="/workers",
        required_roles=["admin", "operator"],
    ),
    MenuItem(
        id="hosts",
        label="Hosts",
        icon="Monitor",
        path="/hosts",
        required_roles=["admin"],
    ),
    MenuItem(
        id="repos",
        label="Repositories",
        icon="FolderGit",
        path="/repos",
        required_roles=["admin"],
    ),
    MenuItem(
        id="users",
        label="Users & Roles",
        icon="Users",
        path="/users",
        required_roles=["admin"],
    ),
]

# Registry of app_id → menu items
# Add new apps here as they are onboarded
APP_MENUS: dict[str, list[MenuItem]] = {
    "agent-runner": AGENT_RUNNER_MENU,
}


def _filter_menu(items: list[MenuItem], user_role: str) -> list[dict]:
    """Filter menu items based on user role, recursively."""
    result = []
    for item in items:
        if user_role in item.required_roles:
            entry = item.to_dict()
            if item.children:
                entry["children"] = _filter_menu(item.children, user_role)
            result.append(entry)
    return result


def get_navigation(
    app_id: str = "agent-runner",
    user: UserContext = Depends(get_current_user),
) -> list[dict]:
    """Return the navigation menu filtered by the user's role.

    Query parameter `app_id` selects which app's menu to return.
    """
    menu = APP_MENUS.get(app_id)
    if menu is None:
        return []
    return _filter_menu(menu, user.role)
