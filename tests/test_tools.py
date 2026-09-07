import pytest

from app.core.permissions import PermissionManager
from app.tools.calculator import CalculatorTool
from app.tools.dispatcher import ToolDispatcher
from app.tools.filesystem import DataFileTool
from app.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_calculator_does_not_execute_code() -> None:
    tool = CalculatorTool()
    assert await tool.execute(expression="2 + 3 * 4") == "14"
    with pytest.raises(ValueError):
        await tool.execute(expression="__import__('os').getcwd()")


@pytest.mark.asyncio
async def test_dispatcher_enforces_permission_policy(tmp_path) -> None:
    registry = ToolRegistry()
    registry.register(DataFileTool(tmp_path))
    dispatcher = ToolDispatcher(registry, PermissionManager(True))
    (tmp_path / "note.txt").write_text("hello", encoding="utf-8")
    assert await dispatcher.execute("read_file", path="note.txt") == "hello"


@pytest.mark.asyncio
async def test_filesystem_tool_blocks_path_escape(tmp_path) -> None:
    tool = DataFileTool(tmp_path)
    with pytest.raises(PermissionError):
        await tool.execute(path="../outside.txt")
