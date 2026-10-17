from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from ai.context.models import PortfolioContext
from ai.core.exceptions import ConfigurationError


def merge_contexts(cxts: Sequence[PortfolioContext]) -> PortfolioContext:
    """Join evidence from several sources; language and target come from the first."""
    if not cxts:
        raise ConfigurationError("At least one evidence source is required.")

    seen: set[str] = set()
    dups: set[str] = set()

    for cxt in cxts:
        for evd in cxt.evidences:
            if evd.identifier in seen:
                dups.add(evd.identifier)

            seen.add(evd.identifier)

    if dups:
        raise ConfigurationError(
            "Duplicate evidence identifiers: " + ", ".join(sorted(dups))
        )

    return replace(
        cxts[0],
        evidences=tuple(evd for cxt in cxts for evd in cxt.evidences),
    )
