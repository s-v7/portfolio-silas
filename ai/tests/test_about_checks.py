from __future__ import annotations

import pytest

from ai.agents.about_agent import AboutDraft
from ai.agents.base import AgentResult
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import AgentExecutionError
from ai.workflows.about_checks import make_about_check

VALID = (
    "Silas built SIGEC v2. It indexed 1.1M ARTs on a blockchain.\n\n"
    "He modernized SistemaCrea. The platform covers 224 municipalities."
)


def context() -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="sigec",
                source="profile",
                content=(
                    "SIGEC v2 indexed 1.1M ARTs on a blockchain "
                    "and covers 224 municipalities."
                ),
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="planned",
                source="profile",
                content="Plans to reach 900 municipalities.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )


def run_check(text: str) -> None:
    result = AgentResult(
        agent="about-agent",
        output=AboutDraft(content=text, provider="fake", model="fake-model"),
    )

    make_about_check(context())(result)


def test_accepts_a_grounded_two_paragraph_text() -> None:
    run_check(VALID)


def test_rejects_wrong_paragraph_count() -> None:
    with pytest.raises(AgentExecutionError, match="expected 2 paragraphs, found 1"):
        run_check(VALID.replace("\n\n", " "))


def test_rejects_too_few_sentences() -> None:
    with pytest.raises(AgentExecutionError, match="sentences, found 2"):
        run_check("One sentence only.\n\nAnother one.")


def test_rejects_too_many_sentences() -> None:
    text = (
        "Fact one. Fact two. Fact three. Fact four.\n\n"
        "Fact five. Fact six. Fact seven."
    )

    with pytest.raises(AgentExecutionError, match="sentences, found 7"):
        run_check(text)


def test_rejects_forbidden_phrase() -> None:
    text = VALID.replace(
        "Silas built SIGEC v2.",
        "Silas is a passionate engineer. He built SIGEC v2.",
    )

    with pytest.raises(AgentExecutionError, match="forbidden phrase: passionate"):
        run_check(text)


def test_rejects_number_missing_from_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="numbers not in evidence: 5"):
        run_check(VALID.replace("1.1M", "5M"))


def test_unverified_evidence_does_not_ground_numbers() -> None:
    with pytest.raises(AgentExecutionError, match="numbers not in evidence: 900"):
        run_check(VALID.replace("224", "900"))


def test_rejects_markdown_structure() -> None:
    with pytest.raises(AgentExecutionError, match="lists, headers"):
        run_check("# Title\n\n" + VALID)


def test_reports_every_violation_at_once() -> None:
    with pytest.raises(AgentExecutionError) as error:
        run_check("# Title\n\nA passionate sentence with 9.")

    message = str(error.value)

    assert "forbidden phrase: passionate" in message
    assert "numbers not in evidence: 9" in message
    assert "lists, headers" in message
