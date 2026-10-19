from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.context.evidence_import import write_evidence_file
from ai.context.github_import import fetch_repos, to_evidences
from ai.core.exceptions import ConfigurationError

DEFAULT_OUTPUT = Path("ai/output/evidence/github_evidence.json")


def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Import public GitHub repositories as unverified evidence."
    )
    prs.add_argument("--owner", required=True)
    prs.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    prs.add_argument("--language", default="en")
    prs.add_argument("--include-forks", action="store_true")
    return prs


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        repos = fetch_repos(args.owner)
        evds, skipped = to_evidences(repos, include_forks=args.include_forks)
        write_evidence_file(evds, args.output, args.language)
    except ConfigurationError as err:
        print(f"GitHub import failed: {err}", file=sys.stderr)
        return 1

    print(
        f"Imported {len(evds)} repositories ({skipped} skipped) "
        f"as unverified: {args.output}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
