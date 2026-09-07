from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


Handler = Callable[[Event], Awaitable[None]]


class EventBus:
    """Small in-process async pub/sub bus used to decouple runtime modules."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Handler) -> None:
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Handler) -> None:
        if handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)

    async def publish(self, event: Event) -> None:
        handlers = tuple(self._handlers.get(event.name, ()))
        if not handlers:
            return
        results = await asyncio.gather(*(handler(event) for handler in handlers), return_exceptions=True)
        errors = [result for result in results if isinstance(result, Exception)]
        if errors:
            raise RuntimeError(f"{len(errors)} event handler(s) failed") from errors[0]
