from __future__ import annotations

from typing import Any

import pytest
from pytest import MonkeyPatch

from ai.core.contracts import (
    GenerationOptions,
    Message,
    ProviderRequest,
    TaskType,
)
from ai.core.exceptions import ProviderError
from ai.providers.anthropic_provider import AnthropicProvider


def request(*msgs: Message) -> ProviderRequest:
    return ProviderRequest(
        task=TaskType.SHORT_TEXT,
        messages=msgs,
        options=GenerationOptions(temperature=0.2, max_tokens=100),
    )


def test_maps_roles_and_joins_the_system_messages(monkeypatch: MonkeyPatch) -> None:
    prv = AnthropicProvider(api_key="test-key")
    seen: dict[str, Any] = {}

    def fake_create(**kwargs: Any) -> Any:
        seen.update(kwargs)
        raise RuntimeError("stop here")

    monkeypatch.setattr(prv._client.messages, "create", fake_create)
    req = request(
        Message(role="system", content="first rule"),
        Message(role="user", content="question"),
        Message(role="assistant", content="answer"),
        Message(role="system", content="second rule"),
    )

    with pytest.raises(ProviderError, match="stop here"):
        prv.generate(req)

    assert seen["system"] == "first rule\n\nsecond rule"
    assert seen["messages"] == [
        {"role": "user", "content": "question"},
        {"role": "assistant", "content": "answer"},
    ]


def test_rejects_unsupported_roles() -> None:
    prv = AnthropicProvider(api_key="test-key")

    with pytest.raises(ProviderError, match="only system, user and assistant"):
        prv.generate(request(Message(role="tool", content="x")))


def test_requires_a_user_or_assistant_message() -> None:
    prv = AnthropicProvider(api_key="test-key")

    with pytest.raises(ProviderError, match="at least one user or assistant"):
        prv.generate(request(Message(role="system", content="only rules")))
