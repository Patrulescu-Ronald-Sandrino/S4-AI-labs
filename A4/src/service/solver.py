import time
from random import randint
from typing import Optional, Tuple, List, Dict

from src.domain.ant import Ant
from src.domain.drone import Drone
from src.domain.map import Map
from src.domain.problem_constants import *


class Solver:
    def __init__(self, map_instance: Map, drone: Drone):
        self.__map: Map = map_instance
        self.__drone: Drone = drone

        self.__sensors: List[Tuple[int, int]] = []
        self.__sensors_gains: Dict[Tuple[int, int], Dict[int, int]] = {}
        self.__minimum_distances_between_sensors: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {}
        self.__pheromone_matrix: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {}
        self.__minimum_distances_between_start_and_senors: Dict[Tuple[int, int], float] = {}

    def __prepare(self):
        # TODO IDEA: use a dictionary with None values instead of a list for better performance
        self.__sensors: List[Tuple[int, int]] = self.__map.find_cells(Map.Cell.SENSOR)
        Ant.sensors = self.__sensors

        # self.__pheromone_matrix: List[List[float]] = [[1.0 for _ in range(self.number_of_sensors)] for _ in range(self.number_of_sensors)]  # TODO: remove later
        self.__pheromone_matrix: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {
            row: {column: 1.0 for column in self.__sensors} for row in self.__sensors}
        Ant.pheromone_matrix = self.__pheromone_matrix

        # TODO IDEA: pass the sensors list to the methods from below (for performance increase)
        self.__sensors_gains: Dict[Tuple[int, int], Dict[int, int]] = self.__map.compute_sensors_gains(MAX_SENSOR_CAPACITY)

        self.__minimum_distances_between_sensors: Dict[
            Tuple[int, int], Dict[Tuple[int, int], float]] = self.__map.compute_minimum_distances_between_sensors()
        Ant.minimum_distances_between_sensors = self.__minimum_distances_between_sensors

        self.__minimum_distances_between_start_and_senors = {
            sensor: self.__map.compute_minimum_distance(self.__drone.position, sensor) for sensor in self.__sensors}
        Ant.minimum_distances_between_start_and_senors = self.__minimum_distances_between_start_and_senors

    @property
    def number_of_sensors(self) -> int:
        return len(self.__sensors)

    def epoch(self, number_of_ants: int, number_of_iterations: int) -> Optional[Ant]:
        ants: List[Ant] = [Ant(self.number_of_sensors, self.__drone) for _ in range(number_of_ants)]

        # move ants
        for _ in range(self.number_of_sensors):
            for ant in ants:
                ant.move()

        # simulate pheromone evaporation
        for row in self.__sensors:
            for column in self.__sensors:
                self.__pheromone_matrix[row][column] *= (1 - RHO)

        # update the trace with the pheromones left by the ants
        pheromones_unit_quantities = [1.0 / ant.fitness for ant in ants if
                                      ant.fitness != 0]  # TODO: deal with ant.fitness = 0 properly
        for ant in ants:
            ant_sensors = list(ant.path)
            for index in range(len(ant_sensors) - 1):
                current_sensor: Tuple[int, int] = ant_sensors[index]
                next_sensor: Tuple[int, int] = ant_sensors[index + 1]

                self.__pheromone_matrix[current_sensor][next_sensor] += pheromones_unit_quantities[index]

        # return max(ants, key=lambda a: a.fitness)
        return min(ants, key=lambda a: a.fitness)

    def run(self, number_of_epochs: int, number_of_ants: int, number_of_iterations: int) -> Tuple[Optional[Ant], float]:
        best_ant: Optional[Ant] = None

        self.__prepare()
        start_time: float = time.time()
        for epoch_number in range(1, number_of_epochs + 1):
            print(f'[epoch {epoch_number}/{number_of_epochs}] START ' + '-' * 30)  # TODO END remove

            epoch_best_ant = self.epoch(number_of_ants, number_of_iterations)
            best_ant = Ant.get_best(best_ant, epoch_best_ant)

            # if best_ant is not None:  # TODO END remove
            #     if best_ant.path != epoch_best_ant.path or id(best_ant) != id(epoch_best_ant):
            #         print(f'RAISED to fitness: {best_ant.fitness} path: {best_ant.path}')
            #     else:
            #         print(f'fitness: {best_ant.fitness} path: {best_ant.path}')
            # else:
            #     print(f'best_ant: None')

            print(f'[epoch {epoch_number}/{number_of_epochs}] END ' + '-' * 30)  # TODO END remove
            print()
        end_time: float = time.time()

        return Ant.add_energy_levels(best_ant, self.__sensors_gains), end_time - start_time


class SolverTools:
    @staticmethod
    def place_drone_on_empty_cell(map_instance: Map, drone: Drone) -> None:
        if map_instance.value_at(drone.position) == Map.Cell.EMPTY:
            raise Exception("Drone already on an empty cell!")

        empty_cells: List[Tuple[int, int]] = map_instance.find_cells(Map.Cell.EMPTY)
        if len(empty_cells) == 0:
            raise Exception("No empty cells were found to place the drone!")

        drone.position = empty_cells[randint(0, len(empty_cells) - 1)]
