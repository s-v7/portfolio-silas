from __future__ import annotations

import os
from typing import Any

import requests

from ai.core.contracts import LLMProvider, ProviderRequest, ProviderResponse
from ai.core.exceptions import ProviderError
from ai.core.model_router import get_model


class ProxyProvider(LLMProvider):
    """Provedor HTTP que delega as requisições de LLM para o portfólio-llm-proxy."""
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 60
    ) -> None:
        self._api_key = (
            api_key
            or os.getenv("PORTFOLIO_PROXY_API_KEY")
            or os.getenv("LLM_API_KEY")
        )
        url = (
            base_url
            or os.getenv("PORTFOLIO_PROXY_URL")
            or "http://localhost:8080/v1"
        )
        self._base_url = url.rstrip("/")
        self._timeout = timeout
    @property
    def name(self) -> str:
        return "proxy"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        model = request.model or get_model(
            request.task.value,
            self.name
        )

        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        payload: dict[str, Any] = {
            "model": model,
            "task": request.task.value,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content
                }
                for message in request.messages
            ],
            "options": {
                "max_tokens": request.options.max_tokens,
                "temperature": request.options.temperature,
                "metadata": dict(request.options.metadata)
            },
        }

        try:
            response = requests.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self._timeout
            )
        except requests.RequestException as exc:
            raise ProviderError(
                f"Portfólio LLM Proxy request failed: {exc}"
            ) from exc
        if not response.ok:
            raise ProviderError(
                f"Portfólio LLM Proxy returned HTTP {response.status_code}: "
                f"{self._error_message(response)}"
            )
        try:
            data: dict[str, Any] = response.json()

            if "choices" in data:
                raw_content = data["choices"][0]["messages"].get("content", "")
            else:
                raw_content = data.get("content", "")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError(
                "Portfólio LLM Proxy returned an invalid response structure."
            ) from exc
        if not isinstance(raw_content, str):
            raise ProviderError(
                "Portfólio LLM Proxy returned non-textual content."
            )
        content = raw_content.strip()

        if not content:
            raise ProviderError("Portfolio LLM Proxy returned an Empty response.")

        returned_provider = data.get("provider", self.name)
        returned_model = data.get("model", model)
        usage = data.get("usage", {})

        return ProviderResponse(
            content=content,
            provider=returned_provider,
            model=returned_model,
            metadata={
                "usage": usage if isinstance(usage, dict) else {},
            },
        )

    @staticmethod
    def _error_message(response: requests.Response) -> str:
        try:
            data: object = response.json()
        except ValueError:
            return response.text

        if isinstance(data, dict):
            error = data.get("error")
            if isinstance(error, dict) and "message" in error:
                return str(error["message"])
            if isinstance(error, str):
                return error
            if "detail" in data:
                return str(data["detail"])
        return response.text

