from __future__ import annotations

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, parse_salary_range, sort_vacancies
from src.vacancy import Vacancy


def test_utils_parse_salary_range_common() -> None:
    assert parse_salary_range("100000-150000") == (100000, 150000)
    assert parse_salary_range("100000–150000") == (100000, 150000)
    assert parse_salary_range("50000") == (50000, 10**18)
    assert parse_salary_range("abc") == (0, 10**18)


def test_utils_filter_sort_top_salary() -> None:
    v1 = Vacancy("Python Dev", "u1", 100, 100, "remote")
    v2 = Vacancy("Java Dev", "u2", 200, 200, "office")
    v3 = Vacancy("Python QA", "u3", 150, 150, "tests")

    filtered = filter_vacancies([v1, v2, v3], ["python"])
    assert [v.url for v in filtered] == ["u1", "u3"]

    sorted_list = sort_vacancies([v1, v2, v3])
    assert [v.url for v in sorted_list] == ["u2", "u3", "u1"]

    top2 = get_top_vacancies(sorted_list, 2)
    assert [v.url for v in top2] == ["u2", "u3"]

    ranged = get_vacancies_by_salary([v1, v2, v3], "120-180")
    assert [v.url for v in ranged] == ["u3"]
