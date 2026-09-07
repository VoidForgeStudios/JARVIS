from __future__ import annotations

from enum import IntEnum


class PermissionLevel(IntEnum):
    SAFE = 0
    NORMAL = 1
    DESTRUCTIVE = 2
    CRITICAL = 3


class PermissionManager:
    """Policy gate; model/tool code cannot bypass this decision point."""

    def __init__(self, require_confirmation_for_destructive: bool = True) -> None:
        self.require_confirmation_for_destructive = require_confirmation_for_destructive

    def requires_confirmation(self, level: PermissionLevel) -> bool:
        return self.require_confirmation_for_destructive and level >= PermissionLevel.DESTRUCTIVE

    async def authorize(self, level: PermissionLevel, *, confirmed: bool = False) -> bool:
        if not self.requires_confirmation(level):
            return True
        return confirmed
