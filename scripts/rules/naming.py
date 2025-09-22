import ast
import re
from typing import Any, Pattern

from ..error import Error
from .rules import Rules


class NamingRule:
    """Правило именования идентификатора"""

    def __init__(self, key: str, toml: str, pattern: Pattern[str]):
        """Инициализация правила полями, которые будут использоваться при проверке имен и выводе ошибок"""
        self.key = key
        self.toml = toml
        self.pattern = re.compile(pattern)


class NamingRules(Rules):
    """Проверка именования идентификаторов"""

    _CAMEL_CASE_PATTERN = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    _SNAKE_CASE_PATTERN = re.compile(r'^[a-z_][a-z0-9_]*$')

    _CHECKERS = {
        ast.ClassDef: lambda self, node: self._check_class(node),
        ast.FunctionDef: lambda self, node: self._check_function(node),
        ast.Name: lambda self, node: self._check_variable(node),
        ast.Attribute: lambda self, node: self._check_attribute(node),
    }

    _RULES = {
        ast.ClassDef: NamingRule("N001", "class_camel_case", _CAMEL_CASE_PATTERN),
        ast.FunctionDef: NamingRule("N002", "function_snake_case", _SNAKE_CASE_PATTERN),
        ast.Name: NamingRule("N003", "variables_snake_case", _SNAKE_CASE_PATTERN),
        ast.arg: NamingRule("N004", "args_snake_case", _SNAKE_CASE_PATTERN),
        ast.Attribute: NamingRule("N005", "attributes_snake_case", _SNAKE_CASE_PATTERN),
    }

    def __init__(self, config: dict[str, Any], code: str) -> None:
        """Инициализация проверки"""
        super().__init__(config, code)

    def check(self) -> list[Error]:
        """Запуск проверок для переданного python кода с учетом конфига"""
        tree = ast.parse(self._code)
        for node in ast.walk(tree):
            for ast_type, checker in self._CHECKERS.items():
                if isinstance(node, ast_type):
                    checker(self, node)
        return self._errors

    def _check_class(self, node: ast.ClassDef) -> None:
        """Проверка для классов"""
        self._check_name(node, node.name, self._RULES[ast.ClassDef])
        self._check_class_variables(node)

    def _check_function(self, node: ast.FunctionDef) -> None:
        """Проверка для функций и их аргументов"""
        self._check_name(node, node.name, self._RULES[ast.FunctionDef])
        self._check_function_args(node)

    def _check_variable(self, node: ast.Name) -> None:
        """Проверка для переменных"""
        if isinstance(node.ctx, ast.Store):
            self._check_name(node, node.id, self._RULES[ast.Name])

    def _check_attribute(self, node: ast.Attribute) -> None:
        """Проверка для аттрибутов"""
        if isinstance(node.value, ast.Name) and isinstance(node.ctx, ast.Store) and node.value.id == "self":
            self._check_name(node, node.attr, self._RULES[ast.Attribute])

    def _check_class_variables(self, node: ast.ClassDef) -> None:
        """Проверка для переменных внутри переданного класса"""
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        self._check_variable(target)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                self._check_variable(item.target)

    def _check_function_args(self, node: ast.FunctionDef) -> None:
        """Проверка для аргументов внутри переданной функции"""
        for arg in (
            node.args.args
            + node.args.kwonlyargs
            + ([node.args.vararg] if node.args.vararg else [])
            + ([node.args.kwarg] if node.args.kwarg else [])
        ):
            self._check_name(arg, arg.arg, self._RULES[ast.arg])

    def _check_name(self, node: Any, name: str, rule: NamingRule) -> None:
        """Проверка конкретного имени по переданному правилу"""
        match = re.match(pattern=rule.pattern, string=name)
        style_error = Error.CATCHABLE_N_ERRORS.get(rule.key)
        if style_error is None:
            raise ValueError("Unknown error key!")

        if self._config.get(rule.toml) and match is None:
            self._errors.append(Error(style_error, line_number=node.lineno))
