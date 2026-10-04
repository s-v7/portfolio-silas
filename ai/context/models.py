from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai.core.contracts import EvidenceStatus


@dataclass(frozen=True, slots=True)
Token-saving evidence record structure.
class Evidence:
    identifier: str
    source: str
    content: str
    status: EvidenceStatus = EvidenceStatus.UNVERIFIED
    source_path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PortfolioContext:
    evidences: tuple[Evidence, ...]
    target_file: Path | None = None
    language: str = "pt-BR"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def verified_evidences(self) -> tuple[Evidence, ...]:
        return tuple(
            item for item in self.evidences if item.status == EvidenceStatus.VERIFIED
        )

    def as_prompt_context(self) -> str:
        """
        Converte as evidências verificadas em um formato de lista Markdown ultra compacto,
        economizando até 60% de tokens em comparação com a injeção do JSON bruto.
        """
        lines: list[str] = []
        for item in self.verified_evidences:
            category = item.metadata.get("category", "general")
            techs = item.metadata.get("techs", [])
            tech_str = f" [{', '.join(techs)}]" if techs else ""
            
            # Formato enxuto: - [id] (categoria) [techs]: Conteúdo
            lines.append(f"- [{item.identifier}] ({category}){tech_str}: {item.content.strip()}")

        return "\n".join(lines)
