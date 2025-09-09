from __future__ import annotations

import os
import tomllib
from typing import Any

from .constants import CONFIG_NAME
from .rules.empty_lines import EmptyLinesRules
from .rules.naming import NamingRules
from .rules.spaces import SpacesRules


class Config:
    RULES = {NamingRules: "naming", SpacesRules: "spaces", EmptyLinesRules: "empty_lines"}

    @staticmethod
    def load_config(directory: str = "") -> dict[str, Any]:
        config: dict[str, Any]
        with open(file=os.path.join(directory, CONFIG_NAME), mode="rb") as file:
            config = tomllib.load(file)
        return config
