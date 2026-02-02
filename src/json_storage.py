from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.base_storage import BaseStorage
from src.vacancy import Vacancy


class JSONStorage(BaseStorage):
    """
    Хранилище вакансий в JSON.
    """

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        self.__filename: str = filename
        self.__path: Path = Path(self.__filename)
        self.__path.parent.mkdir(parents=True, exist_ok=True)

        if not self.__path.exists():
            self.__write([])

    def __read(self) -> List[Dict[str, Any]]:
        try:
            with self.__path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [x for x in data if isinstance(x, dict)]
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __write(self, data: List[Dict[str, Any]]) -> None:
        with self.__path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        current = self.__read()

        existing_urls = {row.get("url") for row in current if isinstance(row, dict)}
        for v in vacancies:
            if v.url in existing_urls:
                continue

            current.append(
                {
                    "title": v.title,
                    "url": v.url,
                    "salary_from": v.salary_from,
                    "salary_to": v.salary_to,
                    "description": v.description,
                }
            )
            existing_urls.add(v.url)

        self.__write(current)

    def get_vacancies(
        self,
        *,
        keyword: Optional[str] = None,
        top_n: Optional[int] = None,
    ) -> List[Vacancy]:
        rows = self.__read()
        vacancies: List[Vacancy] = [
            Vacancy(
                title=str(r.get("title") or ""),
                url=str(r.get("url") or ""),
                salary_from=r.get("salary_from"),
                salary_to=r.get("salary_to"),
                description=str(r.get("description") or ""),
            )
            for r in rows
        ]

        if keyword:
            key = keyword.lower().strip()
            vacancies = [v for v in vacancies if key in v.title.lower() or key in v.description.lower()]

        vacancies.sort(reverse=True)

        if top_n is not None:
            n = max(0, int(top_n))
            vacancies = vacancies[:n]

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        rows = self.__read()
        filtered = [r for r in rows if str(r.get("url")) != vacancy.url]
        self.__write(filtered)
