import argparse

from linter import Linter


class CLI:
    """Консольный интерфейс линтера"""

    @staticmethod
    def run() -> None:
        """Парсинг полученных аргументов и запуск линтера"""
        parser = argparse.ArgumentParser(description="Python Linter")
        parser.add_argument('files_path', help="Absolute or relative path to input file or directory")
        args = parser.parse_args()

        print("Processing...")

        linter = Linter(args.files_path)
        # TODO: обработка случая, когда нет ошибок
        for error, codeline in linter.run():
            # TODO: (опционально) добавить красок в эти сообщения
            print(f"Line {error.line_number}: '{codeline}'")
            print(f"{error.key}: {error.style.capitalize()} error!")
            print()
