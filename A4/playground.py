import random
import sys
from enum import IntEnum
from typing import Tuple


def main():
    pass
    # slicing()
    # int_enums()
    # tuple_args()
    # ranges()
    # max_values()
    get_random_key_from_dictionary()


def slicing():
    a = [1, 2, 3]
    b = a[:]
    b[1] = 3
    print(a)
    print(b)
    print(b[:-1])


def get_random_key_from_dictionary():
    print(random.choice(list({1: 2, 3: 5, 5: 6}.keys())))
    print(random.choice(list({1: 2, 3: 5, 5: 6}.keys())))
    print(random.choice(list({1: 2, 3: 5, 5: 6}.keys())))
    return


def max_values():
    print(float('inf'))
    print(int(float('inf')))
    print(float('inf') == float('inf'))
    print(sys.maxsize)
    print(float('inf') - sys.maxsize)
    print(type(float('inf')))


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
