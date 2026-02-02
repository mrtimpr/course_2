from __future__ import annotations

import json
from pathlib import Path

from src.json_storage import JSONStorage
from src.vacancy import Vacancy


def test_json_storage_default_filename_private_attr() -> None:
    """У JSONStorage есть дефолтное имя файла и оно приватное."""
    storage = JSONStorage()
    assert hasattr(storage, "_JSONStorage__filename")
    assert getattr(storage, "_JSONStorage__filename") == "data/vacancies.json"


def test_json_storage_adds_without_overwrite_and_deduplicates(tmp_path: Path) -> None:
    file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(file))

    v1 = Vacancy("A", "u1", 10, 20, "x")
    v2 = Vacancy("B", "u2", 30, 40, "y")
    v1_dup = Vacancy("A-dup", "u1", 999, 999, "dup")  # тот же url => дубль

    storage.add_vacancies([v1, v2])
    storage.add_vacancies([v1_dup])  # не должен добавиться

    data = json.loads(file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 2

    urls = {row["url"] for row in data}
    assert urls == {"u1", "u2"}

    # добавление без обнуления (не перезаписываем "с нуля")
    storage.add_vacancies([Vacancy("C", "u3", 1, 2, "z")])
    data2 = json.loads(file.read_text(encoding="utf-8"))
    assert len(data2) == 3


def test_json_storage_get_filters_and_topn(tmp_path: Path) -> None:
    file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(file))

    v1 = Vacancy("Python Dev", "u1", 100, 100, "python")
    v2 = Vacancy("Java Dev", "u2", 200, 200, "java")
    v3 = Vacancy("Python QA", "u3", 150, 150, "python tests")
    storage.add_vacancies([v1, v2, v3])

    py = storage.get_vacancies(keyword="python")
    assert len(py) == 2

    top1 = storage.get_vacancies(top_n=1)
    assert len(top1) == 1
    assert top1[0].title == "Java Dev"  # max зарплата


def test_json_storage_delete(tmp_path: Path) -> None:
    file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(file))

    v1 = Vacancy("A", "u1", 10, 10, "")
    v2 = Vacancy("B", "u2", 20, 20, "")
    storage.add_vacancies([v1, v2])

    storage.delete_vacancy(v1)
    remaining = storage.get_vacancies()
    assert len(remaining) == 1
    assert remaining[0].url == "u2"
