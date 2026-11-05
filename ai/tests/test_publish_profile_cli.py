from __future__ import annotations

from pathlib import Path

from pytest import CaptureFixture

from ai.scripts import publish_profile
from ai.services.profile_block import ANCHOR, START

PAGE = f"top\n{ANCHOR}\nbottom\n"


def setup(tmp_path: Path, text: str = "## Projects\n- A") -> tuple[Path, Path]:
    repo = tmp_path / "profile"
    repo.mkdir()
    (repo / "README.md").write_text(PAGE, encoding="utf-8")
    src = tmp_path / "gen.md"
    src.write_text(text, encoding="utf-8")

    return repo, src


def test_updates_the_readme_without_touching_git(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    repo, src = setup(tmp_path)

    code = publish_profile.main(["--repo", str(repo), "--source", str(src)])
    out = (repo / "README.md").read_text(encoding="utf-8")

    assert code == 0
    assert START in out
    assert "## Projects" in out
    assert not (repo / ".git").exists()
    assert "nothing was commited or pushed" in capsys.readouterr().out


def test_a_second_run_reports_no_change(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    repo, src = setup(tmp_path)
    publish_profile.main(["--repo", str(repo), "--source", str(src)])
    capsys.readouterr()

    code = publish_profile.main(["--repo", str(repo), "--source", str(src)])
    assert code == 0

    assert "No change" in capsys.readouterr().out


def test_a_missing_readme_fails_cleanly(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    _, src = setup(tmp_path)

    code = publish_profile.main(
        ["--repo", str(tmp_path / "nope"), "--source", str(src)]
    )

    assert code == 1
    assert "README not found" in capsys.readouterr().err


def test_a_missing_source_leaves_the_readme_untouched(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    repo, _ = setup(tmp_path)

    code = publish_profile.main(
        ["--repo", str(repo), "--source", str(tmp_path / "none.md")]
    )

    assert code == 1
    assert "Generated text not found" in capsys.readouterr().err
    assert (repo / "README.md").read_text(encoding="utf-8") == PAGE
