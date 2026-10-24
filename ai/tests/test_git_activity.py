from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path

from ai.context.evidence_import import write_evidence_file
from ai.context.git_activity import (
    Activity,
    activity_evidence,
    collect_activity,
    language_counts,
)
from ai.context.json_loader import load_portfolio_context
from ai.tests.git_helpers import ME, OTHER, make_repo

MAR = "2026-03-05T10:00:00-03:00"
MAY = "2026-05-20T10:00:00-03:00"
OLD = "2025-01-01T10:00:00-03:00"


def clone(src: Path, dst: Path) -> Path:
    subprocess.run(
        ["git", "clone", "-q", str(src), str(dst)],
        check=True,
        capture_output=True,
    )
    return dst


def test_language_counts_ignore_generated_folders() -> None:
    cnt = language_counts(
        [
            "a.py",
            "src/b.py",
            "android/app/Main.kt",
            "node_modules/x/y.js",
            "build/z.py",
            "c.java",
            "",
            "README.md",
        ]
    )

    assert cnt == Counter({"Python": 2, "Java": 1})


def test_sums_commits_across_repositories(tmp_path: Path) -> None:
    rep_a = make_repo(tmp_path / "a", [(ME, MAR), (ME, MAY)])
    rep_b = make_repo(tmp_path / "b", [(ME, OLD), (OTHER, MAR)])

    act, skipped, dups = collect_activity([rep_a, rep_b], [ME])

    assert act is not None
    assert (act.repos, act.commits) == (2, 3)
    assert (act.first, act.last) == ("2025-01", "2026-05")
    assert (skipped, dups) == (0, 0)


def test_a_clone_of_the_same_repository_counts_once(tmp_path: Path) -> None:
    src = make_repo(tmp_path / "src", [(ME, MAR), (ME, MAY)])
    cln = clone(src, tmp_path / "copy")

    act, _, dups = collect_activity([src, cln], [ME])

    assert act is not None
    assert (act.repos, act.commits) == (1, 2)
    assert dups == 1


def test_skips_repositories_without_commits_by_the_author(tmp_path: Path) -> None:
    mine = make_repo(tmp_path / "mine", [(ME, MAR)])
    theirs = make_repo(tmp_path / "theirs", [(OTHER, MAY)])
    (tmp_path / "plain").mkdir()

    act, skipped, _ = collect_activity([mine, theirs, tmp_path / "plain"], [ME])

    assert act is not None
    assert (act.repos, act.commits) == (1, 1)
    assert skipped == 2


def test_min_commits_leaves_small_repositories_out(tmp_path: Path) -> None:
    big = make_repo(tmp_path / "big", [(ME, MAR), (ME, MAY)])
    small = make_repo(tmp_path / "small", [(ME, OLD)])

    act, skipped, _ = collect_activity([big, small], [ME], min_commits=2)

    assert act is not None
    assert act.commits == 2
    assert skipped == 1


def test_returns_none_when_nobody_committed(tmp_path: Path) -> None:
    theirs = make_repo(tmp_path / "theirs", [(OTHER, MAR)])

    act, skipped, dups = collect_activity([theirs], [ME])

    assert act is None
    assert (skipped, dups) == (1, 0)


def test_languages_are_summed_across_repositories(tmp_path: Path) -> None:
    rep_a = make_repo(tmp_path / "a", [(ME, MAR)], ["x.py", "y.py"])
    rep_b = make_repo(tmp_path / "b", [(ME, MAY)], ["Z.java"])

    act, _, _ = collect_activity([rep_a, rep_b], [ME])

    assert act is not None
    assert act.languages == ("Python", "Java")


def activity(commits: int = 1642, repos: int = 42) -> Activity:
    return Activity(repos, commits, "2022-04", "2026-10", ("Python", "TypeScript"))


def test_evidence_text_has_a_thousands_separator_and_no_names() -> None:
    evd = activity_evidence(activity())

    assert evd["identifier"] == "git-activity"
    assert evd["status"] == "verified"
    assert evd["content"] == (
        "Git activity across 42 repositories: 1,642 commits by the author, "
        "from 2022-04 to 2026-10. Main languages: Python, TypeScript."
    )


def test_singular_wording() -> None:
    evd = activity_evidence(activity(commits=1, repos=1))

    assert "across 1 repository: 1 commit by the author" in evd["content"]


def test_evidence_file_loads_as_verified(tmp_path: Path) -> None:
    dst = tmp_path / "act.json"
    write_evidence_file([activity_evidence(activity())], dst)

    cxt = load_portfolio_context(dst)

    assert [evd.identifier for evd in cxt.verified_evidences] == ["git-activity"]


def test_evidence_marks_the_commit_total_as_mandatory() -> None:
    assert activity_evidence(activity())["metadata"]["must_mention"] == ["1,642"]
