from __future__ import annotations

from pathlib import Path

from ai.core.exceptions import FileChangeValidationError


class DraftWriter:
    def __init__(
        self,
        output_root: Path,
    ) -> None:
        self._output_root = output_root.resolve()

    def write(
        self,
        relative_path: str,
        content: str,
    ) -> Path:
        normalized_content = content.strip()

        if not normalized_content:
            raise FileChangeValidationError(
                "Draft content cannot be empty."
            )

        destination = (
            self._output_root / relative_path
        ).resolve()

        if not destination.is_relative_to(self._output_root):
            raise FileChangeValidationError(
                "Draft destination is outside the configured "
                "output directory."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            f"{normalized_content}\n",
            encoding="utf-8",
        )

        return destination
