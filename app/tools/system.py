from __future__ import annotations

import os
import platform
from typing import Any

from app.core.permissions import PermissionLevel

from .base import ToolSpec


class SystemInfoTool:
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="system_info",
            description="Return basic non-sensitive local operating-system and runtime information.",
            parameters={},
            permission_level=PermissionLevel.SAFE,
        )

    async def execute(self) -> dict[str, Any]:
        return {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "cpu_count": os.cpu_count(),
        }
