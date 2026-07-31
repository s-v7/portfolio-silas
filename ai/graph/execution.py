from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from time import perf_counter
from typing import Any


class NodeExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class NodeExecutionRecord:
    node: str
    status: NodeExecutionStatus
    duration_ms: float = 0.0
    output: Any = None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class GraphExecutionReport:
    graph: str
    records: tuple[NodeExecutionRecord, ...]
    results: dict[str, Any] = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return all(
            record.status
            in {
                NodeExecutionStatus.SUCCEEDED,
                NodeExecutionStatus.SKIPPED,
            }
            for record in self.records
        )

    @property
    def failed_nodes(self) -> tuple[str, ...]:
        return tuple(
            record.node
            for record in self.records
            if record.status is NodeExecutionStatus.FAILED
        )


class NodeTimer:
    def __enter__(self) -> NodeTimer:
        self._started_at = perf_counter()
        self.duration_ms = 0.0
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        del exc_type, exc_value, traceback
        self.duration_ms = (
            perf_counter() - self._started_at
        ) * 1_000
