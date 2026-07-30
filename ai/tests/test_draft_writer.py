from pathlib import Path

import pytest

from ai.core.exceptions import FileChangeValidationError
from ai.services.draft_writer import DraftWriter


def test_writes_draft_inside_output_directory(
    tmp_path: Path,
) -> None:
    writer = DraftWriter(output_root=tmp_path)

    destination = writer.write(
        relative_path="README.pt.md",
        content="# Portfolio\n",
    )

    assert destination == tmp_path / "README.pt.md"
    assert destination.read_text(encoding="utf-8") == "# Portfolio\n"


def test_creates_parent_directories(
    tmp_path: Path,
) -> None:
    writer = DraftWriter(output_root=tmp_path)

    destination = writer.write(
        relative_path="readme/README.pt.md",
        content="# Draft\n",
    )

    assert destination.exists()
    assert destination.parent == tmp_path / "readme"


def test_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    writer = DraftWriter(output_root=tmp_path)

    with pytest.raises(
        FileChangeValidationError,
        match="outside the configured output directory",
    ):
        writer.write(
            relative_path="../README.md",
            content="# Invalid\n",
        )


def test_rejects_empty_content(
    tmp_path: Path,
) -> None:
    writer = DraftWriter(output_root=tmp_path)

    with pytest.raises(
        FileChangeValidationError,
        match="cannot be empty",
    ):
        writer.write(
            relative_path="README.pt.md",
            content="   ",
        )
