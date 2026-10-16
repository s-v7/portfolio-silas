from __future__ import annotations

import re
from collections.abc import Callable

from ai.agents.base import AgentResult
from ai.agents.bio_agent import BioDraft
from ai.context.models import PortfolioContext
from ai.core.exceptions import AgentExecutionError
from ai.workflows.about_checks import (
    AUTHORSHIP_VERBS,
    FORBIDDEN_PHRASES,
    OWNERSHIP_CLAIMS,
)

EXTRA_FORBIDDEN = ("guru", "ninja", "rockstar")
MIN_LINES = 2
MAX_LINES = 3

_NUM = re.compile(r"\d+(?:[.,]\d+)*")
_MD = re.compile(r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|```)|\*\*", re.MULTILINE)


def _has(txt: str, words: tuple[str, ...]) -> bool:
    return any(
        re.search(rf"\b{re.escape(wrd)}\b", txt, re.IGNORECASE) for wrd in words
    )


def find_violations(txt: str, evd_txt: str) -> list[str]:
    bio = txt.strip()
    vios: list[str] = []

    lines = [ln for ln in bio.splitlines() if ln.strip()]
    if not MIN_LINES <= len(lines) <= MAX_LINES:
        vios.append(f"expected {MIN_LINES}-{MAX_LINES} lines, found {len(lines)}")

    for phrase in (*FORBIDDEN_PHRASES, *EXTRA_FORBIDDEN):
        if _has(bio, (phrase,)):
            vios.append(f"forbidden phrase: {phrase}")

    for claim in OWNERSHIP_CLAIMS:
        if _has(bio, (claim,)) and not _has(evd_txt, (claim,)):
            vios.append(f"unsupported ownership claim: {claim}")

    if not _has(evd_txt, AUTHORSHIP_VERBS):
        for verb in AUTHORSHIP_VERBS:
            if _has(bio, (verb,)):
                vios.append(f"unsupported authorship claim: {verb}")

    if _MD.search(bio):
        vios.append("markdown is not allowed")

    nums = set(_NUM.findall(bio))
    if not nums:
        vios.append("expected at least one concrete number")

    unknown = sorted(nums - set(_NUM.findall(evd_txt)))
    if unknown:
        vios.append(f"numbers not in evidence: {', '.join(unknown)}")

    return vios


def make_bio_check(
    cxt: PortfolioContext,
) -> Callable[[AgentResult[BioDraft]], None]:
    evd_txt = "\n".join(evd.content for evd in cxt.verified_evidences)

    def check(rst: AgentResult[BioDraft]) -> None:
        vios = find_violations(rst.output.content, evd_txt)

        if vios:
            raise AgentExecutionError("Bio check failed: " + "; ".join(vios))

    return check
