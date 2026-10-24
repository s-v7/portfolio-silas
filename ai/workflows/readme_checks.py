from __future__ import annotations

import re
from collections.abc import Callable, Iterable

from ai.agents.base import AgentResult
from ai.agents.readme_agent import ReadmeDraft
from ai.context.models import PortfolioContext
from ai.core.exceptions import AgentExecutionError
from ai.workflows.about_checks import (
    AUTHORSHIP_VERBS,
    FORBIDDEN_PHRASES,
    IMPACT_STEMS,
    OWNERSHIP_CLAIMS,
)

PLACEHOLDERS = (
    "example.com",
    "your-username",
    "your_username",
    "lorem ipsum",
    "[link]",
    "](#)",
)

_NUM = re.compile(r"\d+(?:[.,]\d+)*")
_LIST_MARK = re.compile(r"^\s*\d+[.)]\s+", re.MULTILINE)
_URL = re.compile(r"https?://[^\s)>\]\"']+")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_TODO = re.compile(r"\b(?:TODO|TBD)\b")
_FENCE = re.compile(r"^\s*```", re.MULTILINE)


def _has(txt: str, words: Iterable[str]) -> bool:
    return any(
        re.search(rf"\b{re.escape(wrd)}\b", txt, re.IGNORECASE) for wrd in words
    )


def find_violations(txt: str, evd_txt: str) -> list[str]:
    doc = txt.strip()

    if not doc:
        return ["the README is empty"]

    vios: list[str] = []

    for phrase in FORBIDDEN_PHRASES:
        if _has(doc, (phrase,)):
            vios.append(f"forbidden phrase: {phrase}")

    for claim in OWNERSHIP_CLAIMS:
        if _has(doc, (claim,)) and not _has(evd_txt, (claim,)):
            vios.append(f"unsupported ownership claim: {claim}")

    if not _has(evd_txt, AUTHORSHIP_VERBS):
        for verb in AUTHORSHIP_VERBS:
            if _has(doc, (verb,)):
                vios.append(f"unsupported authorship claim: {verb}")

    for stem in IMPACT_STEMS:
        pat = rf"\b{stem}\w*"
        in_doc = re.search(pat, doc, re.IGNORECASE)
        in_evd = re.search(pat, evd_txt, re.IGNORECASE)

        if in_doc and not in_evd:
            vios.append(f"unsupported impact claim: {stem}")

    if _FENCE.search(doc):
        vios.append("code fences are not allowed")

    low = doc.lower()

    for plc in PLACEHOLDERS:
        if plc in low:
            vios.append(f"placeholder text: {plc}")

    if _TODO.search(doc):
        vios.append("placeholder text: TODO/TBD")

    for url in sorted({unk.rstrip(".,;:") for unk in _URL.findall(doc)}):
        if url not in evd_txt:
            vios.append(f"link not in evidence: {url}")

    for eml in sorted(set(_EMAIL.findall(doc))):
        if eml not in evd_txt:
            vios.append(f"e-mail not in evidence: {eml}")

    body = _LIST_MARK.sub("", _URL.sub("", doc))
    unknown = sorted(set(_NUM.findall(body)) - set(_NUM.findall(evd_txt)))

    if unknown:
        vios.append(f"numbers not in evidence: {', '.join(unknown)}")

    return vios


def make_readme_check(
    cxt: PortfolioContext,
) -> Callable[[AgentResult[ReadmeDraft]], None]:
    evd_txt = "\n".join(evd.content for evd in cxt.verified_evidences)

    def check(rst: AgentResult[ReadmeDraft]) -> None:
        vios = find_violations(rst.output.content, evd_txt)

        if vios:
            raise AgentExecutionError(
                "README check failed: "
                + "; ".join(vios)
                + "\n--- rejected text ---\n"
                + rst.output.content
            )

    return check
