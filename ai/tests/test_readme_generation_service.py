from __future__ import annotations

from pathlib import Path

import pytest

from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import EvidenceValidationError
from ai.services.draft_writer import DraftWriter
from ai.services.readme_generation_service import (
    ReadmeGenerationService,
)


class FakeProvider(LLMProvider):
    def __init__(
        self,
        content: str = "# Silas Vasconcelos Cruz\n\nBackend Engineer.",
    ) -> None:
        self.content = content
        self.requests: list[ProviderRequest] = []

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.requests.append(request)

        return ProviderResponse(
            content=self.content,
            provider=self.name,
            model="fake-model",
            metadata={"tokens": 42},
        )


def build_verified_context() -> PortfolioContext:
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
            Evidence(
                identifier="git-jakarta",
                source="git",
                content=(
                    "Migrated a corporate application "
                    "to Jakarta EE 10 and Java 17."
                ),
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def test_generates_and_writes_readme_draft(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(tmp_path),
    )

    result = service.generate(
        context=build_verified_context(),
        agent_input=ReadmeAgentInput(),
    )

    assert result.destination == tmp_path / "README.pt.md"
    assert result.destination.exists()

    assert result.destination.read_text(
        encoding="utf-8"
    ) == (
        "# Silas Vasconcelos Cruz\n\n"
        "Backend Engineer.\n"
    )

    assert result.provider == "fake"
    assert result.model == "fake-model"
    assert result.evidence_count == 2
    assert result.rejected_evidence_count == 0
    assert result.warnings == ()
    assert len(provider.requests) == 1


def test_uses_custom_draft_path(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(tmp_path),
    )

    result = service.generate(
        context=build_verified_context(),
        agent_input=ReadmeAgentInput(language="en"),
        relative_path="readme/README.en.md",
    )

    assert result.destination == (
        tmp_path / "readme" / "README.en.md"
    )
    assert result.destination.exists()


def test_does_not_send_unverified_evidence_to_provider(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()

    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="verified-fastapi",
                source="git",
                content="Implemented FastAPI endpoints.",
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="planned-kubernetes",
                source="roadmap",
                content="Kubernetes migration is planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(tmp_path),
    )

    result = service.generate(
        context=context,
        agent_input=ReadmeAgentInput(),
    )

    assert len(provider.requests) == 1

    prompt = provider.requests[0].messages[-1].content

    assert "Implemented FastAPI endpoints." in prompt
    assert "Kubernetes migration is planned." not in prompt
    assert result.evidence_count == 1
    assert result.rejected_evidence_count == 1


def test_rejects_context_without_verified_evidence(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()

    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="planned-kubernetes",
                source="roadmap",
                content="Kubernetes migration is planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(tmp_path),
    )

    with pytest.raises(
        EvidenceValidationError,
        match="No verified evidence",
    ):
        service.generate(
            context=context,
            agent_input=ReadmeAgentInput(),
        )

    assert not provider.requests
    assert not (tmp_path / "README.pt.md").exists()


def test_rejects_empty_context(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(tmp_path),
    )

    with pytest.raises(
        EvidenceValidationError,
        match="No verified evidence",
    ):
        service.generate(
            context=PortfolioContext(evidences=()),
            agent_input=ReadmeAgentInput(),
        )

    assert not provider.requests
