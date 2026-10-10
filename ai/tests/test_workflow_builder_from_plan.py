from __future__ import annotations

import pytest

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.agents.registry import AgentRegistry
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.executor.parallel_executor import ParallelExecutor
from ai.planner.plan import ExecutionPlan
from ai.planner.planner import PlannerAgent, PlannerInput
from ai.workflows.builder import WorkflowBuilder


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


def registry() -> AgentRegistry:
    value = AgentRegistry()
    value.register(ReadmeAgent(FakeProvider()))
    value.register(EvidenceValidatorAgent[None]())
    return value


def plan_for(
    reg: AgentRegistry,
    *capabilities: str,
) -> ExecutionPlan:
    result = PlannerAgent(reg).execute(
        PlannerInput(
            objective="Generate README",
            required_capabilities=capabilities,
        ),
        PortfolioContext(evidences=()),
    )
    return result.output.plan


def verified_context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="repo-1",
                source="github",
                content="Built a typed agent graph execution engine.",
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def test_builds_one_node_per_plan_step() -> None:
    reg = registry()

    graph = WorkflowBuilder.from_plan(
        plan_for(reg, "portfolio"),
        reg,
    ).build()

    assert graph.node_names == ("readme-agent", "evidence-validator")


def test_uses_plan_objective_as_default_name() -> None:
    reg = registry()

    graph = WorkflowBuilder.from_plan(plan_for(reg, "markdown"), reg).build()

    assert graph.name == "Generate README"


def test_accepts_name_override() -> None:
    reg = registry()

    graph = WorkflowBuilder.from_plan(
        plan_for(reg, "markdown"),
        reg,
        name="readme-flow",
    ).build()

    assert graph.name == "readme-flow"


def test_rejects_plan_without_steps() -> None:
    reg = registry()

    with pytest.raises(ValueError, match="no steps"):
        WorkflowBuilder.from_plan(plan_for(reg, "does-not-exist"), reg)


def test_plan_to_executed_workflow_end_to_end() -> None:
    reg = registry()

    graph = (
        WorkflowBuilder.from_plan(
            plan_for(reg, "portfolio"),
            reg,
            input_factories={"readme-agent": ReadmeAgentInput},
        )
        .depends_on("readme-agent", "evidence-validator")
        .build()
    )

    report = ParallelExecutor().execute(graph, verified_context())

    assert report.succeeded is True
    assert set(report.results) == {"readme-agent", "evidence-validator"}
