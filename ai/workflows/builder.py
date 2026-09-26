from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai.agents.base import Agent
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.graph.graph import AgentGraph
from ai.graph.node import GraphNode


@dataclass(frozen=True, slots=True)
class WorkflowNodeSpec:
    name: str
    agent: str
    dependencies: tuple[str, ...] = ()
    continue_on_error: bool = False


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

    def add(
        self,
        name: str,
        agent: str,
        *,
        continue_on_error: bool = False,
    ) -> WorkflowBuilder:
        normalized_name = name.strip()
        normalized_agent = agent.strip()

        if not normalized_name:
            raise ValueError("Workflow node name cannot be empty.")

        if not normalized_agent:
            raise ValueError("Agent name cannot be empty.")

        if normalized_name in self._nodes:
            raise ValueError(
                f"Workflow node '{normalized_name}' is already defined."
            )

        self._registry.get(normalized_agent)

        self._nodes[normalized_name] = WorkflowNodeSpec(
            name=normalized_name,
            agent=normalized_agent,
            continue_on_error=continue_on_error,
        )

        return self

    def depends_on(
        self,
        node: str,
        *dependencies: str,
    ) -> WorkflowBuilder:
        if node not in self._nodes:
            raise KeyError(
                f"Workflow node '{node}' is not defined."
            )

        for dependency in dependencies:
            if dependency not in self._nodes:
                raise KeyError(
                    f"Workflow node '{dependency}' is not defined."
                )

        current = self._nodes[node]

        self._nodes[node] = WorkflowNodeSpec(
            name=current.name,
            agent=current.agent,
            dependencies=tuple(
                dict.fromkeys(
                    (*current.dependencies, *dependencies)
                )
            ),
            continue_on_error=current.continue_on_error,
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
            ) -> Any:
                portfolio_context = graph_context.context

                if not isinstance(
                    portfolio_context,
                    PortfolioContext,
                ):
                    raise TypeError(
                        "Workflow graph context must contain "
                        "a PortfolioContext."
                    )

                return current_agent.execute(
                    None,
                    portfolio_context,
                )

            graph.add_node(
                GraphNode(
                    name=spec.name,
                    dependencies=spec.dependencies,
                    handler=handler,
                    continue_on_error=spec.continue_on_error,
                )
            )

        return graph
