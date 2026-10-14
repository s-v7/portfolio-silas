from __future__ import annotations

from pathlib import Path

from ai.context.json_loader import load_portfolio_context

PROFILE = Path(__file__).resolve().parents[1] / "data" / "profile_evidence.json"


def test_profile_loads_with_english_language() -> None:
    context = load_portfolio_context(PROFILE)

    assert context.language == "en"
    assert context.evidences


def test_every_profile_evidence_is_verified_and_non_empty() -> None:
    context = load_portfolio_context(PROFILE)

    assert len(context.verified_evidences) == len(context.evidences)
    assert all(item.content.strip() for item in context.evidences)


def test_profile_identifiers_are_unique() -> None:
    context = load_portfolio_context(PROFILE)
    identifiers = [item.identifier for item in context.evidences]

    assert len(identifiers) == len(set(identifiers))


def test_crea_pi_role_is_described_as_ended() -> None:
    context = load_portfolio_context(PROFILE)
    role = next(item for item in context.evidences if item.identifier == "crea-pi-role")

    assert "ended" in role.content


def test_sigec_states_authorship_and_leadership() -> None:
    context = load_portfolio_context(PROFILE)
    sigec = next(item for item in context.evidences if item.identifier == "sigec-v2")

    assert "authored" in sigec.content
    assert "led" in sigec.content


def test_sigec_modernization_states_what_it_ran_alongside() -> None:
    context = load_portfolio_context(PROFILE)
    sigec = next(item for item in context.evidences if item.identifier == "sigec-v2")

    assert "in parallel with" in sigec.content
    assert "external APIs" in sigec.content
