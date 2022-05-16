from __future__ import annotations

import copy
import random
from typing import Optional, Tuple, Dict, List, Callable, Set

from src.domain.drone import Drone
from src.domain.problem_constants import *
from src.tools.collections import last_key, last_value
from src.tools.constants import INFINITY


class Ant:
    __pheromone_matrix: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {}
    __sensors: List[Tuple[int, int]] = []
    __minimum_distances_between_sensors: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {}
    __minimum_distances_between_start_and_senors: Dict[Tuple[int, int], float] = {}

    @property
    def pheromone_matrix(self) -> Dict[Tuple[int, int], Dict[Tuple[int, int], float]]:
        return self.__pheromone_matrix

    @pheromone_matrix.setter
    def pheromone_matrix(self, pheromone_matrix: Dict[Tuple[int, int], Dict[Tuple[int, int], float]]) -> None:
        self.__pheromone_matrix = pheromone_matrix

    @property
    def sensors(self) -> List[Tuple[int, int]]:
        return self.__sensors

    @sensors.setter
    def sensors(self, sensors: List[Tuple[int, int]]) -> None:
        self.__sensors = sensors

    @property
    def minimum_distances_between_sensors(self) -> Dict[Tuple[int, int], Dict[Tuple[int, int], float]]:
        return self.__minimum_distances_between_sensors

    @minimum_distances_between_sensors.setter
    def minimum_distances_between_sensors(self, minimum_distances_between_sensors: Dict[Tuple[int, int], Dict[Tuple[int, int], float]]):
        self.__minimum_distances_between_sensors = minimum_distances_between_sensors

    @property
    def minimum_distances_between_start_and_senors(self) -> Dict[Tuple[int, int], float]:
        return self.__minimum_distances_between_start_and_senors

    @minimum_distances_between_start_and_senors.setter
    def minimum_distances_between_start_and_senors(self, minimum_distances_between_start_and_senors: Dict[Tuple[int, int], float]):
        self.__minimum_distances_between_start_and_senors = minimum_distances_between_start_and_senors

    def __init__(self, size: int, drone: Drone):
        self.__size: int = size
        self.__path: Dict[Tuple[int, int]] = {}
        self.__fitness: int = 0

        self.__start: Tuple[int, int] = drone.position
        self.__battery: int = drone.energy

        self.__coverage: int = -1

    @property
    def coverage(self) -> int:
        return self.__coverage

    @property
    def path(self) -> Dict[Tuple[int, int]]:
        return self.__path

    @property
    def fitness(self) -> int:
        return self.__fitness

    @property
    def battery(self) -> int:
        return self.__battery

    @property
    def __last_sensor(self) -> Tuple[int, int]:
        """
        throws an exception if the path is empty
        :return:
        """
        return last_key(self.path)

    def distance_from_last_sensor(self, sensor: Tuple[int, int]) -> float:
        if len(self.path) == 0:
            return self.minimum_distances_between_start_and_senors[sensor]
        return self.minimum_distances_between_sensors[self.__last_sensor][sensor]

    def __compute_next_sensors(self) -> Dict[Tuple[int, int]]:  # List[index] vs Dict[position] vs List[position] ?
        potential_next_sensors: Dict[Tuple[int, int]] = {}

        for sensor_index, sensor in enumerate(self.sensors):
            if sensor in self.__path or self.distance_from_last_sensor(sensor) == INFINITY:
                continue
            potential_next_sensors[sensor] = None
        return potential_next_sensors

    def __compute_sensors_probabilities(self, sensors: Dict[Tuple[int, int]]) -> Dict[Tuple[int, int], float]:
        # probabilities: Dict[Tuple[int, int], float] = {}
        #
        # for sensor in sensors:
        #     probabilities[sensor] = self.__compute_sensor_probability(sensor)
        #
        # return probabilities
        return {sensor: self.__compute_sensor_probability(sensor) for sensor in sensors}

    def __trace_from_last_sensor(self, sensor: Tuple[int, int]) -> float:
        if len(self.path) == 0:
            return 1.0
        return self.pheromone_matrix[self.__last_sensor][sensor]

    def __compute_sensor_probability(self, sensor: Tuple[int, int]) -> float:
        distance_from_last_sensor: float = self.distance_from_last_sensor(sensor)
        trace_from_last_sensor: float = self.__trace_from_last_sensor(sensor)

        return (distance_from_last_sensor ** BETA) * (trace_from_last_sensor ** ALPHA)
        # return (trace_from_last_sensor ** ALPHA)
        # return (distance_from_last_sensor ** BETA)

    def move(self) -> bool:
        next_sensors: Dict[Tuple[int, int]] = self.__compute_next_sensors()

        if len(next_sensors) == 0:
            return False

        # compute probabilities
        sensors_probabilities: Dict[Tuple[int, int], float] = self.__compute_sensors_probabilities(next_sensors)

        # select the next sensor and add it
        next_sensor: Tuple[int, int] = Ant.select_next_sensor(sensors_probabilities)
        self.__add_next_sensor(next_sensor)
        return True

    def __add_next_sensor(self, next_sensor: Tuple[int, int]):
        self.__battery -= self.distance_from_last_sensor(next_sensor)
        self.__fitness += self.distance_from_last_sensor(next_sensor)
        self.__path[next_sensor] = None

    @staticmethod
    def select_next_sensor(sensors_probabilities: Dict[Tuple[int, int], float]) -> Tuple[int, int]:
        if random.random() < Q0:
            return max(sensors_probabilities, key=lambda sensor: sensors_probabilities.get(sensor))  # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        return Ant.__roulette_sensor(sensors_probabilities)

    @staticmethod
    def __roulette_sensor(sensors_probabilities: Dict[Tuple[int, int], float]) -> Tuple[int, int]:
        probabilities_sum: float = sum(sensors_probabilities.values())

        if probabilities_sum == 0:
            return random.choice(list(sensors_probabilities.keys()))  # https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary

        sensors_probabilities_cdf: Dict[Tuple[int, int], float] = Ant.__compute_cdf(sensors_probabilities)

        random_value: float = random.random()
        for sensor, sensor_cdf_value in sensors_probabilities_cdf.items():
            if random_value <= sensor_cdf_value:
                return sensor
        return random.choice(list(sensors_probabilities.keys()))

    @staticmethod
    def __compute_cdf(sensors_probabilities: Dict[Tuple[int, int], float]) -> Dict[Tuple[int, int], float]:
        cdf: Dict[Tuple[int, int], float] = {}
        probabilities_sum: float = sum(sensors_probabilities.values())

        for index, sensor in enumerate(sensors_probabilities):
            if index == 0:
                cdf[sensor] = sensors_probabilities[sensor] / probabilities_sum
                continue
            cdf[sensor] = cdf[last_key(cdf)] + sensors_probabilities[sensor] / probabilities_sum

        return cdf

    @staticmethod
    def add_energy_levels(ant: Ant, sensors_gains: Dict[Tuple[int, int], Dict[int, int]]) -> Ant:
        new_ant: Ant = copy.deepcopy(ant)

        new_ant.__coverage = 0
        for sensor in new_ant.__path:
            new_ant.__path[sensor] = 0

        if new_ant.__battery <= 0:
            return new_ant

        sensors_sorted_by_gain = sorted(new_ant.__path.keys(),
                                        key=lambda s: last_value(sensors_gains[s]) / last_key(sensors_gains[s]))

        for sensor in sensors_sorted_by_gain:
            if new_ant.battery <= 0:
                break

            sensor_max_energy = last_key(sensors_gains[sensor])
            if new_ant.__battery > sensor_max_energy:
                new_ant.__path[sensor] = sensor_max_energy
                new_ant.__battery -= sensor_max_energy
            else:
                new_ant.__path[sensor] = new_ant.__battery
                new_ant.__battery -= 0

            new_ant.__coverage += last_value(sensors_gains[sensor])

        return new_ant

    @staticmethod
    def get_best(first: Optional[Ant], second: Optional[Ant]) -> Optional[Ant]:
        if first is None:
            return second
        if second is None:
            return first
        if len(first.path) > len(second.path):  # TODO: IDEA: compare them on -coverage- instead
            return first
        elif first.fitness == second.fitness:
            return first if first.fitness < second.fitness else second
        else:
            return second
