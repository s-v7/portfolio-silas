from __future__ import annotations

from ai.context.models import PortfolioContext


def required_facts(cxt: PortfolioContext) -> list[str]:
    """Facts that verified evidence marks as mandatory (metadata `must_mention`)."""
    return [
        str(fct)
        for evd in cxt.verified_evidences
        for fct in evd.metadata.get("must_mention", [])
    ]
