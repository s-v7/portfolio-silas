from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import replace
from functools import partial
from pathlib import Path
from typing import Any

from ai.agents.about_agent import AboutAgent, AboutAgentInput
from ai.agents.base import AgentResult
from ai.agents.bio_agent import BioAgent, BioAgentInput
from ai.agents.evidence_validator import (
    EvidenceValidationReport,
    EvidenceValidatorAgent,
)
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.agents.registry import AgentRegistry
from ai.context.json_loader import load_portfolio_context
from ai.context.merge import merge_contexts
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import (
    ConfigurationError,
    EvidenceValidationError,
    FileChangeValidationError,
    ProviderError,
)
from ai.executor.parallel_executor import ParallelExecutor
from ai.graph import NodeExecutionStatus
from ai.planner.plan import ExecutionPlan
from ai.planner.planner import PlannerAgent, PlannerInput
from ai.providers.factory import ProviderFactory
from ai.services.draft_writer import DraftWriter
from ai.workflows.about_checks import make_about_check
from ai.workflows.bio_checks import make_bio_check
from ai.workflows.builder import WorkflowBuilder

README_AGENT = "readme-agent"
ABOUT_AGENT = "about-agent"
BIO_AGENT = "bio-agent"
DEFAULT_OUTPUT_ROOT = Path("ai/output/drafts")


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
    selected = provider or PlanOnlyProvider()

    registry = AgentRegistry()
    registry.register(ReadmeAgent(selected))
    registry.register(EvidenceValidatorAgent[None]())
    registry.register(AboutAgent(selected))
    registry.register(BioAgent(selected))
    return registry


def require_verified_evidence(
    result: AgentResult[EvidenceValidationReport],
) -> None:
    if not result.output.valid:
        raise EvidenceValidationError(
            "No verified evidence is available for README generation."
        )


# Domain tables: what each agent receives, and which check a capability implies.
INPUT_FACTORIES: dict[str, Callable[[PortfolioContext], Any]] = {
    README_AGENT: lambda context: ReadmeAgentInput(language=context.language),
    ABOUT_AGENT: lambda context: AboutAgentInput(language=context.language),
    BIO_AGENT: lambda cxt: BioAgentInput(language=cxt.language),
}

CHECK_FACTORIES: dict[
    str, Callable[[PortfolioContext], Callable[[Any], None]]
] = {
    "verification": lambda context: require_verified_evidence,
    "about": make_about_check,
    "bio": make_bio_check,
}


MAX_RETRIES = 2


def check_reason(msg: str) -> str:
    """Keep only the check's reason: echoing the rejected text invites a copy."""
    return msg.split("\n--- rejected text ---")[0]


# On a rejected text, the agent runs again with the check's reason as feedback.
RETRY_INPUTS: dict[str, Callable[[Any, str], Any]] = {
    ABOUT_AGENT: lambda inp, fdb: replace(inp, feedback=check_reason(fdb)),
    BIO_AGENT: lambda inp, fdb: replace(inp, feedback=check_reason(fdb)),
}


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
        help="Execute the plan and print what the agents generate.",
    )
    parser.add_argument(
        "--evidence-file",
        action="append",
        type=Path,
        default=None,
        help="JSON evidence file (required with --run; repeat to merge).",
    )
    parser.add_argument(
        "--provider",
        choices=("proxy", "openai", "anthropic", "nvidia"),
        default=None,
        help="LLM provider for --run. Defaults to LLM_PROVIDER or proxy.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Relative path inside ai/output/drafts for the generated text.",
    )
    return parser


def output_checks(
    plan: ExecutionPlan,
    context: PortfolioContext,
) -> dict[str, Callable[[Any], None]]:
    checks: dict[str, Callable[[Any], None]] = {}

    for step in plan.steps:
        for capability in step.capabilities:
            factory = CHECK_FACTORIES.get(capability)

            if factory is not None:
                checks[step.agent] = factory(context)

    return checks


def run_plan(
    plan: ExecutionPlan,
    registry: AgentRegistry,
    context: PortfolioContext,
    output: str | None = None,
) -> int:
    agents = {step.agent for step in plan.steps}

    builder = WorkflowBuilder.from_plan(
        plan,
        registry,
        input_factories={
            name: partial(factory, context)
            for name, factory in INPUT_FACTORIES.items()
            if name in agents
        },
        output_checks=output_checks(plan, context),
        retry_inputs=RETRY_INPUTS,
        retries=MAX_RETRIES,
    )

    verifiers = [s.agent for s in plan.steps if "verification" in s.capabilities]
    generators = [s.agent for s in plan.steps if "generation" in s.capabilities]

    # Domain rule: nothing is generated before the evidence is verified.
    if verifiers:
        for generator in generators:
            builder.depends_on(generator, *verifiers)

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

    generated = [name for name in generators if name in report.results]

    for name in generated:
        print()

        if len(generated) > 1:
            print(f"[{name}]")

        print(report.results[name].output.content)

    if output is not None and generated:
        content = report.results[generated[0]].output.content

        try:
            destination = DraftWriter(DEFAULT_OUTPUT_ROOT).write(
                relative_path=output,
                content=content,
            )
        except FileChangeValidationError as error:
            print(f"Could not write draft: {error}", file=sys.stderr)
            return 1

        print(f"Draft: {destination}")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.run and args.evidence_file is None:
        print("--run requires --evidence-file.", file=sys.stderr)
        return 1

    if args.output is not None and not args.run:
        print("--output requires --run.", file=sys.stderr)
        return 1

    try:
        if args.run:
            context = merge_contexts(
                [load_portfolio_context(pth) for pth in args.evidence_file]
            )
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

    generators = [s for s in plan.steps if "generation" in s.capabilities]

    if args.output is not None and len(generators) != 1:
        print(
            "--output needs a plan with exactly one generating agent.",
            file=sys.stderr,
        )
        return 1

    print(f"Objective: {plan.objective}")
    print("Agents:")

    for step in plan.steps:
        print(f"- {step.agent} [{', '.join(step.capabilities)}]")

    if args.run:
        return run_plan(plan, registry, context, args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
