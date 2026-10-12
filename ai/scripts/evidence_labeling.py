from __future__ import annotations

import re

# Short or ambiguous keywords must match as whole tokens, otherwise
# "java" matches "javascript", ".c" matches ".css" and "db" matches "feedback".
BOUNDARY_KEYWORDS = frozenset({"java", "node", "db", "vue", ".c", ".sh"})

_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "ai-mcp-llm",
        (
            "mcp",
            "llm",
            "agent",
            "neural",
            "art-analysis",
            "model-spinning",
            "creapi-ai",
            "phantom-search",
            "machine-learning",
        ),
    ),
    (
        "backend-java-enterprise",
        (
            "iped",
            "glassfish",
            "payara",
            "netbeans",
            "sistemacrea",
            "ru-creapi",
            "jakarta",
            "java",
        ),
    ),
    (
        "frontend-node-ts",
        (
            "react",
            "nextjs",
            "typescript",
            "rufrontend",
            "portfolio-silas",
            "frontend",
            "vue",
            "node",
        ),
    ),
    (
        "systems-c-shell",
        (
            "ponteiros",
            "sleuthkit",
            "patch",
            "refactor_sigec",
            "shell",
            ".sh",
            ".c",
        ),
    ),
    (
        "infra-db-tools",
        ("db", "dump", "venv", "schema", "migration", "postgres", "mysql"),
    ),
    (
        "finance-tools",
        ("finance", "financeira", "calculadora", "cal_"),
    ),
    (
        "backend-python",
        ("fastapi", "flask", "django", "crea-fastapi", "trojan", "lotto", "python"),
    ),
)


def _matches(text: str, keyword: str) -> bool:
    if keyword not in BOUNDARY_KEYWORDS:
        return keyword in text

    lead = "" if keyword.startswith(".") else "(?<![a-z0-9])"
    pattern = f"{lead}{re.escape(keyword)}(?![a-z0-9])"

    return re.search(pattern, text) is not None


def heuristic_labeling(
    identifier: str,
    content: str,
    source_path: str = "",
) -> str:
    """Pick an ecosystem category, prioritising project names and exact tokens."""
    text = f"{identifier} {content} {source_path}".lower()

    if "portfolio-silas" in text:
        return "ai-mcp-llm"

    for label, keywords in _RULES:
        if any(_matches(text, keyword) for keyword in keywords):
            return label

    return "general-dev"
