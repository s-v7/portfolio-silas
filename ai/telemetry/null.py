from __future__ import annotations

from ai.telemetry.events import TelemetryEvent


class NullTelemetry:
    def emit(self, event: TelemetryEvent) -> None:
        del event
