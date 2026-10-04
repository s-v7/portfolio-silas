from __future__ import annotations

import json
from pathlib import Path

INSIGHTS_PATH = Path("ai/data/ecosystem_insights.json")
REPORT_MD_PATH = Path("ECOSYSTEM_INSIGHTS.md")


def generate_markdown() -> None:
    if not INSIGHTS_PATH.exists():
        raise FileNotFoundError(f"Arquivo '{INSIGHTS_PATH}' não encontrado.")

    data = json.loads(INSIGHTS_PATH.read_text(encoding="utf-8"))
    distribution = data.get("ecosystem_distribution", {})
    total = data.get("total_unique_evidences", 0)

    lines = [
        "# Relatório da Rede Neural - Análise do Ecossistema\n",
        f"**Total de Projetos e Evidências Mapeadas:** {total}\n",
        "## Distribuição por Categoria de Software\n",
        "| Categoria | Qtd. Projetos | Proporção (%) |",
        "| :--- | :---: | :---: |",
    ]

    for cat, metrics in distribution.items():
        lines.append(f"| `{cat}` | {metrics['count']} | {metrics['percentage']:.2f}% |")

    lines.extend([
        "\n## Arquitetura da Rede Neural (PyTorch MLP)",
        "- **Entrada:** Vetorização TF-IDF (Unigramas e Bigramas, 500 features).",
        "- **Camadas Ocultas:** `Linear(500, 128)` -> `BatchNorm1d` -> `ReLU` -> `Dropout(0.3)` -> `Linear(128, 64)` -> `ReLU`.",
        "- **Camada de Saída:** `Linear(64, num_classes)` com Perda Cross-Entropy.",
        "- **Otimizador:** AdamW (Learning Rate: 0.008, Weight Decay: 0.01).",
        "\n---\n*Relatório gerado automaticamente pelo pipeline de IA do Portfolio Silas.*",
    ])

    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Sucesso] Documentação exportada para: '{REPORT_MD_PATH}'")


if __name__ == "__main__":
    generate_markdown()
