from __future__ import annotations

import pytest

from ai.memory.in_memory import InMemoryMemory


def test_set_and_get_stores_value() -> None:
    memory = InMemoryMemory()

    memory.set("objective", "Generate README")

    assert memory.get("objective") == "Generate README"


def test_has_reflects_key_presence() -> None:
    memory = InMemoryMemory()

    assert memory.has("objective") is False

    memory.set("objective", "Generate README")

    assert memory.has("objective") is True


def test_get_raises_for_missing_key() -> None:
    memory = InMemoryMemory()

    with pytest.raises(KeyError, match="is not set"):
        memory.get("missing")


def test_delete_removes_key() -> None:
    memory = InMemoryMemory()
    memory.set("objective", "Generate README")

    memory.delete("objective")

    assert memory.has("objective") is False


def test_delete_is_idempotent_for_missing_key() -> None:
    memory = InMemoryMemory()

    memory.delete("missing")  # should not raise


def test_set_overwrites_existing_value() -> None:
    memory = InMemoryMemory()
    memory.set("objective", "first")

    memory.set("objective", "second")

    assert memory.get("objective") == "second"
