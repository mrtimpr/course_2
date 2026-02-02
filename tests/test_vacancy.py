from __future__ import annotations

import pytest

from src.vacancy import Vacancy


def test_vacancy_slots_present() -> None:
    """Vacancy должен использовать __slots__."""
    assert hasattr(Vacancy, "__slots__")
    assert isinstance(Vacancy.__slots__, tuple)
    assert len(Vacancy.__slots__) >= 4


def test_vacancy_validation_and_defaults() -> None:
    """Проверка валидации зарплаты и обязательных полей."""
    v = Vacancy("Title", "http://example.com", "not-int", None, None)
    assert v.salary_from == 0
    assert v.salary_to == 0
    assert v.description == ""

    with pytest.raises(ValueError):
        Vacancy("", "http://example.com", 1, 2, "x")

    with pytest.raises(ValueError):
        Vacancy("Title", "", 1, 2, "x")

    # приватные валидаторы существуют (name mangling)
    assert hasattr(v, "_Vacancy__validate_title")
    assert hasattr(v, "_Vacancy__validate_salary")
    assert hasattr(v, "_Vacancy__validate_url")
    assert hasattr(v, "_Vacancy__validate_description")


def test_vacancy_comparison_by_salary() -> None:
    """Сравнение вакансий по salary_avg через магические методы."""
    low = Vacancy("Low", "u1", 10, 10, "d")
    high = Vacancy("High", "u2", 100, 200, "d")

    assert high > low
    assert low < high
    assert high >= low
    assert low <= high


def test_vacancy_from_hh_item_and_cast_list() -> None:
    item = {
        "name": "QA",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 50000, "to": 70000},
        "snippet": {"requirement": "tests"},
    }
    v = Vacancy.from_hh_item(item)
    assert v.title == "QA"
    assert v.url == "https://hh.ru/vacancy/123"
    assert v.salary_from == 50000
    assert v.salary_to == 70000
    assert "tests" in v.description

    lst = Vacancy.cast_to_object_list([item])
    assert len(lst) == 1
    assert isinstance(lst[0], Vacancy)
