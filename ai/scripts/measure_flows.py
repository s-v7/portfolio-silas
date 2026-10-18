from __future__ import annotations

import argparse
import contextlib
import io
import re
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from ai.scripts import plan_workflow

FLOWS: dict[str, str] = {"about": "Write about me", "bio": "Write my bio"}
DEFAULT_EVIDENCE = Path("ai/data/profile_evidence.json")
MAX_RUNS = 20

_REASON = re.compile(r"check failed: ([^\n]*)")


def _reasons(err_txt: str) -> list[str]:
    mat = _REASON.search(err_txt)

    if mat:
        return mat.group(1).split("; ")

    lns = [ln for ln in err_txt.splitlines() if ln.strip()]

    return [lns[0]] if lns else ["unknown failure"]


def run_once(
    flow: str,
    files: Sequence[Path],
    provider: str | None,
) -> tuple[bool, list[str]]:
    out, err = io.StringIO(), io.StringIO()
    args = ["--objective", FLOWS[flow], "--capability", flow, "--run"]

    for pth in files:
        args += ["--evidence-file", str(pth)]

    if provider:
        args += ["--provider", provider]

    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = plan_workflow.main(args)

    if code == 0:
        return True, []

    return False, _reasons(err.getvalue())


def _runs(val: str) -> int:
    num = int(val)

    if not 1 <= num <= MAX_RUNS:
        raise argparse.ArgumentTypeError(f"must be between 1 and {MAX_RUNS}")

    return num


def build_parser() -> argparse.ArgumentParser:
    prs = argparse.ArgumentParser(
        description="Run the About and bio flows N times and count approvals."
    )
    prs.add_argument("--runs", type=_runs, default=5)
    prs.add_argument("--flow", choices=("about", "bio", "both"), default="both")
    prs.add_argument("--evidence-file", action="append", type=Path, default=None)
    prs.add_argument(
        "--provider",
        choices=("proxy", "openai", "anthropic", "nvidia"),
        default=None,
    )
    return prs


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    flows = list(FLOWS) if args.flow == "both" else [args.flow]
    files = args.evidence_file or [DEFAULT_EVIDENCE]

    print(f"{args.runs} run(s) per flow; each run is one provider call.")

    for flw in flows:
        cnt: Counter[str] = Counter()
        ok = 0

        for _ in range(args.runs):
            passed, rsn = run_once(flw, files, args.provider)
            ok += passed
            cnt.update(rsn)

        print(f"{flw}: {ok}/{args.runs} passed")

        for txt, num in cnt.most_common():
            print(f"  {num}x {txt}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
