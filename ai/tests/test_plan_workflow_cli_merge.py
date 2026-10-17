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


class RecordingProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0
        self.last_prompt = ""

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.calls += 1
        self.last_prompt = request.messages[-1].content

        return ProviderResponse(
            content=GROUNDED,
            provider=self.name,
            model="fake-model",
        )


def evd_file(tmp_path: Path, name: str, idf: str, content: str) -> Path:
    pth = tmp_path / name
    pth.write_text(
        json.dumps(
            {
                "language": "en",
                "evidences": [
                    {
                        "identifier": idf,
                        "source": "profile",
                        "content": content,
                        "status": "verified",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return pth


def run(monkeypatch: MonkeyPatch, prv: RecordingProvider, *files: Path) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)

    args = ["--objective", "Write about me", "--capability", "about", "--run"]

    for pth in files:
        args += ["--evidence-file", str(pth)]

    return plan_workflow.main(args)


def test_prompt_contains_evidence_from_every_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    prv = RecordingProvider()
    fst = evd_file(tmp_path, "hand.json", "hand", "Wrote the fiscal engine.")
    snd = evd_file(tmp_path, "imp.json", "imp", "Ran an ERP modernization.")

    code = run(monkeypatch, prv, fst, snd)

    assert code == 0
    assert "Wrote the fiscal engine." in prv.last_prompt
    assert "Ran an ERP modernization." in prv.last_prompt


def test_duplicate_identifier_across_files_fails_before_any_call(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = RecordingProvider()
    fst = evd_file(tmp_path, "a.json", "same", "First.")
    snd = evd_file(tmp_path, "b.json", "same", "Second.")

    code = run(monkeypatch, prv, fst, snd)

    assert code == 1
    assert "Duplicate evidence identifiers: same" in capsys.readouterr().err
    assert prv.calls == 0
