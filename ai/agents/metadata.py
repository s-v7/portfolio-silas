from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentMetadata:
    name: str
    responsibility: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    capabilities: tuple[str, ...]
