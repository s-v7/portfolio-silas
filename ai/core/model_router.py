from __future__ import annotations

from ai.core.exceptions import ConfigurationError

MODEL_BY_TASK: dict[str, dict[str, str]] = {
    "openai": {
        "short_text": "gpt-4o-mini",
        "long_markdown": "gpt-4o-mini",
        "analysis": "gpt-4o-mini",
        "review": "gpt-4o-mini",
        "translation": "gpt-4o-mini",
    },
    "anthropic": {
        "short_text": "claude-sonnet-4-5",
        "long_markdown": "claude-opus-4-5",
        "analysis": "claude-sonnet-4-5",
        "review": "claude-sonnet-4-5",
        "translation": "claude-sonnet-4-5",
    },
    "nvidia": {
        "short_text": "meta/llama-3.1-70b-instruct",
        "long_markdown": "meta/llama-3.1-70b-instruct",
        "analysis": "nvidia/llama-3.1-nemotron-70b-instruct",
        "review": "nvidia/llama-3.1-nemotron-70b-instruct",
        "translation": "meta/llama-3.1-70b-instruct",
    },
}


def get_model(task: str, provider: str) -> str:
    provider_name = provider.strip().lower()
    task_name = task.strip().lower()

    provider_map = MODEL_BY_TASK.get(provider_name)

    if provider_map is None:
        supported = ", ".join(sorted(MODEL_BY_TASK))
        raise ConfigurationError(
            f"Unknown provider '{provider_name}'. "
            f"Supported providers: {supported}."
        )

    model = provider_map.get(task_name)

    if model is None:
        supported_tasks = ", ".join(sorted(provider_map))
        raise ConfigurationError(
            f"Unknown task '{task_name}' for provider '{provider_name}'. "
            f"Supported tasks: {supported_tasks}."
        )

    return model
