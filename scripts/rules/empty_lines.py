import tokenize as tkn
from io import StringIO
from typing import Any, Callable, Generator

from scripts.error import Error

from ..fixer import Fixer
from .rules import Rules


class EmptyLinesRules(Rules):
    """Правило для пустых строк"""

    def __init__(self, config: dict[str, Any], code: str) -> None:
        """Инициализация проверки"""
        super().__init__(config, code)

    def check(self) -> list[Error]:
        """Запуск проверок для переданного python кода с учетом конфига"""
        tokens = tkn.generate_tokens(StringIO(self._code).readline)
        self._check_empty_lines_count(tokens)
        self._check_last_lines()

        return self._errors

    def fix(self) -> str:
        """Запуск нужного, исправляющего данный тип ошибок класса"""
        return EmptyLinesFixer(self._code).fix(self._errors)

    @staticmethod
    def get_string_name() -> str:
        return "empty_lines"

    def _check_empty_lines_count(self, tokens: Generator[tkn.TokenInfo, None, None]) -> None:
        """Проверка, что число пустых строк подряд не превышает двух"""
        current_line = counter = 0
        for token in tokens:
            if token.start[0] == current_line:
                continue
            current_line = token.start[0]
            if self._check_empty_line(token):
                counter += 1
                if counter > 2:
                    self._add_error(key="E001", lineno=current_line)
            else:
                counter = 0

    def _check_last_lines(self) -> None:
        """Проверка, что есть пустая строка в конце файла"""
        all_lines = self._code.split('\n')
        if len(all_lines) < 2 or not self._config.get("check_last_empty_line"):
            return
        two_last_lines = all_lines[-2:]
        if two_last_lines[0].strip() != "" and two_last_lines[1].strip() == "":
            return
        self._add_error(key="E002", lineno=len(all_lines))

    def _check_empty_line(self, token: tkn.TokenInfo) -> bool:
        """Проверка, что строка действительно пустая и ее нужно учитывать"""
        if not self._config.get("check_empty_lines") or token.type not in (tkn.NL, tkn.NEWLINE):
            return False
        return token.line.strip() == ""

    def _add_error(self, key: str, lineno: int) -> Error:
        """Добавление в список ошибки, обнаруженной на указанной строке, с переданным кодом"""
        style_error = Error.CATCHABLE_E_ERRORS.get(key)
        if style_error is None:
            raise ValueError("Unknown error key!")
        error = Error(style_error, line_number=lineno)
        self._errors.append(error)
        return error


class EmptyLinesFixer(Fixer):
    """Класс, исправляющий ошибки расстановки пробелов и отступов"""

    def __init__(self, code: str):
        fixers: dict[str, Callable[[int], None]] = {
            "E001": self._remove_extra_lines,
            "E002": self._add_last_empty_line,
        }
        super().__init__(code, fixers)

    def _remove_extra_lines(self, lineno: int) -> None:
        """Удаление лишних строк"""
        self._code_lines.pop(lineno)
        self._offset += 1

    def _add_last_empty_line(self, lineno: int) -> None:
        """Добавление пустой строки в конце файла при ее отсутсвии"""
        self._code_lines.append('')
