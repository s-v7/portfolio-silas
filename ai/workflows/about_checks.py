from __future__ import annotations

import re
from collections.abc import Callable

from ai.agents.about_agent import AboutDraft
from ai.agents.base import AgentResult
from ai.context.models import PortfolioContext
from ai.core.exceptions import AgentExecutionError

FORBIDDEN_PHRASES = (
    "seasoned",
    "passionate",
    "dedicated",
    "leverage",
    "synergy",
    "results-driven",
    "dynamic",
    "innovative",
    "hard-working",
    "years of experience",
)

OWNERSHIP_CLAIMS = (
    "led",
    "leads",
    "spearheaded",
    "architected",
    "pioneered",
    "headed",
    "directed",
    "managed",
    "owned",
)

EXPECTED_PARAGRAPHS = 2
MIN_SENTENCES = 4
MAX_SENTENCES = 6

_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_MARKDOWN_STRUCTURE = re.compile(
    r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|```)",
    re.MULTILINE,
)


def find_violations(text: str, evidence_text: str) -> list[str]:
    stripped = text.strip()
    violations: list[str] = []

    paragraphs = [p for p in _PARAGRAPH_BREAK.split(stripped) if p.strip()]
    if len(paragraphs) != EXPECTED_PARAGRAPHS:
        violations.append(
            f"expected {EXPECTED_PARAGRAPHS} paragraphs, found {len(paragraphs)}"
        )

    sentences = [s for s in _SENTENCE_END.split(stripped) if s.strip()]
    if not MIN_SENTENCES <= len(sentences) <= MAX_SENTENCES:
        violations.append(
            f"expected {MIN_SENTENCES}-{MAX_SENTENCES} sentences, "
            f"found {len(sentences)}"
        )

    for phrase in FORBIDDEN_PHRASES:
        if re.search(rf"\b{re.escape(phrase)}\b", stripped, re.IGNORECASE):
            violations.append(f"forbidden phrase: {phrase}")

    for claim in OWNERSHIP_CLAIMS:
        pattern = rf"\b{claim}\b"
        in_text = re.search(pattern, stripped, re.IGNORECASE)
        in_evidence = re.search(pattern, evidence_text, re.IGNORECASE)

        if in_text and not in_evidence:
            violations.append(f"unsupported ownership claim: {claim}")

    if _MARKDOWN_STRUCTURE.search(stripped):
        violations.append("lists, headers and code blocks are not allowed")

    known_numbers = set(_NUMBER.findall(evidence_text))
    unknown = sorted(set(_NUMBER.findall(stripped)) - known_numbers)
    if unknown:
        violations.append(f"numbers not in evidence: {', '.join(unknown)}")

    return violations


def make_about_check(
    context: PortfolioContext,
) -> Callable[[AgentResult[AboutDraft]], None]:
    evidence_text = "\n".join(
        evidence.content for evidence in context.verified_evidences
    )

    def check(result: AgentResult[AboutDraft]) -> None:
        violations = find_violations(result.output.content, evidence_text)

        if violations:
            raise AgentExecutionError(
                "About check failed: " + "; ".join(violations)
            )

    return check
