from __future__ import annotations

import pytest

from ai.scripts.evidence_labeling import heuristic_labeling


@pytest.mark.parametrize(
    ("identifier", "content", "expected"),
    [
        ("local-portfolio-silas-readme", "Site pessoal", "ai-mcp-llm"),
        ("local-engine", "Orquestra agent com mcp", "ai-mcp-llm"),
        (
            "local-app",
            "Aplicacao backend em java com jakarta",
            "backend-java-enterprise",
        ),
        ("local-iped-readme", "Ferramenta forense", "backend-java-enterprise"),
        ("local-svc", "Calculadora financeira", "finance-tools"),
        ("local-api", "Servico em FastAPI", "backend-python"),
        ("local-x", "build com node e vue", "frontend-node-ts"),
        ("local-notes", "arquivo main.c com funcoes", "systems-c-shell"),
        ("local-db_dumps-struct", "estrutura", "infra-db-tools"),
    ],
)
def test_labels_keep_expected_categories(
    identifier: str,
    content: str,
    expected: str,
) -> None:
    assert heuristic_labeling(identifier, content) == expected


def test_java_does_not_match_javascript() -> None:
    label = heuristic_labeling("local-spa", "React app em javascript")

    assert label == "frontend-node-ts"


def test_c_extension_does_not_match_css() -> None:
    label = heuristic_labeling("local-site", "arquivo styles.css e index.html")

    assert label == "general-dev"


def test_db_does_not_match_feedback() -> None:
    label = heuristic_labeling("local-forms", "formulario de feedback dos usuarios")

    assert label == "general-dev"
