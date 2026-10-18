# mypy: ignore-errors


class person:
    def __init__(self, name: str, Age: int) -> None:
        self.Name = name
        self.age = Age

    def ToString(self) -> str:
        if 1 == 1:
            return f"{self.Name}: {self.age} years old"


class My_Class:
    pass


# комментарий на новой строке
def main() -> None:
    """А здесь вообще докстринг"""
    Bob = person("Bob", 19)
    print(Bob.ToString())


if __name__ == "__main__":
    main()  # комментарии
