from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import ProviderError
from ai.scripts import generate_readme


class UnavailableProvider(LLMProvider):
    @property
    def name(self) -> str:
        return "unavailable"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        raise ProviderError("proxy unreachable")


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
        lambda provider: UnavailableProvider(),
    )

    return evidence_file


def test_returns_error_when_provider_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    evidence_file = prepare(tmp_path, monkeypatch)

    exit_code = generate_readme.main(
        ["--evidence-file", str(evidence_file)]
    )

    assert exit_code == 1
    assert "proxy unreachable" in capsys.readouterr().err


def test_trace_shows_failure_when_provider_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    evidence_file = prepare(tmp_path, monkeypatch)

    exit_code = generate_readme.main(
        ["--evidence-file", str(evidence_file), "--trace"]
    )

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "[trace] node.failed node=generate-readme" in output
    assert "[trace] workflow.failed" in output
