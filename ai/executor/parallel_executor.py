from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from typing import Any

from ai.context.models import PortfolioContext
from ai.graph.execution import (
    GraphExecutionReport,
    NodeExecutionRecord,
    NodeExecutionStatus,
    NodeTimer,
)
from ai.graph.graph import AgentGraph
from ai.graph.node import GraphExecutionContext, GraphNode
from ai.telemetry import NullTelemetry, Telemetry, TelemetryEvent

__all__ = ["ParallelExecutor"]


class ParallelExecutor:
    def __init__(
        self,
        max_workers: int | None = None,
        telemetry: Telemetry | None = None,
    ) -> None:
        self._max_workers = max_workers
        self._telemetry: Telemetry = telemetry or NullTelemetry()

    def execute(
        self,
        graph: AgentGraph,
        portfolio: PortfolioContext,
        inputs: dict[str, Any] | None = None,
    ) -> GraphExecutionReport:
        levels = graph.execution_levels()

        execution_context = GraphExecutionContext(
            portfolio=portfolio,
            inputs=dict(inputs or {}),
            results={},
        )

        self._emit(
            "workflow.started",
            graph=graph.name,
            node_count=len(graph.node_names),
        )

        records: list[NodeExecutionRecord] = []
        statuses: dict[str, NodeExecutionStatus] = {}
        halted = False

        for level in levels:
            if halted:
                for node_name in level:
                    statuses[node_name] = NodeExecutionStatus.SKIPPED
                    self._emit(
                        "node.skipped",
                        graph=graph.name,
                        node=node_name,
                    )
                    records.append(
                        NodeExecutionRecord(
                            node=node_name,
                            status=NodeExecutionStatus.SKIPPED,
                            error=(
                                "Skipped because graph execution halted "
                                "after a prior failure."
                            ),
                        )
                    )
                continue

            level_records, level_halted = self._execute_level(
                level=level,
                graph=graph,
                execution_context=execution_context,
                statuses=statuses,
            )
            records.extend(level_records)
            halted = halted or level_halted

        report = GraphExecutionReport(
            graph=graph.name,
            records=tuple(records),
            results=dict(execution_context.results),
        )

        self._emit(
            "workflow.completed" if report.succeeded else "workflow.failed",
            graph=graph.name,
            failed_nodes=report.failed_nodes,
        )

        return report

    def _execute_level(
        self,
        level: tuple[str, ...],
        graph: AgentGraph,
        execution_context: GraphExecutionContext,
        statuses: dict[str, NodeExecutionStatus],
    ) -> tuple[list[NodeExecutionRecord], bool]:
        records: list[NodeExecutionRecord] = []
        runnable: list[GraphNode] = []

        for node_name in level:
            node = graph.get_node(node_name)

            failed_dependencies = tuple(
                dependency
                for dependency in node.dependencies
                if statuses.get(dependency)
                in {NodeExecutionStatus.FAILED, NodeExecutionStatus.SKIPPED}
            )

            if failed_dependencies:
                statuses[node_name] = NodeExecutionStatus.SKIPPED
                self._emit(
                    "node.skipped",
                    graph=graph.name,
                    node=node_name,
                )
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

            runnable.append(node)

        halted = False

        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            future_to_node = {
                pool.submit(
                    self._run_node,
                    graph.name,
                    node,
                    execution_context,
                ): node
                for node in runnable
            }

            for future in future_to_node:
                node = future_to_node[future]
                record = future.result()

                records.append(record)
                statuses[node.name] = record.status

                if record.status is NodeExecutionStatus.SUCCEEDED:
                    execution_context.results[node.name] = record.output
                elif not node.continue_on_error:
                    halted = True

        return records, halted

    def _run_node(
        self,
        graph_name: str,
        node: GraphNode,
        execution_context: GraphExecutionContext,
    ) -> NodeExecutionRecord:
        timer = NodeTimer()

        self._emit("node.started", graph=graph_name, node=node.name)

        try:
            with timer:
                output = node.handler(execution_context)
        except Exception as error:
            self._emit(
                "node.failed",
                graph=graph_name,
                node=node.name,
                duration_ms=timer.duration_ms,
                error=f"{type(error).__name__}: {error}",
            )
            return NodeExecutionRecord(
                node=node.name,
                status=NodeExecutionStatus.FAILED,
                duration_ms=timer.duration_ms,
                error=f"{type(error).__name__}: {error}",
                exception=error,
            )

        self._emit(
            "node.completed",
            graph=graph_name,
            node=node.name,
            duration_ms=timer.duration_ms,
        )

        return NodeExecutionRecord(
            node=node.name,
            status=NodeExecutionStatus.SUCCEEDED,
            duration_ms=timer.duration_ms,
            output=output,
        )

    def _emit(self, name: str, **attributes: Any) -> None:
        # Telemetry observes; a faulty sink must never affect execution.
        with suppress(Exception):
            self._telemetry.emit(
                TelemetryEvent(name=name, attributes=attributes)
            )
