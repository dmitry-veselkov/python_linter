import tokenize as tkn
from io import StringIO
from typing import Any

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
        current_line = 0
        counter = 0
        for token in tokens:
            if token.start[0] == current_line:
                continue
            current_line = token.start[0]
            # TODO: добавить проверку на пустую строку в конце файла
            if self._check_empty_line(token):
                counter += 1
                if counter > 2:
                    self._errors.append(Error(style="empty lines", key="S001", line_number=current_line))
                    counter = 0
            else:
                counter = 0
        return self._errors

    def _check_empty_line(self, token: tkn.TokenInfo) -> bool:
        """Проверка, что строка действительно пустая и ее нужно учитывать"""
        if not self._config.get("check_empty_lines") or token.type not in (tkn.NL, tkn.NEWLINE):
            return False
        return token.line.strip() == ""
