from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.scripts import generate_readme


class FakeProvider(LLMProvider):
    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        return ProviderResponse(
            content="# Generated README",
            provider=self.name,
            model="fake-model",
            metadata={},
        )


def prepare(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    evidence_file = tmp_path / "evidence.json"
    evidence_file.write_text(
        json.dumps(
            {
                "language": "pt-BR",
                "evidences": [
                    {
                        "identifier": "fastapi",
                        "source": "git",
                        "content": "Implemented FastAPI endpoints.",
                        "status": "verified",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        generate_readme,
        "DEFAULT_OUTPUT_ROOT",
        tmp_path / "drafts",
    )
    monkeypatch.setattr(
        generate_readme,
        "create_provider",
        lambda provider: FakeProvider(),
    )

    return evidence_file


def test_trace_flag_prints_telemetry_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    evidence_file = prepare(tmp_path, monkeypatch)

    exit_code = generate_readme.main(["--evidence-file", str(evidence_file), "--trace"])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "[trace] workflow.started" in output
    assert "[trace] node.completed node=write-draft" in output
    assert "[trace] workflow.completed" in output


def test_no_trace_output_without_flag(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    evidence_file = prepare(tmp_path, monkeypatch)

    exit_code = generate_readme.main(["--evidence-file", str(evidence_file)])

    assert exit_code == 0
    assert "[trace]" not in capsys.readouterr().out
