from __future__ import annotations

import pytest

from ai.agents.base import AgentResult
from ai.agents.bio_agent import BioDraft
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import AgentExecutionError
from ai.workflows.bio_checks import make_bio_check

VALID = (
    "Silas built a fiscal engine that indexed 1.1M ARTs on a blockchain.\n"
    "He modernized an ERP on Jakarta EE."
)
FACTS = "Silas authored a fiscal engine that indexed 1.1M ARTs on a blockchain."


def cxt_with(content: str) -> PortfolioContext:
    return PortfolioContext(
        evidences=(
            Evidence(
                identifier="profile",
                source="profile",
                content=content,
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )


def run_check(txt: str, cxt: PortfolioContext | None = None) -> None:
    rst = AgentResult(
        agent="bio-agent",
        output=BioDraft(content=txt, provider="fake", model="fake-model"),
    )

    make_bio_check(cxt or cxt_with(FACTS))(rst)


def test_accepts_a_grounded_two_line_bio() -> None:
    run_check(VALID)


def test_rejects_a_single_line() -> None:
    with pytest.raises(AgentExecutionError, match="expected 2-3 lines, found 1"):
        run_check("Silas built a fiscal engine that indexed 1.1M ARTs.")


def test_rejects_four_lines() -> None:
    with pytest.raises(AgentExecutionError, match="expected 2-3 lines, found 4"):
        run_check(VALID + "\nLine three about 1.1M.\nLine four.")


def test_rejects_markdown() -> None:
    with pytest.raises(AgentExecutionError, match="markdown is not allowed"):
        run_check("- " + VALID)


def test_rejects_forbidden_phrase() -> None:
    with pytest.raises(AgentExecutionError, match="forbidden phrase: ninja"):
        run_check(VALID.replace("He modernized", "A ninja who modernized"))


def test_rejects_number_missing_from_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="numbers not in evidence: 9"):
        run_check(VALID.replace("1.1M", "9M"))


def test_requires_at_least_one_number() -> None:
    with pytest.raises(AgentExecutionError, match="at least one concrete number"):
        run_check("Silas built a fiscal engine.\nHe modernized an ERP.")


def test_rejects_ownership_claim_without_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="ownership claim: led"):
        run_check(VALID.replace("He modernized", "He led"))


def test_rejects_authorship_claim_without_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="authorship claim: built"):
        run_check(VALID, cxt_with("A fiscal engine indexed 1.1M ARTs."))
