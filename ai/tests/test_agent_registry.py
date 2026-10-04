from __future__ import annotations

import pytest

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)


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


def test_registers_and_gets_agent() -> None:
    registry = AgentRegistry()
    agent = ReadmeAgent(FakeProvider())

    registry.register(agent)

    assert len(registry) == 1
    assert registry.get("readme-agent") is agent


def test_lists_agent_metadata() -> None:
    registry = AgentRegistry()

    registry.register(ReadmeAgent(FakeProvider()))
    registry.register(EvidenceValidatorAgent[None]())

    metadata = registry.list()

    assert len(metadata) == 2
    assert metadata[0].name == "readme-agent"
    assert metadata[1].name == "evidence-validator"


def test_finds_agents_by_capability() -> None:
    registry = AgentRegistry()

    registry.register(ReadmeAgent(FakeProvider()))
    registry.register(EvidenceValidatorAgent[None]())

    markdown_agents = registry.find_by_capability("markdown")
    evidence_agents = registry.find_by_capability(
        "evidence-validation"
    )

    assert tuple(
        item.name for item in markdown_agents
    ) == ("readme-agent",)

    assert tuple(
        item.name for item in evidence_agents
    ) == ("evidence-validator",)


def test_rejects_duplicate_agent_name() -> None:
    registry = AgentRegistry()

    registry.register(ReadmeAgent(FakeProvider()))

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(ReadmeAgent(FakeProvider()))


def test_rejects_unknown_agent() -> None:
    registry = AgentRegistry()

    with pytest.raises(
        KeyError,
        match="not registered",
    ):
        registry.get("unknown-agent")
