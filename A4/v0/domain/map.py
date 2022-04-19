import inspect
import pickle
import random
import sys
from typing import List

import numpy as np
import texttable

from tools.math import out_of_range
from v0.domain.constants import MapPosition, MAP_FILL, MAP_ROWS, MAP_COLUMNS, MAP_FILEPATH, MAX_SENSOR_ENERGY, \
    Direction, \
    MIN_SENSOR_ENERGY
from v0.domain.position import Position


class Map:
    def __init__(self, rows: int = MAP_ROWS, columns: int = MAP_COLUMNS) -> None:
        if rows < 0:
            raise ValueError("[error][{}.{}()] Failed to create map: {}\n".format(__class__,
                                                                                  inspect.stack()[0].function,
                                                                                  "No. of rows must be >= 0"))
        if columns < 0:
            raise ValueError("[error][{}.{}()] Failed to create map: {}\n".format(__class__,
                                                                                  inspect.stack()[0].function,
                                                                                  "No. of columns must be >= 0"))
        self.__rows: int = rows
        self.__columns: int = columns
        self.__surface = np.zeros((self.__rows, self.__columns))
        self.__sensors = {}  # type Dict[Position, List[int]]  # if a value in the list is -1 => it's not computed.
        # Has length == 1 + MAX_SENSOR_ENERGY

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def columns(self) -> int:
        return self.__columns

    def is_position_inside_map(self, position: Position) -> bool:
        """
        NOTE: use together with raise IndexError
        :param position:
        :return:
        """
        return position.x < self.__columns and position.y < self.__rows

    def at(self, position: Position) -> MapPosition:
        if not self.is_position_inside_map(position):
            raise IndexError("[error][{}.{}()] Failed to access map position: {}\n".format(__class__,
                                                                                           inspect.stack()[0].function,
                                                                                           "Position not in map range"))
        return self.__surface[position.x][position.y]

    def get_number_of_sensors(self) -> int:
        return len(self.__sensors)

    def add_sensors(self, sensors_positions: List[Position]) -> None:
        """
        adds sensors that are in map range, do not exist already and do not overlap a wall.
        also computes the max # of squares that can be seen in any direction
        """
        for index, (sensor_x, sensor_y) in enumerate(sensors_positions):
            sensor_position: Position = Position(sensor_x, sensor_y)

            if self.is_position_inside_map(sensor_position):
                # if self.at(sensor_position) == MapPosition.SENSOR: # or this
                if sensor_position in self.__sensors:
                    sys.stderr.write("[warn][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function,
                                                                   "Position: " + str((sensor_x, sensor_y)) +
                                                                   " at index: " + index + " is skipped: it is already "
                                                                                           "a sensor."))

                elif self.at(sensor_position) == MapPosition.WALL:
                    sys.stderr.write("[warn][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function,
                                                                   "Position: " + str((sensor_x, sensor_y)) +
                                                                   " at index: " + index + " is skipped: it is a wall.")
                                     )

                else:
                    self.__sensors[sensor_position] = self.compute_sensor_gains(sensor_position)
                    self.__surface[sensor_x][sensor_y] = MapPosition.SENSOR
            else:
                sys.stderr.write("[warn][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function,
                                                               "Position: " + str((sensor_x, sensor_y)) + " at index: "
                                                               + index + " is skipped: invalid position."))

    def compute_sensor_gains(self, sensor_position: Position, last_energy_level: int = MAX_SENSOR_ENERGY) -> List[int]:
        if out_of_range(last_energy_level, MIN_SENSOR_ENERGY, MAX_SENSOR_ENERGY):
            raise ValueError("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, "Invalid value "
                                                                                                    "for last energy "
                                                                                                    "level: must be "
                                                                                                    "in range [{}, "
                                                                                                    "{}]."
                                                            .format(MIN_SENSOR_ENERGY, MAX_SENSOR_ENERGY)))

        ### V1
        # gain: List[int] = [0]
        # for energy in range(1, last_energy_level + 1):
        #     squares_seen: int = gain[-1]
        #
        #     for direction in Direction:
        #         potential_visible_position: Position = sensor_position.to(direction, energy)
        #
        #         if not self.is_position_inside_map(potential_visible_position) \
        #                 or self.at(potential_visible_position) == MapPosition.WALL:
        #             continue
        #
        #         squares_seen += 1
        #
        #     gain.append(squares_seen)
        ### V2
        # gain: List[int] = [0] + [-1 for _ in range(MAX_SENSOR_ENERGY)]
        # for direction in Direction:
        #     for energy in range(1, last_energy_level + 1):
        #         if gain[energy] == -1:
        #             gain[energy] = gain[energy - 1]
        #
        #         potential_visible_position: Position = sensor_position.to(direction, energy)
        #         if not self.is_position_inside_map(potential_visible_position) \
        #                 or self.at(potential_visible_position) == MapPosition.WALL:
        #             break
        #
        #         gain[energy] += 1
        ### V3
        gain: List[int] = [0]
        for direction in Direction:
            for energy in range(1, last_energy_level + 1):
                if len(gain) == energy:
                    gain.append(gain[energy - 1])

                potential_visible_position: Position = sensor_position.to(direction, energy)
                if not self.is_position_inside_map(potential_visible_position) \
                        or self.at(potential_visible_position) == MapPosition.WALL:
                    break

                gain[energy] += 1
        ###

        return gain + [-1 for _ in range(MAX_SENSOR_ENERGY - last_energy_level)]  # (1 + l) + ? = 1 + M => ? = M - l

    def randomize(self, fill: float = MAP_FILL) -> 'Map':
        for row in range(self.__rows):
            for column in range(self.__columns):
                if random.random() <= fill:
                    self.__surface[row][column] = MapPosition.WALL
        return self

    def save_map(self, map_filepath: str = MAP_FILEPATH) -> None:
        try:
            with open(map_filepath, "wb") as output_file:
                pickle.dump(self, output_file)
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to save map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def load_map(self, map_filepath: str = MAP_FILEPATH) -> 'Map':
        try:
            with open(map_filepath, "rb") as input_file:
                loaded_map: 'Map' = pickle.load(input_file)
                self.__rows = loaded_map.__rows
                self.__columns = loaded_map.__columns
                self.__surface = loaded_map.__surface
                self.__sensors = loaded_map.__sensors
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
                string = string + str(int(self.__surface[row][column])) + " "
            string = string + "\n"
        return string
