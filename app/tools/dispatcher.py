from __future__ import annotations

from typing import Any

from app.core.permissions import PermissionManager
from .registry import ToolRegistry


class ToolDispatcher:
    """Executes registered tools only after the central permission policy authorizes them."""

    def __init__(self, registry: ToolRegistry, permissions: PermissionManager) -> None:
        self.registry = registry
        self.permissions = permissions

    async def execute(self, name: str, *, confirmed: bool = False, **kwargs: Any) -> Any:
        tool = self.registry.get(name)
        if not await self.permissions.authorize(tool.spec.permission_level, confirmed=confirmed):
            raise PermissionError(f"Tool '{name}' requires explicit confirmation.")
        return await tool.execute(**kwargs)
