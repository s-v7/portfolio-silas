from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ai.context.models import PortfolioContext

NodeHandler = Callable[["GraphExecutionContext"], Any]


@dataclass(frozen=True, slots=True)
class GraphNode:
    name: str
    handler: NodeHandler
    dependencies: tuple[str, ...] = ()
    continue_on_error: bool = False

    def __post_init__(self) -> None:
        normalized_name = self.name.strip()

        if not normalized_name:
            raise ValueError(
                "Graph node name cannot be empty."
            )

        if len(set(self.dependencies)) != len(
            self.dependencies
        ):
            raise ValueError(
                f"Graph node '{normalized_name}' "
                "contains duplicate dependencies."
            )

        if normalized_name in self.dependencies:
            raise ValueError(
                f"Graph node '{normalized_name}' "
                "cannot depend on itself."
            )


@dataclass(slots=True)
class GraphExecutionContext:
    portfolio: PortfolioContext
    inputs: dict[str, Any]
    results: dict[str, Any]

    def get_input(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.inputs.get(key, default)

    def get_result(self, node_name: str) -> Any:
        if node_name not in self.results:
            raise KeyError(
                f"Result for graph node '{node_name}' "
                "is not available."
            )

        return self.results[node_name]
