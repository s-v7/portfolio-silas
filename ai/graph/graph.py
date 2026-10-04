from __future__ import annotations

from collections import defaultdict
from typing import Any

from ai.context.models import PortfolioContext
from ai.graph.execution import (
    GraphExecutionReport,
    NodeExecutionRecord,
    NodeExecutionStatus,
    NodeTimer,
)
from ai.graph.node import GraphExecutionContext, GraphNode


class AgentGraph:
    def __init__(self, name: str) -> None:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Graph name cannot be empty.")

        self.name = normalized_name
        self._nodes: dict[str, GraphNode] = {}

    def add_node(self, node: GraphNode) -> AgentGraph:
        if node.name in self._nodes:
            raise ValueError(f"Graph node '{node.name}' is already registered.")

        self._nodes[node.name] = node
        return self

    @property
    def node_names(self) -> tuple[str, ...]:
        return tuple(self._nodes)

    def validate(self) -> None:
        for node in self._nodes.values():
            for dependency in node.dependencies:
                if dependency not in self._nodes:
                    raise ValueError(
                        f"Graph node '{node.name}' depends on unknown node "
                        f"'{dependency}'."
                    )

        self._topological_order()

    def execute(
        self,
        portfolio: PortfolioContext,
        inputs: dict[str, Any] | None = None,
    ) -> GraphExecutionReport:
        self.validate()

        execution_context = GraphExecutionContext(
            portfolio=portfolio,
            inputs=dict(inputs or {}),
            results={},
        )

        records: list[NodeExecutionRecord] = []
        statuses: dict[str, NodeExecutionStatus] = {}

        for node_name in self._topological_order():
            node = self._nodes[node_name]

            if failed_dependencies := tuple(
                dependency
                for dependency in node.dependencies
                if statuses.get(dependency)
                in {
                    NodeExecutionStatus.FAILED,
                    NodeExecutionStatus.SKIPPED,
                }
            ):
                statuses[node_name] = NodeExecutionStatus.SKIPPED
                records.append(
                    NodeExecutionRecord(
                        node=node_name,
                        status=NodeExecutionStatus.SKIPPED,
                        error=(
                            "Skipped because dependencies did not complete "
                            f"successfully: {', '.join(failed_dependencies)}"
                        ),
                    )
                )
                continue

            try:
                with NodeTimer() as timer:
                    output = node.handler(execution_context)

                execution_context.results[node_name] = output
                statuses[node_name] = NodeExecutionStatus.SUCCEEDED

                records.append(
                    NodeExecutionRecord(
                        node=node_name,
                        status=NodeExecutionStatus.SUCCEEDED,
                        duration_ms=timer.duration_ms,
                        output=output,
                    )
                )
            except Exception as error:
                statuses[node_name] = NodeExecutionStatus.FAILED

                records.append(
                    NodeExecutionRecord(
                        node=node_name,
                        status=NodeExecutionStatus.FAILED,
                        duration_ms=timer.duration_ms,
                        error=f"{type(error).__name__}: {error}",
                        exception=error,
                    )
                )

                if not node.continue_on_error:
                    self._append_pending_as_skipped(
                        records=records,
                        statuses=statuses,
                        current_node=node_name,
                    )
                    break

        return GraphExecutionReport(
            graph=self.name,
            records=tuple(records),
            results=dict(execution_context.results),
        )

    def get_node(self, name: str) -> GraphNode:
        if name not in self._nodes:
            raise KeyError(f"Graph node '{name}' is not registered.")

        return self._nodes[name]

    def execution_levels(self) -> tuple[tuple[str, ...], ...]:
        indegree = {
            node_name: len(node.dependencies) for node_name, node in self._nodes.items()
        }

        dependents: dict[str, list[str]] = defaultdict(list)

        for node_name, node in self._nodes.items():
            for dependency in node.dependencies:
                dependents[dependency].append(node_name)

        current_level = [
            node_name for node_name, degree in indegree.items() if degree == 0
        ]

        levels: list[tuple[str, ...]] = []
        visited_count = 0

        while current_level:
            levels.append(tuple(current_level))
            visited_count += len(current_level)

            next_level: list[str] = []

            for node_name in current_level:
                for dependent in dependents[node_name]:
                    indegree[dependent] -= 1

                    if indegree[dependent] == 0:
                        next_level.append(dependent)

            current_level = next_level

        if visited_count != len(self._nodes):
            raise ValueError("Agent graph contains a dependency cycle.")

        return tuple(levels)

    def _topological_order(self) -> tuple[str, ...]:
        return tuple(
            node_name for level in self.execution_levels() for node_name in level
        )

    def _append_pending_as_skipped(
        self,
        records: list[NodeExecutionRecord],
        statuses: dict[str, NodeExecutionStatus],
        current_node: str,
    ) -> None:
        for node_name in self._topological_order():
            if node_name == current_node or node_name in statuses:
                continue

            statuses[node_name] = NodeExecutionStatus.SKIPPED
            records.append(
                NodeExecutionRecord(
                    node=node_name,
                    status=NodeExecutionStatus.SKIPPED,
                    error=(
                        "Skipped because graph execution stopped after "
                        f"failure in '{current_node}'."
                    ),
                )
            )
