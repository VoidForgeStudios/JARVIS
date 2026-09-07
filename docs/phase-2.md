# Phase 2 — Brain and Provider Abstraction

Phase 2 introduces a provider-neutral language-model boundary without coupling the rest of JARVIS to a vendor SDK.

## Components

- `app/brain/llm.py` — request/response contracts and provider errors.
- `app/brain/providers.py` — deterministic offline mock plus lazy Anthropic adapter.
- `app/brain/prompts.py` — configurable JARVIS personality/system prompt.
- `app/brain/router.py` — deterministic intent routing scaffold.
- `app/brain/service.py` — `Brain` service that constructs LLM requests.
- `app/core/orchestrator.py` — routes conversational requests into `Brain` and emits lifecycle events.

## Provider selection

Development defaults to `mock` so a fresh checkout does not require network access or secrets.
Set `JARVIS_LLM_PROVIDER=anthropic`, `JARVIS_LLM_MODEL=<model>`, and
`JARVIS_ANTHROPIC_API_KEY=<secret>` locally to use Claude.

Secrets belong in `.env` or an external secret manager and must never be committed.

## Explicit non-goals

Phase 2 does not yet implement tool calling, memory retrieval, voice I/O, streaming, or autonomous agents.
Those capabilities will plug into the same orchestration boundary in later phases.
