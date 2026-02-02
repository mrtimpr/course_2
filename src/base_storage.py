from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.vacancy import Vacancy


class BaseStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем вакансий.
    """

    @abstractmethod
    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Добавить вакансии в хранилище."""
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(
        self,
        *,
        keyword: Optional[str] = None,
        top_n: Optional[int] = None,
    ) -> List[Vacancy]:
        """Получить вакансии по критериям."""
        raise NotImplementedError

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища."""
        raise NotImplementedError
