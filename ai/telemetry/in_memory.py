from __future__ import annotations

from threading import Lock

from ai.telemetry.events import TelemetryEvent


class InMemoryTelemetry:
    def __init__(self) -> None:
        self._events: list[TelemetryEvent] = []
        self._lock = Lock()

    @property
    def events(self) -> tuple[TelemetryEvent, ...]:
        with self._lock:
            return tuple(self._events)

    def emit(self, event: TelemetryEvent) -> None:
        with self._lock:
            self._events.append(event)
