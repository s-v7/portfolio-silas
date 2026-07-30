from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus
from ai.core.exceptions import ConfigurationError


def _as_mapping(
    value: object,
    field_name: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(
            f"Field '{field_name}' must be a JSON object."
        )

    return {
        str(key): item
        for key, item in value.items()
    }


def _as_required_string(
    value: object,
    field_name: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(
            f"Field '{field_name}' must be a non-empty string."
        )

    return value.strip()


def _parse_status(
    value: object,
    identifier: str,
) -> EvidenceStatus:
    status_name = _as_required_string(
        value,
        f"evidences[{identifier}].status",
    )

    try:
        return EvidenceStatus(status_name.lower())
    except ValueError as error:
        supported = ", ".join(
            status.value
            for status in EvidenceStatus
        )

        raise ConfigurationError(
            f"Invalid evidence status '{status_name}' "
            f"for '{identifier}'. Supported values: "
            f"{supported}."
        ) from error


def _parse_evidence(
    value: object,
    index: int,
) -> Evidence:
    data = _as_mapping(
        value,
        f"evidences[{index}]",
    )

    identifier = _as_required_string(
        data.get("identifier"),
        f"evidences[{index}].identifier",
    )
    source = _as_required_string(
        data.get("source"),
        f"evidences[{index}].source",
    )
    content = _as_required_string(
        data.get("content"),
        f"evidences[{index}].content",
    )

    status = _parse_status(
        data.get("status", EvidenceStatus.UNVERIFIED.value),
        identifier,
    )

    source_path_value = data.get("source_path")

    if source_path_value is None:
        source_path = None
    elif isinstance(source_path_value, str):
        source_path = Path(source_path_value)
    else:
        raise ConfigurationError(
            f"Field 'source_path' for evidence "
            f"'{identifier}' must be a string or null."
        )

    metadata_value = data.get("metadata", {})

    return Evidence(
        identifier=identifier,
        source=source,
        content=content,
        status=status,
        source_path=source_path,
        metadata=_as_mapping(
            metadata_value,
            f"evidences[{index}].metadata",
        ),
    )


def load_portfolio_context(
    source: Path,
) -> PortfolioContext:
    try:
        raw: object = json.loads(
            source.read_text(encoding="utf-8")
        )
    except FileNotFoundError as error:
        raise ConfigurationError(
            f"Evidence file does not exist: {source}"
        ) from error
    except json.JSONDecodeError as error:
        raise ConfigurationError(
            f"Evidence file contains invalid JSON: {source}"
        ) from error

    data = _as_mapping(raw, "root")
    evidences_value = data.get("evidences")

    if not isinstance(evidences_value, list):
        raise ConfigurationError(
            "Field 'evidences' must be a JSON array."
        )

    evidences = tuple(
        _parse_evidence(value, index)
        for index, value in enumerate(evidences_value)
    )

    language_value = data.get("language", "pt-BR")
    language = _as_required_string(
        language_value,
        "language",
    )

    target_file_value = data.get("target_file")

    if target_file_value is None:
        target_file = None
    elif isinstance(target_file_value, str):
        target_file = Path(target_file_value)
    else:
        raise ConfigurationError(
            "Field 'target_file' must be a string or null."
        )

    metadata = _as_mapping(
        data.get("metadata", {}),
        "metadata",
    )

    return PortfolioContext(
        evidences=evidences,
        target_file=target_file,
        language=language,
        metadata=metadata,
    )
