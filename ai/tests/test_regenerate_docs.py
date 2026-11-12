from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.scripts import plan_workflow, regenerate_docs

ABOUT = (
    "Silas builds fiscal intelligence systems. He indexed ARTs on a "
    "blockchain.\n\n"
    "He modernized an ERP on Jakarta EE. The work runs in production."
)
BIO = (
    "Silas authored a fiscal engine that indexed 1.1M ARTs on a blockchain.\n"
    "He modernized an ERP on Jakarta EE."
)
INVENTED = "It covers 999 municipalities."


class ScriptedProvider(LLMProvider):
    def __init__(self, about: str = ABOUT, bio: str = BIO) -> None:
        self.about = about
        self.bio = bio

    @property
    def name(self) -> str:
        return "fake"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        is_about = "About section" in request.messages[-1].content

        return ProviderResponse(
            content=self.about if is_about else self.bio,
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


def run(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    prv: ScriptedProvider,
    *extra: str,
) -> int:
    monkeypatch.setattr(plan_workflow, "create_provider", lambda name: prv)
    monkeypatch.setattr(plan_workflow, "DEFAULT_OUTPUT_ROOT", tmp_path / "drafts")

    return regenerate_docs.main(
        [
            "--evidence-file",
            str(evd_file(tmp_path)),
            "--docs-dir",
            str(tmp_path / "docs"),
            *extra,
        ]
    )


def test_writes_both_documents_and_reports_the_change(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(tmp_path, monkeypatch, ScriptedProvider())
    about = (tmp_path / "docs" / "about.md").read_text(encoding="utf-8")
    bio = (tmp_path / "docs" / "bio.txt").read_text(encoding="utf-8")

    assert code == regenerate_docs.EXIT_CHANGED
    assert about.startswith("Silas builds fiscal intelligence systems.")
    assert about.endswith("\n")
    assert bio.startswith("Silas authored a fiscal engine")
    assert "Updated" in capsys.readouterr().out


def test_identical_output_changes_nothing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    run(tmp_path, monkeypatch, ScriptedProvider())
    before = (tmp_path / "docs" / "about.md").read_text(encoding="utf-8")
    capsys.readouterr()

    code = run(tmp_path, monkeypatch, ScriptedProvider())

    assert code == 0
    assert "No changes." in capsys.readouterr().out
    assert (tmp_path / "docs" / "about.md").read_text(encoding="utf-8") == before


def test_updates_only_the_document_whose_text_changed(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    run(tmp_path, monkeypatch, ScriptedProvider())
    capsys.readouterr()
    newer = ABOUT.replace("The work runs in production.", "The work runs daily.")

    code = run(tmp_path, monkeypatch, ScriptedProvider(about=newer))
    out = capsys.readouterr().out

    assert code == regenerate_docs.EXIT_CHANGED
    assert "about.md" in out
    assert "bio.txt" not in out
    assert "runs daily" in (tmp_path / "docs" / "about.md").read_text(encoding="utf-8")


def test_a_rejected_about_writes_nothing_and_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(tmp_path, monkeypatch, ScriptedProvider(about=ABOUT + " " + INVENTED))
    err = capsys.readouterr().err

    assert code == regenerate_docs.EXIT_FAILED
    assert "Regeneration failed for about" in err
    assert "numbers not in evidence: 999" in err
    assert not (tmp_path / "docs").exists()


def test_a_rejected_bio_keeps_the_good_about_from_being_written(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(tmp_path, monkeypatch, ScriptedProvider(bio=BIO + "\n" + INVENTED))

    assert code == regenerate_docs.EXIT_FAILED
    assert "Regeneration failed for bio" in capsys.readouterr().err
    assert not (tmp_path / "docs").exists()


def test_dry_run_reports_without_writing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    code = run(tmp_path, monkeypatch, ScriptedProvider(), "--dry-run")

    assert code == regenerate_docs.EXIT_CHANGED
    assert "Would update" in capsys.readouterr().out
    assert not (tmp_path / "docs").exists()


def test_a_single_flow_touches_only_its_document(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    run(tmp_path, monkeypatch, ScriptedProvider(), "--flow", "bio")

    assert (tmp_path / "docs" / "bio.txt").is_file()
    assert not (tmp_path / "docs" / "about.md").exists()


def test_missing_evidence_fails_cleanly(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        plan_workflow, "create_provider", lambda name: ScriptedProvider()
    )
    monkeypatch.setattr(plan_workflow, "DEFAULT_OUTPUT_ROOT", tmp_path / "drafts")

    code = regenerate_docs.main(
        [
            "--evidence-file",
            str(tmp_path / "missing.json"),
            "--docs-dir",
            str(tmp_path / "docs"),
        ]
    )

    assert code == regenerate_docs.EXIT_FAILED
