from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai.context.json_loader import load_portfolio_context
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError


def write_json(
    path: Path,
    data: object,
) -> None:
    path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )


def test_loads_portfolio_context(
    tmp_path: Path,
) -> None:
    source = tmp_path / "evidence.json"

    write_json(
        source,
        {
            "language": "pt-BR",
            "target_file": "README.md",
            "metadata": {
                "purpose": "portfolio",
            },
            "evidences": [
                {
                    "identifier": "fastapi",
                    "source": "git",
                    "content": "Implemented FastAPI endpoints.",
                    "status": "verified",
                    "source_path": "backend/app.py",
                    "metadata": {
                        "category": "backend",
                    },
                }
            ],
        },
    )

    context = load_portfolio_context(source)

    assert context.language == "pt-BR"
    assert context.target_file == Path("README.md")
    assert len(context.evidences) == 1

    evidence = context.evidences[0]

    assert evidence.identifier == "fastapi"
    assert evidence.status is EvidenceStatus.VERIFIED
    assert evidence.source_path == Path(
        "backend/app.py"
    )


def test_defaults_evidence_to_unverified(
    tmp_path: Path,
) -> None:
    source = tmp_path / "evidence.json"

    write_json(
        source,
        {
            "evidences": [
                {
                    "identifier": "planned",
                    "source": "roadmap",
                    "content": "Planned capability.",
                }
            ]
        },
    )

    context = load_portfolio_context(source)

    assert (
        context.evidences[0].status
        is EvidenceStatus.UNVERIFIED
    )


def test_rejects_invalid_status(
    tmp_path: Path,
) -> None:
    source = tmp_path / "evidence.json"

    write_json(
        source,
        {
            "evidences": [
                {
                    "identifier": "invalid",
                    "source": "git",
                    "content": "Invalid evidence.",
                    "status": "approved",
                }
            ]
        },
    )

    with pytest.raises(
        ConfigurationError,
        match="Invalid evidence status",
    ):
        load_portfolio_context(source)


def test_rejects_invalid_json(
    tmp_path: Path,
) -> None:
    source = tmp_path / "evidence.json"
    source.write_text("{invalid", encoding="utf-8")

    with pytest.raises(
        ConfigurationError,
        match="invalid JSON",
    ):
        load_portfolio_context(source)
