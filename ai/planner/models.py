from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanningRequest:
    goal: str
    capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WorkflowPlan:
    workflow: str
    agents: tuple[str, ...]
    capabilities: tuple[str, ...]
