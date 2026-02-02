from __future__ import annotations

from typing import Any, Dict, List

import pytest

from api.base_api import BaseAPI
from api.hh_api import HeadHunterAPI
from tests.conftest import MockResponse


def test_base_api_is_abstract() -> None:
    """BaseAPI должен быть абстрактным и не инстанцироваться напрямую."""
    with pytest.raises(TypeError):
        BaseAPI("https://example.com")  # abstract: get_vacancies not implemented


def test_hh_api_connect_called_before_get(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Проверяем:
    - приватный метод подключения существует
    - при get_vacancies сначала запрос на base_url (connect)
    - затем запрос(ы) с params
    """
    calls: List[Dict[str, Any]] = []

    def fake_get(url: str, **kwargs: Any) -> MockResponse:
        calls.append({"url": url, "kwargs": kwargs})

        # 1-й вызов: connect() -> без params
        if len(calls) == 1:
            return MockResponse(200, {"ok": True})

        # Далее: get_vacancies() -> с params
        page = kwargs.get("params", {}).get("page")
        if page == 0:
            return MockResponse(
                200,
                {
                    "items": [
                        {
                            "name": "Python Dev",
                            "alternate_url": "https://hh.ru/vacancy/1",
                            "salary": {"from": 100000, "to": 150000},
                            "snippet": {"requirement": "Python"},
                        }
                    ]
                },
            )
        return MockResponse(200, {"items": []})

    monkeypatch.setattr("requests.get", fake_get)

    api = HeadHunterAPI(per_page=100, pages_limit=20)

    # приватный метод должен существовать (name mangling)
    assert hasattr(api, "_HeadHunterAPI__connect_hh")

    items = api.get_vacancies("Python")
    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0]["name"] == "Python Dev"

    # Проверяем порядок и параметры вызовов requests.get
    assert calls[0]["url"] == "https://api.hh.ru/vacancies"
    assert "params" not in calls[0]["kwargs"]  # connect() без params

    assert calls[1]["url"] == "https://api.hh.ru/vacancies"
    assert calls[1]["kwargs"]["params"]["text"] == "Python"
    assert calls[1]["kwargs"]["params"]["per_page"] == 100
    assert calls[1]["kwargs"]["params"]["page"] == 0


def test_hh_api_raises_on_bad_status(monkeypatch: pytest.MonkeyPatch) -> None:
    """Если connect() возвращает ошибку — get_vacancies должен падать."""

    def fake_get(url: str, **kwargs: Any) -> MockResponse:
        return MockResponse(500, {"error": "fail"})  # connect() -> 500

    monkeypatch.setattr("requests.get", fake_get)

    api = HeadHunterAPI()
    with pytest.raises(RuntimeError):
        api.get_vacancies("Python")
