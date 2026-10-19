from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest import CaptureFixture, MonkeyPatch

from ai.context import github_import
from ai.context.json_loader import load_portfolio_context
from ai.core.exceptions import ConfigurationError
from ai.scripts import import_github


def gh_out(*repos: dict[str, Any]) -> str:
    return json.dumps(list(repos))


def repo(name: str, **extra: Any) -> dict[str, Any]:
    return {"name": name, "description": "Does a thing", "language": "Python", **extra}


def test_imports_repositories_as_unverified(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        github_import, "run_gh", lambda args: gh_out(repo("a"), repo("b"))
    )
    out = tmp_path / "gh.json"

    code = import_github.main(["--owner", "o", "--output", str(out)])
    cxt = load_portfolio_context(out)

    assert code == 0
    assert len(cxt.evidences) == 2
    assert cxt.verified_evidences == ()
    assert "Imported 2 repositories (0 skipped)" in capsys.readouterr().out


def test_include_forks_flag_is_passed_through(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        github_import, "run_gh", lambda args: gh_out(repo("a"), repo("c", fork=True))
    )
    plain, withf = tmp_path / "plain.json", tmp_path / "forks.json"

    import_github.main(["--owner", "o", "--output", str(plain)])
    import_github.main(["--owner", "o", "--output", str(withf), "--include-forks"])

    assert len(load_portfolio_context(plain).evidences) == 1
    assert len(load_portfolio_context(withf).evidences) == 2


def test_gh_failure_is_reported_cleanly(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    def fail(args: list[str]) -> str:
        raise ConfigurationError("gh failed: boom")

    monkeypatch.setattr(github_import, "run_gh", fail)

    code = import_github.main(["--owner", "o", "--output", str(tmp_path / "x.json")])

    assert code == 1
    assert "GitHub import failed: gh failed: boom" in capsys.readouterr().err
