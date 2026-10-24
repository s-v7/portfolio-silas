from __future__ import annotations

import subprocess
from collections import Counter
from collections.abc import Collection, Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ai.context.git_import import LANGUAGES, TOP_LANGUAGES, GitRunner, run_git
from ai.core.contracts import EvidenceStatus

# Generated or vendored folders say nothing about the author's own code.
IGNORED_PARTS = frozenset(
    {
        "node_modules",
        "vendor",
        "build",
        "dist",
        "target",
        "android",
        "ios",
        "linux",
        "macos",
        "windows",
        "third_party",
        "external",
        ".dart_tool",
    }
)


@dataclass(frozen=True, slots=True)
class Activity:
    repos: int
    commits: int
    first: str
    last: str
    languages: tuple[str, ...]


def language_counts(paths: Iterable[str]) -> Counter[str]:
    cnt: Counter[str] = Counter()

    for pth in paths:
        if not pth:
            continue

        prts = Path(pth).parts

        if any(prt in IGNORED_PARTS for prt in prts[:-1]):
            continue

        if lng := LANGUAGES.get(Path(pth).suffix.lower()):
            cnt[lng] += 1

    return cnt


def _author_commits(
    repo: Path,
    wanted: Collection[str],
    run: GitRunner,
) -> list[tuple[str, datetime]]:
    try:
        log = run(
            [
                "-C",
                str(repo),
                "log",
                "--no-merges",
                "--all",
                "--format=%H%x09%ae%x09%aI",
            ]
        )
    except subprocess.CalledProcessError:
        return []

    out: list[tuple[str, datetime]] = []

    for ln in log.splitlines():
        hsh, _, rest = ln.partition("\t")
        eml, _, iso = rest.partition("\t")

        if hsh and iso.strip() and eml.strip().lower() in wanted:
            out.append((hsh, datetime.fromisoformat(iso.strip())))

    return out


def _tracked_files(repo: Path, run: GitRunner) -> list[str]:
    try:
        return run(["-C", str(repo), "ls-files", "-z"]).split("\0")
    except subprocess.CalledProcessError:
        return []


def collect_activity(
    repos: Iterable[Path],
    emails: Collection[str],
    min_commits: int = 1,
    runner: GitRunner | None = None,
) -> tuple[Activity | None, int, int]:
    """Sum the author's commits; return (activity, skipped, duplicate clones).

    Commits are identified by hash, so a clone of the same project adds nothing.
    """
    run = runner or run_git
    wanted = {eml.lower() for eml in emails}
    found: list[tuple[Path, list[tuple[str, datetime]]]] = []
    skipped = 0

    for repo in repos:
        cms = _author_commits(repo, wanted, run)

        if len(cms) < max(1, min_commits):
            skipped += 1
            continue

        found.append((repo, cms))

    found.sort(key=lambda itm: (-len(itm[1]), str(itm[0])))

    seen: set[str] = set()
    dts: list[datetime] = []
    lngs: Counter[str] = Counter()
    kept = 0
    dups = 0

    for repo, cms in found:
        new = [(hsh, dte) for hsh, dte in cms if hsh not in seen]

        if not new:
            dups += 1
            continue

        seen.update(hsh for hsh, _ in new)
        dts.extend(dte for _, dte in new)
        lngs.update(language_counts(_tracked_files(repo, run)))
        kept += 1

    if not dts:
        return None, skipped, dups

    ranked = sorted(lngs.items(), key=lambda kv: (-kv[1], kv[0]))

    return (
        Activity(
            repos=kept,
            commits=len(dts),
            first=min(dts).strftime("%Y-%m"),
            last=max(dts).strftime("%Y-%m"),
            languages=tuple(nme for nme, _ in ranked[:TOP_LANGUAGES]),
        ),
        skipped,
        dups,
    )


def activity_evidence(act: Activity) -> dict[str, Any]:
    reps = "repository" if act.repos == 1 else "repositories"
    cmt = "commit" if act.commits == 1 else "commits"
    txt = (
        f"In local git history, the author made {act.commits:,} {cmt} "
        f"across {act.repos} {reps}, "
        f"from {act.first} to {act.last}."
    )

    if act.languages:
        txt += f" Main languages: {', '.join(act.languages)}."

    return {
        "identifier": "git-activity",
        "source": "git",
        "content": txt,
        "status": EvidenceStatus.VERIFIED.value,
        "metadata": {
            "category": "git",
            "techs": list(act.languages),
            "commits": act.commits,
            "repositories": act.repos,
            "must_mention": [f"{act.commits:,}"],
        },
    }
