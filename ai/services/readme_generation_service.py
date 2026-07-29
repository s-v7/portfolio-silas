from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import PortfolioContext
from ai.core.exceptions import EvidenceValidationError
from ai.services.draft_writer import DraftWriter


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
        self._readme_agent = readme_agent
        self._draft_writer = draft_writer
        self._evidence_validator = (
            evidence_validator
            or EvidenceValidatorAgent[None]()
        )

    def generate(
        self,
        context: PortfolioContext,
        agent_input: ReadmeAgentInput,
        relative_path: str = "README.pt.md",
    ) -> ReadmeGenerationResult:
        validation_result = self._evidence_validator.execute(
            None,
            context,
        )
        validation = validation_result.output

        if not validation.verified:
            raise EvidenceValidationError(
                "No verified evidence is available "
                "for README generation."
            )

        validated_context = PortfolioContext(
            evidences=tuple(validation.verified),
            target_file=context.target_file,
            language=context.language,
            metadata=dict(context.metadata),
        )

        agent_result = self._readme_agent.execute(
            agent_input,
            validated_context,
        )

        destination = self._draft_writer.write(
            relative_path=relative_path,
            content=agent_result.output.content,
        )

        return ReadmeGenerationResult(
            destination=destination,
            provider=agent_result.output.provider,
            model=agent_result.output.model,
            evidence_count=len(validation.verified),
            rejected_evidence_count=len(
                validation.rejected
            ),
            warnings=tuple(validation.warnings),
        )
