from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai.core.contracts import EvidenceStatus


@dataclass(frozen=True)
class Evidence:
    identifier: str
    source: str
    content: str
    status: EvidenceStatus = EvidenceStatus.UNVERIFIED
    source_path: Path | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PortfolioContext:
    evidences: tuple[Evidence, ...]
    target_file: Path | None = None
    language: str = "pt-BR"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def verified_evidences(self) -> tuple[Evidence, ...]:
        return tuple(
            evidence
            for evidence in self.evidences
            if evidence.status is EvidenceStatus.VERIFIED
        )

    def as_prompt_context(self) -> str:
        sections: list[str] = []

        for evidence in self.verified_evidences:
            sections.append(
                "\n".join(
                    (
                        f"[Evidence: {evidence.identifier}]",
                        f"Source: {evidence.source}",
                        evidence.content.strip(),
                    )
                )
            )

        return "\n\n".join(sections)
