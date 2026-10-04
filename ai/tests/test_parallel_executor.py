from __future__ import annotations

import time

import pytest

from ai.context.models import PortfolioContext
from ai.executor.parallel_executor import ParallelExecutor
from ai.graph import AgentGraph, GraphNode, NodeExecutionStatus


def empty_context() -> PortfolioContext:
    return PortfolioContext(evidences=())


def test_executes_independent_level_nodes_concurrently() -> None:
    graph = AgentGraph("concurrent")

    def slow(_context: object) -> str:
        time.sleep(0.15)
        return "done"

    graph.add_node(GraphNode(name="a", handler=slow))
    graph.add_node(GraphNode(name="b", handler=slow))

    started_at = time.perf_counter()
    report = ParallelExecutor().execute(graph, empty_context())
    elapsed = time.perf_counter() - started_at

    assert report.succeeded is True
    assert elapsed < 0.28


def test_executes_diamond_dependencies_with_correct_results() -> None:
    graph = AgentGraph("diamond")

    graph.add_node(GraphNode(name="collect", handler=lambda context: 1))
    graph.add_node(
        GraphNode(
            name="validate",
            dependencies=("collect",),
            handler=lambda context: context.get_result("collect") + 1,
        )
    )
    graph.add_node(
        GraphNode(
            name="enrich",
            dependencies=("collect",),
            handler=lambda context: context.get_result("collect") + 2,
        )
    )
    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("validate", "enrich"),
            handler=lambda context: (
                context.get_result("validate") + context.get_result("enrich")
            ),
        )
    )

    report = ParallelExecutor().execute(graph, empty_context())

    assert report.succeeded is True
    assert report.results["generate"] == 5


def test_halts_remaining_levels_after_hard_failure() -> None:
    graph = AgentGraph("hard-failure")

    def fail(_context: object) -> None:
        raise RuntimeError("provider unavailable")

    graph.add_node(GraphNode(name="validate", handler=fail))
    graph.add_node(GraphNode(name="unrelated", handler=lambda context: "ok"))
    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("validate",),
            handler=lambda context: "README",
        )
    )

    report = ParallelExecutor().execute(graph, empty_context())

    assert report.succeeded is False
    assert report.failed_nodes == ("validate",)

    statuses = {record.node: record.status for record in report.records}
    assert statuses["unrelated"] == NodeExecutionStatus.SUCCEEDED
    assert statuses["generate"] == NodeExecutionStatus.SKIPPED


def test_continues_after_non_blocking_failure() -> None:
    graph = AgentGraph("resilient")

    def fail(_context: object) -> None:
        raise RuntimeError("optional node failed")

    graph.add_node(GraphNode(name="optional", handler=fail, continue_on_error=True))
    graph.add_node(GraphNode(name="independent", handler=lambda context: "completed"))

    report = ParallelExecutor().execute(graph, empty_context())

    assert report.results["independent"] == "completed"
    assert report.failed_nodes == ("optional",)


def test_raises_for_dependency_cycle() -> None:
    graph = AgentGraph("cyclic")

    graph.add_node(
        GraphNode(name="first", dependencies=("second",), handler=lambda context: None)
    )
    graph.add_node(
        GraphNode(name="second", dependencies=("first",), handler=lambda context: None)
    )

    with pytest.raises(ValueError, match="dependency cycle"):
        ParallelExecutor().execute(graph, empty_context())


def test_matches_sequential_results_for_same_graph() -> None:
    def build_graph() -> AgentGraph:
        graph = AgentGraph("comparison")
        graph.add_node(GraphNode(name="collect", handler=lambda context: 1))
        graph.add_node(
            GraphNode(
                name="generate",
                dependencies=("collect",),
                handler=lambda context: context.get_result("collect") + 1,
            )
        )
        return graph

    sequential_report = build_graph().execute(empty_context())
    parallel_report = ParallelExecutor().execute(build_graph(), empty_context())

    assert sequential_report.succeeded == parallel_report.succeeded
    assert sequential_report.results == parallel_report.results
