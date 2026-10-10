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
from ai.executor.parallel_executor import ParallelExecutor
from ai.services.draft_writer import DraftWriter
from ai.services.readme_generation_service import (
    ReadmeGenerationService,
)
from ai.telemetry import InMemoryTelemetry


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
            content="# Silas",
            provider=self.name,
            model="fake-model",
        )


def context_with(status: EvidenceStatus) -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="fastapi",
                source="git",
                content="Implemented FastAPI authentication.",
                status=status,
            ),
        )
    )


def build_service(
    tmp_path: Path,
    telemetry: InMemoryTelemetry,
) -> ReadmeGenerationService:
    return ReadmeGenerationService(
        readme_agent=ReadmeAgent(FakeProvider()),
        draft_writer=DraftWriter(tmp_path),
        executor=ParallelExecutor(telemetry=telemetry),
    )


def test_service_generates_with_injected_executor(
    tmp_path: Path,
) -> None:
    telemetry = InMemoryTelemetry()
    service = build_service(tmp_path, telemetry)

    result = service.generate(
        context=context_with(EvidenceStatus.VERIFIED),
        agent_input=ReadmeAgentInput(),
    )

    assert result.provider == "fake"
    assert result.destination.exists()
    assert telemetry.events[-1].name == "workflow.completed"


def test_service_still_raises_original_error_with_executor(
    tmp_path: Path,
) -> None:
    telemetry = InMemoryTelemetry()
    service = build_service(tmp_path, telemetry)

    with pytest.raises(EvidenceValidationError):
        service.generate(
            context=context_with(EvidenceStatus.UNVERIFIED),
            agent_input=ReadmeAgentInput(),
        )

    assert telemetry.events[-1].name == "workflow.failed"
