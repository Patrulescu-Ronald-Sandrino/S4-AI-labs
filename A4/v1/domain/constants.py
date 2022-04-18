from enum import IntEnum
from typing import Union, List, Tuple


"Problem constants"
MAP_HEIGHT: int = 20
MAP_WIDTH: int = 20
MAP_SOURCE: str = ""  # "" - means random
DRONE_X: int = 5
DRONE_Y: int = 5
DRONE_BATTERY: int = 5
SENSORS: Union[int, List[Tuple[int, int]]] = 5  # a list of sensors positions or a number of random sensors


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_DELTA = {Direction.UP: (0, 1),
                   Direction.RIGHT: (1, 0),
                   Direction.DOWN: (0, -1),
                   Direction.LEFT: (-1, 0)}


