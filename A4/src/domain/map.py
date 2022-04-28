from __future__ import annotations

import copy
import inspect
import sys
from enum import IntEnum
from queue import Queue
from typing import Dict, List, Optional, Callable, Tuple, Set

import texttable as texttable

import tools.collections
from tools.collections import create_dictionary_matrix


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTIONS: Dict[Direction, Tuple[int, int]] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


class Map:
    __can_create: bool = False

    class Cell(IntEnum):
        EMPTY = 0
        WALL = 1
        SENSOR = 2

        def __str__(self) -> str:
            return str(self.value)

    def __init__(self, surface: Dict[int, Dict[int, Map.Cell]]):
        if Map.__can_create:
            self.__surface: Dict[int, Dict[int, Map.Cell]] = surface
        else:
            raise NotImplementedError("Please use MapFactory to instantiate!")

    @staticmethod
    def __create(surface: Dict[int, Dict[int, Map.Cell]]) -> Map:
        Map._Map__can_create = True
        map_instance: Map = Map(surface)
        Map._Map__can_create = False

        return map_instance

    @property
    def rows(self) -> int:
        return len(self.__surface)

    @property
    def columns(self) -> int:
        return len(next(iter(self.__surface.values()))) if self.rows > 0 else 0

    @property
    def surface(self) -> Dict[int, Dict[int, Map.Cell]]:
        return copy.deepcopy(self.__surface)

    def __str__(self) -> str:
        matrix_str: str = ""

        for row in range(self.rows):
            row_str: str = ""

            for column in range(self.columns):
                row_str += '' if row_str == '' else ' '  # add spaces between them, excepting for the first value in the column
                row_str += f'{self.surface[row][column]}'

            matrix_str += f'{row_str}\n'

        return matrix_str
        # return "".join([functools.reduce(lambda x, y: f'{x} {y}', map(lambda cell: str(cell), row.values())) + '\n' for row in self.surface.values()])

    def to_texttable(self, column_width: int = 3) -> str:
        table: texttable.Texttable = texttable.Texttable()

        table.set_cols_align(['c' for _ in range(self.columns + 1)])
        table.set_cols_width([column_width for _ in range(self.columns + 1)])
        table.add_row([""] + [str(column_index) for column_index in range(self.columns)])
        for row_index, row in self.surface.items():
            table.add_row([row_index] + [int(cell) for cell in row.values()])

        return table.draw()

    def is_in_map(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.columns

    def find_cells(self, cell: Map.Cell) -> List[Tuple[int, int]]:
        # return [(row, column) for row in self.surface.keys() for column in self.surface[row] if self.surface[row][column] == cell]
        return [(row, column) for row in range(self.rows) for column in range(self.columns) if self.surface[row][column] == cell]

    def is_not_wall(self, row: int, column: int) -> bool:
        return self.surface[row][column] != Map.Cell.WALL

    def compute_sensor_gains(self, row: int, column: int, last_energy_level: int = -1) -> Dict[int, int]:
        gains: Dict[int, int] = {0: 0}
        if last_energy_level == 0:
            return gains

        for direction in Direction:
            energy: int = 1
            current_row, current_column = Map.shift((row, column), direction)

            # compute individual gain for each energy
            while self.is_in_map(current_row, current_column) and self.is_not_wall(current_row, current_column):
                gains[energy] = gains[energy] + 1 if gains.__contains__(energy) else 1
                if energy == last_energy_level > 0:
                    break

                energy += 1
                current_row, current_column = Map.shift((current_row, current_column), direction)
                
        # add to each energy level the gain from the previous one
        for energy in range(2, len(gains)):
            gains[energy] += gains[energy - 1]

        return gains

    def compute_sensors_gains(self, last_energy_level: int = -1) -> Dict[Tuple[int, int], Dict[int, int]]:
        return {position: self.compute_sensor_gains(*position, last_energy_level) for position in self.find_cells(Map.Cell.SENSOR)}

    @staticmethod
    def shift(position: Tuple[int, int], direction: Direction, steps: int = 1) -> Tuple[int, int]:
        row, column = position
        delta_row, delta_column = DIRECTIONS[direction]

        return row + delta_row * steps, column + delta_column * steps

    def compute_minimum_distance(self, source: Tuple[int, int], destination: Tuple[int, int]) -> float:
        # V = rows * columns
        # E = rows * (columns - 1) + (rows - 1) * columns = V^2 - rows - columns
        queue: Queue = Queue()
        visited: Set[Tuple[int, int]] = set()
        distances: Dict[Tuple[int, int], float] = {(row, column): float('inf') for row in range(self.rows) for column in range(self.columns)}

        visited.add(source)
        distances[source] = 0
        queue.put(source)

        while queue.not_empty:
            current: Tuple[int, int] = queue.get()

            for neighbour in (Map.shift(current, direction) for direction in Direction):
                if not self.is_in_map(*neighbour) or neighbour in visited:
                    continue

                visited.add(neighbour)
                distances[neighbour] = distances[current] + 1
                queue.put(neighbour)

                if neighbour == destination:
                    return distances[neighbour]

        return float('inf')

    def compute_minimum_distances_between_sensors(self) -> Dict[Tuple[int, int], Dict[Tuple[int, int], float]]:
        sensors: List[Tuple[int, int]] = self.find_cells(Map.Cell.SENSOR)
        return {sensor1: {sensor2: self.compute_minimum_distance(sensor1, sensor2) for sensor2 in sensors} for sensor1 in sensors}


class MapWriter:
    @staticmethod
    def to_text_file(map_instance: Map, filename: str) -> None:
        try:
            with open(filename, 'w') as file:
                file.write(map_instance.__str__())
        except Exception as e:
            raise Exception(f'[error][{__class__}.{inspect.stack()[0].function}()] Failed to save map to file: {filename}. Reason: {e}')


class MapFactory:

    @staticmethod
    def __parse_text_file_content(lines_list: List[str]) -> Dict[int, Dict[int, Map.Cell]]:
        surface: Dict[int, Dict[int, Map.Cell]] = {}

        for row_index, line in enumerate(lines_list):
            row = {column_index: Map.Cell(int(cell_value)) for column_index, cell_value in enumerate(line.strip().split(' '))}
            
            # test for same number of columns
            if row_index > 0 and len(row) != len(surface[row_index - 1]):
                raise ValueError(f'Row {row_index + 1} has {len(row)} columns. Expected: {len(surface[row_index - 1])}')
            surface[row_index] = row

        return surface

    @staticmethod
    def from_text_file(filename: str) -> Map:
        try:
            with open(filename, 'r') as file:
                lines_list: List[str] = file.readlines()
                surface: Dict[int, Dict[int, Map.Cell]] = MapFactory.__parse_text_file_content(lines_list)

                return Map._Map__create(surface)
        except Exception as e:
            raise Exception(f'[error][{__class__}.{inspect.stack()[0].function}()] Failed to load map from file: {filename}. Reason: {e}')


class MapBuilder:
    def __init__(self):
        self.__map_instance: Optional[Map] = None

    def get(self) -> Map:
        return self.__map_instance

    def from_predicate(self, predicate: Callable[[int, int], Map.Cell], rows: int, columns: int) -> MapBuilder:
        self.__map_instance = Map._Map__create(create_dictionary_matrix(predicate, rows, columns))
        return self
