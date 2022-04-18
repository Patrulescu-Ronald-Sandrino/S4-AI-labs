import inspect
from typing import Tuple

from v0.domain.constants import MAX_INT, Direction, DIRECTION_DELTA


class Position:
    def __init__(self, x: int, y: int):
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

    # @x.setter
    # def x(self, x: int) -> None:
    #     self.__x = x

    # @y.setter
    # def y(self, y: int) -> None:
    #     self.__y = y

    # @xy.setter
    # def xy(self, position: Tuple[int, int]) -> None:
    #     self.__x, self.__y = position

    def to(self, direction: Direction, steps: int = 1) -> 'Position':
        """
        Creates a new position, to the given direction.
        If one of the parameters goes below 0, then POSITION_INVALID is returned.
        A negative 'steps' value inverses the direction. Ex: Position.to(RIGHT, 3) == Position.to(LEFT, -3)
        """
        delta_x, delta_y = DIRECTION_DELTA[direction]
        try:
            return Position(self.__x + delta_x * steps, self.__y + delta_y * steps)
        except ValueError:
            return POSITION_INVALID

    def __eq__(self, other: 'Position') -> bool:
        return self.__x == other.__x and self.__y == other.__y

    def __str__(self):
        return str(self.xy)


POSITION_INVALID: Position = Position(MAX_INT, MAX_INT)
