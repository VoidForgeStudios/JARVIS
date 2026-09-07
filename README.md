# JARVIS

**JUST A RATHER VERY INTELLIGENT SYSTEM**

A modular, voice-first personal AI assistant for Windows 11 first, with future macOS/Linux portability. The project is intentionally built in phases so every layer remains testable and replaceable.

## Current status: Phase 1 — foundation

Implemented:

- Typed runtime configuration via Pydantic Settings.
- Async in-process event bus.
- Central permission model with safe/normal/destructive/critical levels.
- Explicit tool specification and registry.
- Orchestrator skeleton with honest `not_implemented` responses.
- Runnable terminal interface (`help`, `status`, `exit`).
- Structured console logging.
- Foundational pytest coverage.
- Architecture and security boundaries documented.

Not yet implemented: voice I/O, LLM provider calls, browser/computer control, memory, agents, web research, vision, smart home, telemetry HUD, reminders, and proactive behavior.

## Development

Requires Python 3.12+.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m app.main
pytest
```

If PowerShell execution policy blocks activation, run the module with the virtual environment's Python directly instead.

## Configuration

Runtime settings use the `JARVIS_` environment prefix. Secrets belong only in local `.env` files or a future secret manager; never commit credentials.

## Design principles

1. **Modular:** providers and tools are replaceable.
2. **Permission-first:** the model cannot bypass destructive-action confirmation.
3. **Observable:** log state and tool activity without exposing private chain-of-thought.
4. **Honest:** unavailable capabilities return explicit not-implemented states.
5. **Interruptible:** later voice/task layers must support cancellation.
6. **Local-first where practical:** computer, files and telemetry should remain under explicit user control.

See [`docs/architecture.md`](docs/architecture.md) for the current boundary map.
