from __future__ import annotations

import os
from typing import Any

import requests

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import ConfigurationError, ProviderError
from ai.core.model_router import get_model


class NvidiaProvider(LLMProvider):
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        timeout: int = 90,
    ) -> None:
        self._api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

        if not self._api_key:
            raise ConfigurationError("NVIDIA_API_KEY is required.")

    @property
    def name(self) -> str:
        return "nvidia"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        model = request.model or get_model(
            request.task.value,
            self.name,
        )

        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in request.messages
            ],
            "max_tokens": request.options.max_tokens,
        }

        if request.options.temperature is not None:
            payload["temperature"] = request.options.temperature

        try:
            response = requests.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise ProviderError(
                f"NVIDIA request failed: {exc}"
            ) from exc

        if not response.ok:
            raise ProviderError(
                f"NVIDIA returned HTTP {response.status_code}: "
                f"{response.text}"
            )

        try:
            data: dict[str, Any] = response.json()
            raw_content = data["choices"][0]["message"].get(
                "content",
                "",
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError(
                "NVIDIA returned an invalid response structure."
            ) from exc

        if not isinstance(raw_content, str):
            raise ProviderError(
                "NVIDIA returned non-textual content."
            )

        content = raw_content.strip()

        if not content:
            raise ProviderError("NVIDIA returned an empty response.")

        usage = data.get("usage", {})

        return ProviderResponse(
            content=content,
            provider=self.name,
            model=model,
            metadata={
                "usage": usage if isinstance(usage, dict) else {},
            },
        )
