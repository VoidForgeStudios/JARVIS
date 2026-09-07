from __future__ import annotations

import json

from app.brain.llm import LLMProvider, LLMRequest
from app.brain.prompts import build_system_prompt
from app.brain.router import IntentKind, IntentRouter
from app.core.events import Event, EventBus
from app.memory.parser import parse_forget, parse_remember
from app.memory.service import MemoryService
from app.text.session import TextSessionStore
from app.tools.dispatcher import ToolDispatcher


class TextService:
    """Text-only application service with tools and explicit persistent memory."""

    def __init__(self, provider: LLMProvider, settings, event_bus: EventBus, dispatcher: ToolDispatcher | None = None, memory: MemoryService | None = None) -> None:
        self.provider = provider
        self.router = IntentRouter()
        self.sessions = TextSessionStore()
        self.settings = settings
        self.system_prompt = build_system_prompt(settings)
        self.event_bus = event_bus
        self.dispatcher = dispatcher
        self.memory = memory

    async def _tool_request(self, text: str) -> str:
        lowered = text.lower()
        try:
            if lowered.startswith("calculate "):
                return await self.dispatcher.execute("calculator", expression=text[10:].strip())
            if lowered.startswith("read file "):
                return await self.dispatcher.execute("read_file", path=text[10:].strip())
            if lowered.startswith("find files"):
                pattern = text[len("find files"):].strip() or "*"
                return await self.dispatcher.execute("find_files", pattern=pattern)
            if lowered == "system info":
                result = await self.dispatcher.execute("system_info")
                return json.dumps(result, indent=2, sort_keys=True)
        except (FileNotFoundError, PermissionError, ValueError) as exc:
            return f"Tool request blocked: {exc}"
        return "That tool is not enabled in the text-only phase."

    async def _memory_request(self, text: str) -> str:
        if self.memory is None:
            return "Persistent memory is not configured."
        try:
            if text.lower().startswith("remember "):
                category, key, content = parse_remember(text)
                memory = self.memory.remember(category, key, content)
                await self.event_bus.publish(Event("memory.remembered", {"id": memory.id, "category": memory.category}))
                return f"Remembered {memory.key}."
            key = parse_forget(text)
            deleted = self.memory.forget(key)
            await self.event_bus.publish(Event("memory.forgotten", {"key": key, "deleted": deleted}))
            return f"Forgot {key}." if deleted else f"I had no saved memory for {key}."
        except ValueError as exc:
            return f"Memory request rejected: {exc}"

    async def chat(self, session_id: str, text: str) -> str:
        normalized = text.strip()
        if not normalized:
            return "I didn't catch a request."

        route = self.router.route(normalized)
        await self.event_bus.publish(Event("text.received", {"session_id": session_id, "intent": route.kind.value}))
        if route.kind is IntentKind.UNKNOWN:
            return "I didn't catch a request."
        if route.kind is IntentKind.MEMORY_REQUEST:
            return await self._memory_request(normalized)
        if route.kind is IntentKind.TOOL_REQUEST:
            if self.dispatcher is None:
                return "Tools are not configured for this runtime."
            return await self._tool_request(normalized)

        session = self.sessions.get_or_create(session_id)
        session.add_user(normalized)
        request = LLMRequest(
            messages=list(session.messages),
            system=self.system_prompt,
            model=self.settings.llm_model,
            temperature=self.settings.llm_temperature,
            max_tokens=self.settings.llm_max_tokens,
        )
        response = await self.provider.complete(request)
        session.add_assistant(response.text)
        await self.event_bus.publish(Event("text.responded", {"session_id": session_id, "provider": response.provider}))
        return response.text
