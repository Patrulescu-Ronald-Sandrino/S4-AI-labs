from typing import Tuple

from domain.position import Position


class Drone:
    def __init__(self, x: int, y: int, battery: int):
        self.__position: Position = Position(x, y)
        self.__battery: int = battery

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position.xy

    @position.setter
    def position(self, position: Position) -> None:
        self.__position = position

    @property
    def battery(self) -> int:
        return self.__battery
