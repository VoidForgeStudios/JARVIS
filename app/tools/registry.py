from __future__ import annotations

from typing import Any

from .base import Tool


class ToolRegistry:
    """Explicit registry for tools exposed to the orchestrator/LLM layer."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        name = tool.spec.name
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.spec.name,
                "description": tool.spec.description,
                "parameters": tool.spec.parameters,
                "permission_level": int(tool.spec.permission_level),
            }
            for tool in self._tools.values()
        ]
