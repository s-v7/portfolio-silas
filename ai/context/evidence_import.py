from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError


def read_jsonl(src: Path) -> tuple[list[dict[str, Any]], int]:
    """Read extractor records as unverified evidence; return them and a skip count.

    The extractor's own status is ignored on purpose: text a project wrote
    about itself is a claim, not a verified fact.
    """
    try:
        txt = src.read_text(encoding="utf-8")
    except FileNotFoundError as err:
        raise ConfigurationError(f"Evidence dataset does not exist: {src}") from err

    by_id: dict[str, dict[str, Any]] = {}
    skipped = 0

    for num, ln in enumerate(txt.splitlines(), start=1):
        if not ln.strip():
            continue

        try:
            rec = json.loads(ln)
        except json.JSONDecodeError as err:
            raise ConfigurationError(f"Invalid JSON on line {num} of {src}.") from err

        if not isinstance(rec, dict):
            skipped += 1
            continue

        # Older extractor runs wrote `source`; newer ones write `type`.
        label = rec.get("source") or rec.get("type")

        if not (
            isinstance(rec.get("identifier"), str)
            and isinstance(label, str)
            and isinstance(rec.get("content"), str)
            and rec["identifier"].strip()
            and label.strip()
            and rec["content"].strip()
        ):
            skipped += 1
            continue

        meta = rec.get("metadata")
        evd_meta: dict[str, Any] = dict(meta) if isinstance(meta, dict) else {}

        if "extract_at" in rec:
            evd_meta["extracted_at"] = rec["extract_at"]

        evd: dict[str, Any] = {
            "identifier": rec["identifier"].strip(),
            "source": label.strip(),
            "content": rec["content"].strip(),
            "status": EvidenceStatus.UNVERIFIED.value,
            "metadata": evd_meta,
        }

        if isinstance(rec.get("source_path"), str):
            evd["source_path"] = rec["source_path"]

        by_id[evd["identifier"]] = evd

    return list(by_id.values()), skipped


def write_evidence_file(
    evds: list[dict[str, Any]],
    dst: Path,
    language: str = "en",
) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps(
            {"language": language, "evidences": evds}, ensure_ascii=False, indent=2
        )
        + "\n",
        encoding="utf-8",
    )


def promote(src: Path, ids: Iterable[str]) -> int:
    """Mark the listed evidences as verified; nothing is written on error."""
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError as err:
        raise ConfigurationError(f"Evidence file does not exist: {src}") from err
    except json.JSONDecodeError as err:
        raise ConfigurationError(f"Evidence file contains invalid JSON: {src}") from err

    evds = data.get("evidences") if isinstance(data, dict) else None

    if not isinstance(evds, list):
        raise ConfigurationError("Field 'evidences' must be a JSON array.")

    wanted = set(ids)
    known = {evd.get("identifier") for evd in evds if isinstance(evd, dict)}
    missing = sorted(wanted - known)

    if missing:
        raise ConfigurationError("Unknown evidence identifiers: " + ", ".join(missing))

    count = 0

    for evd in evds:
        if isinstance(evd, dict) and evd.get("identifier") in wanted:
            evd["status"] = EvidenceStatus.VERIFIED.value
            count += 1

    src.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return count
