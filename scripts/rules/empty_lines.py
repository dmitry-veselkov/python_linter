import tokenize as tkn
from io import StringIO
from typing import Any, Generator

from ..error import Error
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
                    counter = 0
            else:
                counter = 0

    def _check_last_lines(self) -> None:
        """Проверка, что есть пустая строка в конце файла"""
        all_lines = self._code.split('\n')
        if len(all_lines) < 2:
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

    def _add_error(self, key: str, lineno: int) -> None:
        """Добавление в список ошибки, обнаруженной на указанной строке, с переданным кодом"""
        style_error = Error.CATCHABLE_E_ERRORS.get(key)
        if style_error is None:
            raise ValueError("Unknown error key!")
        self._errors.append(Error(style_error, line_number=lineno))
