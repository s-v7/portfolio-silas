from __future__ import annotations

import pytest

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    ProviderRequest,
    ProviderResponse,
)
from ai.planner.planner import PlannerAgent, PlannerInput


class FakeProvider:
    @property
    def name(self) -> str:
        return "fake"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=self.name,
            content="Fake content",
        )  # type: ignore


def registry() -> AgentRegistry:
    result = AgentRegistry()
    provider = FakeProvider()

    # Passamos a instância do FakeProvider para o ReadmeAgent
    result.register(ReadmeAgent(provider=provider))  # type: ignore
    result.register(
        EvidenceValidatorAgent[None]()
    )  # Ajuste aqui se o EvidenceValidatorAgent também exigir argumento

    return result


def test_planner_discovers_agents_by_capability() -> None:
    planner = PlannerAgent(registry())

    result = planner.execute(
        PlannerInput(
            objective="Generate a technical portfolio README",
            required_capabilities=("markdown",),
        ),
        PortfolioContext(evidences=()),
    )

    assert tuple(agent.name for agent in result.output.agents) == ("readme-agent",)


def test_planner_requires_all_capabilities() -> None:
    planner = PlannerAgent(registry())

    result = planner.execute(
        PlannerInput(
            objective="Validate portfolio evidence",
            required_capabilities=(
                "evidence-validation",
                "verification",
            ),
        ),
        PortfolioContext(evidences=()),
    )

    assert tuple(agent.name for agent in result.output.agents) == (
        "evidence-validator",
    )


def test_planner_can_return_all_registered_agents() -> None:
    planner = PlannerAgent(registry())

    result = planner.execute(
        PlannerInput(
            objective="Inspect available portfolio capabilities",
        ),
        PortfolioContext(evidences=()),
    )

    assert tuple(agent.name for agent in result.output.agents) == (
        "readme-agent",
        "evidence-validator",
    )


def test_planner_exposes_execution_metadata() -> None:
    planner = PlannerAgent(registry())

    result = planner.execute(
        PlannerInput(
            objective="Generate README",
            required_capabilities=("markdown",),
        ),
        PortfolioContext(evidences=()),
    )

    assert result.metadata["candidate_count"] == 1
    assert result.metadata["required_capabilities"] == ("markdown",)


def test_planner_rejects_empty_objective() -> None:
    planner = PlannerAgent(registry())

    with pytest.raises(ValueError, match="Planner objective cannot be empty."):
        planner.execute(
            PlannerInput(objective=" "),
            PortfolioContext(evidences=()),
        )


def test_planner_produces_execution_plan() -> None:
    planner = PlannerAgent(registry())

    result = planner.execute(
        PlannerInput(
            objective="Generate README",
            required_capabilities=("markdown",),
        ),
        PortfolioContext(evidences=()),
    )

    assert result.output.plan.objective == "Generate README"
    assert tuple(step.agent for step in result.output.plan.steps) == ("readme-agent",)

    assert result.output.plan.steps[0].capabilities == (
        "markdown",
        "generation",
        "portfolio",
        "github",
    )
