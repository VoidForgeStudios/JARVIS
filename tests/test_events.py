import pytest

from app.core.events import Event, EventBus


@pytest.mark.asyncio
async def test_event_bus_delivers_events() -> None:
    bus = EventBus()
    received = []

    async def handler(event: Event) -> None:
        received.append(event.payload["value"])

    bus.subscribe("test", handler)
    await bus.publish(Event("test", {"value": 42}))
    assert received == [42]
