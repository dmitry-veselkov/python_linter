# Python Linter

## Краткое описание
**Linter** (*линтер*) — статический анализатор кода, который указывает на участки программы, где были допущены стилистические ошибки. Так, данный линтер может обнаружить следующие разновидности ошибок:
* именование идентификаторов (некорректные имена переменных, классов, функций и пр.)
* расстановка пробелов (лишние пробелы, использование табуляции и пр.)
* пустые строки (остутствие пустой строки в конце файла, слишком большое число пустых строк подряд)

## Список команд и детали реализации
Команда для запуска линтера в общем виде:

```python script.script files_path```

**Позиционные аргументы:**
* files_path - абсолютный или относительный путь к проверяемому файлу или директории файлов

Для корректной работы программы в директории с проверяемыми линтером файлами должен быть специальный config-файл:

Название config-файла: `linter_config.toml`

```
[spaces]
trailing_spaces = true
indentations = true
operators = true

[empty_lines]
check_empty_lines = true
check_last_empty_line = true

[naming]
function_snake_case = true
variables_snake_case = true
args_snake_case = true
class_camel_case = true
attributes_snake_case = true
```

Каждому параметру в config-файле соответствуют ошибки, которые в зависимости от установленного флага true/false будут учитываться или, соответственно, опускаться при проверке.

```
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
```

## Выполненные пункты чек-листа:
- [x] Добавлен .gitignore
- [x] Создано виртуальное окружение
- [x] Есть файл requirements.txt или pyproject.toml
- [x] Настроены линтеры: mypy и flake8
- [x] Настроены форматтеры: isort и black
- [x] Написаны тесты
- [x] Написана документация к каждому методу, классу и функции
- [x] Написан красивый README.md
- [x] (Для консольных утилит) написан help
