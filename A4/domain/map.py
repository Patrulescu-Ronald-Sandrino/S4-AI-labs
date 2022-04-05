import inspect
import pickle
import random

import numpy as np
import texttable

from domain.constants import MapPosition, MAP_FILL, MAP_ROWS, MAP_COLUMNS
from domain.position import Position


class Map:
    def __init__(self, rows: int = MAP_ROWS, columns: int = MAP_COLUMNS) -> None:
        self.__rows: int = rows
        self.__columns: int = columns
        self.__surface = np.zeros((self.__rows, self.__columns))
        self.__sensors = []  # type List[Position]

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def columns(self) -> int:
        return self.__columns

    def is_position_valid(self, position: Position) -> bool:
        return position.x < self.__columns and position.y < self.__rows

    def at(self, position: Position) -> MapPosition:
        return self.__surface[position.x][position.y] if self.is_position_valid(position) else MapPosition.OUT_OF_RANGE

    def randomize(self, fill: float = MAP_FILL) -> 'Map':
        for row in range(self.__rows):
            for column in range(self.__columns):
                if random.random() <= fill:
                    self.__surface[row][column] = MapPosition.WALL
        return self

    def save_map(self, map_filepath: str = "assets/test.map") -> None:
        try:
            with open(map_filepath, "wb") as output_file:
                pickle.dump(self, output_file)
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to save map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def load_map(self, map_filepath: str = "assets/test.map") -> 'Map':
        try:
            with open(map_filepath, "rb") as input_file:
                loaded_map: 'Map' = pickle.load(input_file)
                self.__rows = loaded_map.__rows
                self.__columns = loaded_map.__columns
                self.__surface = loaded_map.__surface
            return self
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to load map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def to_table(self) -> str:
        table: texttable.Texttable = texttable.Texttable()
        table.set_cols_align(['c' for _ in range(0, self.__columns + 1)])
        table.set_cols_width([5 for _ in range(0, self.__columns + 1)])
        table.add_rows([[""] + [str(_) for _ in range(0, self.__columns)]])
        table.add_rows([[str(row)] + [str(self.__surface[row][column]) for column in range(0, self.__columns)]
                        for row in range(0, self.__rows)])
        return table.draw()

    def __str__(self) -> str:
        string = ""
        for row in range(self.__rows):
            for column in range(self.__columns):
                string = string + str(int(self.__surface[row][column]))
            string = string + "\n"
        return string
