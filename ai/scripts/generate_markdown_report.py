from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from ai.scripts.evidence_dataset import TRAINABLE_KINDS, record_kind

INSIGHTS_PATH = Path("ai/data/ecosystem_insights.json")
METRICS_PATH = Path("ai/models/metrics.json")
REPORT_MD_PATH = Path("ECOSYSTEM_INSIGHTS.md")


def _metrics_lines(metrics: dict[str, Any] | None) -> list[str]:
    if not metrics or metrics.get("test_accuracy") is None:
        return ["Sem avaliação em dados separados."]

    out = [
        f"- **Acurácia em dados separados:** {metrics['test_accuracy'] * 100:.1f}% "
        f"({metrics['test_examples']} exemplos de teste)",
    ]

    if metrics.get("majority_baseline") is not None:
        out.append(
            "- **Linha de base (sempre a classe mais comum):** "
            f"{metrics['majority_baseline'] * 100:.1f}%"
        )

    out.append(
        "- Os rótulos vêm de uma regra, então a acurácia mede o quanto a rede "
        "imita a regra, não a verdade sobre os projetos."
    )

    return out


def build_markdown(data: dict[str, Any], metrics: dict[str, Any] | None) -> str:
    cls = data.get("classifications", [])
    kept = [item for item in cls if record_kind(item["identifier"]) in TRAINABLE_KINDS]
    cnt = Counter(item["predicted_category"] for item in kept)
    cats = list(data.get("ecosystem_distribution", {})) or sorted(cnt)
    total = len(kept)
    left_out = len(cls) - total

    lines = [
        "# Relatório da Rede Neural - Análise do Ecossistema\n",
        f"**Evidências analisadas (README e CHANGELOG):** {total}\n",
        f"{left_out} resumos de pasta ficaram de fora: eles listam só extensões "
        "e nomes de arquivo.\n",
        "## Distribuição por Categoria de Software\n",
        "As categorias são heurísticas (regras sobre o texto), não uma "
        "classificação verificada.\n",
        "| Categoria | Qtd. Evidências | Proporção (%) |",
        "| :--- | :---: | :---: |",
    ]

    for cat in cats:
        pct = cnt[cat] / total * 100 if total else 0.0
        lines.append(f"| `{cat}` | {cnt[cat]} | {pct:.2f}% |")

    lines.extend(["\n## Avaliação\n", *_metrics_lines(metrics)])

    lines.extend(
        [
            "\n## Arquitetura da Rede Neural (PyTorch MLP)",
            "- **Entrada:** Vetorização TF-IDF (Unigramas e Bigramas, 500 features).",
            "- **Camadas Ocultas:** `Linear(500, 128)` -> `BatchNorm1d` -> `ReLU` "
            "-> `Dropout(0.3)` -> `Linear(128, 64)` -> `ReLU`.",
            "- **Camada de Saída:** `Linear(64, num_classes)` com Perda "
            "Cross-Entropy.",
            "- **Otimizador:** AdamW (Learning Rate: 0.008, Weight Decay: 0.01).",
            "\n---\n*Relatório gerado automaticamente pelo pipeline de IA do "
            "Portfolio Silas.*",
        ]
    )

    return "\n".join(lines)


def generate_markdown() -> None:
    if not INSIGHTS_PATH.exists():
        raise FileNotFoundError(f"Arquivo '{INSIGHTS_PATH}' não encontrado.")

    data = json.loads(INSIGHTS_PATH.read_text(encoding="utf-8"))
    metrics = (
        json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        if METRICS_PATH.exists()
        else None
    )

    REPORT_MD_PATH.write_text(build_markdown(data, metrics), encoding="utf-8")
    print(f"[Sucesso] Documentação exportada para: '{REPORT_MD_PATH}'")


if __name__ == "__main__":
    generate_markdown()
