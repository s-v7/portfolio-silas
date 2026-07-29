from __future__ import annotations

from typing import Any

import pytest
import requests

from ai.core.contracts import (
    GenerationOptions,
    Message,
    ProviderRequest,
    TaskType,
)
from ai.core.exceptions import ProviderError
from ai.providers.openai_provider import OpenAIProvider


class FakeResponse:
    def __init__(
        self,
        payload: dict[str, Any],
        *,
        ok: bool = True,
        status_code: int = 200,
        text: str = "",
    ) -> None:
        self._payload = payload
        self.ok = ok
        self.status_code = status_code
        self.text = text

    def json(self) -> dict[str, Any]:
        return self._payload


def build_request() -> ProviderRequest:
    return ProviderRequest(
        messages=(
            Message(
                role="user",
                content="Generate a professional summary.",
            ),
        ),
        task=TaskType.SHORT_TEXT,
        options=GenerationOptions(max_tokens=100),
    )


def test_generates_text_from_openai(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        *args: object,
        **kwargs: object,
    ) -> FakeResponse:
        return FakeResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Backend engineer.",
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 4,
                },
            }
        )

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OpenAIProvider(api_key="fake-key")
    response = provider.generate(build_request())

    assert response.content == "Backend engineer."
    assert response.provider == "openai"
    assert response.model
    assert response.metadata["usage"]["prompt_tokens"] == 10


def test_rejects_empty_openai_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        *args: object,
        **kwargs: object,
    ) -> FakeResponse:
        return FakeResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": " ",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OpenAIProvider(api_key="fake-key")

    with pytest.raises(ProviderError, match="empty response"):
        provider.generate(build_request())


def test_wraps_network_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        *args: object,
        **kwargs: object,
    ) -> FakeResponse:
        raise requests.ConnectionError("network unavailable")

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OpenAIProvider(api_key="fake-key")

    with pytest.raises(ProviderError, match="request failed"):
        provider.generate(build_request())


def test_rejects_invalid_response_structure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        *args: object,
        **kwargs: object,
    ) -> FakeResponse:
        return FakeResponse({"unexpected": True})

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OpenAIProvider(api_key="fake-key")

    with pytest.raises(
        ProviderError,
        match="invalid response structure",
    ):
        provider.generate(build_request())
