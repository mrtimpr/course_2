from __future__ import annotations

from typing import List, Tuple

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], words: List[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам в описании или названии.
    """
    lowered = [w.lower().strip() for w in words if w.strip()]
    if not lowered:
        return vacancies

    result: List[Vacancy] = []
    for v in vacancies:
        text = (v.title + " " + v.description).lower()
        if all(word in text for word in lowered):
            result.append(v)
    return result


def parse_salary_range(s: str) -> Tuple[int, int]:
    """
    Парсит диапазон зарплат из строки вида '100000-150000' или '100000 150000'.
    Возвращает (min_salary, max_salary).
    """
    cleaned = s.replace("–", "-").replace("—", "-").replace(" ", "")
    if "-" not in cleaned:
        value = int(cleaned) if cleaned.isdigit() else 0
        return value, 10**18

    left, right = cleaned.split("-", 1)
    min_salary = int(left) if left.isdigit() else 0
    max_salary = int(right) if right.isdigit() else 10**18
    return min_salary, max_salary


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Оставляет вакансии, попадающие в диапазон зарплат (по средней зарплате).
    """
    min_salary, max_salary = parse_salary_range(salary_range)
    return [v for v in vacancies if min_salary <= v.salary_avg <= max_salary]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты.
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий (после сортировки по зарплате).
    """
    n = max(0, int(top_n))
    return vacancies[:n]
