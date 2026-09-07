# JARVIS text-only mode

Phase 3 is intentionally text-only. No microphone, wake word, VAD, STT, or TTS dependencies are introduced.

## HTTP API

Run the application with:

```powershell
uvicorn app.text.server:create_app --factory --host 127.0.0.1 --port 8000
```

Health:

`GET /health`

Chat:

`POST /api/text/chat`

Example JSON:

```json
{"session_id":"default","message":"Hello JARVIS"}
```

Clear a session:

`DELETE /api/text/sessions/{session_id}`

The default provider is the deterministic mock provider. To use Claude, configure `JARVIS_LLM_PROVIDER=anthropic`, `JARVIS_LLM_MODEL`, and `JARVIS_ANTHROPIC_API_KEY` locally.

## Scope

Implemented: text input, session context, routing, provider abstraction, responses, HTTP health/chat endpoints.

Not implemented: voice/audio, computer control, memory persistence, browser automation, background agents, proactive behaviour.
