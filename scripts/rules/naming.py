import ast
import re
from collections import defaultdict
from typing import Any, Callable, Pattern

from ..error import Error, NamingError
from ..fixer import Fixer
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
        super().__init__(config, code)
        self._known_classes: set[str] = set()

    def fix(self) -> str:
        """Запуск нужного, исправляющего данный тип ошибок класса"""
        return NamingFixer(self._code).fix(self._errors)

    def check(self) -> list[Error]:
        """Запуск проверок для переданного python кода с учетом конфига"""
        tree = ast.parse(self._code)
        for node in ast.walk(tree):
            for ast_type, checker in self._CHECKERS.items():
                if isinstance(node, ast_type):
                    checker(self, node)
        return self._errors

    @staticmethod
    def get_string_name() -> str:
        return "naming"

    def _check_class(self, node: ast.ClassDef) -> None:
        """Проверка для классов"""
        self._known_classes.add(node.name)
        self._check_name(node, node.name, self._RULES[ast.ClassDef])

    def _check_function(self, node: ast.FunctionDef) -> None:
        """Проверка для функций и их аргументов"""
        self._check_name(node, node.name, self._RULES[ast.FunctionDef])
        self._check_function_args(node)

    def _check_variable(self, node: ast.Name) -> None:
        """Проверка для переменных"""
        if isinstance(node.ctx, ast.Store):
            self._check_name(node, node.id, self._RULES[ast.Name])
        elif isinstance(node.ctx, ast.Load):
            if node.id in self._known_classes:
                self._check_name(node, node.id, self._RULES[ast.ClassDef])
            else:
                self._check_name(node, node.id, self._RULES[ast.Name])

    def _check_attribute(self, node: ast.Attribute) -> None:
        """Проверка для аттрибутов"""
        if isinstance(node.value, ast.Name) and isinstance(node.ctx, ast.Store) and node.value.id == "self":
            self._check_name(node, node.attr, self._RULES[ast.Attribute])
        elif isinstance(node.ctx, ast.Load):
            self._check_name(node, node.attr, self._RULES[ast.Attribute])

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
            self._errors.append(NamingError(style_error, node.lineno, name))


class NamingFixer(Fixer):
    """Класс, исправляющий ошибки именования переменных, классов, функций и пр."""

    _NAME_ATTRS = {
        ast.ClassDef: "name",
        ast.FunctionDef: "name",
        ast.Name: "id",
        ast.arg: "arg",
        ast.Attribute: "attr",
    }

    def __init__(self, code: str):
        fixers: dict[str, Callable[[int], None]] = {
            "N001": self._fix_class_name,
            "N002": self._fix_function_name,
            "N003": self._fix_variable_name,
            "N004": self._fix_argument_name,
            "N005": self._fix_attribute_name,
        }

        super().__init__(code, fixers)
        self._tree = ast.parse(code)
        self._known_classes: set[str] = set()
        self._names = self._find_all_names()

    def _find_all_names(self) -> dict[Any, dict[str, list[ast.AST]]]:
        """Поиск всех имен и их вхождений и объединение их в словарь по категориям"""
        all_names: dict[Any, dict[str, list[ast.AST]]] = {
            ast.ClassDef: defaultdict(list),
            ast.FunctionDef: defaultdict(list),
            ast.Name: defaultdict(list),
            ast.arg: defaultdict(list),
            ast.Attribute: defaultdict(list),
        }

        for node in ast.walk(self._tree):
            for node_type, attr_name in self._NAME_ATTRS.items():
                if isinstance(node, node_type):
                    node_name = getattr(node, attr_name)

                    if node_name in self._known_classes:
                        all_names[ast.ClassDef][node_name].append(node)
                    elif node_type is ast.ClassDef:
                        self._known_classes.add(node_name)
                        all_names[ast.ClassDef][node_name].append(node)
                    else:
                        all_names[node_type][node_name].append(node)

                    break

        return all_names

    def _fix_class_name(self, lineno: int) -> None:
        """Исправление имени класса"""
        self._fix_name(ast.ClassDef, self._convert_to_camel_case)

    def _fix_function_name(self, lineno: int) -> None:
        """Исправление имен функций и методов"""
        self._fix_name(ast.FunctionDef, self._convert_to_snake_case)

    def _fix_variable_name(self, lineno: int) -> None:
        """Исправление имен переменных"""
        self._fix_name(ast.Name, self._convert_to_snake_case)

    def _fix_argument_name(self, lineno: int) -> None:
        """Исправление имен аргументов"""
        self._fix_name(ast.arg, self._convert_to_snake_case)

    def _fix_attribute_name(self, lineno: int) -> None:
        """Исправление имен аттрибутов"""
        self._fix_name(ast.Attribute, self._convert_to_snake_case)

    def _fix_name(self, role: Any, converter: Callable[[str], str]) -> None:
        """Исправление имени с помощью переданного метода для преобразования форматов"""
        if self._current_error is None or not isinstance(self._current_error, NamingError):
            return

        role_names = self._names.get(role)
        if role_names is None:
            return

        current_name = self._current_error.wrong_name
        nodes = role_names.get(current_name)
        if nodes is None:
            return

        for node in nodes:
            if not isinstance(node, ast.stmt):
                return
            num = node.lineno - self._offset
            self._code_lines[num] = self._code_lines[num].replace(current_name, converter(current_name))

            del role_names[current_name]

    @staticmethod
    def _convert_to_camel_case(old_name: str) -> str:
        """Получить из snake_case UpperCamelCase"""
        parts = re.split(r'[_\s]+', old_name)
        return ''.join(p.capitalize() for p in parts if p)

    @staticmethod
    def _convert_to_snake_case(old_name: str) -> str:
        """Получить из UpperCamelCase snake_case"""
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', old_name)
        return name.lower()
