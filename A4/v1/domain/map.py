from __future__ import annotations

import copy
import inspect
import pickle
from enum import IntEnum
from random import random, randint
from typing import List, Tuple, Dict

import numpy as np
import texttable

import tools.collections
from tools.collections import flat_map


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_DELTA = {Direction.UP: (0, 1),
                   Direction.RIGHT: (1, 0),
                   Direction.DOWN: (0, -1),
                   Direction.LEFT: (-1, 0)}


class Map:
    class CellType(IntEnum):
        EMPTY = 0
        WALL = 1
        SENSOR = 2

    def __init__(self, rows: int, columns: int):
        self.__rows = rows
        self.__columns = columns
        # self.__surface: List[List[Map.CellType.EMPTY]] = [[Map.CellType.EMPTY for _ in range(columns)] for _ in range(rows)]
        self.__surface: List[List[Map.CellType.EMPTY]] = tools.collections.create_matrix(lambda x, y: Map.CellType.EMPTY
                                                                                         , self.rows, self.columns)

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def columns(self) -> int:
        return self.__columns

    @property
    def surface(self) -> List[List[Map.CellType]]:
        return copy.deepcopy(self.__surface)

    def is_position_valid(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.columns

    def add_walls_random(self, fill: float) -> Map:
        """replaces the old cellTypes' values"""
        new_map: Map = Map(self.rows, self.columns)

        for i in range(new_map.rows):
            for j in range(new_map.columns):
                if random() < fill:
                    new_map.__surface[i][j] = Map.CellType.WALL

        return new_map

    def add_sensors_from_list(self, sensors_list: List[Tuple[int, int]]):
        """adds sensors only on empty cellTypes"""
        new_map: Map = copy.deepcopy(self)

        for sensor_row, sensor_column in sensors_list:
            if self.surface[sensor_row][sensor_column] == Map.CellType.EMPTY:
                self.surface[sensor_row][sensor_column] = Map.CellType.SENSOR

        return new_map

    def add_sensors_random(self, count: int) -> Map:
        """adds sensors only on empty cellTypes"""
        new_map: Map = copy.deepcopy(self)

        for _ in range(count):
            row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)
            if self.surface[row][column] == Map.CellType.EMPTY:
                self.surface[row][column] = Map.CellType.SENSOR

        return new_map

    def find_all(self, cell_type: CellType) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []

        for index, current_cell_type in enumerate(flat_map(self.surface, lambda x: x)):
            if current_cell_type == cell_type:
                result.append((int(index / self.columns), index % self.columns))

        return result

    def __find_distances_to_walls(self, row: int, column: int) -> Dict[Direction, int]:
        result: Dict[Direction, int] = {direction: 0 for direction in Direction}

        for direction in Direction:
            delta_column, delta_row = DIRECTION_DELTA[direction]
            next_row, next_column = row + delta_row, column + delta_column

            while self.is_position_valid(next_row, next_column) and self.__surface[next_row][next_column] != Map.CellType.WALL:
                result[direction] += 1
                next_row, next_column = next_row + delta_row, next_column + delta_column

        return result

    def compute_sensors_gains(self) -> Dict[Tuple[int, int], List[int]]:
        result: Dict[Tuple[int, int], List[int]] = {}
        sensors: List[Tuple[int, int]] = self.find_all(Map.CellType.SENSOR)

        # TODO #1: this and remove __find_distances_to_walls

        return result

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
        table.add_rows([[str(row)] + [str(int(self.__surface[row][column])) for column in range(0, self.__columns)]
                        for row in range(0, self.__rows)], False)
        return table.draw()
