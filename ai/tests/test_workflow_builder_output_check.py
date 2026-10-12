from __future__ import annotations

from typing import Any

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.executor.parallel_executor import ParallelExecutor
from ai.graph import NodeExecutionStatus
from ai.planner.plan import ExecutionPlan, ExecutionStep
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


def context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="repo-1",
                source="github",
                content="Built an agent graph engine.",
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def block(result: Any) -> None:
    del result
    raise ValueError("blocked by check")


def test_failing_check_fails_node_and_skips_dependents() -> None:
    graph = (
        WorkflowBuilder("checked", registry())
        .add("validate", "evidence-validator", output_check=block)
        .add("generate", "readme-agent")
        .depends_on("generate", "validate")
        .build()
    )

    report = ParallelExecutor().execute(graph, context())
    statuses = {record.node: record.status for record in report.records}

    assert report.failed_nodes == ("validate",)
    assert statuses["generate"] is NodeExecutionStatus.SKIPPED
    assert report.records[0].error == "ValueError: blocked by check"


def test_check_receives_the_agent_result() -> None:
    seen: list[str] = []

    def record(result: Any) -> None:
        seen.append(result.agent)

    graph = (
        WorkflowBuilder("checked", registry())
        .add("validate", "evidence-validator", output_check=record)
        .build()
    )

    report = ParallelExecutor().execute(graph, context())

    assert report.succeeded is True
    assert seen == ["evidence-validator"]


def test_from_plan_applies_output_checks() -> None:
    plan = ExecutionPlan(
        objective="Validate",
        steps=(ExecutionStep(agent="evidence-validator"),),
    )

    graph = WorkflowBuilder.from_plan(
        plan,
        registry(),
        output_checks={"evidence-validator": block},
    ).build()

    report = ParallelExecutor().execute(graph, context())

    assert report.failed_nodes == ("evidence-validator",)


def test_depends_on_keeps_the_output_check() -> None:
    graph = (
        WorkflowBuilder("checked", registry())
        .add("first", "evidence-validator")
        .add("second", "evidence-validator", output_check=block)
        .depends_on("second", "first")
        .build()
    )

    report = ParallelExecutor().execute(graph, context())

    assert report.failed_nodes == ("second",)
