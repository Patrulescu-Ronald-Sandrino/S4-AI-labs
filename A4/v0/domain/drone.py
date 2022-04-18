import inspect
from typing import Tuple

from v0.domain.position import Position


class Drone:
    def __init__(self, position: Position, energy: int):
        self.__position: Position = position
        if energy < 0:
            raise ValueError("[error][{}.{}()] Failed to create drone: {}\n".format(__class__,
                                                                                    inspect.stack()[0].function,
                                                                                    "Energy must be >= 0"))
        self.__energy: int = energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position.xy

    @position.setter
    def position(self, position: Position) -> None:
        self.__position = position

    @property
    def energy(self) -> int:
        return self.__energy
