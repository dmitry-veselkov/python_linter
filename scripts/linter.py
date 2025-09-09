import os

from .config import Config


class Linter:
    def __init__(self, files_path: str) -> None:
        (self.files, self.directory) = self._parse_files_path(files_path)
        self.config = Config.load_config(self.directory)

    def run(self) -> None:
        for file_path in self.files:
            code = self._read_file(file_path)
            self._run_all_checks(code)

    def _run_all_checks(self, code: str) -> None:
        for rules in Config.RULES.keys():
            rules_key = Config.RULES[rules]
            local_config = self.config[rules_key]
            rules(local_config, code).check()  # type: ignore[abstract]

    @staticmethod
    def _read_file(file_path: str) -> str:
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def _parse_files_path(files_path: str) -> tuple[list[str], str]:
        """Полученный из командной строки пути метод разбирает на список файлов и их директорию"""
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
