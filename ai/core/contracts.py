from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TaskType(StrEnum):
    SHORT_TEXT = "short_text"
    LONG_MARKDOWN = "long_markdown"
    ANALYSIS = "analysis"
    REVIEW = "review"
    TRANSLATION = "translation"


class EvidenceStatus(StrEnum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    CONFLICTING = "conflicting"


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class GenerationOptions:
    max_tokens: int = 2_000
    temperature: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderRequest:
    messages: Sequence[Message]
    task: TaskType
    model: str | None = None
    options: GenerationOptions = field(default_factory=GenerationOptions)


@dataclass(frozen=True)
class ProviderResponse:
    content: str
    provider: str
    model: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


class LLMProvider(ABC):
    """Provider-independent contract used by portfolio agents."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError
