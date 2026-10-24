from __future__ import annotations

from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)


class RecordingProvider(LLMProvider):
    def __init__(self) -> None:
        self.prompt = ""

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.prompt = request.messages[-1].content

        return ProviderResponse(
            content="# README",
            provider=self.name,
            model="fake-model",
        )


def cxt() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="a",
                source="t",
                content="Implemented FastAPI endpoints.",
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def test_feedback_is_added_after_the_evidence() -> None:
    prv = RecordingProvider()

    ReadmeAgent(prv).execute(
        ReadmeAgentInput(feedback="numbers not in evidence: 9"), cxt()
    )

    assert "Your previous answer was rejected: numbers not in evidence: 9" in prv.prompt
    assert prv.prompt.index("rejected") > prv.prompt.index("Verified evidence")


def test_no_feedback_means_no_rejection_note() -> None:
    prv = RecordingProvider()

    ReadmeAgent(prv).execute(ReadmeAgentInput(), cxt())

    assert "rejected" not in prv.prompt
