# JARVIS

**JUST A RATHER VERY INTELLIGENT SYSTEM**

A modular, text-first personal AI assistant for Windows 11 first, with future macOS/Linux portability. The project is intentionally built in phases so every layer remains testable and replaceable.

## Current status: Phase 4 — persistent memory

Implemented:

- Typed runtime configuration via Pydantic Settings.
- Async in-process event bus.
- Central permission model with safe/normal/destructive/critical levels.
- Explicit tool specification and registry.
- Safe text tools: calculator, sandboxed file access/search, and system information.
- Provider-neutral LLM contracts with offline mock and optional Anthropic adapter.
- Text sessions with conversational context.
- SQLite persistent memory using SQLAlchemy.
- Explicit `remember` and `forget` commands.
- Memory categories and keyword retrieval.
- Memory tests and safety boundaries.

### Memory commands

Memory is **not** saved automatically. The user must explicitly request it.

```text
remember PREFERENCES coffee = black
remember PROJECTS jarvis = build the assistant in phases
forget coffee
```

Supported categories: `USER_PROFILE`, `PREFERENCES`, `PEOPLE`, `PROJECTS`, `DEVICES`, `LOCATIONS`, `ROUTINES`, `CONVERSATIONS`, `TASKS`, `IMPORTANT_FACTS`.

The SQLite database is created as `data/jarvis_memory.db` by default. Keep the `data/` directory private and never commit its contents.

## Development

Requires Python 3.12+.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.text.server:create_app --factory --host 127.0.0.1 --port 8000
pytest
```

## Configuration

Runtime settings use the `JARVIS_` environment prefix. Secrets belong only in local `.env` files or a future secret manager; never commit credentials.

## Design principles

1. **Modular:** providers and tools are replaceable.
2. **Permission-first:** the model cannot bypass destructive-action confirmation.
3. **Explicit memory:** JARVIS never silently persists personal information.
4. **Observable:** log state and tool activity without exposing private chain-of-thought.
5. **Honest:** unavailable capabilities return explicit not-implemented states.
6. **Local-first where practical:** computer, files, memory and telemetry remain under explicit user control.

Not yet implemented: voice I/O, wake word/VAD/STT/TTS, browser automation, unrestricted computer control, shell execution, semantic/vector memory, autonomous agents, vision, smart home, telemetry HUD, reminders, and proactive behavior.

See [`docs/architecture.md`](docs/architecture.md) and [`docs/text-mode.md`](docs/text-mode.md) for current boundaries.
