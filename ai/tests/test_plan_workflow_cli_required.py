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

BASE = (
    "Silas builds fiscal intelligence systems. He indexed ARTs on a "
    "blockchain.\n\n"
    "He modernized an ERP on Jakarta EE. The work runs in production."
)
WITH_FACT = BASE + " It has 1,577 commits."


class SequenceProvider(LLMProvider):
    def __init__(self, outs: list[str]) -> None:
        self.outs = outs
        self.prompts: list[str] = []

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        idx = min(len(self.prompts), len(self.outs) - 1)
        self.prompts.append(request.messages[-1].content)

        return ProviderResponse(
            content=self.outs[idx],
            provider=self.name,
            model="fake-model",
        )


def evd_file(tmp_path: Path, must: bool) -> Path:
    pth = tmp_path / "evidence.json"
    pth.write_text(
        json.dumps(
            {
                "language": "en",
                "evidences": [
                    {
                        "identifier": "activity",
                        "source": "git",
                        "content": (
                            "Fiscal engine indexed ARTs on a blockchain. "
                            "Git activity: 1,577 commits by the author."
                        ),
                        "status": "verified",
                        "metadata": {"must_mention": ["1,577"]} if must else {},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return pth


def run(
    tmp_path: Path, monkeypatch: MonkeyPatch, prv: SequenceProvider, must: bool
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)

    return plan_workflow.main(
        [
            "--objective",
            "Write about me",
            "--capability",
            "about",
            "--run",
            "--evidence-file",
            str(evd_file(tmp_path, must)),
        ]
    )


def test_a_missing_required_fact_is_retried_with_the_reason(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = SequenceProvider([BASE, WITH_FACT])

    code = run(tmp_path, monkeypatch, prv, must=True)

    assert code == 0
    assert "Mention these facts exactly as written: 1,577." in prv.prompts[0]
    assert "missing required fact: 1,577" in prv.prompts[1]
    assert "It has 1,577 commits." in capsys.readouterr().out


def test_nothing_is_demanded_when_the_evidence_does_not_ask(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    prv = SequenceProvider([BASE])

    code = run(tmp_path, monkeypatch, prv, must=False)

    assert code == 0
    assert len(prv.prompts) == 1
    assert "Mention these facts" not in prv.prompts[0]
