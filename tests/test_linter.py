import unittest

from scripts.linter import Linter
from scripts.rules.naming import NamingRules


class TestLinter(unittest.TestCase):
    def test_syntactic_analysis(self) -> None:
        # file_path = "./src/"
        file_path = f"./src/{self.test_syntactic_analysis.__name__}.py"
        linter = Linter(file_path)
        linter.run()

    def test_path_parser(self) -> None:
        # Linter._parse_files_path(f"./src/{self.test_syntactic_analysis.__name__}.py")
        print(Linter._parse_files_path("./src/"))
        # Linter._parse_files_path("52")

    def test_naming(self) -> None:
        rules = NamingRules(dict(), "def main():")
        rules.check()
