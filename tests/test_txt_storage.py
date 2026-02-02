from __future__ import annotations

from pathlib import Path

import pytest

from src.txt_storage import TXTStorage
from src.vacancy import Vacancy


def test_txt_storage_is_stub(tmp_path: Path) -> None:
    storage = TXTStorage(str(tmp_path / "v.txt"))

    with pytest.raises(NotImplementedError):
        storage.add_vacancies([])

    with pytest.raises(NotImplementedError):
        storage.get_vacancies()

    with pytest.raises(NotImplementedError):
        storage.delete_vacancy(Vacancy("A", "u1", 1, 1, ""))
