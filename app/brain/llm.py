from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence


@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class LLMRequest:
    messages: Sequence[ChatMessage]
    system: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int = 1024
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class LLMResponse:
    text: str
    model: str
    provider: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    stop_reason: str | None = None


class LLMProvider(Protocol):
    name: str

    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Return one assistant response for a normalized request."""


class LLMProviderError(RuntimeError):
    """Base error for provider failures exposed to the orchestrator."""


class LLMConfigurationError(LLMProviderError):
    """Raised when a provider cannot be used because configuration is missing."""


class LLMRequestError(LLMProviderError):
    """Raised when a provider rejects a request."""
