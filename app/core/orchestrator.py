from __future__ import annotations

from dataclasses import dataclass

from app.brain.llm import LLMProviderError
from app.brain.router import IntentKind, IntentRouter
from app.brain.service import Brain
from .events import Event, EventBus
from .permissions import PermissionManager


@dataclass(slots=True)
class OrchestratorResult:
    status: str
    response: str


class Orchestrator:
    """Coordinates routing and conversational LLM execution."""

    def __init__(self, event_bus: EventBus, permissions: PermissionManager, brain: Brain) -> None:
        self.event_bus = event_bus
        self.permissions = permissions
        self.brain = brain
        self.router = IntentRouter()

    async def handle_text(self, text: str) -> OrchestratorResult:
        normalized = text.strip()
        if not normalized:
            return OrchestratorResult("ignored", "I didn't catch a request.")
        await self.event_bus.publish(Event("request.received", {"text": normalized}))
        route = self.router.route(normalized)
        await self.event_bus.publish(Event("request.routed", {"intent": route.kind.value}))

        if route.kind is not IntentKind.CONVERSATION:
            return OrchestratorResult(
                "not_implemented",
                "I can route that request, but the required tool or memory capability is not implemented yet.",
            )

        try:
            response = await self.brain.respond(route.text)
        except LLMProviderError as exc:
            await self.event_bus.publish(Event("llm.error", {"error": str(exc)}))
            return OrchestratorResult("error", f"I couldn't reach the language model: {exc}")

        await self.event_bus.publish(
            Event("response.generated", {"provider": response.provider, "model": response.model})
        )
        return OrchestratorResult("ok", response.text)
