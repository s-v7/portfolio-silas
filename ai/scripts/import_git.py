from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.context.evidence_import import write_evidence_file
from ai.context.git_activity import activity_evidence, collect_activity
from ai.context.git_import import (
    collect_stats,
    default_email,
    repos_from_dataset,
    to_evidences,
)
from ai.core.exceptions import ConfigurationError

DEFAULT_DATASET = Path("ai/data/dataset_evidence.jsonl")
DEFAULT_OUTPUT = Path("ai/output/evidence/git_evidence.json")
DEFAULT_ACTIVITY = Path("ai/output/evidence/git_activity.json")


def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Compute evidence from local git history (the author's commits)."
    )
    prs.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    prs.add_argument(
        "--repo",
        action="append",
        type=Path,
        default=None,
        help="Repository path (repeatable); replaces the dataset scan.",
    )
    prs.add_argument(
        "--email",
        action="append",
        default=None,
        help="Author e-mail (repeatable). Defaults to git config user.email.",
    )
    prs.add_argument(
        "--exclude",
        action="append",
        default=None,
        help="Folder name to leave out (repeatable), e.g. third-party projects.",
    )
    prs.add_argument("--min-commits", type=int, default=1)
    prs.add_argument(
        "--aggregate",
        action="store_true",
        help="One evidence with totals and languages; no repository is named.",
    )
    prs.add_argument("--output", type=Path, default=None)
    prs.add_argument("--language", default="en")
    return prs


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        emls = args.email or [default_email()]
        repos = (
            [pth.resolve() for pth in args.repo]
            if args.repo
            else repos_from_dataset(args.dataset)
        )
        skip = set(args.exclude or [])
        repos = [pth for pth in repos if pth.name not in skip]

        if args.aggregate:
            out = args.output or DEFAULT_ACTIVITY
            act, skipped, dups = collect_activity(repos, emls, args.min_commits)

            if act is None:
                raise ConfigurationError("No commits by the author were found.")

            write_evidence_file([activity_evidence(act)], out, args.language)
            print(
                f"Computed activity across {act.repos} repositories "
                f"({skipped} without commits, {dups} duplicate clones) "
                f"as verified: {out}"
            )
            return 0

        out = args.output or DEFAULT_OUTPUT
        sts, skipped = collect_stats(repos, emls, args.min_commits)
        write_evidence_file(to_evidences(sts), out, args.language)
    except ConfigurationError as err:
        print(f"Git import failed: {err}", file=sys.stderr)
        return 1

    print(
        f"Imported {len(sts)} repositories ({skipped} skipped) as verified "
        f"(computed from git history): {out}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
