from __future__ import annotations

from typing import Any

from ai.scripts.generate_markdown_report import build_markdown


def cls(idf: str, cat: str) -> dict[str, str]:
    return {"identifier": idf, "predicted_category": cat}


DATA: dict[str, Any] = {
    "ecosystem_distribution": {"a": {}, "b": {}},
    "classifications": [
        cls("p1-readme", "a"),
        cls("p2-readme", "a"),
        cls("p3-readme", "b"),
        cls("p3-changelog", "b"),
        cls("d1-struct", "a"),
        cls("d2-struct", "a"),
    ],
}
METRICS: dict[str, Any] = {
    "test_accuracy": 0.625,
    "test_examples": 8,
    "majority_baseline": 0.5,
}


def test_counts_only_readmes_and_changelogs() -> None:
    out = build_markdown(DATA, None)

    assert "**Evidências analisadas (README e CHANGELOG):** 4" in out
    assert "| `a` | 2 | 50.00% |" in out
    assert "| `b` | 2 | 50.00% |" in out


def test_reports_the_folder_summaries_left_out() -> None:
    assert "2 resumos de pasta ficaram de fora" in build_markdown(DATA, None)


def test_calls_the_rows_evidence_and_not_projects() -> None:
    out = build_markdown(DATA, None)

    assert "Qtd. Evidências" in out
    assert "Qtd. Projetos" not in out
    assert "heurísticas" in out


def test_shows_held_out_accuracy_next_to_the_baseline() -> None:
    out = build_markdown(DATA, METRICS)

    assert "**Acurácia em dados separados:** 62.5% (8 exemplos de teste)" in out
    assert "**Linha de base (sempre a classe mais comum):** 50.0%" in out
    assert "imita a regra" in out


def test_says_so_when_there_is_no_held_out_evaluation() -> None:
    assert "Sem avaliação em dados separados." in build_markdown(DATA, None)


def test_an_empty_dataset_does_not_divide_by_zero() -> None:
    out = build_markdown({"classifications": []}, None)

    assert "**Evidências analisadas (README e CHANGELOG):** 0" in out
