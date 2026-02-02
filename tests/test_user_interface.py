from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.json_storage import JSONStorage
from src.user_interface import user_interaction


def test_user_interaction_human_readable_output(tmp_path: Path) -> None:
    """
    Проверяем:
    - user_interaction использует переданные api/storage
    - вывод человекочитаемый (строки, а не dict/list)
    """
    storage = JSONStorage(str(tmp_path / "vacancies.json"))

    class FakeAPI:
        def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
            assert keyword == "Python"
            return [
                {
                    "name": "Python Dev",
                    "alternate_url": "u1",
                    "salary": {"from": 100, "to": 100},
                    "snippet": {"requirement": "python"},
                },
                {
                    "name": "Java Dev",
                    "alternate_url": "u2",
                    "salary": {"from": 200, "to": 200},
                    "snippet": {"requirement": "java"},
                },
            ]

    inputs = iter(["Python", "1", "python"])  # search_query, top_n, filter words

    printed: List[str] = []

    def fake_input(prompt: str) -> str:
        return next(inputs)

    def fake_print(text: str) -> None:
        printed.append(text)

    user_interaction(
        storage=storage,
        api=FakeAPI(),  # type: ignore[arg-type]
        input_func=fake_input,
        print_func=fake_print,
    )

    joined = "\n".join(printed)
    assert "Ссылка:" in joined
    assert "Зарплата:" in joined
    assert "Описание:" in joined

    # не печатаем сырые dict/list
    assert "{" not in joined
    assert "[" not in joined
