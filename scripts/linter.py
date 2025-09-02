# import ast
import os
import tomllib
from typing import Any


class Linter:
    _CONFIG_NAME = "linter_config.toml"

    def __init__(self, files_path: str) -> None:
        (self.files, self.directory) = self._parse_files_path(files_path)
        self.rules = self._load_rules()

    def run(self) -> None:
        for file in self.files:
            code = self._read_code(file)
            print(code)

    @staticmethod
    def _read_code(file_path: str) -> str:
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def _parse_files_path(files_path: str) -> tuple[list[str], str]:
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
        return os.path.splitext(file)[1] == ".py"

    def _load_rules(self) -> dict[str, Any]:
        with open(file=os.path.join(self.directory, self._CONFIG_NAME), mode="rb") as file:
            config = tomllib.load(file)
            print(config)
        return config
