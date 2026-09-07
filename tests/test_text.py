import pytest

from app.brain.providers import MockProvider
from app.core.config import Settings
from app.core.events import EventBus
from app.core.permissions import PermissionManager
from app.text.service import TextService
from app.tools.calculator import CalculatorTool
from app.tools.dispatcher import ToolDispatcher
from app.tools.filesystem import DataFileTool, FindDataFilesTool
from app.tools.registry import ToolRegistry
from app.tools.system import SystemInfoTool


def build_service(tmp_path):
    settings = Settings(llm_provider="mock", llm_model="mock-1", data_dir=tmp_path)
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(DataFileTool(tmp_path))
    registry.register(FindDataFilesTool(tmp_path))
    registry.register(SystemInfoTool())
    dispatcher = ToolDispatcher(registry, PermissionManager(True))
    return TextService(MockProvider(), settings, EventBus(), dispatcher)


@pytest.mark.asyncio
async def test_text_session_keeps_context(tmp_path):
    service = build_service(tmp_path)
    first = await service.chat("s1", "Hello")
    second = await service.chat("s1", "How are you?")
    assert first == "Mock response: Hello"
    assert second == "Mock response: How are you?"
    assert len(service.sessions.get_or_create("s1").messages) == 4


@pytest.mark.asyncio
async def test_calculator_tool_works_from_text(tmp_path):
    service = build_service(tmp_path)
    assert await service.chat("s1", "calculate 6 * 7") == "42"


@pytest.mark.asyncio
async def test_file_tool_is_sandboxed(tmp_path):
    (tmp_path / "note.txt").write_text("hello", encoding="utf-8")
    service = build_service(tmp_path)
    assert await service.chat("s1", "read file note.txt") == "hello"
