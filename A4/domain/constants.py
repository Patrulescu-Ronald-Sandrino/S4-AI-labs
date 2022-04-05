
from enum import IntEnum


"""Map Constants"""

MAP_ROWS: int = 20
MAP_COLUMNS: int = 20
MAP_FILL: float = 0.2


class MapPosition(IntEnum):
    OUT_OF_RANGE = -1
    EMPTY = 0
    WALL = 1
    SENSOR = 2


"""Other constants"""

