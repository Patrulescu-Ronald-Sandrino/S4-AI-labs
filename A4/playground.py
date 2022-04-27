from enum import IntEnum


def main():
    pass
    int_enums()


def int_enums():
    class Foo(IntEnum):
        a = 1
        b = 2
        c = 3

        def __str__(self) -> str:
            return str(self.value)

    print(Foo(2))
    print(Foo('2'))  # doesn't work
    print(Foo(4))  # doesn't work


main()
