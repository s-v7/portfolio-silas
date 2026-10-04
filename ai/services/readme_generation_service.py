from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import PortfolioContext
from ai.graph import GraphExecutionReport, NodeExecutionStatus
from ai.services.draft_writer import DraftWriter
from ai.workflows.readme_generation_graph import (
    WRITE_DRAFT_NODE,
    ReadmeDraftWriteResult,
    ReadmeGenerationGraph,
)


@dataclass(frozen=True, slots=True)
class ReadmeGenerationResult:
    destination: Path
    provider: str
    model: str
    evidence_count: int
    rejected_evidence_count: int
    warnings: tuple[str, ...]


class ReadmeGenerationService:
    def __init__(
        self,
        readme_agent: ReadmeAgent,
        draft_writer: DraftWriter,
        evidence_validator: (
            EvidenceValidatorAgent[None] | None
        ) = None,
    ) -> None:
        self._workflow = ReadmeGenerationGraph(
            readme_agent=readme_agent,
            draft_writer=draft_writer,
            evidence_validator=evidence_validator,
        )

    def generate(
        self,
        context: PortfolioContext,
        agent_input: ReadmeAgentInput,
        relative_path: str = "README.pt.md",
    ) -> ReadmeGenerationResult:
        report = self._workflow.execute(
            context=context,
            agent_input=agent_input,
            relative_path=relative_path,
        )

        self._raise_graph_failure(report)

        workflow_result = cast(
            ReadmeDraftWriteResult,
            report.results[WRITE_DRAFT_NODE],
        )

        return ReadmeGenerationResult(
            destination=workflow_result.destination,
            provider=workflow_result.provider,
            model=workflow_result.model,
            evidence_count=workflow_result.evidence_count,
            rejected_evidence_count=(
                workflow_result.rejected_evidence_count
            ),
            warnings=workflow_result.warnings,
        )

    @staticmethod
    def _raise_graph_failure(
        report: GraphExecutionReport,
    ) -> None:
        if report.succeeded:
            return

        failed_record = next(
            (
                record
                for record in report.records
                if record.status is NodeExecutionStatus.FAILED
            ),
            None,
        )

        if failed_record is None:
            raise RuntimeError(
                "README generation graph failed without "
                "a failed node record."
            )

        if failed_record.exception is not None:
            raise failed_record.exception

        raise RuntimeError(
            f"README generation failed in node "
            f"'{failed_record.node}': "
            f"{failed_record.error or 'unknown error'}"
        )
