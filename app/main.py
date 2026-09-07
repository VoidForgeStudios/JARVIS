from __future__ import annotations

import asyncio

from app.brain.providers import build_provider
from app.brain.service import Brain
from app.core.config import Settings
from app.core.events import EventBus
from app.core.logging import configure_logging
from app.core.orchestrator import Orchestrator
from app.core.permissions import PermissionManager
from app.tools.registry import ToolRegistry


def build_runtime() -> tuple[Settings, EventBus, Orchestrator, ToolRegistry]:
    settings = Settings()
    settings.ensure_data_dir()
    configure_logging(settings.log_level)
    event_bus = EventBus()
    permissions = PermissionManager(settings.require_confirmation_for_destructive)
    registry = ToolRegistry()
    provider = build_provider(settings)
    brain = Brain(provider, settings)
    orchestrator = Orchestrator(event_bus, permissions, brain)
    return settings, event_bus, orchestrator, registry


async def run_terminal() -> None:
    settings, _, orchestrator, registry = build_runtime()
    print(f"{settings.app_name} foundation online. provider={settings.llm_provider}")
    print("Type 'help' for commands; type 'exit' to quit.")
    while True:
        try:
            text = await asyncio.to_thread(input, "JARVIS> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        command = text.strip()
        if command.lower() in {"exit", "quit"}:
            break
        if command.lower() == "help":
            print("Commands: help, status, exit")
            continue
        if command.lower() == "status":
            print(f"status=online tools={len(registry.names())} provider={settings.llm_provider} data_dir={settings.data_dir}")
            continue
        result = await orchestrator.handle_text(command)
        print(result.response)


def main() -> None:
    asyncio.run(run_terminal())


if __name__ == "__main__":
    main()
