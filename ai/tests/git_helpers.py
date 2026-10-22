from __future__ import annotations

import os
import subprocess
from collections.abc import Sequence
from pathlib import Path

ME = "me@example.com"
OTHER = "other@example.com"


def make_repo(
    pth: Path,
    commits: Sequence[tuple[str, str]],
    files: Sequence[str] = (),
) -> Path:
    """Create a real repository: commits are (author e-mail, ISO date) pairs."""
    pth.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "-C", str(pth), "init", "-q"], check=True, capture_output=True
    )

    for nme in files:
        (pth / nme).write_text("x", encoding="utf-8")

    if files:
        subprocess.run(
            ["git", "-C", str(pth), "add", "."], check=True, capture_output=True
        )

    for eml, dte in commits:
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": eml,
            "GIT_AUTHOR_DATE": dte,
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": eml,
            "GIT_COMMITTER_DATE": dte,
        }
        subprocess.run(
            [
                "git", "-C", str(pth), "-c", "commit.gpgsign=false",
                "commit", "--allow-empty", "-q", "-m", "msg",
            ],
            check=True,
            capture_output=True,
            env=env,
        )

    return pth
