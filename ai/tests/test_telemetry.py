from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest

from ai.telemetry import InMemoryTelemetry, NullTelemetry, TelemetryEvent


def test_event_defaults_attributes_and_timestamp() -> None:
    event = TelemetryEvent(name="node.started")

    assert event.attributes == {}
    assert event.timestamp > 0


def test_event_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        TelemetryEvent(name="  ")


def test_in_memory_records_events_in_order() -> None:
    telemetry = InMemoryTelemetry()

    telemetry.emit(TelemetryEvent(name="workflow.started"))
    telemetry.emit(TelemetryEvent(name="workflow.completed"))

    assert tuple(event.name for event in telemetry.events) == (
        "workflow.started",
        "workflow.completed",
    )


def test_events_snapshot_is_not_affected_by_later_emits() -> None:
    telemetry = InMemoryTelemetry()
    telemetry.emit(TelemetryEvent(name="first"))

    snapshot = telemetry.events
    telemetry.emit(TelemetryEvent(name="second"))

    assert len(snapshot) == 1
    assert len(telemetry.events) == 2


def test_in_memory_is_thread_safe() -> None:
    telemetry = InMemoryTelemetry()

    def emit_many(_: int) -> None:
        for index in range(100):
            telemetry.emit(TelemetryEvent(name=f"event.{index}"))

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(emit_many, range(8)))

    assert len(telemetry.events) == 800


def test_null_telemetry_discards_events() -> None:
    NullTelemetry().emit(TelemetryEvent(name="node.started"))
