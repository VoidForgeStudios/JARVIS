from __future__ import annotations

from .llm import ChatMessage, LLMProvider, LLMRequest, LLMResponse
from .prompts import build_system_prompt


class Brain:
    """Provider-neutral conversational brain. Tools and memory plug in around this boundary."""

    def __init__(self, provider: LLMProvider, settings) -> None:
        self.provider = provider
        self.settings = settings

    async def respond(self, text: str, history: list[ChatMessage] | None = None) -> LLMResponse:
        messages = list(history or [])
        messages.append(ChatMessage(role="user", content=text))
        request = LLMRequest(
            messages=messages,
            system=build_system_prompt(self.settings),
            model=self.settings.llm_model or None,
            max_tokens=self.settings.llm_max_tokens,
            temperature=self.settings.llm_temperature,
        )
        return await self.provider.complete(request)
