from __future__ import annotations

from typing import Any

from ai.agents.base import Agent
from ai.agents.metadata import AgentMetadata


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent[Any, Any]] = {}

    def register(self,agent: Agent[Any, Any]) -> None:
        metadata = agent.metadata

        if metadata.name in self._agents:
            raise ValueError(f"Agent '{metadata.name}' is already registered.")
        self._agents[metadata.name] = agent

    def get(self,name: str) -> Agent[Any, Any]:
        try:
            return self._agents[name]
        except KeyError as exc:
            raise KeyError(f"Agent '{name}' is not registered.") from exc

    def list(self) -> tuple[AgentMetadata, ...]:
        return tuple(agent.metadata for agent in self._agents.values())

    def find_by_capability(self,capability: str) -> tuple[AgentMetadata, ...]:
        return tuple(
            metadata
            for metadata in self.list()
            if capability in metadata.capabilities
        )

    def __len__(self) -> int:
        return len(self._agents)
