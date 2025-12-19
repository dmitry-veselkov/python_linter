import pathlib
from typing import Any, Generator

from .config import Config
from .error import Error
from .rules.empty_lines import EmptyLinesRules  # noqa: F401
from .rules.naming import NamingRules  # noqa: F401
from .rules.spaces import SpacesRules  # noqa: F401


class Linter:
    """Линтер для проверки корректности именования идентификаторов, расстановки пробелов и пустых строк"""

    def __init__(self, files_path: str, auto_correct: bool) -> None:
        """Инициализация нового линтера для переданного файла или директории файлов"""
        (self._files, self._directory) = self._parse_files_path(files_path)
        self._auto_correct = auto_correct
        self._config = Config.load_config(self._directory)

    def run(self) -> Generator[tuple[Error, str], None, None]:
        """Запуск линтера для всех файлов"""
        for file_path in self._files:
            code = self._read_file(file_path)
            file_errors, fixed_code = self.run_all_checks(code, self._config, self._auto_correct)
            for error, codeline in self._parse_file_errors(code, file_errors):
                yield error, codeline

            if self._auto_correct:
                self._write_fixed_code(file_path, fixed_code)

    @staticmethod
    def run_all_checks(code: str, config: dict[str, Any], auto_correct: bool) -> tuple[list[Error], str]:
        """Запуск всех включенных в конфиге проверок для переданного python кода"""
        all_errors: list[Error] = []
        for rule_type in (NamingRules, SpacesRules, EmptyLinesRules):
            string_name = rule_type.get_string_name()
            local_config = config[string_name]

            rule = rule_type(local_config, code)  # type: ignore[abstract]
            errors = rule.check()
            all_errors.extend(errors)

            if auto_correct:
                code = rule.fix()

        return all_errors, code

    @staticmethod
    def _parse_file_errors(code: str, file_errors: list[Error]) -> Generator[tuple[Error, str], None, None]:
        """Вывод всех найденных ошибок для переданного кода с указанием номера строки и типа ошибки"""
        lines = code.split('\n')
        file_errors.sort(key=lambda x: x.line_number)
        for error in file_errors:
            codeline = lines[error.line_number - 1].lstrip()
            yield error, codeline

    @staticmethod
    def _write_fixed_code(file_path: pathlib.Path, fixed_code: str) -> None:
        """Запись исправленной версии кода в файлик"""
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(fixed_code)

    @staticmethod
    def _read_file(file_path: pathlib.Path) -> str:
        """Получение содержимого переданного файла"""
        with open(file_path, encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def _parse_files_path(files_path: str) -> tuple[list[pathlib.Path], pathlib.Path]:
        """Разбор полученных из командной строки путей на список файлов и их директорию"""
        path = pathlib.Path(files_path)
        if path.is_file():
            if Linter._is_python_file(path):
                return [path], path.parents[0]
            raise ValueError(f"The file '{files_path}' is not a python file")

        if path.is_dir():
            files = []
            for file in path.iterdir():
                file_path = pathlib.Path(files_path, file)
                if file_path.is_file() and Linter._is_python_file(file):
                    files.append(file_path)
            return files, path

        raise FileNotFoundError(f"No such file or directory: '{files_path}'")

    @staticmethod
    def _is_python_file(file: pathlib.Path) -> bool:
        """Проверка расширения .py у файла"""
        return file.suffix == ".py"
