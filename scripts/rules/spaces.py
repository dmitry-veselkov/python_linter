import io
import tokenize as tkn
from typing import Any

from ..error import Error
from .rules import Rules


class SpacesRules(Rules):
    """Правило расстановки пробелов"""

    _OPERATORS = {"=", "+", "-", "*", "/", "//", "%", "**", "=="}

    def __init__(self, config: dict[str, Any], code: str) -> None:
        """Инициализация проверки"""
        super().__init__(config, code)

    def check(self) -> list[Error]:
        """Запуск проверок для переданного python кода с учетом конфига"""
        tokens = tkn.generate_tokens(io.StringIO(self._code).readline)
        last_lineno = 0
        # TODO: подключить конфиг к проверке
        for token in tokens:
            if last_lineno != token.start[0]:
                self._check_trailing_spaces(token)
            self._check_indentation(token)
            self._check_operators(token)
            last_lineno = token.start[0]
        return self._errors

    def _check_trailing_spaces(self, token: tkn.TokenInfo) -> None:
        """Проверка лишних пробелов в конце строки"""
        if token.line.rstrip("\n").endswith(" "):
            self._add_error(key="S002", lineno=token.start[0])

    def _check_indentation(self, token: tkn.TokenInfo) -> None:
        """Проверка некорректных отступов в начале строки"""
        if token.type != tkn.INDENT:
            return

        if "\t" in token.string:
            self._add_error(key="S003", lineno=token.start[0])
        elif len(token.string) % 4 != 0:
            self._add_error(key="S004", lineno=token.start[0])

    def _check_operators(self, token: tkn.TokenInfo) -> None:
        """Проверка на наличие пробелов вокруг операторов"""
        if token.type != tkn.OP or token.string not in self._OPERATORS:
            return

        check_left = token.start[1] > 0 and token.line[token.start[1] - 1] == " "
        check_right = token.end[1] < len(token.line) and token.line[token.end[1]] == " "

        if not check_right or not check_left:
            self._add_error(key="S005", lineno=token.start[0])

    def _add_error(self, key: str, lineno: int) -> None:
        """Добавление ошибки расстановки пробелов в список"""
        self._errors.append(Error(style="spaces", key=key, line_number=lineno))
