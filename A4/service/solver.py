import inspect
from typing import Optional, List, Tuple, Union

from domain.drone import Drone
from domain.environment import Environment
from domain.map import Map
from domain.position import Position


class Solver:
    def __init__(self):
        self.__environment: Optional[Environment] = None

    def read_environment_from_file(self, environment_filepath: str):
        """ file format
        1: <drone x> <drone y>
        2: <drone energy>
        3: <map file path>/<<map # of rows> <map # of columns>>
        4: <x of first sensor> <y of first sensor>
        5: <x of second sensor> <y of second sensor>
        ...
        n: <x of last sensor> <y of last sensor> # n must be >= 5
        """
        try:
            with open(environment_filepath, "r") as input_file:
                first_line: str = input_file.readline()
                drone_coordinates: List[str] = first_line.strip().split(" ", 2)
                if drone_coordinates.__len__() != 2:
                    raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                              inspect.stack()[
                                                                                                  0].function,
                                                                                              "Could not split the "
                                                                                              "1st line by \' \' "
                                                                                              "in two splits"))
                try:
                    coordinate: str = "x"
                    drone_x = int(drone_coordinates[0])
                    coordinate = "y"
                    drone_y = int(drone_coordinates[1])
                except ValueError as e:
                    raise ValueError("[error][{}.{}()] Failed to parse env file: {}\n".format(__class__,
                                                                                              inspect.stack()[
                                                                                                  0].function,
                                                                                              "Drone's " + coordinate +
                                                                                              " coordinate is NOT "
                                                                                              "convertible to int"))
                second_line: str = input_file.readline()


                [drone_x, drone_y] = map(lambda value: int(value), first_line.strip().split(" ", 2))
        except OSError as e:
            raise IOError("[error][{}.{}()] Failed to load map: {}\n".format(__class__, inspect.stack()[0].function, e))

    def set_up_environment(self, drone_x: int,
                           drone_y: int,
                           drone_energy: int,
                           sensors_positions_tuples: List[Tuple[int, int]],
                           map_filepath_or_dimensions: Union[str, Tuple[int, int]]) -> None:
        map_: Map
        if isinstance(map_filepath_or_dimensions, str):
            map_ = Map().load_map(map_filepath_or_dimensions)  # TODO catch exceptions in UI
        else:
            rows, columns = map_filepath_or_dimensions
            map_ = Map(rows, columns).randomize()  # TODO catch exception in UI

        drone_position: Position = Position(drone_x, drone_y)
        if not map_.is_position_valid(drone_position):
            raise IndexError("[error][{}.{}()] Failed to set up environment: {}\n".format(__class__,
                                                                                          inspect.stack()[0].function,
                                                                                          "Drone position must be in "
                                                                                          "map range"))
        drone: Drone = Drone(drone_position, drone_energy)

        map_.add_sensors([Position(x, y) for x, y in sensors_positions_tuples])

        self.__environment: Environment = Environment(map_, drone)

    def run(self):
        """
        runs the solver
        :return: atm, nothing
        :raise ValueError: if the environment is NOT set
        """
        if self.__environment is None:
            raise ValueError("[error][{}.{}()] Failed to run solver: {}\n".format(__class__,
                                                                                  inspect.stack()[0].function,
                                                                                  "Environment is NOT set"))
        pass  # TODO
