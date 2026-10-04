from __future__ import annotations

from typing import Any


class InMemoryMemory:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        if key not in self._store:
            raise KeyError(f"Memory key '{key}' is not set.")

        return self._store[key]

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def has(self, key: str) -> bool:
        return key in self._store

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
