from __future__ import annotations

from pathlib import Path

from src.csv_storage import CSVStorage
from src.vacancy import Vacancy


def test_csv_storage_add_get_delete_and_dedup(tmp_path: Path) -> None:
    file = tmp_path / "vacancies.csv"
    storage = CSVStorage(str(file))

    v1 = Vacancy("A", "u1", 10, 10, "x")
    v2 = Vacancy("B", "u2", 20, 20, "y")
    v1_dup = Vacancy("A2", "u1", 999, 999, "dup")

    storage.add_vacancies([v1, v2])
    storage.add_vacancies([v1_dup])

    got = storage.get_vacancies()
    assert len(got) == 2

    storage.delete_vacancy(v2)
    got2 = storage.get_vacancies()
    assert len(got2) == 1
    assert got2[0].url == "u1"
