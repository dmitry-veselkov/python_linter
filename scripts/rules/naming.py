import ast
from typing import Any

from .rules import Rules


class NamingRules(Rules):
    def __init__(self, config: dict[str, Any], code: str) -> None:
        super().__init__(config, code)

    def check(self) -> None:
        tree = ast.parse(self.code)
        for node in ast.walk(tree):
            if self._is_name(node):
                print(node)

    @staticmethod
    def _is_name(node: Any) -> bool:
        return isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef)
