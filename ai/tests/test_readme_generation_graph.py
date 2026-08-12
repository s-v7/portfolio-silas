from __future__ import annotations

from pathlib import Path

from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import (
    EvidenceStatus,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.graph import NodeExecutionStatus
from ai.services.draft_writer import DraftWriter
from ai.workflows.readme_generation_graph import (
    GENERATE_README_NODE,
    VALIDATE_EVIDENCE_NODE,
    WRITE_DRAFT_NODE,
    ReadmeDraftWriteResult,
    ReadmeGenerationGraph,
)


class FakeProvider(LLMProvider):
    def __init__(
        self,
        content: str = "# Silas\n\nBackend and AI engineering.",
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
        )


def build_context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="fastapi",
                source="git",
                content="Implemented FastAPI authentication.",
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="planned-kubernetes",
                source="roadmap",
                content="Kubernetes deployment is planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )


def build_workflow(
    tmp_path: Path,
    provider: FakeProvider | None = None,
) -> ReadmeGenerationGraph:
    selected_provider = provider or FakeProvider()

    return ReadmeGenerationGraph(
        readme_agent=ReadmeAgent(selected_provider),
        draft_writer=DraftWriter(tmp_path),
    )


def test_executes_readme_workflow_in_order(
    tmp_path: Path,
) -> None:
    workflow = build_workflow(tmp_path)

    report = workflow.execute(
        context=build_context(),
        agent_input=ReadmeAgentInput(),
        relative_path="README.generated.md",
    )

    assert report.succeeded is True

    assert tuple(record.node for record in report.records) == (
        VALIDATE_EVIDENCE_NODE,
        GENERATE_README_NODE,
        WRITE_DRAFT_NODE,
    )

    assert all(
        record.status is NodeExecutionStatus.SUCCEEDED
        for record in report.records
    )


def test_writes_generated_readme(
    tmp_path: Path,
) -> None:
    workflow = build_workflow(tmp_path)

    report = workflow.execute(
        context=build_context(),
        agent_input=ReadmeAgentInput(),
        relative_path="drafts/README.pt.md",
    )

    result = report.results[WRITE_DRAFT_NODE]

    assert isinstance(result, ReadmeDraftWriteResult)
    assert result.destination == (
        tmp_path / "drafts/README.pt.md"
    ).resolve()
    assert result.destination.read_text(
        encoding="utf-8"
    ) == "# Silas\n\nBackend and AI engineering.\n"
    assert result.provider == "fake"
    assert result.model == "fake-model"
    assert result.evidence_count == 1
    assert result.rejected_evidence_count == 1


def test_sends_only_verified_evidence_to_provider(
    tmp_path: Path,
) -> None:
    provider = FakeProvider()
    workflow = build_workflow(tmp_path, provider)

    workflow.execute(
        context=build_context(),
        agent_input=ReadmeAgentInput(),
    )

    assert provider.last_request is not None

    prompt = provider.last_request.messages[-1].content

    assert "Implemented FastAPI authentication" in prompt
    assert "Kubernetes deployment is planned" not in prompt


def test_stops_when_no_verified_evidence_exists(
    tmp_path: Path,
) -> None:
    workflow = build_workflow(tmp_path)

    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="planned-kubernetes",
                source="roadmap",
                content="Kubernetes deployment is planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    report = workflow.execute(
        context=context,
        agent_input=ReadmeAgentInput(),
    )

    assert report.succeeded is False
    assert report.failed_nodes == (
        VALIDATE_EVIDENCE_NODE,
    )

    assert report.records[0].status is NodeExecutionStatus.FAILED
    assert report.records[1].status is NodeExecutionStatus.SKIPPED
    assert report.records[2].status is NodeExecutionStatus.SKIPPED

    assert WRITE_DRAFT_NODE not in report.results
    assert not (tmp_path / "README.pt.md").exists()


def test_records_provider_failure(
    tmp_path: Path,
) -> None:
    class FailingProvider(FakeProvider):
        def generate(
            self,
            request: ProviderRequest,
        ) -> ProviderResponse:
            del request
            raise RuntimeError("provider unavailable")

    workflow = build_workflow(
        tmp_path,
        FailingProvider(),
    )

    report = workflow.execute(
        context=build_context(),
        agent_input=ReadmeAgentInput(),
    )

    assert report.succeeded is False
    assert report.failed_nodes == (
        GENERATE_README_NODE,
    )

    assert report.records[0].status is NodeExecutionStatus.SUCCEEDED
    assert report.records[1].status is NodeExecutionStatus.FAILED
    assert report.records[2].status is NodeExecutionStatus.SKIPPED
