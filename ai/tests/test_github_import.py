from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
from pytest import MonkeyPatch

from ai.context import github_import
from ai.context.evidence_import import promote, write_evidence_file
from ai.context.github_import import fetch_repos, parse_pages, to_evidences
from ai.context.json_loader import load_portfolio_context
from ai.core.exceptions import ConfigurationError


def repo(name: str = "svc", **extra: Any) -> dict[str, Any]:
    return {"name": name, "description": "Does a thing", "language": "Python", **extra}


def test_parses_paginated_output_with_several_arrays() -> None:
    out = json.dumps([repo("a")]) + "\n" + json.dumps([repo("b")])

    assert [item["name"] for item in parse_pages(out)] == ["a", "b"]


def test_rejects_output_that_is_not_a_list_of_repositories() -> None:
    with pytest.raises(ConfigurationError, match="Unexpected output"):
        parse_pages('{"message": "Not Found"}')

    with pytest.raises(ConfigurationError, match="Unexpected output"):
        parse_pages("not json")


def test_forks_are_left_out_unless_requested() -> None:
    repos = [repo("mine"), repo("copy", fork=True)]

    kept, skipped = to_evidences(repos)
    with_forks, _ = to_evidences(repos, include_forks=True)

    assert [evd["identifier"] for evd in kept] == ["github-mine"]
    assert skipped == 1
    assert len(with_forks) == 2


def test_skips_repositories_with_nothing_to_say() -> None:
    bare: dict[str, Any] = {
        "name": "empty",
        "description": None,
        "topics": [],
        "language": "C",
    }

    evds, skipped = to_evidences([bare, {"description": "no name"}])

    assert evds == []
    assert skipped == 2


def test_builds_content_and_techs_from_the_repository() -> None:
    item = repo(
        "svc",
        description="Fiscal bot.",
        topics=["telegram", "alerts"],
        html_url="https://github.com/o/svc",
    )

    evd = to_evidences([item])[0][0]

    assert evd["content"] == (
        "GitHub repository svc: Fiscal bot. Primary language: Python. "
        "Topics: telegram, alerts."
    )
    assert evd["status"] == "unverified"
    assert evd["metadata"]["techs"] == ["Python", "telegram", "alerts"]
    assert evd["metadata"]["url"] == "https://github.com/o/svc"


def test_fetch_passes_the_owner_to_gh() -> None:
    seen: list[list[str]] = []

    def runner(args: list[str]) -> str:
        seen.append(args)
        return json.dumps([repo("a")])

    repos = fetch_repos("s-v7", runner)

    assert repos[0]["name"] == "a"
    assert "users/s-v7/repos?per_page=100&type=owner" in seen[0]


def test_missing_gh_is_reported(monkeypatch: MonkeyPatch) -> None:
    def boom(*args: Any, **kwargs: Any) -> Any:
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", boom)

    with pytest.raises(ConfigurationError, match="not installed"):
        github_import.run_gh(["api", "x"])


def test_gh_failure_includes_its_message(monkeypatch: MonkeyPatch) -> None:
    def fail(*args: Any, **kwargs: Any) -> Any:
        raise subprocess.CalledProcessError(1, "gh", stderr="HTTP 404 Not Found")

    monkeypatch.setattr(subprocess, "run", fail)

    with pytest.raises(ConfigurationError, match="HTTP 404"):
        github_import.run_gh(["api", "x"])


def test_written_file_loads_and_only_promoted_items_are_verified(
    tmp_path: Path,
) -> None:
    evds, _ = to_evidences([repo("a"), repo("b")])
    dst = tmp_path / "gh.json"
    write_evidence_file(evds, dst)

    assert load_portfolio_context(dst).verified_evidences == ()

    promote(dst, ["github-b"])
    ids = [evd.identifier for evd in load_portfolio_context(dst).verified_evidences]

    assert ids == ["github-b"]
