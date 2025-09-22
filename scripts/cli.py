import argparse

from .error import Error
from .linter import Linter


class CLI:
    """Консольный интерфейс линтера"""

    @staticmethod
    def run() -> None:
        """Парсинг полученных аргументов и запуск линтера"""
        args = CLI._parse_arguments()
        files_path: str = args.files_path
        CLI.start_linter(files_path)

    @staticmethod
    def start_linter(files_path: str) -> None:
        """Запуск линтера для переданных файлов"""
        linter = Linter(files_path)
        errors_count = 0
        for error, codeline in linter.run():
            errors_count += 1
            CLI._print_error(error, codeline)

        CLI._print_work_result(errors_count)

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        """Парсинг аргументов, полученных из консоли"""
        parser = argparse.ArgumentParser(description="Python Linter")
        parser.add_argument('files_path', help="Absolute or relative path to input file or directory")
        return parser.parse_args()

    @staticmethod
    def _print_error(error: Error, codeline: str) -> None:
        """Вывод ошибки вместе со строкой, на которой ошибка была обнаружена"""
        print(f"Line {error.line_number}: '\033[34m{codeline}\033[0m'")
        print(f"\033[31m{error.style_error.key}\033[0m: {error.style_error.message}")
        print()

    @staticmethod
    def _print_work_result(errors_count: int) -> None:
        """Финальное сообщение, о числе обнаруженных ошибок"""
        if errors_count == 0:
            print("\033[32mNo stylistic errors were found!\033[0m")
        else:
            print(f"\033[32m{errors_count} errors were detected!\033[0m")
        print()
