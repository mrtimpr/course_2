from __future__ import annotations

from typing import Any


class MockResponse:
    """Простой мок ответа requests.get()."""

    def __init__(self, status_code: int = 200, payload: Any | None = None) -> None:
        self.status_code = status_code
        self._payload = payload if payload is not None else {}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")

    def json(self) -> Any:
        return self._payload
