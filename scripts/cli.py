import argparse

from linter import Linter


class CLI:
    @staticmethod
    def run() -> None:
        """Парсинг полученных аргументов и запуск линтера"""
        parser = argparse.ArgumentParser(description="Python Linter")
        parser.add_argument('files_path', help="Absolute or relative path to input file or directory")
        args = parser.parse_args()

        print("Processing...")

        linter = Linter(args.files_path)
        linter.run()
