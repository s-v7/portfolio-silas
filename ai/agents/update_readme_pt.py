from __future__ import annotations

from pathlib import Path

from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.json_loader import load_portfolio_context
from ai.providers.factory import ProviderFactory
from ai.services.draft_writer import DraftWriter
from ai.services.readme_generation_service import ReadmeGenerationService

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_FILE = PROJECT_ROOT / "docs" / "evidences.json"  # ou o caminho correto do seu JSON de evidências
OUTPUT_DIR = PROJECT_ROOT / "ai" / "output" / "drafts"


def main() -> None:
    print("[update_readme_pt] Carregando contexto do portfólio...")
    context = load_portfolio_context(EVIDENCE_FILE)
    provider = ProviderFactory.create()

    service = ReadmeGenerationService(
        readme_agent=ReadmeAgent(provider),
        draft_writer=DraftWriter(OUTPUT_DIR),
    )

    print("[update_readme_pt] Gerando README em português...")
    result = service.generate(
        context=context,
        agent_input=ReadmeAgentInput(
            language="pt-BR",
            audience="recrutadores técnicos e gestores de Engenharia",
            title="Silas Vasconcelos Cruz",
        ),
        relative_path="README.pt.md",
    )

    print(f"[update_readme_pt] Rascunho gravado em: {result.destination}")
    print(f"[update_readme_pt] Provedor: {result.provider} | Modelo: {result.model}")


if __name__ == "__main__":
    main()
