from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture

from ai.context.json_loader import load_portfolio_context
from ai.scripts import import_evidences


def dataset(tmp_path: Path) -> Path:
    src = tmp_path / "dataset.jsonl"
    src.write_text(
        "\n".join(
            json.dumps(
                {
                    "identifier": idf,
                    "source": "README",
                    "content": f"Fact {idf}.",
                    "status": "verified",
                }
            )
            for idf in ("a", "b")
        )
        + "\n",
        encoding="utf-8",
    )
    return src


def test_import_then_promote_end_to_end(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    out = tmp_path / "evidence" / "imported.json"

    code_imp = import_evidences.main(
        ["import", "--source", str(dataset(tmp_path)), "--output", str(out)]
    )
    assert load_portfolio_context(out).verified_evidences == ()

    code_pro = import_evidences.main(["promote", "--file", str(out), "--id", "b"])
    cxt = load_portfolio_context(out)

    assert (code_imp, code_pro) == (0, 0)
    assert [evd.identifier for evd in cxt.verified_evidences] == ["b"]
    assert "Promoted 1 evidence(s)" in capsys.readouterr().out


def test_promote_unknown_id_fails_cleanly(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    out = tmp_path / "imported.json"
    import_evidences.main(
        ["import", "--source", str(dataset(tmp_path)), "--output", str(out)]
    )

    code = import_evidences.main(["promote", "--file", str(out), "--id", "zzz"])

    assert code == 1
    assert "Unknown evidence identifiers: zzz" in capsys.readouterr().err


def test_import_fails_cleanly_for_a_missing_dataset(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    code = import_evidences.main(["import", "--source", str(tmp_path / "none.jsonl")])

    assert code == 1
    assert "does not exist" in capsys.readouterr().err
