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
    "Silas authored a fiscal engine that indexed 1.1M ARTs on a blockchain.\n"
    "He modernized an ERP on Jakarta EE."
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


def evd_file(tmp_path: Path, status: str = "verified") -> Path:
    pth = tmp_path / "evidence.json"
    pth.write_text(
        json.dumps(
            {
                "language": "en",
                "evidences": [
                    {
                        "identifier": "sigec",
                        "source": "profile",
                        "content": (
                            "Silas authored a fiscal engine that indexed "
                            "1.1M ARTs on a blockchain."
                        ),
                        "status": status,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return pth


def run(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    prv: ScriptedProvider,
    status: str = "verified",
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)

    return plan_workflow.main(
        [
            "--objective",
            "Write my bio",
            "--capability",
            "bio",
            "--run",
            "--evidence-file",
            str(evd_file(tmp_path, status)),
        ]
    )


def test_bio_flow_runs_through_the_same_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(tmp_path, monkeypatch, ScriptedProvider())

    out = capsys.readouterr().out

    assert code == 0
    assert "- bio-agent" in out
    assert "about-agent" not in out
    assert "indexed 1.1M ARTs" in out


def test_bio_check_rejects_an_invented_number(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(
        tmp_path,
        monkeypatch,
        ScriptedProvider(GROUNDED.replace("1.1M", "9M")),
    )

    assert code == 1
    assert "numbers not in evidence: 9" in capsys.readouterr().err


def test_bio_without_verified_evidence_does_not_call_provider(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = ScriptedProvider()

    code = run(tmp_path, monkeypatch, prv, "unverified")

    assert code == 1
    assert "verified evidence" in capsys.readouterr().err
    assert prv.calls == 0
