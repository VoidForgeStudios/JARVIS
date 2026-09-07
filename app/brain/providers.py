from __future__ import annotations

from .llm import (
    ChatMessage,
    LLMConfigurationError,
    LLMProviderError,
    LLMRequest,
    LLMRequestError,
    LLMResponse,
)


class MockProvider:
    """Deterministic offline provider for development and tests."""

    name = "mock"

    def __init__(self, model: str = "mock-1") -> None:
        self.model = model

    async def complete(self, request: LLMRequest) -> LLMResponse:
        last = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
        text = f"Mock response: {last}" if last else "Mock provider is online."
        return LLMResponse(text=text, model=request.model or self.model, provider=self.name)


class AnthropicProvider:
    """Claude adapter. The SDK is imported lazily so offline mode remains usable."""

    name = "anthropic"

    def __init__(self, api_key: str | None, default_model: str) -> None:
        if not api_key:
            raise LLMConfigurationError("Anthropic API key is not configured.")
        if not default_model:
            raise LLMConfigurationError("An Anthropic model must be configured.")
        self.api_key = api_key
        self.default_model = default_model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
            except ImportError as exc:
                raise LLMConfigurationError(
                    "The Anthropic SDK is not installed. Install the project with the llm extra."
                ) from exc
            self._client = AsyncAnthropic(api_key=self.api_key)
        return self._client

    async def complete(self, request: LLMRequest) -> LLMResponse:
        messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
            if m.role in {"user", "assistant"}
        ]
        try:
            result = await self._get_client().messages.create(
                model=request.model or self.default_model,
                max_tokens=request.max_tokens,
                system=request.system or "",
                messages=messages,
                **({"temperature": request.temperature} if request.temperature is not None else {}),
            )
        except Exception as exc:
            raise LLMRequestError(f"Anthropic request failed: {exc}") from exc

        text = "".join(block.text for block in result.content if getattr(block, "type", None) == "text")
        usage = getattr(result, "usage", None)
        return LLMResponse(
            text=text,
            model=result.model,
            provider=self.name,
            input_tokens=getattr(usage, "input_tokens", None),
            output_tokens=getattr(usage, "output_tokens", None),
            stop_reason=getattr(result, "stop_reason", None),
        )


def build_provider(settings):
    provider = settings.llm_provider.lower().strip()
    if provider == "mock":
        return MockProvider(settings.llm_model or "mock-1")
    if provider == "anthropic":
        return AnthropicProvider(settings.anthropic_api_key, settings.llm_model)
    raise LLMConfigurationError(f"Unsupported LLM provider: {provider}")
