from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from typing import Any

from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError

GhRunner = Callable[[list[str]], str]


def run_gh(args: list[str]) -> str:
    try:
        rst = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    except FileNotFoundError as err:
        raise ConfigurationError("GitHub CLI (gh) is not installed.") from err
    except subprocess.CalledProcessError as err:
        raise ConfigurationError(f"gh failed: {err.stderr.strip()}") from err

    return rst.stdout


def parse_pages(txt: str) -> list[dict[str, Any]]:
    """Parse `gh api --paginate` output: several JSON arrays back to back."""
    dec = json.JSONDecoder()
    repos: list[dict[str, Any]] = []
    pos = 0

    while True:
        while pos < len(txt) and txt[pos].isspace():
            pos += 1

        if pos >= len(txt):
            return repos

        try:
            obj, pos = dec.raw_decode(txt, pos)
        except json.JSONDecodeError as err:
            raise ConfigurationError("Unexpected output from gh.") from err

        if not isinstance(obj, list):
            raise ConfigurationError("Unexpected output from gh.")

        repos.extend(item for item in obj if isinstance(item, dict))


def fetch_repos(owner: str, runner: GhRunner | None = None) -> list[dict[str, Any]]:
    out = (runner or run_gh)(
        ["api", "--paginate", f"users/{owner}/repos?per_page=100&type=owner"]
    )

    return parse_pages(out)


def to_evidences(
    repos: list[dict[str, Any]],
    include_forks: bool = False,
) -> tuple[list[dict[str, Any]], int]:
    """Turn repositories into unverified evidence; return them and a skip count."""
    evds: list[dict[str, Any]] = []
    skipped = 0

    for repo in repos:
        name = repo.get("name")
        desc = repo.get("description")
        lang = repo.get("language")
        tpcs = [tpc for tpc in repo.get("topics") or [] if isinstance(tpc, str)]
        desc_txt = desc.strip() if isinstance(desc, str) else ""
        lang_txt = lang.strip() if isinstance(lang, str) else ""

        if not isinstance(name, str) or not name.strip():
            skipped += 1
            continue

        if (repo.get("fork") and not include_forks) or (not desc_txt and not tpcs):
            skipped += 1
            continue

        txt = f"GitHub repository {name.strip()}"

        if desc_txt:
            txt += f": {desc_txt}"

        txt = txt.rstrip(".") + "."

        if lang_txt:
            txt += f" Primary language: {lang_txt}."

        if tpcs:
            txt += f" Topics: {', '.join(tpcs)}."

        meta: dict[str, Any] = {
            "category": "github",
            "techs": ([lang_txt] if lang_txt else []) + tpcs,
        }

        for key in ("html_url", "pushed_at"):
            if isinstance(repo.get(key), str):
                meta["url" if key == "html_url" else key] = repo[key]

        evds.append(
            {
                "identifier": f"github-{name.strip()}",
                "source": "github",
                "content": txt,
                "status": EvidenceStatus.UNVERIFIED.value,
                "metadata": meta,
            }
        )

    return evds, skipped
