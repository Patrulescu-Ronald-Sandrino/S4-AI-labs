from __future__ import annotations

import copy
import inspect
from enum import IntEnum
from typing import Dict, List


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
    def __create(surface: Dict[int, Dict[int, Map.Cell]]) -> Map:
        Map._Map__can_create = True
        map_instance: Map = Map(surface)
        Map._Map__can_create = False

        return map_instance

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

                return MapFactory.__create(surface)
        except Exception as e:
            raise Exception(f'[error][{__class__}.{inspect.stack()[0].function}()] Failed to load map from file: {filename}. Reason: {e}')
