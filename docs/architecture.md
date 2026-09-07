# JARVIS architecture

JARVIS is designed as a modular, voice-first personal assistant. Phase 1 deliberately implements only the runtime foundation.

```text
Input (future voice / typed)
        |
        v
Wake word -> VAD -> STT -> Router -> Orchestrator -> LLM
                                             |
                                             v
                                      PermissionManager
                                             |
                                             v
                                        Tool Registry
                                             |
                                             v
                                   Observation / result
                                             |
                                  Memory + TTS + HUD
```

## Boundaries

- `core/`: configuration, events, permissions, orchestration and logging.
- `tools/`: explicit tool contracts and registry; tools are not unrestricted shell access.
- `voice/`, `brain/`, `agents/`, `memory/`, `integrations/`, `ui/`: reserved for later phases.
- `tests/`: contract tests for foundational behavior.

## Safety model

Every executable tool declares a `PermissionLevel`. Destructive and critical actions are confirmation-gated by the central `PermissionManager`; future LLM/tool code must not implement its own bypass.

## Phase 1 non-goals

No real microphone, wake word, STT/TTS, LLM calls, browser automation, computer control, persistent memory, background agents, smart-home integration, or HUD are claimed as implemented yet.
