class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def to_string(self) -> str:
        return f"{self.name}: {self.age} years old"


def main() -> None:
    bob = Person("Bob", 19)
    print(bob.to_string())


if __name__ == "__main__":
    main()
