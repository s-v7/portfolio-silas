from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ai.agents.base import Agent, AgentResult
from ai.agents.metadata import AgentMetadata
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.memory import Memory
from ai.planner.plan import ExecutionPlan, ExecutionStep

__all__ = [
    "ExecutionPlan",
    "ExecutionStep",
    "PlannerInput",
    "PlannerOutput",
    "PlannedAgent",
    "PlannerAgent",
]


@dataclass(frozen=True, slots=True)
class PlannerInput:
    objective: str
    required_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PlannerOutput:
    agents: tuple[AgentMetadata, ...]
    plan: ExecutionPlan


@dataclass(frozen=True, slots=True)
class PlannedAgent:
    name: str
    responsibility: str
    capabilities: tuple[str, ...]


class PlannerAgent(Agent[PlannerInput, PlannerOutput]):
    name = "planner-agent"
    responsibility = "Select agents and produce execution plans from capabilities."

    def __init__(
        self,
        registry: AgentRegistry,
        memory: Memory | None = None,
    ) -> None:
        super().__init__()
        self._registry = registry
        self._memory = memory

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name=self.name,
            responsibility=self.responsibility,
            inputs=("PlannerInput", "PortfolioContext"),
            outputs=("PlannerOutput",),
            capabilities=(
                "planning",
                "agent-discovery",
                "capability-selection",
            ),
        )

    def execute(
        self, agent_input: PlannerInput, context: PortfolioContext
    ) -> AgentResult[PlannerOutput]:
        del context

        objective = agent_input.objective.strip()

        if not objective:
            raise ValueError("Planner objective cannot be empty.")

        required = agent_input.required_capabilities
        memory = self._memory
        key = self._memory_key(objective, required)
        cache_hit = False

        if memory is not None and memory.has(key):
            output = cast(PlannerOutput, memory.get(key))
            cache_hit = True
        else:
            output = self._build_output(objective, required)

            if memory is not None:
                memory.set(key, output)

        return AgentResult(
            agent=self.name,
            output=output,
            metadata={
                "candidate_count": len(output.agents),
                "required_capabilities": required,
                "step_count": len(output.plan.steps),
                "cache_hit": cache_hit,
            },
        )

    def _memory_key(
        self,
        objective: str,
        required: tuple[str, ...],
    ) -> str:
        registered = tuple(metadata.name for metadata in self._registry.list())

        return f"planner:plan:{(objective, required, registered)!r}"

    def _build_output(
        self,
        objective: str,
        required: tuple[str, ...],
    ) -> PlannerOutput:
        candidates = self._agents_for_capabilities(required)
        steps = tuple(
            ExecutionStep(
                agent=metadata.name,
                capabilities=metadata.capabilities,
            )
            for metadata in candidates
        )

        return PlannerOutput(
            agents=candidates,
            plan=ExecutionPlan(objective=objective, steps=steps),
        )

    def _agents_for_capabilities(
        self,
        capabilities: tuple[str, ...],
    ) -> tuple[AgentMetadata, ...]:
        required = set(capabilities)

        return tuple(
            metadata
            for metadata in self._registry.list()
            if required.issubset(metadata.capabilities)
        )
