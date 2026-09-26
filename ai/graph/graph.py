from __future__ import annotations

from collections import defaultdict, deque
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
            raise ValueError(
                f"Graph node '{node.name}' is already registered."
            )

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

            failed_dependencies = tuple(
                dependency
                for dependency in node.dependencies
                if statuses.get(dependency)
                in {
                    NodeExecutionStatus.FAILED,
                    NodeExecutionStatus.SKIPPED,
                }
            )

            if failed_dependencies:
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

    def _topological_order(self) -> tuple[str, ...]:
        indegree = {
            node_name: len(node.dependencies)
            for node_name, node in self._nodes.items()
        }

        dependents: dict[str, list[str]] = defaultdict(list)

        for node_name, node in self._nodes.items():
            for dependency in node.dependencies:
                dependents[dependency].append(node_name)

        queue = deque(
            node_name
            for node_name, degree in indegree.items()
            if degree == 0
        )

        ordered: list[str] = []

        while queue:
            node_name = queue.popleft()
            ordered.append(node_name)

            for dependent in dependents[node_name]:
                indegree[dependent] -= 1

                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(ordered) != len(self._nodes):
            raise ValueError("Agent graph contains a dependency cycle.")

        return tuple(ordered)

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
