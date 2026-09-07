# JARVIS

**JUST A RATHER VERY INTELLIGENT SYSTEM**

A modular, text-first personal AI assistant for Windows 11 first, with future voice and macOS/Linux portability. The project is intentionally built in phases so every layer remains testable and replaceable.

## Current status: text-first Phase 3

Implemented:

- Typed runtime configuration via Pydantic Settings.
- Async in-process event bus.
- Central permission model with safe/normal/destructive/critical levels.
- Explicit tool specification, registry, and permission-gated dispatcher.
- Provider-neutral LLM interface with offline mock provider and optional Anthropic/Claude adapter.
- Configurable JARVIS personality and response style.
- Text conversation sessions.
- HTTP text API with health endpoint.
- Safe calculator tool using a restricted AST evaluator.
- Sandboxed file reading/search limited to the configured JARVIS data directory.
- Basic local system information tool.
- Terminal text interface.
- Tests for tool safety, filesystem boundaries, permissions, and text sessions.

Not yet implemented: microphone, wake word, VAD, STT/TTS, browser automation, unrestricted computer control, persistent memory, background agents, web research, vision, smart-home integration, telemetry HUD, reminders, and proactive behavior.

## Text commands

The terminal and HTTP text service support conversational input plus:

```text
calculate 6 * 7
system info
find files *.txt
read file notes/example.txt
```

File operations are restricted to the configured `JARVIS_DATA_DIR`/`data_dir`. There is no unrestricted shell execution in this phase.

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

For the optional Claude adapter:

```powershell
python -m pip install -e ".[llm]"
$env:JARVIS_LLM_PROVIDER="anthropic"
$env:JARVIS_LLM_MODEL="<configured-model>"
$env:JARVIS_ANTHROPIC_API_KEY="<local-secret>"
```

Never commit real credentials.

## Design principles

1. **Modular:** providers and tools are replaceable.
2. **Permission-first:** the model cannot bypass destructive-action confirmation.
3. **Observable:** log state and tool activity without exposing private chain-of-thought.
4. **Honest:** unavailable capabilities return explicit not-implemented states.
5. **Local-first:** filesystem and system inspection stay under explicit application boundaries.
6. **No unrestricted shell:** command execution will require a later, separately designed permission layer.

See `docs/architecture.md` for the boundary map.
