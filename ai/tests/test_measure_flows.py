from __future__ import annotations

import json
from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.scripts import measure_flows, plan_workflow

ABOUT = (
    "Silas builds fiscal intelligence systems. He indexed ARTs on a "
    "blockchain.\n\n"
    "He modernized an ERP on Jakarta EE. The work runs in production."
)
BIO = (
    "Silas authored a fiscal engine that indexed 1.1M ARTs on a blockchain.\n"
    "He modernized an ERP on Jakarta EE."
)
INVENTED = " It covers 999 municipalities."


class ScriptedProvider(LLMProvider):
    def __init__(self, invent: bool = False) -> None:
        self.invent = invent
        self.calls = 0

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.calls += 1
        about = "About section" in request.messages[-1].content
        txt = ABOUT if about else BIO

        if self.invent:
            txt += INVENTED if about else "\nIt covers 999 municipalities."

        return ProviderResponse(content=txt, provider=self.name, model="fake-model")


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
                        "content": (
                            "Silas authored a fiscal engine that indexed "
                            "1.1M ARTs on a blockchain."
                        ),
                        "status": "verified",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return pth


def measure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    prv: ScriptedProvider,
    *args: str,
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)

    return measure_flows.main(["--evidence-file", str(evd_file(tmp_path)), *args])


def test_counts_approvals_for_both_flows(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = ScriptedProvider()

    code = measure(tmp_path, monkeypatch, prv, "--runs", "2")
    out = capsys.readouterr().out

    assert code == 0
    assert "about: 2/2 passed" in out
    assert "bio: 2/2 passed" in out
    assert prv.calls == 4


def test_counts_each_rejection_reason(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    measure(tmp_path, monkeypatch, ScriptedProvider(invent=True), "--runs", "2")
    out = capsys.readouterr().out

    assert "about: 0/2 passed" in out
    assert "bio: 0/2 passed" in out
    assert out.count("2x numbers not in evidence: 999") == 2


def test_a_single_flow_runs_only_that_flow(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    prv = ScriptedProvider()

    measure(tmp_path, monkeypatch, prv, "--runs", "3", "--flow", "bio")
    out = capsys.readouterr().out

    assert "bio: 3/3 passed" in out
    assert "about:" not in out
    assert prv.calls == 3


def test_runs_above_the_cap_are_rejected() -> None:
    with pytest.raises(SystemExit):
        measure_flows.main(["--runs", str(measure_flows.MAX_RUNS + 1)])
