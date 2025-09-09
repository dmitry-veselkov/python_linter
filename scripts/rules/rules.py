from abc import ABC, abstractmethod
from typing import Any


class Rules(ABC):
    def __init__(self, config: dict[str, Any], code: str):
        self.config = config
        self.code = code

    @abstractmethod
    def check(self) -> None:
        pass
