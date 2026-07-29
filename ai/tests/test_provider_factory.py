from __future__ import annotations

import pytest

from ai.core.exceptions import ConfigurationError
from ai.providers.factory import ProviderFactory
from ai.providers.nvidia_provider import NvidiaProvider
from ai.providers.openai_provider import OpenAIProvider


def test_creates_openai_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    provider = ProviderFactory.create("openai")

    assert isinstance(provider, OpenAIProvider)
    assert provider.name == "openai"


def test_creates_nvidia_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NVIDIA_API_KEY", "fake-key")

    provider = ProviderFactory.create("nvidia")

    assert isinstance(provider, NvidiaProvider)
    assert provider.name == "nvidia"


def test_uses_environment_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    provider = ProviderFactory.create()

    assert provider.name == "openai"


def test_rejects_unknown_provider() -> None:
    with pytest.raises(ConfigurationError, match="Unsupported provider"):
        ProviderFactory.create("invalid")


def test_rejects_empty_registered_provider_name() -> None:
    with pytest.raises(
        ConfigurationError,
        match="Provider name cannot be empty",
    ):
        ProviderFactory.register("", lambda: ProviderFactory.create("openai"))
