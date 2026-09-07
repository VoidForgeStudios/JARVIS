import pytest

from app.brain.llm import ChatMessage, LLMRequest
from app.brain.providers import MockProvider
from app.brain.router import IntentKind, IntentRouter
from app.brain.service import Brain
from app.core.config import Settings


@pytest.mark.asyncio
async def test_mock_provider_is_deterministic():
    provider = MockProvider()
    result = await provider.complete(LLMRequest([ChatMessage("user", "Hello")]))
    assert result.provider == "mock"
    assert result.text == "Mock response: Hello"


def test_router_classifies_basic_requests():
    router = IntentRouter()
    assert router.route("remember my name").kind is IntentKind.MEMORY_REQUEST
    assert router.route("open Notepad").kind is IntentKind.TOOL_REQUEST
    assert router.route("How are you?").kind is IntentKind.CONVERSATION


@pytest.mark.asyncio
async def test_brain_uses_configured_personality():
    settings = Settings(llm_provider="mock", llm_model="mock-1", user_name="Alex")
    brain = Brain(MockProvider(), settings)
    result = await brain.respond("Test")
    assert result.text == "Mock response: Test"
