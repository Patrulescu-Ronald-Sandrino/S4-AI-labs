import sys
from enum import IntEnum

"""General Constants"""
MAX_INT = sys.maxsize


"""Map Constants"""

MAP_ROWS: int = 20
MAP_COLUMNS: int = 20
MAP_FILL: float = 0.2
MAP_FILEPATH: str = "assets/test.map"


class MapPosition(IntEnum):
    EMPTY = 0
    WALL = 1
    SENSOR = 2


MIN_SENSOR_ENERGY = 0
MAX_SENSOR_ENERGY = 5

MIN_NUMBER_OF_SENSORS = 2


"""Position Constants"""


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_DELTA = {Direction.UP: (0, 1),
                   Direction.RIGHT: (1, 0),
                   Direction.DOWN: (0, -1),
                   Direction.LEFT: (-1, 0)}


"""Other constants"""

