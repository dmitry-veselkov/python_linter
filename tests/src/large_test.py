# mypy: ignore-errors


def BigFunc0(a, b, c):
    total = a + b + c
    if total > 0:
        print("А русские буковки ты как прочитаешь интересно")
    else:
        print("Total is less than or equal 0")


def BigFunc1(a, b, c):
    total = a * b + c
    if total > 1:
        print("Total is greater than 1")
    else:
        print("Total is less than or equal 1")


def BigFunc2(a, b, c):
    total = a - b + c
    if total > 2:
        print("Total is greater than 2")
    else:
        print("Total is less than or equal 2")


def BigFunc3(a, b, c):
    total = a + b * c
    if total > 3:
        print("Total is greater than 3")
    else:
        print("Total is less than or equal 3")


def BigFunc4(a, b, c):
    total = (a + b) * c
    if total > 4:
        print("Total is greater than 4")
    else:
        print("Total is less than or equal 4")


def BigFunc5(a, b, c):
    total = a**b + c
    if total > 5:
        print("Total is greater than 5")
    else:
        print("Total is less than or equal 5")


def BigFunc6(a, b, c):
    total = a + b - b
    if total > 6:
        print("Total is greater than 6")
    else:
        print("Total is less than or equal 6")


def BigFunc7(a, b, c):
    total = a - b - b
    if total > 7:
        print("Total is greater than 7")
    else:
        print("Total is less than or equal 7")


def BigFunc8(a, b, c):
    total = a * b - b
    if total > 8:
        print("Total is greater than 8")
    else:
        print("Total is less than or equal 8")


def BigFunc9(a, b, c):
    total = a * b + b
    if total > 9:
        print("Total is greater than 9")
    else:
        print("Total is less than or equal 9")


# Продолжим до 150 строк с повторением ошибок и случайными числами

x0 = 0
x1 = 1
x2 = 2
x3 = 3
x4 = 4
x5 = 5
x6 = 6
x7 = 7
x8 = 8
x9 = 9
x10 = 10
x11 = 11
x12 = 12
x13 = 13
x14 = 14
x15 = 15
x16 = 16
x17 = 17
x18 = 18
x19 = 19
x20 = 20
x21 = 21
x22 = 22
x23 = 23
x24 = 24

print(BigFunc0(x0, x1, x2))
print(BigFunc1(x3, x4, x5))
print(BigFunc2(x6, x7, x8))
print(BigFunc3(x9, x10, x11))
print(BigFunc4(x12, x13, x14))
print(BigFunc5(x15, x16, x17))
print(BigFunc6(x18, x19, x20))
print(BigFunc7(x21, x22, x23))
print(BigFunc8(x0, x1, x2))
print(BigFunc9(x3, x4, x5))
