from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.context.evidence_import import promote, read_jsonl, write_evidence_file
from ai.core.exceptions import ConfigurationError

DEFAULT_SOURCE = Path("ai/data/dataset_evidence.jsonl")
DEFAULT_OUTPUT = Path("ai/output/evidence/imported_evidence.json")


def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Import extractor evidence as unverified and promote chosen items."
    )
    sub = prs.add_subparsers(dest="command", required=True)

    imp = sub.add_parser(
        "import", help="Convert the extractor dataset (all unverified)."
    )

    imp.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    imp.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    imp.add_argument("--language", default="en")

    pro = sub.add_parser("promote", help="Mark chosen evidence as verified.")
    pro.add_argument("--file", type=Path, default=DEFAULT_OUTPUT)
    pro.add_argument("--id", action="append", dest="ids", required=True)

    return prs


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.command == "import":
            evds, skipped = read_jsonl(args.source)
            write_evidence_file(evds, args.output, args.language)
            print(
                f"Imported {len(evds)} evidences ({skipped} skipped) "
                f"as unverified: {args.output}"
            )
        else:
            count = promote(args.file, args.ids)
            print(f"Promoted {count} evidence(s) to verified: {args.file}")
    except ConfigurationError as err:
        print(f"Evidence import failed: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
