from __future__ import annotations

import json
from pathlib import Path

from pytest import MonkeyPatch

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
        return ProviderResponse(
            content="# Generated README",
            provider=self.name,
            model="fake-model",
            metadata={},
        )


def write_evidence_file(
    destination: Path,
) -> None:
    destination.write_text(
        json.dumps(
            {
                "language": "pt-BR",
                "evidences": [
                    {
                        "identifier": "fastapi",
                        "source": "git",
                        "content": (
                            "Implemented FastAPI endpoints."
                        ),
                        "status": "verified",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_generates_readme_from_cli(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    evidence_file = tmp_path / "evidence.json"
    output_root = tmp_path / "drafts"

    write_evidence_file(evidence_file)

    monkeypatch.setattr(
        generate_readme,
        "DEFAULT_OUTPUT_ROOT",
        output_root,
    )
    monkeypatch.setattr(
        generate_readme,
        "create_provider",
        lambda provider: FakeProvider(),
    )

    exit_code = generate_readme.main(
        [
            "--provider",
            "openai",
            "--evidence-file",
            str(evidence_file),
            "--output",
            "README.pt.md",
        ]
    )

    assert exit_code == 0
    assert (
        output_root / "README.pt.md"
    ).read_text(
        encoding="utf-8"
    ) == "# Generated README\n"


def test_returns_error_for_invalid_evidence_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        generate_readme,
        "create_provider",
        lambda provider: FakeProvider(),
    )

    exit_code = generate_readme.main(
        [
            "--evidence-file",
            str(missing_file),
        ]
    )

    assert exit_code == 1
