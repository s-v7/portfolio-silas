from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from time import time
from typing import Any


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    name: str
    attributes: Mapping[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Telemetry event name cannot be empty.")
