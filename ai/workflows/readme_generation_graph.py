from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from ai.agents.base import AgentResult
from ai.agents.evidence_validator import (
    EvidenceValidationReport,
    EvidenceValidatorAgent,
)
from ai.agents.readme_agent import (
    ReadmeAgent,
    ReadmeAgentInput,
    ReadmeDraft,
)
from ai.context.models import PortfolioContext
from ai.core.exceptions import EvidenceValidationError
from ai.graph import (
    AgentGraph,
    GraphExecutionContext,
    GraphExecutionReport,
    GraphNode,
)
from ai.services.draft_writer import DraftWriter

VALIDATE_EVIDENCE_NODE = "validate-evidence"
GENERATE_README_NODE = "generate-readme"
WRITE_DRAFT_NODE = "write-draft"

README_INPUT_KEY = "readme_input"
RELATIVE_PATH_KEY = "relative_path"


@dataclass(frozen=True, slots=True)
class ReadmeDraftWriteResult:
    destination: Path
    provider: str
    model: str
    evidence_count: int
    rejected_evidence_count: int
    warnings: tuple[str, ...]


class ReadmeGenerationGraph:
    def __init__(
        self,
        readme_agent: ReadmeAgent,
        draft_writer: DraftWriter,
        evidence_validator: EvidenceValidatorAgent[None] | None = None,
    ) -> None:
        self._readme_agent = readme_agent
        self._draft_writer = draft_writer
        self._evidence_validator = (
            evidence_validator or EvidenceValidatorAgent[None]()
        )
        self._graph = self._build_graph()

    def execute(
        self,
        context: PortfolioContext,
        agent_input: ReadmeAgentInput,
        relative_path: str = "README.pt.md",
    ) -> GraphExecutionReport:
        return self._graph.execute(
            portfolio=context,
            inputs={
                README_INPUT_KEY: agent_input,
                RELATIVE_PATH_KEY: relative_path,
            },
        )

    def _build_graph(self) -> AgentGraph:
        graph = AgentGraph("readme-generation")

        graph.add_node(
            GraphNode(
                name=VALIDATE_EVIDENCE_NODE,
                handler=self._validate_evidence,
            )
        )

        graph.add_node(
            GraphNode(
                name=GENERATE_README_NODE,
                dependencies=(VALIDATE_EVIDENCE_NODE,),
                handler=self._generate_readme,
            )
        )

        graph.add_node(
            GraphNode(
                name=WRITE_DRAFT_NODE,
                dependencies=(GENERATE_README_NODE,),
                handler=self._write_draft,
            )
        )

        return graph

    def _validate_evidence(
        self,
        execution: GraphExecutionContext,
    ) -> EvidenceValidationReport:
        result = self._evidence_validator.execute(
            None,
            execution.portfolio,
        )
        validation = result.output

        if not validation.valid:
            raise EvidenceValidationError(
                "No verified evidence is available "
                "for README generation."
            )

        return validation

    def _generate_readme(
        self,
        execution: GraphExecutionContext,
    ) -> AgentResult[ReadmeDraft]:
        validation = cast(
            EvidenceValidationReport,
            execution.get_result(VALIDATE_EVIDENCE_NODE),
        )

        agent_input = cast(
            ReadmeAgentInput,
            execution.get_input(README_INPUT_KEY),
        )

        validated_context = PortfolioContext(
            evidences=validation.verified,
            target_file=execution.portfolio.target_file,
            language=execution.portfolio.language,
            metadata=dict(execution.portfolio.metadata),
        )

        return self._readme_agent.execute(
            agent_input,
            validated_context,
        )

    def _write_draft(
        self,
        execution: GraphExecutionContext,
    ) -> ReadmeDraftWriteResult:
        validation = cast(
            EvidenceValidationReport,
            execution.get_result(VALIDATE_EVIDENCE_NODE),
        )

        agent_result = cast(
            AgentResult[ReadmeDraft],
            execution.get_result(GENERATE_README_NODE),
        )

        relative_path = cast(
            str,
            execution.get_input(
                RELATIVE_PATH_KEY,
                "README.pt.md",
            ),
        )

        destination = self._draft_writer.write(
            relative_path=relative_path,
            content=agent_result.output.content,
        )

        return ReadmeDraftWriteResult(
            destination=destination,
            provider=agent_result.output.provider,
            model=agent_result.output.model,
            evidence_count=len(validation.verified),
            rejected_evidence_count=len(validation.rejected),
            warnings=validation.warnings,
        )
