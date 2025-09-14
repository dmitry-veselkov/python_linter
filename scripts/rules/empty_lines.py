from typing import Any

from ..error import Error
from .rules import Rules


class EmptyLinesRules(Rules):
    def __init__(self, config: dict[str, Any], code: str) -> None:
        super().__init__(config, code)

    def check(self) -> list[Error]:
        return self._errors
