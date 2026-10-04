from __future__ import annotations

from dataclasses import dataclass

from ai.agents.base import Agent, AgentResult
from ai.agents.metadata import AgentMetadata
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
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

    def __init__(self, registry: AgentRegistry) -> None:
        super().__init__()
        self._registry = registry

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

        candidates = self._agents_for_capabilities(agent_input.required_capabilities)
        steps = tuple(
            ExecutionStep(
                agent=metadata.name,
                capabilities=metadata.capabilities,
            )
            for metadata in candidates
        )

        plan = ExecutionPlan(
            objective=objective,
            steps=steps,
        )

        return AgentResult(
            agent=self.name,
            output=PlannerOutput(
                agents=candidates,
                plan=plan,
            ),
            metadata={
                "candidate_count": len(candidates),
                "required_capabilities": agent_input.required_capabilities,
                "step_count": len(steps),
            },
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
