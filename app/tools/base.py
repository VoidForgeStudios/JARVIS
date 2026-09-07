from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from app.core.permissions import PermissionLevel


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    permission_level: PermissionLevel = PermissionLevel.NORMAL


class Tool(Protocol):
    @property
    def spec(self) -> ToolSpec: ...

    async def execute(self, **kwargs: Any) -> Any: ...
