from __future__ import annotations

from typing import Any

import pytest

from ai.agents.base import Agent, AgentResult
from ai.agents.registry import AgentRegistry
from ai.context.models import PortfolioContext
from ai.core.exceptions import AgentExecutionError
from ai.planner.plan import ExecutionPlan, ExecutionStep
from ai.workflows.builder import WorkflowBuilder


class Scripted(Agent[Any, str]):
    name = "scripted"
    responsibility = "Returns scripted outputs and records its inputs."

    def __init__(self, outs: list[str]) -> None:
        super().__init__()
        self.outs = list(outs)
        self.inputs: list[Any] = []

    def execute(
        self,
        agent_input: Any,
        context: PortfolioContext,
    ) -> AgentResult[str]:
        del context
        self.inputs.append(agent_input)

        return AgentResult(agent=self.name, output=self.outs.pop(0))


class Broken(Scripted):
    def execute(self, agent_input: Any, context: PortfolioContext) -> AgentResult[str]:
        self.inputs.append(agent_input)
        raise RuntimeError("provider down")


def reject_bad(rst: AgentResult[str]) -> None:
    if rst.output == "bad":
        raise AgentExecutionError("bad output")


def feed(inp: Any, fdb: str) -> str:
    return f"{inp}|{fdb}"


def cxt() -> PortfolioContext:
    return PortfolioContext(evidences=())


def registry(agent: Scripted) -> AgentRegistry:
    reg = AgentRegistry()
    reg.register(agent)
    return reg


def test_retries_until_the_check_passes_feeding_the_reason() -> None:
    agt = Scripted(["bad", "bad", "good"])
    graph = (
        WorkflowBuilder("w", registry(agt))
        .add(
            "n",
            "scripted",
            input_factory=lambda: "in",
            output_check=reject_bad,
            retry_input=feed,
            retries=2,
        )
        .build()
    )

    rep = graph.execute(cxt())

    assert rep.succeeded is True
    assert rep.results["n"].output == "good"
    assert agt.inputs == ["in", "in|bad output", "in|bad output|bad output"]


def test_gives_up_after_the_limit() -> None:
    agt = Scripted(["bad", "bad", "bad"])
    graph = (
        WorkflowBuilder("w", registry(agt))
        .add(
            "n",
            "scripted",
            input_factory=lambda: "in",
            output_check=reject_bad,
            retry_input=feed,
            retries=1,
        )
        .build()
    )

    rep = graph.execute(cxt())

    assert rep.failed_nodes == ("n",)
    assert len(agt.inputs) == 2
    assert "bad output" in (rep.records[0].error or "")


def test_does_not_retry_without_a_retry_input() -> None:
    agt = Scripted(["bad", "good"])
    graph = (
        WorkflowBuilder("w", registry(agt))
        .add("n", "scripted", output_check=reject_bad, retries=2)
        .build()
    )

    rep = graph.execute(cxt())

    assert rep.failed_nodes == ("n",)
    assert len(agt.inputs) == 1


def test_only_check_failures_are_retried() -> None:
    agt = Broken([])
    graph = (
        WorkflowBuilder("w", registry(agt))
        .add(
            "n",
            "scripted",
            output_check=reject_bad,
            retry_input=feed,
            retries=2,
        )
        .build()
    )

    rep = graph.execute(cxt())

    assert rep.failed_nodes == ("n",)
    assert len(agt.inputs) == 1


def test_from_plan_passes_the_retry_settings() -> None:
    agt = Scripted(["bad", "good"])
    plan = ExecutionPlan(
        objective="Retry",
        steps=(ExecutionStep(agent="scripted"),),
    )
    graph = WorkflowBuilder.from_plan(
        plan,
        registry(agt),
        input_factories={"scripted": lambda: "in"},
        output_checks={"scripted": reject_bad},
        retry_inputs={"scripted": feed},
        retries=1,
    ).build()

    rep = graph.execute(cxt())

    assert rep.succeeded is True
    assert agt.inputs == ["in", "in|bad output"]


def test_negative_retries_are_rejected() -> None:
    bld = WorkflowBuilder("w", registry(Scripted([])))

    with pytest.raises(ValueError, match="retries"):
        bld.add("n", "scripted", retries=-1)
