from __future__ import annotations

from typing import Any

from ai.context.facts import required_facts
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus


def evd(
    idf: str,
    meta: dict[str, Any],
    status: EvidenceStatus = EvidenceStatus.VERIFIED,
) -> Evidence:
    return Evidence(
        identifier=idf, source="t", content="Fact.", status=status, metadata=meta
    )


def test_collects_the_facts_of_verified_evidence() -> None:
    cxt = PortfolioContext(
        evidences=(
            evd("a", {"must_mention": ["1,577"]}),
            evd("b", {"must_mention": ["41", "2022"]}),
            evd("c", {}),
        )
    )

    assert required_facts(cxt) == ["1,577", "41", "2022"]


def test_ignores_unverified_evidence() -> None:
    cxt = PortfolioContext(
        evidences=(evd("a", {"must_mention": ["9"]}, EvidenceStatus.UNVERIFIED),)
    )

    assert required_facts(cxt) == []


def test_nothing_is_required_by_default() -> None:
    assert required_facts(PortfolioContext(evidences=())) == []
