from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from ai.agents.base import Agent
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.graph.graph import AgentGraph
from ai.graph.node import GraphNode
from ai.planner.plan import ExecutionPlan


@dataclass(frozen=True, slots=True)
class WorkflowNodeSpec:
    name: str
    agent: str
    dependencies: tuple[str, ...] = ()
    continue_on_error: bool = False
    input_factory: Callable[[], Any] | None = None
    output_check: Callable[[Any], None] | None = None


class WorkflowBuilder:
    def __init__(
        self,
        name: str,
        registry: AgentRegistry,
    ) -> None:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Workflow name cannot be empty.")

        self._name = normalized_name
        self._registry = registry
        self._nodes: dict[str, WorkflowNodeSpec] = {}

    @classmethod
    def from_plan(
        cls,
        plan: ExecutionPlan,
        registry: AgentRegistry,
        *,
        name: str | None = None,
        input_factories: Mapping[str, Callable[[], Any]] | None = None,
        output_checks: Mapping[str, Callable[[Any], None]] | None = None,
    ) -> WorkflowBuilder:
        if not plan.steps:
            raise ValueError("Execution plan has no steps.")

        factories = input_factories or {}
        checks = output_checks or {}
        builder = cls(name or plan.objective, registry)

        for step in plan.steps:
            builder.add(
                step.agent,
                step.agent,
                input_factory=factories.get(step.agent),
                output_check=checks.get(step.agent),
            )

        return builder

    def add(
        self,
        name: str,
        agent: str,
        *,
        continue_on_error: bool = False,
        input_factory: Callable[[], Any] | None = None,
        output_check: Callable[[Any], None] | None = None,
    ) -> WorkflowBuilder:
        normalized_name = name.strip()
        normalized_agent = agent.strip()

        if not normalized_name:
            raise ValueError("Workflow node name cannot be empty.")

        if not normalized_agent:
            raise ValueError("Agent name cannot be empty.")

        if normalized_name in self._nodes:
            raise ValueError(f"Workflow node '{normalized_name}' is already defined.")

        self._registry.get(normalized_agent)

        self._nodes[normalized_name] = WorkflowNodeSpec(
            name=normalized_name,
            agent=normalized_agent,
            continue_on_error=continue_on_error,
            input_factory=input_factory,
            output_check=output_check,
        )

        return self

    def depends_on(
        self,
        node: str,
        *dependencies: str,
    ) -> WorkflowBuilder:
        if node not in self._nodes:
            raise KeyError(f"Workflow node '{node}' is not defined.")

        for dependency in dependencies:
            if dependency not in self._nodes:
                raise KeyError(f"Workflow node '{dependency}' is not defined.")

        current = self._nodes[node]

        self._nodes[node] = WorkflowNodeSpec(
            name=current.name,
            agent=current.agent,
            dependencies=tuple(dict.fromkeys((*current.dependencies, *dependencies))),
            continue_on_error=current.continue_on_error,
            input_factory=current.input_factory,
            output_check=current.output_check,
        )

        return self

    def build(self) -> AgentGraph:
        graph = AgentGraph(self._name)

        for spec in self._nodes.values():
            agent = self._registry.get(spec.agent)

            def handler(
                graph_context: Any,
                *,
                current_agent: Agent[Any, Any] = agent,
                current_input_factory: Callable[[], Any] | None = spec.input_factory,
                current_output_check: Callable[[Any], None] | None = spec.output_check,
            ) -> Any:
                portfolio_context = graph_context.portfolio

                if not isinstance(
                    portfolio_context,
                    PortfolioContext,
                ):
                    raise TypeError(
                        "Workflow graph context must contain a PortfolioContext."
                    )

                agent_input = (
                    current_input_factory()
                    if current_input_factory is not None
                    else None
                )

                result = current_agent.execute(
                    agent_input,
                    portfolio_context,
                )

                if current_output_check is not None:
                    current_output_check(result)

                return result

            graph.add_node(
                GraphNode(
                    name=spec.name,
                    dependencies=spec.dependencies,
                    handler=handler,
                    continue_on_error=spec.continue_on_error,
                )
            )

        return graph
