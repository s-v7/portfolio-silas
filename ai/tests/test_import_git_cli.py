from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from ai.context import git_import
from ai.context.json_loader import load_portfolio_context
from ai.scripts import import_git
from ai.tests.git_helpers import ME, OTHER, make_repo

MAR = "2026-03-05T10:00:00-03:00"
MAY = "2026-05-20T10:00:00-03:00"


def test_imports_a_repository_as_verified_evidence(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    repo = make_repo(tmp_path / "svc", [(ME, MAR), (ME, MAY)], ["a.py"])
    out = tmp_path / "git.json"

    code = import_git.main(
        ["--repo", str(repo), "--email", ME, "--output", str(out)]
    )
    cxt = load_portfolio_context(out)

    assert code == 0
    assert [evd.identifier for evd in cxt.verified_evidences] == ["git-svc"]
    assert "Imported 1 repositories (0 skipped)" in capsys.readouterr().out


def test_reports_skipped_repositories(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    mine = make_repo(tmp_path / "mine", [(ME, MAR)])
    theirs = make_repo(tmp_path / "theirs", [(OTHER, MAR)])

    code = import_git.main(
        [
            "--repo", str(mine), "--repo", str(theirs),
            "--email", ME, "--output", str(tmp_path / "git.json"),
        ]
    )

    assert code == 0
    assert "Imported 1 repositories (1 skipped)" in capsys.readouterr().out


def test_exclude_drops_repositories_by_folder_name(tmp_path: Path) -> None:
    keep = make_repo(tmp_path / "keep", [(ME, MAR)])
    drop = make_repo(tmp_path / "IPED", [(ME, MAR)])
    out = tmp_path / "git.json"

    import_git.main(
        [
            "--repo", str(keep), "--repo", str(drop), "--email", ME,
            "--exclude", "IPED", "--output", str(out),
        ]
    )

    ids = [evd.identifier for evd in load_portfolio_context(out).evidences]

    assert ids == ["git-keep"]


def test_scans_the_dataset_when_no_repo_is_given(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "svc", [(ME, MAR)])
    src = tmp_path / "dataset.jsonl"
    src.write_text(
        json.dumps({"source_path": str(repo / "README.md")}) + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "git.json"

    code = import_git.main(
        ["--dataset", str(src), "--email", ME, "--output", str(out)]
    )

    assert code == 0
    assert len(load_portfolio_context(out).evidences) == 1


def test_missing_dataset_fails_cleanly(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    code = import_git.main(
        ["--dataset", str(tmp_path / "none.jsonl"), "--email", ME]
    )

    assert code == 1
    assert "Git import failed" in capsys.readouterr().err


def test_missing_email_fails_cleanly(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    def unset(args: list[str]) -> str:
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr(git_import, "run_git", unset)

    code = import_git.main(["--repo", "x"])

    assert code == 1
    assert "No author e-mail" in capsys.readouterr().err
