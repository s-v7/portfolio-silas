from __future__ import annotations

import pytest

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.core.contracts import LLMProvider, ProviderRequest, ProviderResponse
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
        (
            WorkflowBuilder("test", registry())
            .add("missing", "does-not-exist")
        )


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
        builder
        .add("validate", "evidence-validator")
        .add("generate", "readme-agent")
        .depends_on("generate", "validate")
        is builder
    )
