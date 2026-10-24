from __future__ import annotations

import pytest

from ai.agents.base import AgentResult
from ai.agents.readme_agent import ReadmeDraft
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import AgentExecutionError
from ai.workflows.readme_checks import make_readme_check

EVD = (
    "Implemented FastAPI endpoints for the SIGEC v2 project on Python 3.12. "
    "Repository: https://github.com/s-v7/portfolio-silas. Contact: me@example.org."
)
GOOD = (
    "# Silas\n\n## Projects\n\n1. SIGEC v2 on Python 3.12\n2. FastAPI endpoints\n\n"
    "Repository: https://github.com/s-v7/portfolio-silas."
)


def cxt_with(content: str = EVD) -> PortfolioContext:
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
        agent="readme-agent",
        output=ReadmeDraft(content=txt, provider="fake", model="fake-model"),
    )

    make_readme_check(cxt or cxt_with())(rst)


def test_accepts_a_grounded_readme() -> None:
    run_check(GOOD)


def test_rejects_a_number_missing_from_the_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="numbers not in evidence: 99"):
        run_check(GOOD + " Handles 99 requests.")


def test_rejects_a_link_missing_from_the_evidence() -> None:
    with pytest.raises(
        AgentExecutionError, match="link not in evidence: https://other.dev/x"
    ):
        run_check(GOOD + "\n\nSee https://other.dev/x.")


def test_rejects_an_email_missing_from_the_evidence() -> None:
    with pytest.raises(
        AgentExecutionError, match="e-mail not in evidence: other@site.dev"
    ):
        run_check(GOOD + "\n\nWrite to other@site.dev")


def test_rejects_placeholder_text() -> None:
    with pytest.raises(AgentExecutionError, match="placeholder text: example.com"):
        run_check(GOOD + "\n\nSee https://example.com")


def test_rejects_todo_markers() -> None:
    with pytest.raises(AgentExecutionError, match="placeholder text: TODO/TBD"):
        run_check(GOOD + "\n\nTODO add docs")


def test_rejects_code_fences() -> None:
    with pytest.raises(AgentExecutionError, match="code fences are not allowed"):
        run_check(GOOD + "\n\n```python\nprint()\n```")


def test_rejects_an_empty_readme() -> None:
    with pytest.raises(AgentExecutionError, match="the README is empty"):
        run_check("   ")


def test_rejects_a_forbidden_phrase() -> None:
    with pytest.raises(AgentExecutionError, match="forbidden phrase: passionate"):
        run_check(GOOD + "\n\nA passionate engineer.")


def test_rejects_an_ownership_claim_without_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="ownership claim: led"):
        run_check(GOOD + "\n\nSilas led the project.")


def test_rejects_an_authorship_claim_without_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="authorship claim: built"):
        run_check(GOOD + "\n\nSilas built the API.")


def test_accepts_authorship_when_the_evidence_states_it() -> None:
    cxt = cxt_with("Silas authored it. " + EVD)

    run_check(GOOD + "\n\nSilas built the API.", cxt)


def test_rejects_an_impact_claim_without_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="impact claim: improv"):
        run_check(GOOD + "\n\nIt improved performance.")


def test_the_error_shows_the_rejected_text() -> None:
    with pytest.raises(AgentExecutionError) as err:
        run_check(GOOD + " Handles 99 requests.")

    msg = str(err.value)

    assert "--- rejected text ---" in msg
    assert "Handles 99 requests." in msg


def test_reports_every_violation_at_once() -> None:
    with pytest.raises(AgentExecutionError) as err:
        run_check("# T\n\nTODO 99 see https://other.dev/x")

    msg = str(err.value)

    assert "placeholder text: TODO/TBD" in msg
    assert "link not in evidence" in msg
    assert "numbers not in evidence: 99" in msg


LONG = (
    "Silas implemented the billing service for municipalities in Piaui with "
    "automated alerts and weekly reports for every active contract in the region."
)


def test_rejects_a_text_that_copies_an_evidence() -> None:
    with pytest.raises(AgentExecutionError, match="copies evidence profile: 100%"):
        run_check(LONG, cxt_with(LONG))


def test_a_short_quote_is_not_a_copy() -> None:
    txt = (
        "# Silas\n\nHe worked on the billing service for municipalities in Piaui "
        "with automated alerts, and also maintains a dozen internal tools used by "
        "many people across several teams every single day of the week."
    )

    run_check(txt, cxt_with(LONG))


def test_dynamic_is_allowed_in_a_readme() -> None:
    run_check(GOOD + "\n\nA dynamic list of projects.")


def test_rejects_a_generic_greeting() -> None:
    with pytest.raises(AgentExecutionError, match="generic greeting: welcome to my"):
        run_check("Welcome to my profile!\n\n" + GOOD)


def test_rejects_a_job_title_the_evidence_does_not_state() -> None:
    with pytest.raises(
        AgentExecutionError, match="unsupported self-description: I am a developer"
    ):
        run_check(GOOD + "\n\nI am a developer.")


def test_accepts_a_self_description_the_evidence_states() -> None:
    run_check(GOOD + "\n\nI am a developer.", cxt_with("Silas is a developer. " + EVD))
