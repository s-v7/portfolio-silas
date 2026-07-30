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
)
from ai.providers.factory import ProviderFactory
from ai.services.draft_writer import DraftWriter
from ai.services.readme_generation_service import (
    ReadmeGenerationService,
)

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

    return parser


def main(
    argv: Sequence[str] | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

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
    ) as error:
        print(
            f"README generation failed: {error}",
            file=sys.stderr,
        )
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
