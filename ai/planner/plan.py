from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionStep:
    agent: str
    capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    objective: str
    steps: tuple[ExecutionStep, ...]
