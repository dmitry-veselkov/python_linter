# mypy: ignore-errors


class my_class:
    DefaultValue = 10

    def DoSomething(self, UserName, Age):
        localVar = UserName + str(Age)
        return localVar
