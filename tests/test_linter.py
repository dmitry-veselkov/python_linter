import unittest

from click.testing import CliRunner

from scripts.cli import CLI
from scripts.constants import TOML_NAMES
from scripts.rules.empty_lines import EmptyLinesRules
from scripts.rules.naming import NamingRules
from scripts.rules.rules import Rules
from scripts.rules.spaces import SpacesRules


class TestLinter(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_one_file(self) -> None:
        file_path = "./src/one_file.py"
        self.runner.invoke(CLI.run, ["-files_path", file_path])

    def test_many_files(self) -> None:
        directory = "./src/"
        self.runner.invoke(CLI.run, ["-files_path", directory])

    def test_spaces_rules(self) -> None:
        code_samples: dict[str, tuple[str, bool, str]] = {
            "S001": ("a+1", True, "a + 1"),
            "S002": ("x = 1# comment", True, "x = 1  # comment"),
            "S003": ("x = 1  #bad", True, "x = 1  # bad"),
            "S004": ("x = 1  #", True, "x = 1"),
            "S005": ("x = 1    ", True, "x = 1"),
            "S006": ("\tprint('hello')", True, "    print('hello')"),
            "S007": ("  print('я устал делать python таски')", True, "print('я устал делать python таски')"),
        }
        self._run_tests_for_rule(SpacesRules, code_samples)

    def test_naming_rules(self) -> None:
        code_samples: dict[str, tuple[str, bool, str]] = {
            "N001": ("class myclass:\n    pass", True, "class Myclass:\n    pass"),
            "N002": ("def MyFunction():\n    pass", True, "def my_function():\n    pass"),
            "N003": ("myVar = 1", True, "my_var = 1"),
            "N004": ("def func(MyArg): pass", True, "def func(my_arg):\n    pass"),
            "N005": ("self.MyAttr = 1", True, "self.my_attr = 1"),
        }
        self._run_tests_for_rule(NamingRules, code_samples)

    def test_empty_lines_rules(self) -> None:
        code_samples: dict[str, tuple[str, bool, str]] = {
            "E001": (
                '\n'.join(["def func():", "", "", "", "pass", ""]),
                True,
                "\n".join(["def func():", "", "", "pass", ""]),
            ),
            "E002": ("def main():\n    print('hello')", True, "def main():\n    print('hello')\n"),
        }
        self._run_tests_for_rule(EmptyLinesRules, code_samples)

    def _run_tests_for_rule(self, rule: type[Rules], code_samples: dict[str, tuple[str, bool, str]]) -> None:
        for key, parameters in code_samples.items():
            rule_toml = rule.get_string_name()
            config = self._generate_all_true_config(rule_toml)
            linter = rule(config, parameters[0])
            errors = linter.check()
            self.assertEqual(1, len(errors))
            self.assertEqual(key, errors[0].style_error.key)

            if parameters[1]:
                fixed_code = linter.fix()
                self.assertEqual(fixed_code, parameters[2])

    @staticmethod
    def _generate_all_true_config(rule_name: str) -> dict[str, bool]:
        return {check_name: True for check_name in TOML_NAMES[rule_name]}
