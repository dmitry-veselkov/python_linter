# mypy: ignore-errors


class _person:
    def __init__(self, name: str, Age: int) -> None:
        self.Name = name
        self.ageAge = Age

    def ToString(self) -> str:
        if 1 == 1:
            return f"{self.Name}: {self.ageAge} years old"


class My_Class:
    pass


def main() -> None:
    BoB: _person = _person("Bob", 19)
    print(BoB.ToString())


if __name__ == "__main__":
    main()
