from __future__ import annotations

import argparse
import contextlib
import io
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.scripts import plan_workflow

EXIT_FAILED = 1
EXIT_CHANGED = 10

OBJECTIVES = {"about": "Write about me", "bio": "Write my bio"}
FILES = {"about": "about.md", "bio": "bio.txt"}
DEFAULT_EVIDENCE = Path("ai/data/profile_evidence.json")
DEFAULT_DOCS = Path("docs")


def generate(
    flw: str,
    evds: Sequence[Path],
    prv: str | None,
) -> tuple[str | None, str]:
    """Run one flow through the plan CLI; return its text or the failure message."""
    name = f"regenerate_{flw}.txt"
    drf = plan_workflow.DEFAULT_OUTPUT_ROOT / name
    drf.unlink(missing_ok=True)
    args = [
        "--objective", OBJECTIVES[flw], "--capability", flw,
        "--run", "--output", name,
    ]

    for pth in evds:
        args += ["--evidence-file", str(pth)]

    if prv:
        args += ["--provider", prv]

    out, err = io.StringIO(), io.StringIO()

    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = plan_workflow.main(args)

    if code != 0 or not drf.is_file():
        return None, err.getvalue().strip() or "no draft was written"

    return drf.read_text(encoding="utf-8").strip(), ""


def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Regenerate the About and bio texts; write only if they changed."
    )
    prs.add_argument("--flow", choices=("about", "bio", "both"), default="both")
    prs.add_argument("--evidence-file", action="append", type=Path, default=None)
    prs.add_argument(
        "--provider",
        choices=("proxy", "openai", "anthropic", "nvidia"),
        default=None,
    )
    prs.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS)
    prs.add_argument("--dry-run", action="store_true")
    return prs


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    flws = list(OBJECTIVES) if args.flow == "both" else [args.flow]
    evds = args.evidence_file or [DEFAULT_EVIDENCE]
    new: dict[str, str] = {}

    for flw in flws:
        txt, err = generate(flw, evds, args.provider)

        if txt is None:
            print(f"Regeneration failed for {flw}: {err}", file=sys.stderr)
            return EXIT_FAILED

        new[flw] = txt

    changed: list[Path] = []

    for flw, txt in new.items():
        tgt = args.docs_dir / FILES[flw]
        cur = tgt.read_text(encoding="utf-8").strip() if tgt.is_file() else None

        if cur == txt:
            continue

        changed.append(tgt)

        if not args.dry_run:
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_text(txt + "\n", encoding="utf-8")

    if not changed:
        print("No changes.")
        return 0

    verb = "Would update" if args.dry_run else "Updated"

    for tgt in changed:
        print(f"{verb} {tgt}")

    return EXIT_CHANGED


if __name__ == "__main__":
    raise SystemExit(main())
