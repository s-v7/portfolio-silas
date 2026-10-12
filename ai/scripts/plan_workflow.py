from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai.agents.base import AgentResult
from ai.agents.evidence_validator import (
    EvidenceValidationReport,
    EvidenceValidatorAgent,
)
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.agents.registry import AgentRegistry
from ai.context.json_loader import load_portfolio_context
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import (
    ConfigurationError,
    EvidenceValidationError,
    ProviderError,
)
from ai.executor.parallel_executor import ParallelExecutor
from ai.graph import NodeExecutionStatus
from ai.planner.plan import ExecutionPlan
from ai.planner.planner import PlannerAgent, PlannerInput
from ai.providers.factory import ProviderFactory
from ai.workflows.builder import WorkflowBuilder

README_AGENT = "readme-agent"
VALIDATOR_AGENT = "evidence-validator"


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


def create_provider(provider_name: str | None) -> LLMProvider:
    return ProviderFactory.create(provider_name)


def build_registry(provider: LLMProvider | None = None) -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(ReadmeAgent(provider or PlanOnlyProvider()))
    registry.register(EvidenceValidatorAgent[None]())
    return registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show (and optionally run) the planner's execution plan."
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
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute the plan and print the generated README.",
    )
    parser.add_argument(
        "--evidence-file",
        type=Path,
        default=None,
        help="JSON evidence file (required with --run).",
    )
    parser.add_argument(
        "--provider",
        choices=("proxy", "openai", "anthropic", "nvidia"),
        default=None,
        help="LLM provider for --run. Defaults to LLM_PROVIDER or proxy.",
    )
    return parser


def require_verified_evidence(
    result: AgentResult[EvidenceValidationReport],
) -> None:
    if not result.output.valid:
        raise EvidenceValidationError(
            "No verified evidence is available for README generation."
        )


def run_plan(
    plan: ExecutionPlan,
    registry: AgentRegistry,
    context: PortfolioContext,
) -> int:
    builder = WorkflowBuilder.from_plan(
        plan,
        registry,
        input_factories={
            README_AGENT: lambda: ReadmeAgentInput(language=context.language)
        },
        output_checks={VALIDATOR_AGENT: require_verified_evidence},
    )

    agents = {step.agent for step in plan.steps}

    # Domain knowledge: the README is written only after validation.
    if README_AGENT in agents and VALIDATOR_AGENT in agents:
        builder.depends_on(README_AGENT, VALIDATOR_AGENT)

    report = ParallelExecutor().execute(builder.build(), context)

    if not report.succeeded:
        failed = next(
            record
            for record in report.records
            if record.status is NodeExecutionStatus.FAILED
        )
        print(
            f"Execution failed in '{failed.node}': {failed.error}",
            file=sys.stderr,
        )
        return 1

    if README_AGENT in report.results:
        print()
        print(report.results[README_AGENT].output.content)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.run and args.evidence_file is None:
        print("--run requires --evidence-file.", file=sys.stderr)
        return 1

    try:
        if args.run:
            context = load_portfolio_context(args.evidence_file)
            registry = build_registry(create_provider(args.provider))
        else:
            context = PortfolioContext(evidences=())
            registry = build_registry()

        result = PlannerAgent(registry).execute(
            PlannerInput(
                objective=args.objective,
                required_capabilities=tuple(args.capability or ()),
            ),
            context,
        )
    except (ValueError, ConfigurationError) as error:
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
    print("Agents:")

    for step in plan.steps:
        print(f"- {step.agent} [{', '.join(step.capabilities)}]")

    if args.run:
        return run_plan(plan, registry, context)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
