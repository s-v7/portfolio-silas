from __future__ import annotations

import pytest

from ai.agents.readme_agent import (
    ReadmeAgent,
    ReadmeAgentInput,
)
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import AgentExecutionError


class FakeProvider(LLMProvider):
    def __init__(
        self,
        content: str = "# Silas\nBackend Engineer",
    ) -> None:
        self.content = content
        self.last_request: ProviderRequest | None = None

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.last_request = request

        return ProviderResponse(
            content=self.content,
            provider=self.name,
            model="fake-model",
            metadata={},
        )


def verified_context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="git-fastapi",
                source="git",
                content=(
                    "Implemented FastAPI authentication "
                    "and health endpoints."
                ),
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def test_generates_readme_from_verified_evidence() -> None:
    provider = FakeProvider()
    agent = ReadmeAgent(provider)

    result = agent.execute(
        ReadmeAgentInput(),
        verified_context(),
    )

    assert result.output.content.startswith("# Silas")
    assert result.output.provider == "fake"
    assert result.output.model == "fake-model"
    assert result.metadata["evidence_count"] == 1


def test_sends_verified_context_to_provider() -> None:
    provider = FakeProvider()
    agent = ReadmeAgent(provider)

    agent.execute(
        ReadmeAgentInput(),
        verified_context(),
    )

    assert provider.last_request is not None

    prompt = provider.last_request.messages[-1].content

    assert "Implemented FastAPI authentication" in prompt
    assert "git-fastapi" in prompt


def test_rejects_context_without_verified_evidence() -> None:
    provider = FakeProvider()
    agent = ReadmeAgent(provider)

    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="planned-k8s",
                source="roadmap",
                content="Kubernetes deployment planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    with pytest.raises(
        AgentExecutionError,
        match="requires verified evidence",
    ):
        agent.execute(
            ReadmeAgentInput(),
            context,
        )


def test_rejects_empty_provider_response() -> None:
    provider = FakeProvider(content=" ")
    agent = ReadmeAgent(provider)

    with pytest.raises(
        AgentExecutionError,
        match="returned empty content",
    ):
        agent.execute(
            ReadmeAgentInput(),
            verified_context(),
        )


def test_removes_markdown_code_fence() -> None:
    provider = FakeProvider(
        content=(
            "```markdown\n"
            "# Silas Vasconcelos Cruz\n\n"
            "FastAPI project.\n"
            "```"
        )
    )
    agent = ReadmeAgent(provider)

    result = agent.execute(
        ReadmeAgentInput(),
        verified_context(),
    )

    assert result.output.content == (
        "# Silas Vasconcelos Cruz\n\n"
        "FastAPI project."
    )
