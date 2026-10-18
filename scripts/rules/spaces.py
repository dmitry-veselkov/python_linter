import tokenize as tkn
from io import StringIO
from typing import Any, Callable

from ..error import Error
from ..fixer import Fixer
from .rules import Rules


class SpacesRules(Rules):
    """Правило расстановки пробелов"""

    OPERATORS = {"==", "=", "+", "-", "*", "//", "/", "%", "**", "!="}

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

    def fix(self) -> str:
        """Запуск нужного, исправляющего данный тип ошибок класса"""
        return SpacesFixer(self._code).fix(self._errors)

    @staticmethod
    def get_string_name() -> str:
        return "spaces"

    def _check_comments(self, token: tkn.TokenInfo) -> None:
        """Проверка оформления комментариев"""
        if not self._config.get("comments") or token.type != tkn.COMMENT:
            return

        line = token.line.rstrip()
        before, after = line.split("#", 1)
        before, after = before.lstrip(), after.rstrip()

        if before != "" and before[-2:] != "  ":
            self._add_error(key="S002", lineno=token.start[0])
        if after != "" and after[0] != " ":
            self._add_error(key="S003", lineno=token.start[0])
        if after == "":
            self._add_error(key="S004", lineno=token.start[0])

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
        if not self._config.get("operators") or token.type != tkn.OP or token.string not in self.OPERATORS:
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


class SpacesFixer(Fixer):
    """Класс, исправляющий ошибки расстановки пробелов и отступов"""

    def __init__(self, code: str):
        fixers: dict[str, Callable[[int], None]] = {
            "S001": self._fix_operators,
            "S002": self._fix_comment_spacing,
            "S003": self._fix_comment_spacing,
            "S004": self._fix_empty_comment,
            "S005": self._fix_trailing_spaces,
            "S006": self._fix_tabs,
            "S007": self._fix_indent_size,
        }
        super().__init__(code, fixers)

    def _fix_operators(self, lineno: int) -> None:
        """Расстановка пробелов вокруг математических и логических операторов"""
        line = self._code_lines[lineno]
        tokens = list(tkn.generate_tokens(StringIO(line + "\n").readline))
        new_line = ""
        last_col = 0

        for token in tokens:
            if token.type == tkn.OP and token.string in SpacesRules.OPERATORS:
                new_line += f"{line[last_col:token.start[1]].rstrip()} {token.string} "
                last_col = token.end[1]
            else:
                new_line += line[last_col : token.end[1]]
                last_col = token.end[1]

        self._code_lines[lineno] = new_line.rstrip()

    def _fix_empty_comment(self, lineno: int) -> None:
        """Удаление пустых комментариев"""
        self._code_lines[lineno] = self._code_lines[lineno].replace('#', '').rstrip()

    def _fix_comment_spacing(self, lineno: int) -> None:
        """Расстановка пробелов в комментариях"""
        before, after = self._code_lines[lineno].split("#", 1)
        before, after = before.rstrip(), after.lstrip()

        if before == "":
            self._code_lines[lineno] = f"# {after}"
        else:
            self._code_lines[lineno] = f"{before}  # {after}"

    def _fix_trailing_spaces(self, lineno: int) -> None:
        """Удаление лишних пробелов в конце строки"""
        self._code_lines[lineno] = self._code_lines[lineno].rstrip()

    def _fix_tabs(self, lineno: int) -> None:
        """Замена табуляции на 4 пробела"""
        self._code_lines[lineno] = self._code_lines[lineno].replace("\t", " " * 4)

    def _fix_indent_size(self, lineno: int) -> None:
        """Исправление не кратных четырем отступов"""
        line = self._code_lines[lineno]
        indent = len(line) - len(line.lstrip(" "))
        new_indent = (indent // 4) * 4
        self._code_lines[lineno] = " " * new_indent + line.lstrip()
