import math


def run() -> None:
    # add function calls here
    # alignment_computing()
    # menu_to_str()
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
    commands = list(range(11))
    commands = list(range(99))
    commands = list(range(100))
    commands = list(range(101))
    commands = []
    commands = ["val"]
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


run()
