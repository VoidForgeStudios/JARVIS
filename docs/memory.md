# Persistent memory

Phase 4 introduces explicit, local persistent memory.

## Storage

Memory is stored in SQLite at `<data_dir>/jarvis_memory.db` and managed with SQLAlchemy. The database is local to the configured JARVIS data directory.

## Privacy model

JARVIS does not automatically persist normal conversation. Memory is created only through an explicit `remember` request or a future feature that obtains an equivalent explicit user approval.

`forget <key>` removes matching saved memory. Updating an existing key replaces its content instead of creating unbounded duplicates.

## Retrieval

The current implementation uses simple SQLite text matching across memory keys and content. This is intentionally modest; semantic/vector retrieval can be introduced later without changing the memory service contract.

## Categories

- USER_PROFILE
- PREFERENCES
- PEOPLE
- PROJECTS
- DEVICES
- LOCATIONS
- ROUTINES
- CONVERSATIONS
- TASKS
- IMPORTANT_FACTS

## Examples

```text
remember PREFERENCES coffee = black
remember PROJECTS jarvis = build the assistant in phases
forget coffee
```
