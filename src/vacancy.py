from __future__ import annotations

from typing import Any, Dict, List


class Vacancy:
    """
    Класс для работы с вакансией.
    """

    __slots__ = ("_title", "_url", "_salary_from", "_salary_to", "_description")

    def __init__(self, title: str, url: str, salary_from: int, salary_to: int, description: str) -> None:
        self._title = self.__validate_title(title)
        self._url = self.__validate_url(url)
        self._salary_from = self.__validate_salary(salary_from)
        self._salary_to = self.__validate_salary(salary_to)
        self._description = self.__validate_description(description)

    # приватные валидаторы

    def __validate_title(self, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")
        return value.strip()

    def __validate_url(self, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Ссылка вакансии должна быть непустой строкой.")
        return value.strip()

    def __validate_salary(self, value: Any) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            number = 0
        return max(0, number)

    def __validate_description(self, value: str) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            return str(value)
        return value.strip()

    # публичные свойства

    @property
    def title(self) -> str:
        """Название вакансии."""
        return self._title

    @property
    def url(self) -> str:
        """Ссылка на вакансию."""
        return self._url

    @property
    def salary_from(self) -> int:
        """Зарплата от."""
        return self._salary_from

    @property
    def salary_to(self) -> int:
        """Зарплата до."""
        return self._salary_to

    @property
    def description(self) -> str:
        """Описание/требования."""
        return self._description

    @property
    def salary_avg(self) -> int:
        """Средняя зарплата (для сравнения)."""
        if self._salary_from and self._salary_to:
            return (self._salary_from + self._salary_to) // 2
        return self._salary_from or self._salary_to or 0

    # сравнение вакансий по зарплате

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg < other.salary_avg

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg <= other.salary_avg

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg > other.salary_avg

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg >= other.salary_avg

    def __repr__(self) -> str:
        return f"Vacancy(title={self.title!r}, salary_avg={self.salary_avg}, url={self.url!r})"

    # фабрики

    @classmethod
    def from_hh_item(cls, item: Dict[str, Any]) -> "Vacancy":
        """
        Создаёт объект Vacancy из элемента hh.ru (словаря из items).
        """
        salary = item.get("salary") or {}
        snippet = item.get("snippet") or {}

        title = str(item.get("name") or "")
        url = str(item.get("alternate_url") or item.get("url") or "")

        salary_from = salary.get("from")
        salary_to = salary.get("to")

        description = str(snippet.get("requirement") or snippet.get("responsibility") or "")

        return cls(
            title=title,
            url=url,
            salary_from=salary_from,
            salary_to=salary_to,
            description=description,
        )

    @classmethod
    def cast_to_object_list(cls, items: List[Dict[str, Any]]) -> List["Vacancy"]:
        """
        Преобразует список словарей (items) в список объектов Vacancy.
        """
        return [cls.from_hh_item(x) for x in items]
