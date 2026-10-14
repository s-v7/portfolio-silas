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


def evidence_file(tmp_path: Path) -> Path:
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
                        "status": "verified",
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
    *args: str,
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: provider)
    monkeypatch.setattr(plan_workflow, "DEFAULT_OUTPUT_ROOT", tmp_path / "drafts")

    return plan_workflow.main(["--objective", "Write about me", *args])


def test_output_writes_the_generated_text(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    exit_code = run(
        tmp_path,
        monkeypatch,
        ScriptedProvider(),
        "--capability",
        "about",
        "--run",
        "--evidence-file",
        str(evidence_file(tmp_path)),
        "--output",
        "about.md",
    )

    written = tmp_path / "drafts" / "about.md"

    assert exit_code == 0
    assert "Draft:" in capsys.readouterr().out
    assert "Silas builds fiscal intelligence systems." in written.read_text(
        encoding="utf-8"
    )


def test_output_is_not_written_when_the_check_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    invented = GROUNDED + " It covers 999 municipalities."

    exit_code = run(
        tmp_path,
        monkeypatch,
        ScriptedProvider(invented),
        "--capability",
        "about",
        "--run",
        "--evidence-file",
        str(evidence_file(tmp_path)),
        "--output",
        "about.md",
    )

    assert exit_code == 1
    assert not (tmp_path / "drafts" / "about.md").exists()


def test_output_requires_run(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    exit_code = run(
        tmp_path,
        monkeypatch,
        ScriptedProvider(),
        "--output",
        "about.md",
    )

    assert exit_code == 1
    assert "--output requires --run" in capsys.readouterr().err


def test_output_needs_a_single_generating_agent(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    provider = ScriptedProvider()

    exit_code = run(
        tmp_path,
        monkeypatch,
        provider,
        "--capability",
        "portfolio",
        "--run",
        "--evidence-file",
        str(evidence_file(tmp_path)),
        "--output",
        "all.md",
    )

    assert exit_code == 1
    assert "exactly one generating agent" in capsys.readouterr().err
    assert provider.calls == 0
    assert not (tmp_path / "drafts" / "all.md").exists()
