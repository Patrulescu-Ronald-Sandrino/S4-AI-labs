from __future__ import annotations

import copy
import inspect
import pickle
from enum import IntEnum
from random import random, randint
from typing import List, Tuple

import numpy as np
import texttable


class Map:
    class Position(IntEnum):
        EMPTY = 0
        WALL = 1
        SENSOR = 2

    def __init__(self, rows: int, columns: int):
        self.__rows = rows
        self.__columns = columns
        self.__surface = np.zeros((self.__rows, self.__columns))

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def columns(self) -> int:
        return self.__columns

    @property
    def surface(self) -> List[List[Map.Position]]:
        return [[self.__surface[row][column] for column in range(self.columns)] for row in range(self.rows)]

    def is_position_valid(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.columns

    def add_walls_random(self, fill: float) -> Map:
        """replaces the old positions' values"""
        new_map: Map = Map(self.rows, self.columns)

        for i in range(new_map.rows):
            for j in range(new_map.columns):
                if random() < fill:
                    new_map.__surface[i][j] = Map.Position.WALL

        return new_map

    def add_sensors_from_list(self, sensors_list: List[Tuple[int, int]]):
        """adds sensors only on empty positions"""
        new_map: Map = copy.deepcopy(self)

        for sensor_row, sensor_column in sensors_list:
            if self.surface[sensor_row][sensor_column] == Map.Position.EMPTY:
                self.surface[sensor_row][sensor_column] = Map.Position.SENSOR

        return new_map

    def add_sensors_random(self, count: int) -> Map:
        """adds sensors only on empty positions"""
        new_map: Map = copy.deepcopy(self)

        for _ in range(count):
            row, column = randint(0, self.rows), randint(0, self.columns)
            if self.surface[row][column] == Map.Position.EMPTY:
                self.surface[row][column] = Map.Position.SENSOR

        return new_map

    @staticmethod
    def from_file(filename: str) -> Map:
        try:
            with open(filename, "rb") as input_file:
                return pickle.load(input_file)
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to load map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def save(self, filename: str) -> None:
        try:
            with open(filename, "wb") as output_file:
                pickle.dump(self, output_file)
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to save map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def __str__(self) -> str:
        string = ""
        for row in range(self.rows):
            for column in range(self.columns):
                string = string + str(int(self.surface[row][column])) + " "
            string = string + "\n"
        return string

    def to_texttable(self) -> str:
        table: texttable.Texttable = texttable.Texttable()
        table.set_cols_align(['c' for _ in range(0, self.__columns + 1)])
        table.set_cols_width([5 for _ in range(0, self.__columns + 1)])
        table.add_rows([[""] + [str(_) for _ in range(0, self.__columns)]])
        table.add_rows([[str(row)] + [str(self.__surface[row][column]) for column in range(0, self.__columns)]
                        for row in range(0, self.__rows)])
        return table.draw()
