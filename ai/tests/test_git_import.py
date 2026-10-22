from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from ai.context.evidence_import import write_evidence_file
from ai.context.git_import import (
    RepoStats,
    collect_stats,
    default_email,
    repo_stats,
    repos_from_dataset,
    to_evidences,
)
from ai.context.json_loader import load_portfolio_context
from ai.core.exceptions import ConfigurationError
from ai.tests.git_helpers import ME, OTHER, make_repo

MAR = "2026-03-05T10:00:00-03:00"
MAY = "2026-05-20T10:00:00-03:00"
OLD = "2025-01-01T10:00:00-03:00"


def test_counts_only_the_authors_commits(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(ME, MAR), (ME, MAY), (OTHER, OLD)])

    sts = repo_stats(repo, [ME])

    assert sts is not None
    assert sts.commits == 2
    assert sts.name == "r"


def test_reports_first_and_last_month(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(ME, MAY), (ME, MAR), (OTHER, OLD)])

    sts = repo_stats(repo, [ME])

    assert sts is not None
    assert (sts.first, sts.last) == ("2026-03", "2026-05")


def test_email_match_ignores_case(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(ME, MAR)])

    assert repo_stats(repo, [ME.upper()]) is not None


def test_returns_none_without_commits_by_the_author(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(OTHER, MAR)])

    assert repo_stats(repo, [ME]) is None
    assert repo_stats(make_repo(tmp_path / "empty", []), [ME]) is None


def test_returns_none_for_a_folder_that_is_not_a_repository(tmp_path: Path) -> None:
    (tmp_path / "plain").mkdir()

    assert repo_stats(tmp_path / "plain", [ME]) is None


def test_ranks_languages_by_file_count_and_skips_markup(tmp_path: Path) -> None:
    files = ["a.py", "b.py", "c.java", "d.html", "e.css"]
    repo = make_repo(tmp_path / "r", [(ME, MAR)], files)

    sts = repo_stats(repo, [ME])

    assert sts is not None
    assert sts.languages == ("Python", "Java")


def test_language_ties_are_broken_by_name(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(ME, MAR)], ["x.py", "y.java"])

    sts = repo_stats(repo, [ME])

    assert sts is not None
    assert sts.languages == ("Java", "Python")


def test_collect_stats_counts_skipped_repositories(tmp_path: Path) -> None:
    mine = make_repo(tmp_path / "mine", [(ME, MAR), (ME, MAY)])
    theirs = make_repo(tmp_path / "theirs", [(OTHER, MAR)])
    (tmp_path / "plain").mkdir()
    repos = [mine, theirs, tmp_path / "plain"]

    kept, skipped = collect_stats(repos, [ME])
    none, skipped_all = collect_stats(repos, [ME], min_commits=3)

    assert [sts.name for sts in kept] == ["mine"]
    assert skipped == 2
    assert none == []
    assert skipped_all == 3


def sts(name: str = "svc", commits: int = 3) -> RepoStats:
    return RepoStats(
        name, Path("/x") / name, commits, "2026-03", "2026-05", ("Python",)
    )


def test_evidence_text_and_status() -> None:
    evd = to_evidences([sts()])[0]

    assert evd["identifier"] == "git-svc"
    assert evd["status"] == "verified"
    assert evd["content"] == (
        "Git history of svc: 3 commits by the author, from 2026-03 to 2026-05. "
        "Main languages: Python."
    )
    assert evd["metadata"]["commits"] == 3


def test_singular_commit_wording() -> None:
    assert "1 commit by the author" in to_evidences([sts(commits=1)])[0]["content"]


def test_duplicate_folder_names_get_a_suffix() -> None:
    evds = to_evidences([sts("a"), sts("a"), sts("b")])

    assert [evd["identifier"] for evd in evds] == ["git-a", "git-a-2", "git-b"]


def test_evidence_file_loads_as_verified(tmp_path: Path) -> None:
    dst = tmp_path / "git.json"
    write_evidence_file(to_evidences([sts("a"), sts("b")]), dst)

    cxt = load_portfolio_context(dst)

    assert len(cxt.verified_evidences) == 2
    assert "3 commits by the author" in cxt.as_prompt_context()


def test_repos_from_dataset_finds_repositories_once(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r", [(ME, MAR)])
    (tmp_path / "plain").mkdir()
    src = tmp_path / "dataset.jsonl"
    src.write_text(
        "\n".join(
            [
                json.dumps({"source_path": str(repo / "README.md")}),
                json.dumps({"source_path": str(repo)}),
                json.dumps({"source_path": str(tmp_path / "plain")}),
                json.dumps({"identifier": "no-path"}),
                "",
                "{not json",
            ]
        ),
        encoding="utf-8",
    )

    assert repos_from_dataset(src) == [repo.resolve()]


def test_repos_from_dataset_requires_the_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="does not exist"):
        repos_from_dataset(tmp_path / "missing.jsonl")


def test_default_email_reads_git_config() -> None:
    assert default_email(lambda args: f"{ME}\n") == ME


def test_default_email_reports_a_missing_value() -> None:
    def unset(args: list[str]) -> str:
        raise subprocess.CalledProcessError(1, "git")

    with pytest.raises(ConfigurationError, match="No author e-mail"):
        default_email(unset)
