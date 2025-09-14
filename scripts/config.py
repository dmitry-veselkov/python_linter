from __future__ import annotations

import os
import tomllib
from abc import ABC
from typing import Any

from .constants import CONFIG_NAME
from .rules.empty_lines import EmptyLinesRules
from .rules.naming import NamingRules
from .rules.spaces import SpacesRules


class Config(ABC):
    """Конфиг, необходимый для включения тех проверок, которые будут запущены линтером"""

    RULES = {NamingRules: "naming", SpacesRules: "spaces", EmptyLinesRules: "empty_lines"}

    @staticmethod
    def load_config(directory: str = "") -> dict[str, Any]:
        """Загрузка конфига по переданному (или стандартному) пути"""
        config: dict[str, Any]
        # TODO: корректное поведение при отсутсвии файла с конфигом
        with open(file=os.path.join(directory, CONFIG_NAME), mode="rb") as file:
            config = tomllib.load(file)
        return config
