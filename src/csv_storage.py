from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Optional

from src.base_storage import BaseStorage
from src.vacancy import Vacancy


class CSVStorage(BaseStorage):
    """
    Дополнительное хранилище вакансий в CSV.
    Реализовано как рабочая альтернатива JSONStorage.
    """

    def __init__(self, filename: str = "data/vacancies.csv") -> None:
        self.__filename: str = filename
        self.__path: Path = Path(self.__filename)
        self.__path.parent.mkdir(parents=True, exist_ok=True)

        if not self.__path.exists():
            with self.__path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "title",
                        "url",
                        "salary_from",
                        "salary_to",
                        "description",
                    ],
                )
                writer.writeheader()

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        existing = {v.url for v in self.get_vacancies()}

        with self.__path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["title", "url", "salary_from", "salary_to", "description"],
            )
            for v in vacancies:
                if v.url in existing:
                    continue
                writer.writerow(
                    {
                        "title": v.title,
                        "url": v.url,
                        "salary_from": v.salary_from,
                        "salary_to": v.salary_to,
                        "description": v.description,
                    }
                )
                existing.add(v.url)

    def get_vacancies(self, *, keyword: Optional[str] = None, top_n: Optional[int] = None) -> List[Vacancy]:
        vacancies: List[Vacancy] = []
        with self.__path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                vacancies.append(
                    Vacancy(
                        title=row.get("title", ""),
                        url=row.get("url", ""),
                        salary_from=row.get("salary_from", 0),
                        salary_to=row.get("salary_to", 0),
                        description=row.get("description", ""),
                    )
                )

        if keyword:
            key = keyword.lower().strip()
            vacancies = [v for v in vacancies if key in v.title.lower() or key in v.description.lower()]

        vacancies.sort(reverse=True)

        if top_n is not None:
            vacancies = vacancies[: max(0, int(top_n))]

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        all_items = self.get_vacancies()
        all_items = [v for v in all_items if v.url != vacancy.url]

        with self.__path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["title", "url", "salary_from", "salary_to", "description"],
            )
            writer.writeheader()
            for v in all_items:
                writer.writerow(
                    {
                        "title": v.title,
                        "url": v.url,
                        "salary_from": v.salary_from,
                        "salary_to": v.salary_to,
                        "description": v.description,
                    }
                )
