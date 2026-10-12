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
from ai.scripts import plan_workflow


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
        )


class UnavailableProvider(FakeProvider):
    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        raise ProviderError("provider unavailable")


def evidence_file(tmp_path: Path, status: str = "verified") -> Path:
    path = tmp_path / "evidence.json"
    path.write_text(
        json.dumps(
            {
                "language": "pt-BR",
                "evidences": [
                    {
                        "identifier": "fastapi",
                        "source": "git",
                        "content": "Implemented FastAPI endpoints.",
                        "status": status,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def use_provider(monkeypatch: MonkeyPatch, provider: FakeProvider) -> None:
    monkeypatch.setattr(
        plan_workflow,
        "create_provider",
        lambda name: provider,
    )


def test_run_executes_plan_and_prints_readme(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    use_provider(monkeypatch, FakeProvider())

    exit_code = plan_workflow.main(
        [
            "--objective",
            "Generate README",
            "--capability",
            "portfolio",
            "--run",
            "--evidence-file",
            str(evidence_file(tmp_path)),
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "evidence-validator" in output
    assert "# Generated README" in output


def test_run_requires_evidence_file(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(["--objective", "Generate", "--run"])

    assert exit_code == 1
    assert "requires --evidence-file" in capsys.readouterr().err


def test_run_reports_provider_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    use_provider(monkeypatch, UnavailableProvider())

    exit_code = plan_workflow.main(
        [
            "--objective",
            "Generate README",
            "--capability",
            "markdown",
            "--run",
            "--evidence-file",
            str(evidence_file(tmp_path)),
        ]
    )

    assert exit_code == 1
    assert "provider unavailable" in capsys.readouterr().err


def test_run_without_verified_evidence_fails_cleanly(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    use_provider(monkeypatch, FakeProvider())

    exit_code = plan_workflow.main(
        [
            "--objective",
            "Generate README",
            "--capability",
            "markdown",
            "--run",
            "--evidence-file",
            str(evidence_file(tmp_path, status="unverified")),
        ]
    )

    assert exit_code == 1
    assert "verified evidence" in capsys.readouterr().err


class CountingProvider(FakeProvider):
    def __init__(self) -> None:
        self.calls = 0

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        self.calls += 1
        return super().generate(request)


def test_run_stops_at_validator_without_calling_provider(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    provider = CountingProvider()
    use_provider(monkeypatch, provider)

    exit_code = plan_workflow.main(
        [
            "--objective",
            "Generate README",
            "--capability",
            "portfolio",
            "--run",
            "--evidence-file",
            str(evidence_file(tmp_path, status="unverified")),
        ]
    )

    error = capsys.readouterr().err

    assert exit_code == 1
    assert "evidence-validator" in error
    assert "No verified evidence" in error
    assert provider.calls == 0
