from __future__ import annotations

import os
from collections.abc import Callable

from ai.core.contracts import LLMProvider
from ai.core.exceptions import ConfigurationError
from ai.providers.anthropic_provider import AnthropicProvider
from ai.providers.nvidia_provider import NvidiaProvider
from ai.providers.openai_provider import OpenAIProvider

ProviderBuilder = Callable[[], LLMProvider]


class ProviderFactory:
    _builders: dict[str, ProviderBuilder] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "nvidia": NvidiaProvider,
    }

    @classmethod
    def create(
        cls,
        name: str | None = None,
    ) -> LLMProvider:
        configured_name = (
            name
            if name is not None
            else os.getenv("LLM_PROVIDER", "openai")
        )

        if configured_name is None:
            configured_name = "openai"

        provider_name = configured_name.strip().lower()

        if not provider_name:
            provider_name = "openai"

        builder = cls._builders.get(provider_name)

        if builder is None:
            supported = ", ".join(sorted(cls._builders))

            raise ConfigurationError(
                f"Unsupported provider '{provider_name}'. "
                f"Supported providers: {supported}."
            )

        return builder()

    @classmethod
    def register(
        cls,
        name: str,
        builder: ProviderBuilder,
    ) -> None:
        provider_name = name.strip().lower()

        if not provider_name:
            raise ConfigurationError(
                "Provider name cannot be empty."
            )

        cls._builders[provider_name] = builder
