from __future__ import annotations

import pathlib
import tomllib
from abc import ABC
from typing import Any

from .constants import CONFIG_NAME


class Config(ABC):
    """Конфиг, необходимый для включения тех проверок, которые будут запущены линтером"""

    @staticmethod
    def load_config(directory: pathlib.Path = pathlib.Path.cwd()) -> dict[str, Any]:
        """Загрузка конфига по переданному пути или в текущей директории"""
        config: dict[str, Any]
        path = pathlib.Path(directory, CONFIG_NAME)
        if not path.exists():
            raise FileNotFoundError("The required config file 'linter_config.toml' was not found!")
        with open(file=path, mode="rb") as file:
            config = tomllib.load(file)
        return config
