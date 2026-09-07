from __future__ import annotations

from typing import Any

from app.memory.models import MemoryCategory
from app.memory.service import MemoryService
from app.tools.base import ToolSpec


class RememberTool:
    def __init__(self, memory: MemoryService) -> None:
        self.memory = memory
        self.spec = ToolSpec(
            "remember", "Persist an explicitly supplied memory.",
            {"category": "Memory category", "key": "Stable memory key", "content": "Memory content"},
        )

    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        category = MemoryCategory(kwargs["category"].upper())
        memory = self.memory.remember(category, kwargs["key"], kwargs["content"])
        return {"status": "remembered", "id": memory.id, "category": memory.category, "key": memory.key}


class ForgetTool:
    def __init__(self, memory: MemoryService) -> None:
        self.memory = memory
        self.spec = ToolSpec("forget", "Delete an explicitly requested memory.", {"key": "Memory key"})

    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        count = self.memory.forget(kwargs["key"])
        return {"status": "forgotten", "deleted": count}


class MemorySearchTool:
    def __init__(self, memory: MemoryService) -> None:
        self.memory = memory
        self.spec = ToolSpec("memory_search", "Search saved memories.", {"query": "Search terms"})

    async def execute(self, **kwargs: Any) -> list[dict[str, Any]]:
        return [
            {"id": m.id, "category": m.category, "key": m.key, "content": m.content}
            for m in self.memory.search(kwargs["query"])
        ]
