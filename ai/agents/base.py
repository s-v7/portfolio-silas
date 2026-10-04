from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from ai.agents.metadata import AgentMetadata
from ai.context.models import PortfolioContext
from ai.core.contracts import LLMProvider

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


@dataclass(frozen=True)
class AgentResult(Generic[OutputT]):
    agent: str
    output: OutputT
    provider: str | None = None
    model: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class Agent(ABC, Generic[InputT, OutputT]):
    name: str
    responsibility: str

    def __init__(self, provider: LLMProvider | None = None) -> None:
        self.provider = provider

    @abstractmethod
    def execute(
        self,
        agent_input: InputT,
        context: PortfolioContext,
    ) -> AgentResult[OutputT]:
        raise NotImplementedError


    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name=self.name,
            responsibility=self.responsibility,
            inputs=(self.__class__.__name__,),
            outputs=("AgentResult",),
            capabilities=(),
        )
