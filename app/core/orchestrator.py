from __future__ import annotations

from dataclasses import dataclass

from app.brain.llm import LLMProviderError
from app.brain.router import IntentKind, IntentRouter
from app.brain.service import Brain
from app.tools.dispatcher import ToolDispatcher
from .events import Event, EventBus
from .permissions import PermissionManager


@dataclass(slots=True)
class OrchestratorResult:
    status: str
    response: str


class Orchestrator:
    """Coordinates routing, safe tools, and conversational LLM execution."""

    def __init__(self, event_bus: EventBus, permissions: PermissionManager, brain: Brain,
                 dispatcher: ToolDispatcher | None = None) -> None:
        self.event_bus = event_bus
        self.permissions = permissions
        self.brain = brain
        self.router = IntentRouter()
        self.dispatcher = dispatcher

    async def _execute_tool_request(self, text: str) -> str:
        if self.dispatcher is None:
            return "Tools are not configured for this runtime."
        lowered = text.lower()
        try:
            if lowered.startswith("calculate "):
                return await self.dispatcher.execute("calculator", expression=text[10:].strip())
            if lowered.startswith("read file "):
                return await self.dispatcher.execute("read_file", path=text[10:].strip())
            if lowered.startswith("find files"):
                return await self.dispatcher.execute("find_files", pattern=text[len("find files"):].strip() or "*")
            if lowered == "system info":
                return str(await self.dispatcher.execute("system_info"))
        except (FileNotFoundError, PermissionError, ValueError) as exc:
            return f"Tool request blocked: {exc}"
        return "That tool is not enabled in the text-only phase."

    async def handle_text(self, text: str) -> OrchestratorResult:
        normalized = text.strip()
        if not normalized:
            return OrchestratorResult("ignored", "I didn't catch a request.")
        await self.event_bus.publish(Event("request.received", {"text": normalized}))
        route = self.router.route(normalized)
        await self.event_bus.publish(Event("request.routed", {"intent": route.kind.value}))

        if route.kind is IntentKind.TOOL_REQUEST:
            return OrchestratorResult("tool", await self._execute_tool_request(normalized))
        if route.kind is not IntentKind.CONVERSATION:
            return OrchestratorResult("not_implemented", "That capability is not enabled yet.")

        try:
            response = await self.brain.respond(route.text)
        except LLMProviderError as exc:
            await self.event_bus.publish(Event("llm.error", {"error": str(exc)}))
            return OrchestratorResult("error", f"I couldn't reach the language model: {exc}")

        await self.event_bus.publish(
            Event("response.generated", {"provider": response.provider, "model": response.model})
        )
        return OrchestratorResult("ok", response.text)
