import inspect
import math
import sys

from texttable import Texttable


def run() -> None:
    # add function calls here
    alignment_computing()
    # menu_to_str()
    # files()
    # text_table()
    return


def alignment_computing():
    for i in range(1, 102):
        # print("log({}, 10) = {}".format(i, math.log(i, 10)))
        # print("math.ceil(log({}, 10)) = {}".format(i, math.ceil(math.log(i, 10))))
        # print("math.floor(log({}, 10)) = {}".format(i, math.floor(math.log(i, 10))))
        print("math.floor(log({}, 10)) + 1 = {}".format(i, math.floor(math.log(i, 10)) + 1))


def menu_to_str():
    commands = ["a", "b", "c", "d"]
    commands = list(range(9))
    commands = list(range(10))
    # commands = list(range(11))
    # commands = list(range(99))
    # commands = list(range(100))
    # commands = list(range(101))
    # commands = []
    # commands = ["val"]
    result = ""
    align = math.floor(math.log(max(len(commands) - 1, 1), 10)) + 1  # math - log; math - floor
    print(align)
    for index, command in enumerate(commands):
        pass
        result += "{:>{align}}. {command_name}\n".format(index, align=align, command_name=command)  # string format
    print(result)
    print("size = ", len(commands))
    # print("log = ", math.log(len(commands), 10))
    print("align = ", align)


def files():

    def write(file_name: str, content: str):
        try:
            with open(file_name, "w") as file:
                file.write(content)
        except OSError:
            # sys.stderr.write("[error][{}.{}()]".format(__class__, inspect.stack()[0].function))
            sys.stderr.write("[error][{}.{}()]\n".format("", inspect.stack()[0].function))

    def read(file_name: str):
        try:
            with open(file_name, "r") as file:
                return file.readlines()
        except OSError as exception:
            pass
            # sys.stderr.write(inspect.stack().__str__())
            for line in inspect.stack():
                print(line)
            print(inspect.stack()[0].function)
            print(inspect.stack()[1].function)
            print(exception)
            print(sys.stderr.write("[error][{}.{}()]".format("", inspect.stack()[0].function)))

    class A:
        def foo(self):
            print(inspect.stack()[0].function)
            print(inspect.stack()[1].function)

    # A().foo()
    print("read contents:", read("abc.txt"))


def text_table():
    rows = 20
    columns = 20
    surface = [[row * columns + column for column in range(0, columns)] for row in range(0, rows)]
    # surface = [[rows * columns for column in range(0, columns)] for row in range(0, rows)]
    # for column in surface:
    #     print(column)

    table = Texttable()
    table.set_cols_align(['c' for _ in range(0, columns + 1)])
    # table.set_cols_width([5 for _ in range(0, columns + 1)])
    table.add_rows([[""] + [str(_) for _ in range(0, columns)]] + [[str(row)] + [str(surface[row][column]) for column in range(0, columns)] for row in range(0, rows)])
    print(table.draw())


run()
