from abc import ABC
from typing import Callable

from .error import Error


class Fixer(ABC):
    """Базовый класс, конкретные реализации которого исправляют конкретный тип ошибок"""

    def __init__(self, code: str, fixers: dict[str, Callable[[int], None]]):
        """Инициализация: задание базового отступа и текущего списка исправляющий методов"""
        self._code_lines = code.split("\n")
        self._fixers = fixers
        self._offset = 1
        self._current_error: Error | None = None

    def fix(self, errors: list[Error]) -> str:
        """Метод, который проходит по всем ошибкам и запускает методы, их исправляющие"""
        for error in errors:
            self._current_error = error
            fixer = self._fixers.get(error.style_error.key)
            if fixer:
                fixer(error.line_number - self._offset)

        return "\n".join(self._code_lines)
