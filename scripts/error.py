from pydantic import BaseModel


class StyleError(BaseModel):
    """Код и сообщение для выбранного типа ошибок"""

    key: str
    message: str


class Error:
    """Класс стилистической ошибки, которую может отловить линтер"""

    CATCHABLE_S_ERRORS = {
        "S001": StyleError(key="S001", message="Missing whitespace around operator"),
        "S002": StyleError(key="S002", message="Missing two whitespaces before the #"),
        "S003": StyleError(key="S003", message="Missing whitespace between # and comment"),
        "S004": StyleError(key="S004", message="An empty comment can be deleted"),
        "S005": StyleError(key="S005", message="Extra spaces at the end of the line"),
        "S006": StyleError(key="S006", message="Using tabs"),
        "S007": StyleError(key="S007", message="The number of spaces is not a multiple of 4"),
    }

    CATCHABLE_N_ERRORS = {
        "N001": StyleError(key="N001", message="The class name should be in a CamelCase"),
        "N002": StyleError(key="N002", message="The function name should be in a snake_case"),
        "N003": StyleError(key="N003", message="The variable name should be in a snake_case"),
        "N004": StyleError(key="N004", message="The argument name should be in a snake_case"),
        "N005": StyleError(key="N005", message="The attribute name should be in a snake_case"),
        "N006": StyleError(key="N006", message="The constant name should be in a UPPER_SNAKE_CASE"),
    }

    CATCHABLE_E_ERRORS = {
        "E001": StyleError(key="E001", message="Too many empty lines in a row"),
        "E002": StyleError(key="E002", message="There should be one empty line at the end of the file"),
    }

    def __init__(self, style_error: StyleError, line_number: int):
        """Инициализация новой ошибки"""
        self.style_error = style_error
        self.line_number = line_number


class NamingError(Error):
    """Класс для ошибок именования, сохраняющий еще и само имя"""

    def __init__(self, style_error: StyleError, line_number: int, wrong_name: str) -> None:
        super().__init__(style_error, line_number)
        self.wrong_name = wrong_name
