from __future__ import annotations

import inspect
from typing import Tuple

from domain.constants import Direction, DIRECTION_DELTA
from utils.constants import MAX_INT


class Position:
    def __int__(self, x: int, y: int):
        if x < 0:
            raise ValueError("[error][{}.{}()] Failed to create position: {}\n".format(__class__,
                                                                                       inspect.stack()[0].function,
                                                                                       "x must be >= 0"))
        if y < 0:
            raise ValueError("[error][{}.{}()] Failed to create position: {}\n".format(__class__,
                                                                                       inspect.stack()[0].function,
                                                                                       "y must be >= 0"))

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

    def to(self, direction: Direction, steps: int = 1) -> Position:
        """
        Creates a new position, to the given direction.
        If one of the parameters goes below 0, then POSITION_INVALID is returned.
        A negative 'steps' value inverses the direction. Ex: Position.to(RIGHT, 3) == Position.to(LEFT, -3)
        :param direction:
        :type steps: int
        """
        delta: Tuple[int, int] = DIRECTION_DELTA[direction]
        (delta_x, delta_y) = delta
        try:
            return Position(self.__x + delta[0] * steps, self.__y + delta_y * steps)
        except ValueError:
            return INVALID

    def __eq__(self, other: Position) -> bool:
        return self.__x == other.__x and self.__y == other.__y

    def __str__(self):
        return str(self.xy)

    @staticmethod
    def __get_invalid() -> Position:
        position: Position = Position(0, 0)
        position.__x = position.__y = MAX_INT
        return position

    @classmethod
    def __get_invalid(cls) -> Position:
        position: Position = Position(0, 0)
        position.__x = position.__y = MAX_INT
        return position


# Position.INVALID = Position(MAX_INT, MAX_INT)

