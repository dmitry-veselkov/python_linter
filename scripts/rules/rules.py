from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..error import Error


class Rules(ABC):
    def __init__(self, config: dict[str, Any], code: str):
        self._config = config
        self._code = code
        self._errors: list[Error] = []

    @abstractmethod
    def check(self) -> list[Error]:
        pass

    @staticmethod
    @abstractmethod
    def get_string_name() -> str:
        pass
