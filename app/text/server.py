from __future__ import annotations

from fastapi import FastAPI

from app.brain.providers import build_provider
from app.core.config import Settings
from app.core.events import EventBus
from app.core.permissions import PermissionManager
from app.text.api import TextAPI
from app.text.service import TextService
from app.tools.calculator import CalculatorTool
from app.tools.dispatcher import ToolDispatcher
from app.tools.filesystem import DataFileTool, FindDataFilesTool
from app.tools.registry import ToolRegistry
from app.tools.system import SystemInfoTool


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    settings.ensure_data_dir()
    event_bus = EventBus()
    permissions = PermissionManager(settings.require_confirmation_for_destructive)
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(DataFileTool(settings.data_dir))
    registry.register(FindDataFilesTool(settings.data_dir))
    registry.register(SystemInfoTool())
    dispatcher = ToolDispatcher(registry, permissions)
    provider = build_provider(settings)
    service = TextService(provider, settings, event_bus, dispatcher)

    app = FastAPI(title=settings.app_name, version="0.4.0")
    app.include_router(TextAPI(service).router())

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "mode": "text-only", "provider": provider.name}

    return app
