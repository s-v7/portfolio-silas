from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.scripts import plan_workflow

GROUNDED = (
    "Silas builds fiscal intelligence systems. He indexed ARTs on a "
    "blockchain.\n\n"
    "He modernized an ERP on Jakarta EE. The work runs in production."
)


class ScriptedProvider(LLMProvider):
    def __init__(self, content: str = GROUNDED) -> None:
        self.content = content
        self.calls = 0

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        self.calls += 1

        return ProviderResponse(
            content=self.content,
            provider=self.name,
            model="fake-model",
        )


def evidence_file(tmp_path: Path, status: str = "verified") -> Path:
    path = tmp_path / "evidence.json"
    path.write_text(
        json.dumps(
            {
                "language": "en",
                "evidences": [
                    {
                        "identifier": "sigec",
                        "source": "profile",
                        "content": "Fiscal engine indexed ARTs on a blockchain.",
                        "status": status,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def run(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    provider: ScriptedProvider,
    capability: str,
    status: str = "verified",
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: provider)

    return plan_workflow.main(
        [
            "--objective",
            "Write about me",
            "--capability",
            capability,
            "--run",
            "--evidence-file",
            str(evidence_file(tmp_path, status)),
        ]
    )


def test_about_flow_runs_through_the_same_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    exit_code = run(tmp_path, monkeypatch, ScriptedProvider(), "about")

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "- about-agent" in output
    assert "readme-agent" not in output
    assert "Silas builds fiscal intelligence systems." in output


def test_about_check_rejects_an_invented_number(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    invented = GROUNDED.replace(
        "The work runs in production.",
        "The work runs in production. It covers 999 municipalities.",
    )

    exit_code = run(tmp_path, monkeypatch, ScriptedProvider(invented), "about")

    assert exit_code == 1
    assert "numbers not in evidence: 999" in capsys.readouterr().err


def test_about_without_verified_evidence_fails_cleanly(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    provider = ScriptedProvider()

    exit_code = run(tmp_path, monkeypatch, provider, "about", "unverified")

    assert exit_code == 1
    assert "requires verified evidence" in capsys.readouterr().err
    assert provider.calls == 0


def test_portfolio_run_validates_then_generates_both(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    provider = ScriptedProvider()

    exit_code = run(tmp_path, monkeypatch, provider, "portfolio")

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "- evidence-validator" in output
    assert "[readme-agent]" in output
    assert "[about-agent]" in output
    assert provider.calls == 2
