from __future__ import annotations

from dataclasses import dataclass

from .events import Event, EventBus
from .permissions import PermissionManager


@dataclass(slots=True)
class OrchestratorResult:
    status: str
    response: str


class Orchestrator:
    """Coordinates future router/LLM/tool execution without pretending those modules exist."""

    def __init__(self, event_bus: EventBus, permissions: PermissionManager) -> None:
        self.event_bus = event_bus
        self.permissions = permissions

    async def handle_text(self, text: str) -> OrchestratorResult:
        normalized = text.strip()
        if not normalized:
            return OrchestratorResult("ignored", "I didn't catch a request.")
        await self.event_bus.publish(Event("request.received", {"text": normalized}))
        return OrchestratorResult(
            "not_implemented",
            "The JARVIS foundation is online, but that capability has not been implemented yet.",
        )
