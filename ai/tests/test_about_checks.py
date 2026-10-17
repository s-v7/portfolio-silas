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

FACTS = "SIGEC v2 indexed 1.1M ARTs on a blockchain and covers 224 municipalities."


def context_with(content: str) -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="profile",
                source="profile",
                content=content,
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


def context() -> PortfolioContext:
    return context_with(f"Silas authored SIGEC v2. {FACTS}")


def run_check(text: str, ctx: PortfolioContext | None = None) -> None:
    result = AgentResult(
        agent="about-agent",
        output=AboutDraft(content=text, provider="fake", model="fake-model"),
    )

    make_about_check(ctx or context())(result)


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


def test_rejects_ownership_claim_without_evidence() -> None:
    text = VALID.replace(
        "He modernized SistemaCrea.",
        "He led the SistemaCrea modernization.",
    )

    with pytest.raises(
        AgentExecutionError,
        match="unsupported ownership claim: led",
    ):
        run_check(text)


def test_accepts_ownership_claim_when_evidence_states_it() -> None:
    supported = context_with(
        f"Silas authored SIGEC v2 and led its modernization. "
        f"{FACTS}"
    )
    text = VALID.replace(
        "He modernized SistemaCrea.",
        "He led the SistemaCrea modernization.",
    )

    run_check(text, supported)


def test_rejects_authorship_claim_without_evidence() -> None:
    bare = context_with(FACTS)

    with pytest.raises(
        AgentExecutionError,
        match="unsupported authorship claim: built",
    ):
        run_check(VALID, bare)


def test_authorship_synonym_is_accepted_when_evidence_states_one() -> None:
    run_check(VALID.replace("Silas built SIGEC v2.", "Silas developed SIGEC v2."))


def test_contributed_is_rejected_when_evidence_states_authorship() -> None:
    text = VALID.replace(
        "He modernized SistemaCrea.",
        "He contributed to SistemaCrea.",
    )

    with pytest.raises(
        AgentExecutionError,
        match="unsupported ownership claim: contributed",
    ):
        run_check(text)


def test_rejects_other_verb_forms_of_an_ownership_claim() -> None:
    txt = VALID.replace(
        "He modernized SistemaCrea.",
        "He is contributing to SistemaCrea.",
    )

    with pytest.raises(AgentExecutionError, match="ownership claim: contributing"):
        run_check(txt)


def test_rejects_an_impact_claim_missing_from_the_evidence() -> None:
    txt = VALID.replace(
        "He modernized SistemaCrea.",
        "He enhanced operational efficiency.",
    )

    with pytest.raises(AgentExecutionError, match="impact claim: enhanc"):
        run_check(txt)


def test_accepts_an_impact_word_the_evidence_uses() -> None:
    cxt = context_with(f"Silas authored SIGEC v2 and improved its routing. {FACTS}")
    txt = VALID.replace("He modernized SistemaCrea.", "He improved SistemaCrea.")

    run_check(txt, cxt)


def test_a_system_that_manages_something_is_not_a_role_claim() -> None:
    txt = VALID.replace(
        "The platform covers 224 municipalities.",
        "The platform manages 224 municipalities.",
    )

    run_check(txt)


def test_the_error_shows_the_rejected_text() -> None:
    with pytest.raises(AgentExecutionError) as err:
        run_check(VALID.replace("1.1M", "5M"))

    msg = str(err.value)

    assert "--- rejected text ---" in msg
    assert "It indexed 5M ARTs" in msg
