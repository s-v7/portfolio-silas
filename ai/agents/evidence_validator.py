from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from ai.agents.base import Agent, AgentResult
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus

InputT = TypeVar("InputT")


@dataclass(frozen=True)
class EvidenceValidationReport:
    valid: bool
    verified: tuple[Evidence, ...]
    rejected: tuple[Evidence, ...]
    warnings: tuple[str, ...]


class EvidenceValidatorAgent(
    Agent[InputT, EvidenceValidationReport],
    Generic[InputT],
):
    name = "evidence-validator"
    responsibility = "Validate evidence before content generation."

    def execute(
        self,
        agent_input: InputT,
        context: PortfolioContext,
    ) -> AgentResult[EvidenceValidationReport]:
        del agent_input

        verified = tuple(
            item
            for item in context.evidences
            if item.status is EvidenceStatus.VERIFIED
            and item.content.strip()
        )

        rejected = tuple(
            item
            for item in context.evidences
            if item not in verified
        )

        warnings = tuple(
            (
                f"Evidence '{item.identifier}' was not accepted: "
                f"status={item.status.value}."
            )
            for item in rejected
        )

        report = EvidenceValidationReport(
            valid=bool(verified),
            verified=verified,
            rejected=rejected,
            warnings=warnings,
        )

        return AgentResult(
            agent=self.name,
            output=report,
            metadata={
                "verified_count": len(verified),
                "rejected_count": len(rejected),
            },
        )
