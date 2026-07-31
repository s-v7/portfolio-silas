from __future__ import annotations

import pytest

from ai.context.models import PortfolioContext
from ai.graph import (
    AgentGraph,
    GraphExecutionContext,
    GraphNode,
    NodeExecutionStatus,
)


def empty_context() -> PortfolioContext:
    return PortfolioContext(evidences=())


def test_executes_nodes_in_dependency_order() -> None:
    execution_order: list[str] = []

    def collect(_context: object) -> dict[str, int]:
        execution_order.append("collect")
        return {"evidence": 1}

    def validate(context: GraphExecutionContext) -> object:
        execution_order.append("validate")
        return context.get_result("collect")

    def generate(_context: object) -> str:
        execution_order.append("generate")
        return "README"

    graph = AgentGraph("portfolio")

    graph.add_node(
        GraphNode(
            name="collect",
            handler=collect,
        )
    )

    graph.add_node(
        GraphNode(
            name="validate",
            dependencies=("collect",),
            handler=validate,
        )
    )

    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("validate",),
            handler=generate,
        )
    )

    report = graph.execute(empty_context())

    assert execution_order == ["collect", "validate", "generate"]
    assert report.succeeded is True
    assert report.results["generate"] == "README"


def test_rejects_unknown_dependency() -> None:
    graph = AgentGraph("invalid")

    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("missing",),
            handler=lambda context: None,
        )
    )

    with pytest.raises(ValueError, match="unknown node"):
        graph.validate()


def test_rejects_dependency_cycle() -> None:
    graph = AgentGraph("cyclic")

    graph.add_node(
        GraphNode(
            name="first",
            dependencies=("second",),
            handler=lambda context: None,
        )
    )

    graph.add_node(
        GraphNode(
            name="second",
            dependencies=("first",),
            handler=lambda context: None,
        )
    )

    with pytest.raises(ValueError, match="dependency cycle"):
        graph.validate()


def test_stops_graph_after_node_failure() -> None:
    graph = AgentGraph("failure")

    def fail(_context: object) -> None:
        raise RuntimeError("provider unavailable")

    graph.add_node(
        GraphNode(
            name="validate",
            handler=fail,
        )
    )

    graph.add_node(
        GraphNode(
            name="generate",
            dependencies=("validate",),
            handler=lambda context: "README",
        )
    )

    report = graph.execute(empty_context())

    assert report.succeeded is False
    assert report.failed_nodes == ("validate",)
    assert report.records[0].status is NodeExecutionStatus.FAILED
    assert report.records[1].status is NodeExecutionStatus.SKIPPED


def test_can_continue_after_non_blocking_failure() -> None:
    graph = AgentGraph("resilient")

    def fail(_context: object) -> None:
        raise RuntimeError("optional node failed")

    graph.add_node(
        GraphNode(
            name="optional",
            handler=fail,
            continue_on_error=True,
        )
    )

    graph.add_node(
        GraphNode(
            name="independent",
            handler=lambda context: "completed",
        )
    )

    report = graph.execute(empty_context())

    assert report.results["independent"] == "completed"
    assert report.failed_nodes == ("optional",)


def test_rejects_duplicate_dependencies() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate dependencies",
    ):
        GraphNode(
            name="generate",
            dependencies=("validate", "validate"),
            handler=lambda context: None,
        )


def test_rejects_self_dependency() -> None:
    with pytest.raises(
        ValueError,
        match="cannot depend on itself",
    ):
        GraphNode(
            name="validate",
            dependencies=("validate",),
            handler=lambda context: None,
        )


def test_rejects_missing_result_access() -> None:
    graph = AgentGraph("missing-result")

    graph.add_node(
        GraphNode(
            name="generate",
            handler=lambda context: context.get_result("validate"),
        )
    )

    report = graph.execute(empty_context())

    assert report.succeeded is False
    assert report.failed_nodes == ("generate",)
    assert "is not available" in (report.records[0].error or "")
