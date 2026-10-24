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

GOOD = "# README\n\nImplemented FastAPI endpoints."
BAD = "# README\n\nSee https://other.dev/x for 99 things."


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
                        "identifier": "api",
                        "source": "profile",
                        "content": "Implemented FastAPI endpoints.",
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
            "--objective",
            "Profile README",
            "--capability",
            "github",
            "--run",
            "--evidence-file",
            str(evd_file(tmp_path)),
        ]
    )


def test_a_grounded_readme_is_printed_without_retries(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = SequenceProvider([GOOD])

    code = run(tmp_path, monkeypatch, prv)

    assert code == 0
    assert len(prv.prompts) == 1
    assert "Implemented FastAPI endpoints." in capsys.readouterr().out


def test_a_rejected_readme_is_retried_with_the_reason(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    prv = SequenceProvider([BAD, GOOD])

    code = run(tmp_path, monkeypatch, prv)

    assert code == 0
    assert "Your previous answer" not in prv.prompts[0]
    assert "link not in evidence: https://other.dev/x" in prv.prompts[1]
    assert "numbers not in evidence: 99" in prv.prompts[1]
    assert "--- rejected text ---" not in prv.prompts[1]


def test_it_gives_up_after_the_retry_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = SequenceProvider([BAD])

    code = run(tmp_path, monkeypatch, prv)

    assert code == 1
    assert len(prv.prompts) == plan_workflow.MAX_RETRIES + 1
    assert "README check failed" in capsys.readouterr().err
