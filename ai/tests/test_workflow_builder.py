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
from ai.workflows.builder import WorkflowBuilder


class FakeProvider(LLMProvider):
    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
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


def portfolio_context_with_verified_evidence() -> PortfolioContext:
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


def test_builds_workflow_from_registered_agents() -> None:
    workflow = (
        WorkflowBuilder("readme-generation", registry())
        .add("validate", "evidence-validator")
        .add("generate", "readme-agent")
        .depends_on("generate", "validate")
        .build()
    )

    assert workflow.name == "readme-generation"
    assert workflow.node_names == (
        "validate",
        "generate",
    )


def test_rejects_unknown_agent() -> None:
    with pytest.raises(
        KeyError,
        match="does-not-exist",
    ):
        (WorkflowBuilder("test", registry()).add("missing", "does-not-exist"))


def test_rejects_unknown_dependency() -> None:
    with pytest.raises(
        KeyError,
        match="missing",
    ):
        (
            WorkflowBuilder("test", registry())
            .add("generate", "readme-agent")
            .depends_on("generate", "missing")
        )


def test_rejects_duplicate_node() -> None:
    builder = WorkflowBuilder("test", registry())
    builder.add("generate", "readme-agent")

    with pytest.raises(
        ValueError,
        match="already defined",
    ):
        builder.add("generate", "readme-agent")


def test_builder_is_fluent() -> None:
    builder = WorkflowBuilder("test", registry())

    assert (
        builder.add("validate", "evidence-validator")
        .add("generate", "readme-agent")
        .depends_on("generate", "validate")
        is builder
    )


def test_add_accepts_input_factory_for_agent_input() -> None:
    builder = WorkflowBuilder("test", registry())

    builder.add(
        "generate",
        "readme-agent",
        input_factory=ReadmeAgentInput,
    )

    graph = builder.build()

    assert graph.node_names == ("generate",)


def test_built_workflow_executes_sequentially() -> None:
    workflow = (
        WorkflowBuilder("readme-generation", registry())
        .add("validate", "evidence-validator")
        .add(
            "generate",
            "readme-agent",
            input_factory=ReadmeAgentInput,
        )
        .depends_on("generate", "validate")
        .build()
    )

    report = workflow.execute(portfolio_context_with_verified_evidence())

    assert report.succeeded is True
    assert report.results["validate"] is not None
    assert report.results["generate"] is not None


def test_built_workflow_executes_in_parallel() -> None:
    workflow = (
        WorkflowBuilder("readme-generation", registry())
        .add("validate", "evidence-validator")
        .add(
            "generate",
            "readme-agent",
            input_factory=ReadmeAgentInput,
        )
        .depends_on("generate", "validate")
        .build()
    )

    sequential_report = workflow.execute(portfolio_context_with_verified_evidence())

    workflow_for_parallel = (
        WorkflowBuilder("readme-generation", registry())
        .add("validate", "evidence-validator")
        .add(
            "generate",
            "readme-agent",
            input_factory=ReadmeAgentInput,
        )
        .depends_on("generate", "validate")
        .build()
    )

    parallel_report = ParallelExecutor().execute(
        workflow_for_parallel,
        portfolio_context_with_verified_evidence(),
    )

    assert parallel_report.succeeded is True
    assert sequential_report.succeeded == parallel_report.succeeded
