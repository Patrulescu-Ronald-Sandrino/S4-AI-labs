from enum import IntEnum
from typing import Tuple


def main():
    pass
    # int_enums()
    # tuple_args()
    ranges()


def ranges():
    generator = range(2, 0, -1)
    # print(generator.index(0))
    it = generator.__iter__()
    print(it)

    print(it.__next__())
    print(it.__next__())
    print(it.__next__())  # raises StopIteration
    print(it.__next__())
    print(it.__next__())


def tuple_args():
    def foo(a: Tuple[int, int]):
        print(a)

    foo(2, 3) # unexpected argument


def int_enums():
    class Foo(IntEnum):
        a = 1
        b = 2
        c = 3

        def __str__(self) -> str:
            return str(self.value)

    print(Foo(2))
    print(f'len(Foo)={len(Foo)}')
    print(Foo('2'))  # doesn't work
    print(Foo(4))  # doesn't work

main()
