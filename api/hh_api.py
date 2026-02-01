from __future__ import annotations

from typing import Any, Dict, List

import requests

from api.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """
    Реализация API для hh.ru.
    """

    def __init__(self, *, per_page: int = 100, pages_limit: int = 20) -> None:
        super().__init__(
            base_url="https://api.hh.ru/vacancies",
            headers={"User-Agent": "HH-User-Agent"},
        )
        self.__params: Dict[str, Any] = {"text": "", "page": 0, "per_page": per_page}
        self.__pages_limit: int = pages_limit

    def __connect_hh(self) -> None:
        """
        Приватный метод подключения к API hh.ru.
        Запрос на базовый URL и проверка статус-кода.
        """
        super().connect()

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии по ключевому слову.
        Возвращает список словарей из ключа 'items'.
        """
        self.__connect_hh()

        self.__params["text"] = keyword
        result: List[Dict[str, Any]] = []

        for page in range(self.__pages_limit):
            self.__params["page"] = page

            response = requests.get(
                self._base_url,
                headers=self._headers,
                params=self.__params,
                timeout=self._timeout,
            )
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            if not isinstance(items, list):
                break

            result.extend(items)

            per_page = int(self.__params.get("per_page") or 0)
            if per_page and len(items) < per_page:
                break

        return result
