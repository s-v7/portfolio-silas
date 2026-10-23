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
TOO_LONG = GROUNDED + " Fifth fact. Sixth fact. Seventh fact. Eighth fact."


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


def evd_file(tmp_path: Path) -> Path:
    pth = tmp_path / "evidence.json"
    pth.write_text(
        json.dumps(
            {
                "language": "en",
                "evidences": [
                    {
                        "identifier": "sigec",
                        "source": "profile",
                        "content": "Fiscal engine indexed ARTs on a blockchain.",
                        "status": "verified",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return pth


def run(tmp_path: Path, monkeypatch: MonkeyPatch, prv: SequenceProvider) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)

    return plan_workflow.main(
        [
            "--objective", "Write about me", "--capability", "about", "--run",
            "--evidence-file", str(evd_file(tmp_path)),
        ]
    )


def test_a_rejected_text_is_retried_with_the_reason(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = SequenceProvider([TOO_LONG, GROUNDED])

    code = run(tmp_path, monkeypatch, prv)

    assert code == 0
    assert len(prv.prompts) == 2
    assert "Your previous answer" not in prv.prompts[0]
    assert (
        "Your previous answer was rejected: About check failed: "
        "expected 4-7 sentences, found 8"
    ) in prv.prompts[1]
    assert "Silas builds fiscal intelligence systems." in capsys.readouterr().out


def test_it_gives_up_after_the_retry_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = SequenceProvider([TOO_LONG])

    code = run(tmp_path, monkeypatch, prv)

    assert code == 1
    assert len(prv.prompts) == plan_workflow.MAX_RETRIES + 1
    assert "found 8" in capsys.readouterr().err


def test_only_the_about_and_bio_flows_are_retried() -> None:
    assert set(plan_workflow.RETRY_INPUTS) == {"about-agent", "bio-agent"}
