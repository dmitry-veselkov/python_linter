import click
import termcolor

from .error import Error
from .linter import Linter


class CLI:
    """Консольный интерфейс линтера"""

    @staticmethod
    @click.command()
    @click.option("-files_path", prompt=True)
    def run(files_path: str) -> None:
        """Запуск линтера для указанных в командной строке файлов"""
        linter = Linter(files_path)
        errors_count = 0
        CLI._print_start_message(files_path)
        for error, codeline in linter.run():
            errors_count += 1
            CLI._print_error(error, codeline)

        CLI._print_work_result(errors_count)

    @staticmethod
    def _print_start_message(files_path: str) -> None:
        """Вывод сообщения о начале работы линтера"""
        termcolor.cprint(text=f"\nLinter started working on '{files_path}':\n", color='white', attrs=['bold'])

    @staticmethod
    def _print_error(error: Error, codeline: str) -> None:
        """Вывод ошибки вместе со строкой, на которой ошибка была обнаружена"""
        codeline_colored = termcolor.colored(codeline, 'blue')
        error_key_colored = termcolor.colored(error.style_error.key, 'red')
        print(f"Line {error.line_number}: {codeline_colored}")
        print(f"{error_key_colored}: {error.style_error.message}\n")

    @staticmethod
    def _print_work_result(errors_count: int) -> None:
        """Финальное сообщение, о числе обнаруженных ошибок"""
        if errors_count == 0:
            termcolor.cprint(text="No stylistic errors were found!\n", color='green')
        else:
            termcolor.cprint(text=f"{errors_count} errors were detected!\n", color='green')
