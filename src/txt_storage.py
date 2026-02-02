from __future__ import annotations

from typing import List, Optional

from src.base_storage import BaseStorage
from src.vacancy import Vacancy


class TXTStorage(BaseStorage):
    """
    Дополнительное хранилище (TXT).
    """

    def __init__(self, filename: str = "data/vacancies.txt") -> None:
        self.__filename: str = filename

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        raise NotImplementedError("TXTStorage: реализация может быть добавлена при необходимости.")

    def get_vacancies(self, *, keyword: Optional[str] = None, top_n: Optional[int] = None) -> List[Vacancy]:
        raise NotImplementedError("TXTStorage: реализация может быть добавлена при необходимости.")

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        raise NotImplementedError("TXTStorage: реализация может быть добавлена при необходимости.")
