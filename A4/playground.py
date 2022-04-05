def main():
    # string_parsing()
    # read_line()
    equality()


def string_parsing():
    first_line: str = "12 a"
    [drone_x, drone_y] = map(lambda value: int(value), first_line.strip().split(" ", 2))
    print(drone_x, drone_y)


def read_line():
    filepath = "/tmp/a.txt"
    file_content = "a\nb\nc\n"
    with open(filepath, "w") as output_file:
        output_file.write(file_content)
    with open(filepath, "r") as input_file:
        # print(list(input_file))
        for line in list(input_file):
            print("line=", line.strip(), "|")
        for _ in range(10):
            print(_, input_file.readline())


def equality():
    class A:
        def __init__(self, x: int, y: int):
            self._x: int = x
            self._y: int = y

    class B(A):
        def __init__(self, x, y):
            super(B, self).__init__(x, y)

        def __eq__(self, other: 'B') -> bool:
            if not isinstance(other, B):
                return False
            if not isinstance(other, A):
                return False
            return self._x == other._x and self._y == other._y

    a1: A = A(2, 3)
    a2: A = A(2, 3)
    print("a1 == a2: ", a1 == a2)
    b1: B = B(2, 3)
    b2: B = B(2, 3)
    print("b1 == b2: ", b1 == b2)

    b_list = [b1, b2]
    for b in b_list:
        print("b == B(2, 3)", b == B(2, 3))


if __name__ == "__main__":
    main()
