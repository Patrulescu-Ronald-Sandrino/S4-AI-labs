
from enum import IntEnum


"""Map Constants"""

MAP_ROWS: int = 20
MAP_COLUMNS: int = 20
MAP_FILL: float = 0.2
MAP_FILEPATH: str = "assets/test.map"


class MapPosition(IntEnum):
    EMPTY = 0
    WALL = 1
    SENSOR = 2


"""Other constants"""

