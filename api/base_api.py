from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для работы с API платформ вакансий.
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None) -> None:
        self._base_url: str = base_url
        self._headers: Dict[str, str] = headers or {}
        self._timeout: float = 10.0

    def connect(self) -> None:
        """
        Выполняет подключение к API: запрос на базовый URL и проверка статус-кода.
        """
        response = requests.get(self._base_url, headers=self._headers, timeout=self._timeout)
        response.raise_for_status()

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии по ключевому слову.
        Должен возвращать список словарей (сырой API-ответ в виде items).
        """
        raise NotImplementedError
