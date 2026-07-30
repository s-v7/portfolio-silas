
import pytest

from ai.core.exceptions import ConfigurationError
from ai.core.model_router import get_model


def test_returns_configured_model() -> None:
    model = get_model("analysis", "openai")

    assert model

def test_rejects_unknown_provider() -> None:
    with pytest.raises(ConfigurationError):
        get_model("analysis", "unknown")

def test_rejects_unknown_task() -> None:
    with pytest.raises(ConfigurationError):
        get_model("unknown", "openai")

