from __future__ import annotations

import pytest

from ai.agents.bio_agent import BioAgent, BioAgentInput
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
    TaskType,
)
from ai.core.exceptions import AgentExecutionError


class FakeProvider(LLMProvider):
    def __init__(self, content: str = "Line one.\nLine two.") -> None:
        self.content = content
        self.calls = 0
        self.last_request: ProviderRequest | None = None

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.calls += 1
        self.last_request = request

        return ProviderResponse(
            content=self.content,
            provider=self.name,
            model="fake-model",
        )


def context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="sigec",
                source="test",
                content="Indexed 1.1M ARTs on a SHA-256 blockchain.",
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="planned",
                source="test",
                content="Plans to adopt Kubernetes.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )


def test_metadata_declares_bio_capability_without_markdown() -> None:
    metadata = BioAgent(FakeProvider()).metadata

    assert metadata.name == "bio-agent"
    assert "bio" in metadata.capabilities
    assert "markdown" not in metadata.capabilities
    assert metadata.outputs == ("BioDraft",)


def test_generates_draft_with_provider_details() -> None:
    result = BioAgent(FakeProvider()).execute(BioAgentInput(), context())

    assert result.output.content == "Line one.\nLine two."
    assert result.output.provider == "fake"
    assert result.output.model == "fake-model"
    assert result.metadata["evidence_count"] == 1


def test_prompt_contains_only_verified_evidence() -> None:
    provider = FakeProvider()

    BioAgent(provider).execute(BioAgentInput(), context())

    assert provider.last_request is not None
    prompt = provider.last_request.messages[-1].content

    assert "1.1M ARTs" in prompt
    assert "Kubernetes" not in prompt


def test_uses_short_text_and_asks_for_plain_text() -> None:
    provider = FakeProvider()

    BioAgent(provider).execute(BioAgentInput(), context())

    assert provider.last_request is not None
    assert provider.last_request.task is TaskType.SHORT_TEXT
    assert "plain text" in provider.last_request.messages[-1].content


def test_requires_verified_evidence_without_calling_provider() -> None:
    provider = FakeProvider()
    unverified = PortfolioContext(
        evidences=(
            Evidence(
                identifier="x",
                source="test",
                content="Claim.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    with pytest.raises(AgentExecutionError, match="verified evidence"):
        BioAgent(provider).execute(BioAgentInput(), unverified)

    assert provider.calls == 0


def test_rejects_empty_provider_content() -> None:
    with pytest.raises(AgentExecutionError, match="empty content"):
        BioAgent(FakeProvider("  ")).execute(BioAgentInput(), context())


def test_bio_is_not_part_of_the_portfolio_bundle() -> None:
    assert "portfolio" not in BioAgent(FakeProvider()).metadata.capabilities


def test_prompt_asks_for_three_separate_lines() -> None:
    prv = FakeProvider()

    BioAgent(prv).execute(BioAgentInput(), context())

    assert prv.last_request is not None
    msg = prv.last_request.messages[-1].content

    assert "exactly 3 lines" in msg
    assert "line breaks" in msg


def test_puts_each_sentence_on_its_own_line() -> None:
    prv = FakeProvider("First fact about 1.1M ARTs. Second fact. Third fact.")

    rst = BioAgent(prv).execute(BioAgentInput(), context())

    assert rst.output.content == (
        "First fact about 1.1M ARTs.\nSecond fact.\nThird fact."
    )


def test_keeps_lines_that_are_already_separated() -> None:
    prv = FakeProvider("First fact.\nSecond fact.")

    rst = BioAgent(prv).execute(BioAgentInput(), context())

    assert rst.output.content == "First fact.\nSecond fact."


def test_does_not_split_decimal_numbers() -> None:
    prv = FakeProvider("Indexed 1.1M ARTs on v2.0 of the engine.")

    rst = BioAgent(prv).execute(BioAgentInput(), context())

    assert rst.output.content == "Indexed 1.1M ARTs on v2.0 of the engine."
