from typing import Tuple


class Position:
    def __init__(self, x: int, y: int):
        self.__x: int = x
        self.__y: int = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @x.setter
    def x(self, x: int) -> None:
        self.__x = x

    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    @xy.setter
    def xy(self, position: Tuple[int, int]) -> None:
        self.__x, self.__y = position

    def __str__(self):
        return str(self.xy)
