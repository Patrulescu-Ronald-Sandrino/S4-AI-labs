import copy
import inspect
import pickle
import sys
from enum import Enum
from random import random, randint
from typing import List, Tuple, Dict

import numpy as np
from texttable import Texttable

import utils


class Map:
    class Position(Enum):
        EMPTY = 0
        WALL = 1
        ACCESSIBLE = 2

    def __init__(self, rows: int = utils.MAP_HEIGHT, columns: int = utils.MAP_WIDTH):
        self.rows = rows
        self.columns = columns
        self.surface = np.zeros((self.rows, self.columns))

    @property
    def width(self) -> int:  # getter property
        return self.columns

    @property
    def height(self) -> int:
        return self.rows

    def __getitem__(self, item: int) -> List[int]:
        """
        Returns a deep copy
        :param item:
        :return:
        """
        return copy.deepcopy(self.surface[item])
    
    def at(self, position: Tuple[int, int]) -> Position:
        x, y = position
        return self.surface[y][x]

    def is_position_inside_map(self, position: Tuple[int, int]) -> bool:
        (x, y) = position
        return x in range(self.columns) and y in range(self.rows)

    def random_map(self, fill: float = utils.MAP_RANDOM_FILL) -> 'Map':  # return type Map in order to be able to do map = Map().random_map()
        for i in range(self.rows):
            for j in range(self.columns):
                if random() <= fill:
                    self.surface[i][j] = self.Position.WALL
        return self

    def save_map(self, map_file_path: str = "test.map") -> None:
        try:
            with open(map_file_path, 'wb') as file:
                pickle.dump(self, file)
        except OSError as e:
            sys.stderr.write("[error][{}.{}()] {}".format(__class__, inspect.stack()[0].function, e))
            raise Exception("Failed to save map")

    def load_map(self, map_file_path: str = "test.map") -> 'Map':
        try:
            with open(map_file_path, 'rb') as file:
                loaded_map = pickle.load(file)
                self.rows = loaded_map.rows
                self.columns = loaded_map.columns
                self.surface = loaded_map.surface
            return self
        except OSError as e:
            sys.stderr.write("[error][{}.{}()] {}".format(__class__, inspect.stack()[0].function, e))
            raise Exception("Failed to load map")

    def generate_random_position(self) -> Tuple[int, int]:
        return randint(0, self.columns), randint(0, self.rows)

    def generate_random_position_of_type(self, position_type: Position) -> Tuple[int, int]:
        """
        Generates a random position of a given type
        :param position_type:
        :return: the generated random position as a tuple <br>
                 (width, height) if no such position was found
        """
        tried_positions: Dict[Tuple[int, int], bool] = {}  # static typing

        while len(tried_positions) < self.columns * self.rows:
            random_position = self.generate_random_position()
            if self.at(random_position) == position_type:
                return random_position
            tried_positions[random_position] = True

        return self.columns, self.rows

    def __str__(self) -> str:
        string = ""
        for i in range(self.rows):
            for j in range(self.columns):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def to_table(self) -> str:
        # searched and replaced "([^_])(columns|rows|surface)" with "$1self.$2"
        table = Texttable()  # texttable
        table.set_cols_align(['c' for _ in range(0, self.columns + 1)])
        table.set_cols_width([5 for _ in range(0, self.columns + 1)])
        table.add_rows([[""] + [str(_) for _ in range(0, self.columns)]] + [[str(row)] + [str(self.surface[row][column]) for column in range(0, self.columns)] for row in range(0, self.rows)])
        return table.draw()

