from __future__ import annotations

from fastapi import FastAPI

from app.brain.providers import build_provider
from app.core.config import Settings
from app.core.events import EventBus
from app.text.api import TextAPI
from app.text.service import TextService


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    event_bus = EventBus()
    provider = build_provider(settings)
    service = TextService(provider, settings, event_bus)

    app = FastAPI(title=settings.app_name, version="0.3.0")
    app.include_router(TextAPI(service).router())

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "mode": "text-only", "provider": provider.name}

    return app
