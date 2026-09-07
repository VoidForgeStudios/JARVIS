import pytest

from app.brain.providers import MockProvider
from app.core.events import EventBus
from app.core.config import Settings
from app.text.service import TextService


@pytest.mark.asyncio
async def test_text_session_keeps_context():
    settings = Settings(llm_provider="mock", llm_model="mock-1")
    service = TextService(MockProvider(), settings, EventBus())

    first = await service.chat("s1", "Hello")
    second = await service.chat("s1", "How are you?")

    assert first == "Mock response: Hello"
    assert second == "Mock response: How are you?"
    assert len(service.sessions.get_or_create("s1").messages) == 4


@pytest.mark.asyncio
async def test_non_conversation_capability_is_explicitly_unavailable():
    settings = Settings(llm_provider="mock", llm_model="mock-1")
    service = TextService(MockProvider(), settings, EventBus())

    response = await service.chat("s1", "open calculator")

    assert "not enabled" in response
