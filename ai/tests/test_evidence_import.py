from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ai.context.evidence_import import promote, read_jsonl, write_evidence_file
from ai.context.json_loader import load_portfolio_context
from ai.core.exceptions import ConfigurationError


def rec(identifier: str = "a", content: str = "Text.", **extra: Any) -> dict[str, Any]:
    return {
        "identifier": identifier,
        "source": "README",
        "content": content,
        "status": "verified",
        **extra,
    }


def write_jsonl(pth: Path, recs: list[Any], tail: tuple[str, ...] = ()) -> Path:
    lns = [json.dumps(item) for item in recs] + list(tail)
    pth.write_text("\n".join(lns) + "\n", encoding="utf-8")
    return pth


def imported(tmp_path: Path, recs: list[Any]) -> Path:
    evds, _ = read_jsonl(write_jsonl(tmp_path / "in.jsonl", recs))
    dst = tmp_path / "out.json"
    write_evidence_file(evds, dst)
    return dst


def test_ignores_the_extractor_status(tmp_path: Path) -> None:
    evds, _ = read_jsonl(write_jsonl(tmp_path / "in.jsonl", [rec()]))

    assert evds[0]["status"] == "unverified"


def test_duplicate_identifier_keeps_the_last_record(tmp_path: Path) -> None:
    recs = [rec("a", "old"), rec("b"), rec("a", "new")]

    evds, _ = read_jsonl(write_jsonl(tmp_path / "in.jsonl", recs))

    assert {evd["identifier"]: evd["content"] for evd in evds} == {
        "a": "new",
        "b": "Text.",
    }


def test_skips_incomplete_records_and_counts_them(tmp_path: Path) -> None:
    recs = [rec("a"), {"identifier": "b", "source": "README"}, rec("c", " "), [1]]

    evds, skipped = read_jsonl(write_jsonl(tmp_path / "in.jsonl", recs))

    assert [evd["identifier"] for evd in evds] == ["a"]
    assert skipped == 3


def test_ignores_blank_lines(tmp_path: Path) -> None:
    pth = write_jsonl(tmp_path / "in.jsonl", [rec("a")], tail=("", "   "))

    evds, skipped = read_jsonl(pth)

    assert len(evds) == 1
    assert skipped == 0


def test_invalid_json_reports_the_line_number(tmp_path: Path) -> None:
    pth = write_jsonl(tmp_path / "in.jsonl", [rec()], tail=("{not json",))

    with pytest.raises(ConfigurationError, match="line 2"):
        read_jsonl(pth)


def test_missing_dataset_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="does not exist"):
        read_jsonl(tmp_path / "missing.jsonl")


def test_keeps_source_path_and_extraction_time_as_provenance(tmp_path: Path) -> None:
    item = rec(source_path="/x/README.md", extract_at="2026-10-02", metadata={"k": 1})

    evds, _ = read_jsonl(write_jsonl(tmp_path / "in.jsonl", [item]))

    assert evds[0]["source_path"] == "/x/README.md"
    assert evds[0]["metadata"] == {"k": 1, "extracted_at": "2026-10-02"}


def test_written_file_loads_with_nothing_verified(tmp_path: Path) -> None:
    cxt = load_portfolio_context(imported(tmp_path, [rec("a"), rec("b")]))

    assert cxt.language == "en"
    assert len(cxt.evidences) == 2
    assert cxt.verified_evidences == ()


def test_promote_verifies_only_the_listed_ids(tmp_path: Path) -> None:
    dst = imported(tmp_path, [rec("a"), rec("b"), rec("c")])

    count = promote(dst, ["a", "c"])
    cxt = load_portfolio_context(dst)

    assert count == 2
    assert [evd.identifier for evd in cxt.verified_evidences] == ["a", "c"]


def test_promote_unknown_id_leaves_the_file_untouched(tmp_path: Path) -> None:
    dst = imported(tmp_path, [rec("a")])
    before = dst.read_text(encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Unknown evidence identifiers: zzz"):
        promote(dst, ["a", "zzz"])

    assert dst.read_text(encoding="utf-8") == before


def test_only_promoted_evidence_reaches_the_prompt(tmp_path: Path) -> None:
    dst = imported(tmp_path, [rec("a", "Kept fact."), rec("b", "Left out.")])
    promote(dst, ["a"])

    prompt = load_portfolio_context(dst).as_prompt_context()

    assert "Kept fact." in prompt
    assert "Left out." not in prompt
