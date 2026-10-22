from __future__ import annotations

import json
import subprocess
from collections import Counter
from collections.abc import Callable, Collection, Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError

GitRunner = Callable[[list[str]], str]

LANGUAGES: dict[str, str] = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".sql": "SQL",
    ".sh": "Shell",
    ".dart": "Dart",
    ".kt": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
}
TOP_LANGUAGES = 3


@dataclass(frozen=True, slots=True)
class RepoStats:
    name: str
    path: Path
    commits: int
    first: str
    last: str
    languages: tuple[str, ...]


def run_git(args: list[str]) -> str:
    try:
        rst = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            errors="replace",
            check=True,
        )
    except FileNotFoundError as err:
        raise ConfigurationError("git is not installed.") from err

    return rst.stdout


def default_email(runner: GitRunner | None = None) -> str:
    try:
        out = (runner or run_git)(["config", "user.email"]).strip()
    except subprocess.CalledProcessError as err:
        raise ConfigurationError("No author e-mail configured: use --email.") from err

    if not out:
        raise ConfigurationError("No author e-mail configured: use --email.")

    return out


def repos_from_dataset(src: Path) -> list[Path]:
    """Git repositories whose folder holds a file listed in the extractor dataset."""
    try:
        txt = src.read_text(encoding="utf-8")
    except FileNotFoundError as err:
        raise ConfigurationError(f"Evidence dataset does not exist: {src}") from err

    found: set[Path] = set()

    for ln in txt.splitlines():
        if not ln.strip():
            continue

        try:
            rec = json.loads(ln)
        except json.JSONDecodeError:
            continue

        sp = rec.get("source_path") if isinstance(rec, dict) else None

        if not isinstance(sp, str):
            continue

        pth = Path(sp)
        cand = pth if pth.is_dir() else pth.parent

        if (cand / ".git").exists():
            found.add(cand.resolve())

    return sorted(found)


def repo_stats(
    repo: Path,
    emails: Collection[str],
    runner: GitRunner | None = None,
) -> RepoStats | None:
    """Count the author's commits; None when git fails or there are none."""
    run = runner or run_git
    wanted = {eml.lower() for eml in emails}

    try:
        log = run(
            ["-C", str(repo), "log", "--no-merges", "--all", "--format=%ae%x09%aI"]
        )
    except subprocess.CalledProcessError:
        return None

    dts: list[datetime] = []

    for ln in log.splitlines():
        eml, _, iso = ln.partition("\t")

        if iso.strip() and eml.strip().lower() in wanted:
            dts.append(datetime.fromisoformat(iso.strip()))

    if not dts:
        return None

    try:
        fls = run(["-C", str(repo), "ls-files", "-z"]).split("\0")
    except subprocess.CalledProcessError:
        fls = []

    cnt = Counter(
        LANGUAGES[ext]
        for ext in (Path(fil).suffix.lower() for fil in fls if fil)
        if ext in LANGUAGES
    )
    ranked = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))

    return RepoStats(
        name=repo.name,
        path=repo,
        commits=len(dts),
        first=min(dts).strftime("%Y-%m"),
        last=max(dts).strftime("%Y-%m"),
        languages=tuple(nme for nme, _ in ranked[:TOP_LANGUAGES]),
    )


def collect_stats(
    repos: Iterable[Path],
    emails: Collection[str],
    min_commits: int = 1,
    runner: GitRunner | None = None,
) -> tuple[list[RepoStats], int]:
    kept: list[RepoStats] = []
    skipped = 0

    for repo in repos:
        sts = repo_stats(repo, emails, runner)

        if sts is None or sts.commits < min_commits:
            skipped += 1
            continue

        kept.append(sts)

    return kept, skipped


def to_evidences(stats: Iterable[RepoStats]) -> list[dict[str, Any]]:
    seen: Counter[str] = Counter()
    evds: list[dict[str, Any]] = []

    for sts in stats:
        seen[sts.name] += 1
        suffix = "" if seen[sts.name] == 1 else f"-{seen[sts.name]}"
        plural = "" if sts.commits == 1 else "s"
        txt = (
            f"Git history of {sts.name}: {sts.commits} commit{plural} by the "
            f"author, from {sts.first} to {sts.last}."
        )

        if sts.languages:
            txt += f" Main languages: {', '.join(sts.languages)}."

        evds.append(
            {
                "identifier": f"git-{sts.name}{suffix}",
                "source": "git",
                "content": txt,
                "status": EvidenceStatus.VERIFIED.value,
                "source_path": str(sts.path),
                "metadata": {
                    "category": "git",
                    "techs": list(sts.languages),
                    "commits": sts.commits,
                },
            }
        )

    return evds
