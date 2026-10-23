from __future__ import annotations

import subprocess
from pathlib import Path

from pytest import CaptureFixture

from ai.context.json_loader import load_portfolio_context
from ai.scripts import import_git
from ai.tests.git_helpers import ME, OTHER, make_repo

MAR = "2026-03-05T10:00:00-03:00"
MAY = "2026-05-20T10:00:00-03:00"
OLD = "2025-01-01T10:00:00-03:00"


def test_aggregate_writes_one_evidence_without_repository_names(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    rep_a = make_repo(tmp_path / "secret-client-app", [(ME, MAR), (ME, MAY)], ["a.py"])
    rep_b = make_repo(tmp_path / "other", [(ME, OLD)])
    out = tmp_path / "act.json"

    code = import_git.main(
        [
            "--aggregate", "--repo", str(rep_a), "--repo", str(rep_b),
            "--email", ME, "--output", str(out),
        ]
    )
    cxt = load_portfolio_context(out)

    assert code == 0
    assert [evd.identifier for evd in cxt.verified_evidences] == ["git-activity"]
    assert "3 commits" in cxt.evidences[0].content
    assert "2 repositories" in cxt.evidences[0].content
    assert "secret-client-app" not in out.read_text(encoding="utf-8")
    assert "Computed activity across 2 repositories" in capsys.readouterr().out


def test_aggregate_counts_a_clone_once(tmp_path: Path) -> None:
    src = make_repo(tmp_path / "src", [(ME, MAR), (ME, MAY)])
    subprocess.run(
        ["git", "clone", "-q", str(src), str(tmp_path / "copy")],
        check=True,
        capture_output=True,
    )
    out = tmp_path / "act.json"

    import_git.main(
        [
            "--aggregate", "--repo", str(src), "--repo", str(tmp_path / "copy"),
            "--email", ME, "--output", str(out),
        ]
    )

    content = load_portfolio_context(out).evidences[0].content

    assert "2 commits" in content
    assert "1 repository" in content


def test_aggregate_exclude_drops_repositories_by_name(tmp_path: Path) -> None:
    keep = make_repo(tmp_path / "keep", [(ME, MAR), (ME, MAY)])
    drop = make_repo(tmp_path / "IPED", [(ME, OLD)])
    out = tmp_path / "act.json"

    import_git.main(
        [
            "--aggregate", "--repo", str(keep), "--repo", str(drop),
            "--email", ME, "--exclude", "IPED", "--output", str(out),
        ]
    )

    assert "2 commits" in load_portfolio_context(out).evidences[0].content


def test_aggregate_fails_when_nobody_committed(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    theirs = make_repo(tmp_path / "theirs", [(OTHER, MAR)])

    code = import_git.main(
        [
            "--aggregate", "--repo", str(theirs), "--email", ME,
            "--output", str(tmp_path / "act.json"),
        ]
    )

    assert code == 1
    assert "No commits by the author" in capsys.readouterr().err
