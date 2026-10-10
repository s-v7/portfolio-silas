from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.json_loader import load_portfolio_context
from ai.core.contracts import LLMProvider
from ai.core.exceptions import (
    AgentExecutionError,
    ConfigurationError,
    EvidenceValidationError,
    FileChangeValidationError,
    ProviderError,
)
from ai.executor.parallel_executor import ParallelExecutor
from ai.providers.factory import ProviderFactory
from ai.services.draft_writer import DraftWriter
from ai.services.readme_generation_service import (
    ReadmeGenerationService,
)
from ai.telemetry import InMemoryTelemetry, TelemetryEvent

DEFAULT_OUTPUT_ROOT = Path("ai/output/drafts")


def create_provider(
    provider_name: str | None,
) -> LLMProvider:
    return ProviderFactory.create(provider_name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a GitHub README draft using only "
            "verified portfolio evidence."
        )
    )

    parser.add_argument(
        "--provider",
        choices=("openai", "anthropic", "nvidia"),
        default=None,
        help=(
            "LLM provider. Defaults to LLM_PROVIDER or openai."
        ),
    )
    parser.add_argument(
        "--evidence-file",
        type=Path,
        required=True,
        help="JSON file containing portfolio evidence.",
    )
    parser.add_argument(
        "--output",
        default="README.pt.md",
        help=(
            "Relative output path inside ai/output/drafts."
        ),
    )
    parser.add_argument(
        "--language",
        default=None,
        help=(
            "README language. Defaults to the context language."
        ),
    )
    parser.add_argument(
        "--audience",
        default="technical recruiters",
        help="Target audience for the generated README.",
    )
    parser.add_argument(
        "--title",
        default="Silas Vasconcelos Cruz",
        help="README title.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Print execution telemetry events after the run.",
    )

    return parser


def _format_event(event: TelemetryEvent) -> str:
    parts = [f"[trace] {event.name}"]

    node = event.attributes.get("node")
    if node:
        parts.append(f"node={node}")

    duration = event.attributes.get("duration_ms")
    if isinstance(duration, (int, float)):
        parts.append(f"duration_ms={duration:.2f}")

    return " ".join(parts)


def _print_trace(telemetry: InMemoryTelemetry | None) -> None:
    if telemetry is None:
        return

    for event in telemetry.events:
        print(_format_event(event))


def main(
    argv: Sequence[str] | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    telemetry = InMemoryTelemetry() if args.trace else None
    executor = (
        ParallelExecutor(telemetry=telemetry)
        if telemetry is not None
        else None
    )

    try:
        context = load_portfolio_context(
            args.evidence_file
        )
        provider = create_provider(args.provider)

        service = ReadmeGenerationService(
            readme_agent=ReadmeAgent(provider),
            draft_writer=DraftWriter(
                DEFAULT_OUTPUT_ROOT
            ),
            executor=executor,
        )

        result = service.generate(
            context=context,
            agent_input=ReadmeAgentInput(
                language=args.language or context.language,
                audience=args.audience,
                title=args.title,
            ),
            relative_path=args.output,
        )
    except (
        AgentExecutionError,
        ConfigurationError,
        EvidenceValidationError,
        FileChangeValidationError,
        ProviderError,
    ) as error:
        print(
            f"README generation failed: {error}",
            file=sys.stderr,
        )
        _print_trace(telemetry)
        return 1

    print(f"Draft: {result.destination}")
    print(f"Provider: {result.provider}")
    print(f"Model: {result.model}")
    print(
        f"Verified evidence: "
        f"{result.evidence_count}"
    )
    print(
        f"Rejected evidence: "
        f"{result.rejected_evidence_count}"
    )

    for warning in result.warnings:
        print(f"Warning: {warning}")

    _print_trace(telemetry)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())