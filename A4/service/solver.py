import inspect
import sys
from typing import Optional, List, Tuple, Union

from domain import constants
from domain.constants import MIN_NUMBER_OF_SENSORS
from domain.drone import Drone
from domain.environment import Environment
from domain.map import Map
from domain.position import Position


class Solver:
    def __init__(self):
        self.__environment: Optional[Environment] = None

    def set_up_environment_from_file(self, environment_filepath: str):
        """ file format: EOF
        1: <drone x> <drone y>
        2: <drone energy>
        3: <map file path>/<<map # of rows> <map # of columns>>
        4: <x of first sensor> <y of first sensor>
        5: <x of second sensor> <y of second sensor>
        ...
        n: <x of last sensor> <y of last sensor>
        EOF

        NOTE: number of lines -n- must be >= 3 + MIN_NUMBER_OF_SENSORS
        """
        minimum_number_of_lines: int = 3 + MIN_NUMBER_OF_SENSORS

        try:
            with open(environment_filepath, "r") as input_file:
                lines: List[str] = list(input_file)
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to load map: {}\n".format(__class__, inspect.stack()[0].function, e))

        if len(lines) < minimum_number_of_lines:
            raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                      inspect.stack()[
                                                                                          0].function,
                                                                                      "Expected # of lines >= {}"
                                                                                      ". Got: {}.".format(
                                                                                          minimum_number_of_lines,
                                                                                          len(lines))))

        drone_coordinates: List[str] = lines[0].strip().split(" ", 2)
        if drone_coordinates.__len__() != 2:
            raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                      inspect.stack()[
                                                                                          0].function,
                                                                                      "[line 1] Could not split "
                                                                                      "stripped drone coordinates line:"
                                                                                      " ->{}<- by \' \' in 2."
                                                                                      .format(lines[0].strip())))
        coordinate_type: str = "x"
        coordinate_value: str = drone_coordinates[0]
        try:
            drone_x: int = int(coordinate_value)

            coordinate_type = "y"
            coordinate_value: str = drone_coordinates[1]
            drone_y: int = int(coordinate_value)
        except ValueError as e:
            raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                      inspect.stack()[
                                                                                          0].function,
                                                                                      "[line 1] Drone's " +
                                                                                      coordinate_type + " coordinate: "
                                                                                      + coordinate_value
                                                                                      + " is NOT convertible to int."))
        try:
            drone_energy: int = int(lines[1].strip())
        except ValueError:
            raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                      inspect.stack()[
                                                                                          0].function,
                                                                                      "[line 2] Drone's energy: {}"
                                                                                      "is NOT convertible to int.".
                                                                                      format(lines[1].strip())))
        map_filepath_or_dimensions: Union[str, Tuple[int, int]] = lines[2]

        sensors_coordinates: List[Tuple[int, int]] = []
        for index, sensor_position_line in enumerate(lines[3:]):
            sensor_coordinates: List[str] = sensor_position_line.strip().split(" ", 2)

            if sensor_coordinates.__len__() != 2:
                sys.stderr.write("[warn][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                         inspect.stack()[
                                                                                             0].function,
                                                                                         "[line {}] Could not split "
                                                                                         "stripped sensor coordinates "
                                                                                         "line ->{}<- by  \' \' in 2."
                                                                                         .format(index + 4,
                                                                                                 sensor_position_line
                                                                                                 .strip())))
                continue

            coordinate_type: str = "x"
            coordinate_value: str = sensor_coordinates[0]
            try:
                sensor_x: int = int(coordinate_value)
    
                coordinate_type = "y"
                coordinate_value: str = sensor_coordinates[1]
                sensor_y: int = int(coordinate_value)
            except ValueError as e:
                sys.stderr.write("[warn][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                         inspect.stack()[
                                                                                             0].function,
                                                                                         "[line {}] Sensor's " + 
                                                                                         coordinate_type + 
                                                                                         " coordinate: " + 
                                                                                         coordinate_value +
                                                                                         " coordinate is NOT "
                                                                                         "convertible to int."
                                                                                         .format(index + 4)))
                continue

            sensors_coordinates.append((sensor_x, sensor_y))

        self.set_up_environment(drone_x, drone_y, drone_energy, sensors_coordinates, map_filepath_or_dimensions)

    def set_up_environment(self, drone_x: int,
                           drone_y: int,
                           drone_energy: int,
                           sensors_coordinates: List[Tuple[int, int]],
                           map_filepath_or_dimensions: Union[str, Tuple[int, int]]) -> None:
        map_: Map
        if isinstance(map_filepath_or_dimensions, str):
            map_ = Map().load_map(map_filepath_or_dimensions)  # TODO catch exceptions in UI
        else:
            rows, columns = map_filepath_or_dimensions
            map_ = Map(rows, columns).randomize()  # TODO catch exception in UI

        drone_position: Position = Position(drone_x, drone_y)
        if not map_.is_position_inside_map(drone_position):
            raise IndexError("[error][{}.{}()] Failed to set up environment: {}\n".format(__class__,
                                                                                          inspect.stack()[0].function,
                                                                                          "Drone position must be in "
                                                                                          "map range."))
        drone: Drone = Drone(drone_position, drone_energy)

        map_.add_sensors([Position(x, y) for x, y in sensors_coordinates])
        number_of_added_sensors: int = map_.get_number_of_sensors()
        if number_of_added_sensors < MIN_NUMBER_OF_SENSORS:
            raise ValueError("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, "Expected # of "
                                                                                                    "successfully "
                                                                                                    "added sensors = "
                                                                                                    "{}. Got {}."
                                                            .format(
                MIN_NUMBER_OF_SENSORS, number_of_added_sensors)))
        else:
            sys.stdout.write("[log][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, "Successfully added "
                                                                                                  "{} "
                                                                                                  "sensors.".format(
                number_of_added_sensors)))

        self.__environment: Environment = Environment(map_, drone)

    @staticmethod
    def get_best_solution(first: Optional[List[Position]], second: Optional[List[Position]]) -> Optional[List[Position]]:
        if first is None:
            return second
        if second is None:
            return first

        first_length: int = len(first)
        second_length: int = len(second)

        if first_length > second_length:
            return first
        elif first_length == second_length:
            return
        else:
            return second

    def run(self) -> Optional[List[Position]]:
        """
        runs the solver
        :return: atm, nothing
        :raise ValueError: if the environment is NOT set
        """
        if self.__environment is None:
            raise ValueError("[error][{}.{}()] Failed to run solver: {}\n".format(__class__,
                                                                                  inspect.stack()[0].function,
                                                                                  "Environment is NOT set."))
        best_solution: Optional[List[Position]] = None

        for epoch in range(constants.EPOCHS):
            current_solution = None
            best_solution = None # self.get_best_solution(current_solution, best_solution)
            pass  # TODO

        return best_solution  # energy_levels



