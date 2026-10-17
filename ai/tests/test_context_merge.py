from __future__ import annotations

from pathlib import Path

import pytest

from ai.context.merge import merge_contexts
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError


def cxt(
    *idfs: str, language: str = "en", status: EvidenceStatus = EvidenceStatus.VERIFIED
) -> PortfolioContext:
    return PortfolioContext(
        evidences=tuple(
            Evidence(identifier=idf, source="t", content=f"Fact {idf}.", status=status)
            for idf in idfs
        ),
        language=language,
        target_file=Path("README.md"),
    )


def test_keeps_the_evidence_of_every_source_in_order() -> None:
    mrg = merge_contexts([cxt("a", "b"), cxt("c")])

    assert [evd.identifier for evd in mrg.evidences] == ["a", "b", "c"]


def test_language_and_target_come_from_the_first_source() -> None:
    mrg = merge_contexts([cxt("a", language="pt-BR"), cxt("b", language="en")])

    assert mrg.language == "pt-BR"
    assert mrg.target_file == Path("README.md")


def test_keeps_each_evidence_status() -> None:
    mrg = merge_contexts([cxt("a"), cxt("b", status=EvidenceStatus.UNVERIFIED)])

    assert [evd.identifier for evd in mrg.verified_evidences] == ["a"]


def test_duplicate_identifier_is_an_error() -> None:
    with pytest.raises(ConfigurationError, match="Duplicate evidence identifiers: b"):
        merge_contexts([cxt("a", "b"), cxt("b", "c")])


def test_a_single_source_is_returned_as_is() -> None:
    src = cxt("a")

    assert merge_contexts([src]).evidences == src.evidences


def test_requires_at_least_one_source() -> None:
    with pytest.raises(ConfigurationError, match="At least one"):
        merge_contexts([])
