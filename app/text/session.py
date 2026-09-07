from __future__ import annotations

from dataclasses import dataclass, field

from app.brain.llm import ChatMessage


@dataclass(slots=True)
class TextSession:
    """In-memory conversation context for the text interface."""

    session_id: str
    messages: list[ChatMessage] = field(default_factory=list)

    def add_user(self, text: str) -> None:
        self.messages.append(ChatMessage("user", text))

    def add_assistant(self, text: str) -> None:
        self.messages.append(ChatMessage("assistant", text))


class TextSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, TextSession] = {}

    def get_or_create(self, session_id: str) -> TextSession:
        return self._sessions.setdefault(session_id, TextSession(session_id))

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
