import pytest

from app.core.events import EventBus
from app.core.orchestrator import Orchestrator
from app.core.permissions import PermissionManager


@pytest.mark.asyncio
async def test_orchestrator_handles_empty_text() -> None:
    orchestrator = Orchestrator(EventBus(), PermissionManager())
    result = await orchestrator.handle_text("   ")
    assert result.status == "ignored"


@pytest.mark.asyncio
async def test_orchestrator_marks_future_capabilities_unimplemented() -> None:
    orchestrator = Orchestrator(EventBus(), PermissionManager())
    result = await orchestrator.handle_text("open my browser")
    assert result.status == "not_implemented"
