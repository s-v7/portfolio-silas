from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import ProviderError
from ai.planner.planner import PlannerAgent, PlannerInput


class PlanOnlyProvider(LLMProvider):
    """Stands in for a real provider: planning never calls the model."""

    @property
    def name(self) -> str:
        return "plan-only"

    def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        del request
        raise ProviderError("Plan-only mode does not call a provider.")


def build_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(ReadmeAgent(PlanOnlyProvider()))
    registry.register(EvidenceValidatorAgent[None]())
    return registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show which agents the planner selects for an objective."
    )
    parser.add_argument(
        "--objective",
        required=True,
        help="What should be accomplished.",
    )
    parser.add_argument(
        "--capability",
        action="append",
        default=None,
        help="Required capability (repeat the flag for several).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    planner = PlannerAgent(build_registry())

    try:
        result = planner.execute(
            PlannerInput(
                objective=args.objective,
                required_capabilities=tuple(args.capability or ()),
            ),
            PortfolioContext(evidences=()),
        )
    except ValueError as error:
        print(f"Planning failed: {error}", file=sys.stderr)
        return 1

    plan = result.output.plan

    if not plan.steps:
        print(
            "Planning failed: No registered agent matches the "
            "required capabilities.",
            file=sys.stderr,
        )
        return 1

    print(f"Objective: {plan.objective}")

    for index, step in enumerate(plan.steps, start=1):
        print(f"{index}. {step.agent} [{', '.join(step.capabilities)}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
