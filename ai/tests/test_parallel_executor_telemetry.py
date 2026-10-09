from __future__ import annotations

from ai.context.models import PortfolioContext
from ai.executor.parallel_executor import ParallelExecutor
from ai.graph import AgentGraph, GraphNode
from ai.telemetry import InMemoryTelemetry, TelemetryEvent


def empty_context() -> PortfolioContext:
    return PortfolioContext(evidences=())


def names(telemetry: InMemoryTelemetry) -> tuple[str, ...]:
    return tuple(event.name for event in telemetry.events)


class BrokenTelemetry:
    def emit(self, event: TelemetryEvent) -> None:
        raise RuntimeError("sink unavailable")


def linear_graph() -> AgentGraph:
    graph = AgentGraph("linear")
    graph.add_node(GraphNode(name="a", handler=lambda context: 1))
    graph.add_node(
        GraphNode(
            name="b",
            dependencies=("a",),
            handler=lambda context: 2,
        )
    )
    return graph


def test_emits_lifecycle_events_in_order_for_linear_graph() -> None:
    telemetry = InMemoryTelemetry()

    ParallelExecutor(telemetry=telemetry).execute(
        linear_graph(), empty_context()
    )

    assert names(telemetry) == (
        "workflow.started",
        "node.started",
        "node.completed",
        "node.started",
        "node.completed",
        "workflow.completed",
    )


def test_node_events_carry_graph_node_and_duration() -> None:
    telemetry = InMemoryTelemetry()

    ParallelExecutor(telemetry=telemetry).execute(
        linear_graph(), empty_context()
    )

    completed = [
        event for event in telemetry.events if event.name == "node.completed"
    ]

    assert [event.attributes["node"] for event in completed] == ["a", "b"]
    assert all(event.attributes["graph"] == "linear" for event in completed)
    assert all("duration_ms" in event.attributes for event in completed)


def test_emits_failed_skipped_and_workflow_failed() -> None:
    telemetry = InMemoryTelemetry()
    graph = AgentGraph("failing")

    def fail(_context: object) -> None:
        raise RuntimeError("provider unavailable")

    graph.add_node(GraphNode(name="validate", handler=fail))
    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("validate",),
            handler=lambda context: "README",
        )
    )

    ParallelExecutor(telemetry=telemetry).execute(graph, empty_context())

    assert names(telemetry) == (
        "workflow.started",
        "node.started",
        "node.failed",
        "node.skipped",
        "workflow.failed",
    )

    failed = next(
        event for event in telemetry.events if event.name == "node.failed"
    )
    assert failed.attributes["node"] == "validate"
    assert "RuntimeError" in failed.attributes["error"]


def test_concurrent_nodes_emit_one_started_and_completed_each() -> None:
    telemetry = InMemoryTelemetry()
    graph = AgentGraph("concurrent")

    graph.add_node(GraphNode(name="a", handler=lambda context: "a"))
    graph.add_node(GraphNode(name="b", handler=lambda context: "b"))

    ParallelExecutor(telemetry=telemetry).execute(graph, empty_context())

    emitted = names(telemetry)

    assert emitted.count("node.started") == 2
    assert emitted.count("node.completed") == 2
    assert emitted[0] == "workflow.started"
    assert emitted[-1] == "workflow.completed"


def test_broken_telemetry_does_not_affect_execution() -> None:
    report = ParallelExecutor(telemetry=BrokenTelemetry()).execute(
        linear_graph(), empty_context()
    )

    assert report.succeeded is True
    assert report.results == {"a": 1, "b": 2}


def test_executor_without_telemetry_still_works() -> None:
    report = ParallelExecutor().execute(linear_graph(), empty_context())

    assert report.succeeded is True
