from __future__ import annotations

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.memory import InMemoryMemory
from ai.planner.planner import PlannerAgent, PlannerInput


class FakeProvider(LLMProvider):
    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        return ProviderResponse(
            content="# README",
            provider=self.name,
            model="fake-model",
        )


def readme_only_registry() -> AgentRegistry:
    value = AgentRegistry()
    value.register(ReadmeAgent(FakeProvider()))
    return value


def request(objective: str = "Generate README") -> PlannerInput:
    return PlannerInput(objective=objective)


def context() -> PortfolioContext:
    return PortfolioContext(evidences=())


def test_planner_without_memory_never_reports_cache_hit() -> None:
    planner = PlannerAgent(readme_only_registry())

    first = planner.execute(request(), context())
    second = planner.execute(request(), context())

    assert first.metadata["cache_hit"] is False
    assert second.metadata["cache_hit"] is False


def test_repeated_request_is_served_from_memory() -> None:
    planner = PlannerAgent(
        readme_only_registry(),
        memory=InMemoryMemory(),
    )

    first = planner.execute(request(), context())
    second = planner.execute(request(), context())

    assert first.metadata["cache_hit"] is False
    assert second.metadata["cache_hit"] is True
    assert second.output == first.output


def test_different_objective_is_not_a_cache_hit() -> None:
    planner = PlannerAgent(
        readme_only_registry(),
        memory=InMemoryMemory(),
    )

    planner.execute(request("Generate README"), context())
    other = planner.execute(request("Generate bio"), context())

    assert other.metadata["cache_hit"] is False
    assert other.output.plan.objective == "Generate bio"


def test_registry_change_invalidates_stored_plan() -> None:
    registry = readme_only_registry()
    planner = PlannerAgent(registry, memory=InMemoryMemory())

    first = planner.execute(request(), context())
    registry.register(EvidenceValidatorAgent[None]())
    second = planner.execute(request(), context())

    assert tuple(a.name for a in first.output.agents) == ("readme-agent",)
    assert second.metadata["cache_hit"] is False
    assert tuple(a.name for a in second.output.agents) == (
        "readme-agent",
        "evidence-validator",
    )
