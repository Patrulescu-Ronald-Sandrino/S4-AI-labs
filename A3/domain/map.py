import copy
import inspect
import pickle
import sys
from enum import IntEnum
from random import random, randint
from typing import List, Tuple, Dict

import numpy as np
from texttable import Texttable

import utils


class Map:
    class Position(IntEnum):
        EMPTY = 0
        WALL = 1
        ACCESSIBLE = 2

    def __init__(self, rows: int = utils.MAP_HEIGHT, columns: int = utils.MAP_WIDTH):
        self.__rows = rows
        self.__columns = columns
        self.__surface = np.zeros((self.__rows, self.__columns))

    @property
    def width(self) -> int:  # getter property
        return self.__columns

    @property
    def height(self) -> int:
        return self.__rows

    def __getitem__(self, item: int) -> List[int]:
        """
        Returns a deep copy
        :param item:
        :return:
        """
        return copy.deepcopy(self.__surface[item])
    
    def at(self, position: Tuple[int, int]) -> Position:
        x, y = position
        return self.__surface[y][x]

    def is_position_inside_map(self, position: Tuple[int, int]) -> bool:
        (x, y) = position
        return x in range(self.__columns) and y in range(self.__rows)

    def random_map(self, fill: float = utils.MAP_RANDOM_FILL) -> 'Map':  # return type Map in order to be able to do map = Map().random_map()
        for i in range(self.__rows):
            for j in range(self.__columns):
                if random() <= fill:
                    self.__surface[i][j] = self.Position.WALL
        return self

    def save_map(self, map_file_path: str = "assets/test.map") -> None:
        try:
            with open(map_file_path, 'wb') as file:
                pickle.dump(self, file)
        except OSError as e:
            sys.stderr.write("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, e))
            raise Exception("Failed to save map")

    def load_map(self, map_file_path: str = "assets/test.map") -> 'Map':
        try:
            with open(map_file_path, 'rb') as file:
                loaded_map = pickle.load(file)
                self.__rows = loaded_map.__rows
                self.__columns = loaded_map.__columns
                self.__surface = loaded_map.__surface
            return self
        except OSError as e:
            sys.stderr.write("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, e))
            raise Exception("Failed to load map")

    def generate_random_position(self) -> Tuple[int, int]:
        return randint(0, self.__columns), randint(0, self.__rows)

    def generate_random_position_of_type(self, position_type: Position) -> Tuple[int, int]:
        """
        Generates a random position of a given type
        :param position_type:
        :return: the generated random position as a tuple <br>
                 (width, height) if no such position was found
        """
        tried_positions: Dict[Tuple[int, int], bool] = {}  # static typing

        while len(tried_positions) < self.__columns * self.__rows:
            random_position = self.generate_random_position()
            if self.at(random_position) == position_type:
                return random_position
            tried_positions[random_position] = True

        return self.__columns, self.__rows

    def __str__(self) -> str:
        string = ""
        for i in range(self.__rows):
            for j in range(self.__columns):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def to_table(self) -> str:
        # searched and replaced "([^_])(columns|rows|surface)" with "$1self.$2"
        table = Texttable()  # texttable
        table.set_cols_align(['c' for _ in range(0, self.__columns + 1)])
        table.set_cols_width([5 for _ in range(0, self.__columns + 1)])
        table.add_rows([[""] + [str(_) for _ in range(0, self.__columns)]] + [[str(row)] + [str(self.__surface[row][column]) for column in range(0, self.__columns)] for row in range(0, self.__rows)])
        return table.draw()

    def read_udm_sensors(self, x: int, y: int) -> List[int]:
        readings = [0, 0, 0, 0]
        # UP 
        xf = x - 1
        while (xf >= 0) and (self.__surface[xf][y] == 0):
            xf = xf - 1
            readings[utils.Directions.DOWN] = readings[utils.Directions.UP] + 1
        # DOWN
        xf = x + 1
        while (xf < self.__rows) and (self.__surface[xf][y] == 0):
            xf = xf + 1
            readings[utils.Directions.DOWN] = readings[utils.Directions.DOWN] + 1
        # LEFT
        yf = y + 1
        while (yf < self.__columns) and (self.__surface[x][yf] == 0):
            yf = yf + 1
            readings[utils.Directions.LEFT] = readings[utils.Directions.LEFT] + 1
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.__surface[x][yf] == 0):
            yf = yf - 1
            readings[utils.Directions.RIGHT] = readings[utils.Directions.RIGHT] + 1

        return readings

    def fix_chromosome(self, chromosome: List[int], start_position: Tuple[int, int]) -> List[int]:
        fixed_chromosome = []
        visited = {start_position: True}
        x, y = start_position

        for direction_index in chromosome:
            delta_x, delta_y = utils.DIRECTIONS[direction_index]
            new_position = new_x, new_y = x + delta_x, y + delta_y

            if self.is_position_inside_map(new_position) and self[new_x][new_y] != self.Position.WALL and new_position not in visited:
                (x, y) = new_position
                visited[(x, y)] = True
                fixed_chromosome.append(direction_index)

        return fixed_chromosome
