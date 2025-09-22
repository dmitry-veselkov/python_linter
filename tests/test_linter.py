import unittest
from typing import Type

from scripts.cli import CLI
from scripts.config import Config
from scripts.constants import UNIVERSAL_CONFIG
from scripts.rules.empty_lines import EmptyLinesRules
from scripts.rules.naming import NamingRules
from scripts.rules.rules import Rules
from scripts.rules.spaces import SpacesRules


class TestLinter(unittest.TestCase):
    def test_one_file(self) -> None:
        file_path = "./src/one_file.py"
        CLI.start_linter(file_path)

    def test_many_files(self) -> None:
        directory = "./src/"
        CLI.start_linter(directory)

    def test_spaces_rules(self) -> None:
        code_samples = {
            "S001": "a+1",
            "S002": "x = 1# comment",
            "S003": "x = 1  #bad",
            "S004": "x = 1  #",
            "S005": "x = 1    ",
            "S006": "\tprint('hello')",
            "S007": "  print('я устал делать python таски')",
        }
        self._run_tests_for_rule(SpacesRules, code_samples)

    def test_naming_rules(self) -> None:
        code_samples = {
            "N001": "class myclass: pass",
            "N002": "def MyFunction(): pass",
            "N003": "myVar = 1",
            "N004": "def func(MyArg): pass",
            "N005": "self.MyAttr = 1",
        }
        self._run_tests_for_rule(NamingRules, code_samples)

    def test_empty_lines_rules(self) -> None:
        code_samples = {
            "E001": "def func():\n\n\n\n    pass\n",
            "E002": "def main():\n    print('hello')",
        }
        self._run_tests_for_rule(EmptyLinesRules, code_samples)

    def _run_tests_for_rule(self, rule: Type[Rules], code_samples: dict[str, str]) -> None:
        for key, code in code_samples.items():
            rule_toml = Config.RULES[rule]
            linter = rule(UNIVERSAL_CONFIG[rule_toml], code)
            errors = list(linter.check())
            self.assertEqual(1, len(errors))
            self.assertEqual(key, errors[0].style_error.key)
