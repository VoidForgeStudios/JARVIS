from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IntentKind(StrEnum):
    CONVERSATION = "conversation"
    TOOL_REQUEST = "tool_request"
    MEMORY_REQUEST = "memory_request"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Route:
    kind: IntentKind
    text: str


class IntentRouter:
    """Small deterministic router; richer classification belongs in later phases."""

    def route(self, text: str) -> Route:
        normalized = text.strip()
        lowered = normalized.lower()
        if not normalized:
            return Route(IntentKind.UNKNOWN, normalized)
        if lowered.startswith(("remember ", "forget ")):
            return Route(IntentKind.MEMORY_REQUEST, normalized)
        if lowered.startswith(("open ", "close ", "search ", "run ", "click ", "type ")):
            return Route(IntentKind.TOOL_REQUEST, normalized)
        return Route(IntentKind.CONVERSATION, normalized)
