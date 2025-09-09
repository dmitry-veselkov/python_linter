from typing import Any

from .rules import Rules


class EmptyLinesRules(Rules):
    def __init__(self, config: dict[str, Any], code: str) -> None:
        super().__init__(config, code)

    def check(self) -> None:
        print("Empty lines check")
