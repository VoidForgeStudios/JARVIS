from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

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

    app = FastAPI(title=settings.app_name, version="0.5.0")

    origins = settings.allowed_cors_origins()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type"],
        )

    api_token = settings.api_token.get_secret_value() if settings.api_token else None

    @app.middleware("http")
    async def protect_api(request: Request, call_next):
        # Local-only deployments may leave the token unset. Any remotely exposed
        # deployment should set JARVIS_API_TOKEN.
        if api_token and request.url.path.startswith("/api/"):
            authorization = request.headers.get("Authorization", "")
            if authorization != f"Bearer {api_token}":
                return await _json_error(401, "Invalid or missing API token")
        return await call_next(request)

    app.include_router(TextAPI(service).router())

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "mode": "text-only",
            "provider": provider.name,
            "auth": "token" if api_token else "none",
        }

    return app


async def _json_error(status_code: int, detail: str):
    from fastapi.responses import JSONResponse

    return JSONResponse(status_code=status_code, content={"detail": detail})
