from __future__ import annotations

from typing import Callable, List

from api.hh_api import HeadHunterAPI
from src.base_storage import BaseStorage
from src.json_storage import JSONStorage
from src.utils import filter_vacancies, get_top_vacancies, sort_vacancies
from src.vacancy import Vacancy


def format_vacancy(v: Vacancy) -> str:
    """
    Форматирует вакансию в человекочитаемый вид.
    """
    return (
        f"{v.title}\n" f"Ссылка: {v.url}\n" f"Зарплата: {v.salary_from}-{v.salary_to}\n" f"Описание: {v.description}\n"
    )


def user_interaction(
    storage: BaseStorage | None = None,
    api: HeadHunterAPI | None = None,
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> None:
    """
    Взаимодействие с пользователем через консоль.
    """
    api = api or HeadHunterAPI()
    storage = storage or JSONStorage()

    search_query = input_func("Введите поисковый запрос для hh.ru: ").strip()
    top_n_raw = input_func("Введите количество вакансий для вывода (top N): ").strip()
    filter_words_raw = input_func("Введите ключевые слова для фильтрации (через пробел): ").strip()

    try:
        top_n = int(top_n_raw)
    except ValueError:
        top_n = 5

    items = api.get_vacancies(search_query)
    vacancies: List[Vacancy] = Vacancy.cast_to_object_list(items)

    storage.add_vacancies(vacancies)

    filter_words = [w for w in filter_words_raw.split() if w.strip()]
    saved = storage.get_vacancies()
    filtered = filter_vacancies(saved, filter_words)

    sorted_list = sort_vacancies(filtered)
    top_list = get_top_vacancies(sorted_list, top_n)

    if not top_list:
        print_func("Подходящих вакансий не найдено.")
        return

    for v in top_list:
        print_func(format_vacancy(v))
        print_func("-" * 40)
