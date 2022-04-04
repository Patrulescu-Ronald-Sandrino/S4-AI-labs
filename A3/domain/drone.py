from typing import Tuple


class Drone:
    def __init__(self, x: int, y: int, battery: int = 20):
        self.__x = x
        self.__y = y
        self.__battery = battery

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def position(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @property
    def battery(self) -> int:
        return self.__battery

    def move(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """
        moves the drone to a different position
        :param position: a tuple that contains the new values for x and y
        :return: the old position
        """
        old_position = self.__x, self.__y
        self.__x, self.__y = position
        return old_position
