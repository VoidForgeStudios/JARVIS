import pytest

from app.core.permissions import PermissionLevel, PermissionManager


@pytest.mark.asyncio
async def test_safe_actions_do_not_require_confirmation() -> None:
    manager = PermissionManager(True)
    assert await manager.authorize(PermissionLevel.SAFE)


@pytest.mark.asyncio
async def test_destructive_actions_require_confirmation() -> None:
    manager = PermissionManager(True)
    assert not await manager.authorize(PermissionLevel.DESTRUCTIVE)
    assert await manager.authorize(PermissionLevel.DESTRUCTIVE, confirmed=True)
