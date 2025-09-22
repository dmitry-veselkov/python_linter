import tokenize as tkn
from io import StringIO
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
        tokens = tkn.generate_tokens(StringIO(self._code).readline)
        last_lineno = 0
        for token in tokens:
            if last_lineno != token.start[0]:
                self._check_trailing_spaces(token)
            self._check_indentation(token)
            self._check_operators(token)
            self._check_comments(token)
            last_lineno = token.start[0]
        return self._errors

    def _check_comments(self, token: tkn.TokenInfo) -> None:
        """Проверка оформления комментариев"""
        if not self._config.get("comments") and token.type != tkn.COMMENT:
            return
        line = token.line.rstrip()
        sharp_index = line.find("#")
        if sharp_index > 0 and line[sharp_index - 2 : sharp_index] != "  ":
            self._add_error(key="S002", lineno=token.start[0])
        if sharp_index == len(line) - 1:
            self._add_error(key="S004", lineno=token.start[0])
        if sharp_index < len(line) - 1 and line[sharp_index + 1] != " ":
            self._add_error(key="S003", lineno=token.start[0])

    def _check_trailing_spaces(self, token: tkn.TokenInfo) -> None:
        """Проверка лишних пробелов в конце строки"""
        if self._config.get("trailing_spaces") and token.line.rstrip("\n").endswith(" "):
            self._add_error(key="S005", lineno=token.start[0])

    def _check_indentation(self, token: tkn.TokenInfo) -> None:
        """Проверка некорректных отступов в начале строки"""
        if not self._config.get("indentations") or token.type != tkn.INDENT:
            return

        if "\t" in token.string:
            self._add_error(key="S006", lineno=token.start[0])
        elif len(token.string) % 4 != 0:
            self._add_error(key="S007", lineno=token.start[0])

    def _check_operators(self, token: tkn.TokenInfo) -> None:
        """Проверка на наличие пробелов вокруг операторов"""
        if not self._config.get("operators") or token.type != tkn.OP or token.string not in self._OPERATORS:
            return

        check_left = token.start[1] > 0 and token.line[token.start[1] - 1] == " "
        check_right = token.end[1] < len(token.line) and token.line[token.end[1]] == " "

        if not check_right or not check_left:
            self._add_error(key="S001", lineno=token.start[0])

    def _add_error(self, key: str, lineno: int) -> None:
        """Добавление ошибки расстановки пробелов в список"""
        style_error = Error.CATCHABLE_S_ERRORS.get(key)
        if style_error is None:
            raise ValueError("Unknown error key!")
        self._errors.append(Error(style_error, line_number=lineno))
