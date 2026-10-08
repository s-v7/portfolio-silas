from __future__ import annotations

from typing import Protocol

from ai.telemetry.events import TelemetryEvent


class Telemetry(Protocol):
    def emit(self, event: TelemetryEvent) -> None: ...
