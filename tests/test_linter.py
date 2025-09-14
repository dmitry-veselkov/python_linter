import unittest

from scripts.linter import Linter
from scripts.rules.naming import NamingRules


class TestLinter(unittest.TestCase):
    def test_syntactic_analysis(self) -> None:
        file_path = "../scripts"
        linter = Linter(file_path)
        for error, codeline in linter.run():
            print(f"Line {error.line_number}: '{codeline}'")
            print(f"{error.key}: {error.style.capitalize()} error!")
            print()

    def test_path_parser(self) -> None:
        # Linter._parse_files_path(f"./src/{self.test_syntactic_analysis.__name__}.py")
        print(Linter._parse_files_path("./src/"))
        # Linter._parse_files_path("52")

    def test_naming(self) -> None:
        code = """
class myclass:
    pass
class _badClassName:
    pass
"""
        rules = NamingRules(dict(), code)
        print(rules.check())
