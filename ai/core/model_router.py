MODEL_BY_TASK = {
    "openai": {
        "short_text": "gpt-4o-mini",
        "long_markdown": "gpt-4o-mini",
        "analysis": "gpt-4o-mini",
    },
    "anthropic": {
        "short_text": "claude-sonnet-4-5",
        "long_markdown": "claude-opus-4-5",
        "analysis": "claude-sonnet-4-5",
    },
}


def get_model(task: str, provider: str) -> str:
    provider_map = MODEL_BY_TASK.get(provider, MODEL_BY_TASK["openai"])
    return provider_map.get(task, provider_map["short_text"])
