import os
from typing import Any, Generator

from .config import Config
from .error import Error


class Linter:
    """Линтер для проверки корректности именования идентификаторов, расстановки пробелов и пустых строк"""

    def __init__(self, files_path: str) -> None:
        """Инициализация нового линтера для переданного файла или директории файлов"""
        (self._files, self._directory) = self._parse_files_path(files_path)
        self._config = Config.load_config(self._directory)

    def run(self) -> Generator[tuple[Error, str], None, None]:
        """Запуск линтера для всех файлов"""
        for file_path in self._files:
            code = self._read_file(file_path)
            file_errors = self.run_all_checks(code, self._config)
            for error, codeline in self._parse_file_errors(code, file_errors):
                yield error, codeline

    @staticmethod
    def run_all_checks(code: str, config: dict[str, Any]) -> list[Error]:
        """Запуск всех включенных в конфиге проверок для переданного python кода"""
        all_errors: list[Error] = []
        for rule in Config.RULES.keys():
            rule_key = Config.RULES[rule]
            local_config = config[rule_key]
            rule_errors = rule(local_config, code).check()  # type: ignore[abstract]
            all_errors.extend(rule_errors)
        return all_errors

    @staticmethod
    def _parse_file_errors(code: str, file_errors: list[Error]) -> Generator[tuple[Error, str], None, None]:
        """Вывод всех найденных ошибок для переданного кода с указанием номера строки и типа ошибки"""
        lines = code.split('\n')
        file_errors.sort(key=lambda x: x.line_number)
        for error in file_errors:
            codeline = lines[error.line_number - 1].lstrip()
            yield error, codeline

    @staticmethod
    def _read_file(file_path: str) -> str:
        """Получение содержимого переданного файла"""
        with open(file_path, encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def _parse_files_path(files_path: str) -> tuple[list[str], str]:
        """Разбор полученных из командной строки путей на список файлов и их директорию"""
        if os.path.isfile(files_path):
            if Linter._is_python_file(files_path):
                return [files_path], os.path.dirname(files_path)
            raise ValueError(f"The file '{files_path}' is not a python file")

        if os.path.isdir(files_path):
            files = []
            for file in os.listdir(files_path):
                file_path = os.path.join(files_path, file)
                if os.path.isfile(file_path) and Linter._is_python_file(file_path):
                    files.append(file_path)
            return files, files_path

        raise FileNotFoundError(f"No such file or directory: '{files_path}'")

    @staticmethod
    def _is_python_file(file: str) -> bool:
        """Проверка расширения .py у файла"""
        return os.path.splitext(file)[1] == ".py"
