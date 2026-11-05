from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.core.exceptions import ConfigurationError
from ai.services.profile_block import merge_block

DEFAULT_SOURCE = Path("ai/output/drafts/README.profile.md")

def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Put the generated profile text into a profile repository README."
    )
    prs.add_argument(
        "--repo",
        type=Path,
        required=True,
        help="Clone of the profile repository. Nothing is committed or pushed.",
    )
    prs.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    prs.add_argument("--readme", default="README.md")

    return prs

def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tgt = args.repo / args.readme

    try:
        if not tgt.is_file():
            raise ConfigurationError(f"README not found: {tgt}")

        try:
            gen = args.source.read_text(encoding="utf-8")
        except FileNotFoundError as err:
            raise ConfigurationError(
                f"Generated text not found: {args.source}"
            ) from err

        cur = tgt.read_text(encoding="utf-8")
        new = merge_block(cur, gen)
    except ConfigurationError as err:
        print(f"Profile update failed: {err}", file=sys.stderr)
        return 1

    if new == cur:
        print("No change")
        return 0

    tgt.write_text(new, encoding="utf-8")
    print(f"Updated {tgt}. Review with git diff; nothing was commited or pushed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

