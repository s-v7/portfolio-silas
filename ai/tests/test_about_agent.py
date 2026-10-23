from __future__ import annotations

import pytest

from ai.agents.about_agent import AboutAgent, AboutAgentInput
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
    def __init__(self, content: str = "First paragraph.\n\nSecond one.") -> None:
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


def evidence(
    identifier: str,
    content: str,
    status: EvidenceStatus,
) -> Evidence:
    return Evidence(
        identifier=identifier,
        source="test",
        content=content,
        status=status,
    )


def context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            evidence(
                "sigec",
                "Indexed 1.1M ARTs on a SHA-256 blockchain.",
                EvidenceStatus.VERIFIED,
            ),
            evidence(
                "planned",
                "Plans to adopt Kubernetes.",
                EvidenceStatus.UNVERIFIED,
            ),
        )
    )


def test_metadata_declares_about_capability() -> None:
    metadata = AboutAgent(FakeProvider()).metadata

    assert metadata.name == "about-agent"
    assert "about" in metadata.capabilities
    assert metadata.outputs == ("AboutDraft",)


def test_generates_draft_and_strips_markdown_fence() -> None:
    provider = FakeProvider("```markdown\nFirst.\n\nSecond.\n```")

    result = AboutAgent(provider).execute(AboutAgentInput(), context())

    assert result.output.content == "First.\n\nSecond."
    assert result.output.provider == "fake"
    assert result.output.model == "fake-model"
    assert result.metadata["evidence_count"] == 1


def test_prompt_contains_only_verified_evidence() -> None:
    provider = FakeProvider()

    AboutAgent(provider).execute(AboutAgentInput(), context())

    assert provider.last_request is not None
    prompt = provider.last_request.messages[-1].content

    assert "1.1M ARTs" in prompt
    assert "Kubernetes" not in prompt


def test_uses_short_text_task() -> None:
    provider = FakeProvider()

    AboutAgent(provider).execute(AboutAgentInput(), context())

    assert provider.last_request is not None
    assert provider.last_request.task is TaskType.SHORT_TEXT


def test_prompt_carries_language_and_name() -> None:
    provider = FakeProvider()

    AboutAgent(provider).execute(
        AboutAgentInput(language="pt-BR", name="Ada Lovelace"),
        context(),
    )

    assert provider.last_request is not None
    prompt = provider.last_request.messages[-1].content

    assert "pt-BR" in prompt
    assert "Ada Lovelace" in prompt


def test_requires_verified_evidence_without_calling_provider() -> None:
    provider = FakeProvider()
    unverified = PortfolioContext(
        evidences=(evidence("x", "Claim.", EvidenceStatus.UNVERIFIED),)
    )

    with pytest.raises(AgentExecutionError, match="verified evidence"):
        AboutAgent(provider).execute(AboutAgentInput(), unverified)

    assert provider.calls == 0


def test_rejects_empty_provider_content() -> None:
    with pytest.raises(AgentExecutionError, match="empty content"):
        AboutAgent(FakeProvider("   ")).execute(AboutAgentInput(), context())


def test_prompt_forbids_unsupported_claims_and_asks_for_the_role() -> None:
    provider = FakeProvider()

    AboutAgent(provider).execute(AboutAgentInput(), context())

    assert provider.last_request is not None
    prompt = provider.last_request.messages[-1].content

    assert "leadership or ownership" in prompt
    assert "role or employer" in prompt


def test_prompt_asks_for_seven_sentences_in_two_paragraphs() -> None:
    provider = FakeProvider()

    AboutAgent(provider).execute(AboutAgentInput(), context())

    assert provider.last_request is not None
    prompt = provider.last_request.messages[-1].content

    assert "4 sentences in the first" in prompt
    assert "7 in total" in prompt
    assert "exactly as they appear" in prompt


def test_feedback_is_added_to_the_prompt() -> None:
    prv = FakeProvider()

    AboutAgent(prv).execute(AboutAgentInput(feedback="found 8 sentences"), context())

    assert prv.last_request is not None
    msg = prv.last_request.messages[-1].content

    assert "Your previous answer was rejected: found 8 sentences" in msg
    assert msg.index("rejected") > msg.index("Verified evidence")


def test_no_feedback_means_no_rejection_note() -> None:
    prv = FakeProvider()

    AboutAgent(prv).execute(AboutAgentInput(), context())

    assert prv.last_request is not None
    assert "rejected" not in prv.last_request.messages[-1].content
