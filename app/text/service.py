from __future__ import annotations

from app.brain.llm import ChatMessage, LLMRequest, LLMProvider
from app.brain.prompts import build_system_prompt
from app.brain.router import IntentKind, IntentRouter
from app.core.events import Event, EventBus
from app.text.session import TextSessionStore


class TextService:
    """Text-only application service. Voice and audio are deliberately out of scope."""

    def __init__(self, provider: LLMProvider, user_name: str, user_title: str,
                 response_style: str, event_bus: EventBus) -> None:
        self.provider = provider
        self.router = IntentRouter()
        self.sessions = TextSessionStore()
        self.system_prompt = build_system_prompt(user_name, user_title, response_style)
        self.event_bus = event_bus

    async def chat(self, session_id: str, text: str) -> str:
        normalized = text.strip()
        if not normalized:
            return "I didn't catch a request."

        route = self.router.route(normalized)
        await self.event_bus.publish(Event("text.received", {"session_id": session_id, "intent": route.kind.value}))

        if route.kind is IntentKind.UNKNOWN:
            return "I didn't catch a request."
        if route.kind is not IntentKind.CONVERSATION:
            return "That capability is not enabled in the text-only phase yet."

        session = self.sessions.get_or_create(session_id)
        session.add_user(normalized)
        request = LLMRequest(messages=list(session.messages), system=self.system_prompt)
        response = await self.provider.complete(request)
        session.add_assistant(response.text)
        await self.event_bus.publish(Event("text.responded", {"session_id": session_id, "provider": response.provider}))
        return response.text
