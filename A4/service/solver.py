import time
from random import randint
from typing import List, Optional, Tuple, Dict

import tools.collections
from tools.general import function_name
from domain.ant import Ant
from domain.drone import Drone
from domain.map import Map, Direction, DIRECTION_DELTA
from domain.problem_constants import ITERATIONS, MAX_SENSOR_CAPACITY, RHO


class Solver:
    def __init__(self, map_: Map, drone: Drone):
        self.__map: Map = map_
        self.__drone: Drone = drone
        self.__pheromone_matrix: List[List[Dict[Direction, List[float]]]] = []

    def prepare(self):
        print("before create_pheromone_matrix()")
        self.__pheromone_matrix = self.__map.create_pheromone_matrix()
        print("after create_pheromone_matrix()")

        # make sure the drone is on a free cell
        if self.__map.surface[self.__drone.row][self.__drone.column] != Map.CellType.EMPTY:
            print("before find_all()")
            empty_positions: List[Tuple[int, int]] = self.__map.find_all(Map.CellType.EMPTY)
            print("after find_all()")
            number_of_empty_positions: int = len(empty_positions)
            if number_of_empty_positions == 0:
                raise Exception(f'[{self.__class__.__name__}.{function_name()}()] Could not find an empty cell to place the drone. Try changing some values')

            self.__drone.row, self.__drone.column = empty_positions[randint(0, number_of_empty_positions - 1)]

    def __update_pheromone_matrix(self) -> None:
        initial_pheromone_matrix:  List[List[Dict[Direction, List[float]]]] = self.__map.create_pheromone_matrix()
        for row in range(self.__map.rows):
            for column in range(self.__map.columns):
                for direction in Direction:
                    for energy_level in range(MAX_SENSOR_CAPACITY + 1):
                        tau: float = self.__pheromone_matrix[row][column][direction][energy_level]
                        tau_initial: float = initial_pheromone_matrix[row][column][direction][energy_level]

                        self.__pheromone_matrix[row][column][direction][energy_level] = (1 - RHO) * tau + RHO * tau_initial

    def __move_ants(self, ants_population: List[Ant]) -> List[Ant]:
        moved_ants: List[Ant] = []

        for ant in ants_population:
            if ant.move(self.__pheromone_matrix):
                moved_ants.append(ant)

        return moved_ants
        # return ants_population

    def epoch(self, number_of_ants: int) -> Optional[Ant]:
        moved_ants: List[Ant] = [Ant(self.__drone, self.__map) for _ in range(number_of_ants)]

        print(f"[epoch()] START # of ants: {number_of_ants}")
        for _ in range(ITERATIONS):
            moved_ants = self.__move_ants(moved_ants)
            # print(f"[debug] moved ants, left: {len(moved_ants)}")  # TODO [END] remove this
            # print("ants")
            # for index, ant in enumerate(moved_ants):
            #     print(f'ant {index}: {ant.path}')

        print(f"[debug] len(moved_ants) after {ITERATIONS} iterations: {len(moved_ants)}")
        if len(moved_ants) == 0:
            return None

        self.__update_pheromone_matrix()
        # print(f"[debug] updated pheromone matrix")

        # compute best ant
        best_ant: Ant = max(moved_ants, key=lambda ant: ant.fitness)
        # print(f"[debug] computed best ant: {best_ant.path}")

        # update the pheromone matrix based on the best ant
        for ant in moved_ants:
            for index in range(len(ant.path) - 1):
                (current_row, current_column), _ = list(ant.path.items())[index]
                (next_row, next_column), next_energy = list(ant.path.items())[index + 1]
                direction: Direction = tools.collections.dictionary_key_from_value(DIRECTION_DELTA, (next_column - current_column, next_row - current_row))

                self.__pheromone_matrix[current_row][current_column][direction][next_energy] += (ant.fitness + 1) / (
                            best_ant.fitness + 1)
        # print(f"[debug] updated the pheromone matrix based on the best ant")
        return best_ant

    def run(self, number_of_ants: int, number_of_epochs: int) -> Tuple[Optional[Ant], float]:
        overall_best_ant: Optional[Ant] = None

        print("before prepare()")
        self.prepare()
        print("after prepare()")

        start_time: float = time.time()
        print(f'Drone: {self.__drone.position}')  # TODO [END] remove this
        for epoch in range(number_of_epochs):
            print(f"EPOCH {epoch}")  # TODO [END] remove this

            best_ant_of_epoch: Ant = self.epoch(number_of_ants)

            overall_best_ant = self.compare_ants_and_get_best_one(overall_best_ant, best_ant_of_epoch)
            if overall_best_ant == best_ant_of_epoch:
                if overall_best_ant is None:
                    print("[Solver.run()] overall_best_ant is None")
                else:
                    print(f"[Solver.run()] overall_best_ant == best_ant_of_epoch; fitness: {overall_best_ant.fitness} path: {overall_best_ant.path}")

        end_time: float = time.time()

        return overall_best_ant, end_time - start_time

    @staticmethod
    def compare_ants_and_get_best_one(first: Optional[Ant], second: Optional[Ant]) -> Optional[Ant]:
        if first is None:
            return second

        if second is None:
            return first

        if second.fitness > first.fitness:
            return second
        elif second.fitness == first.fitness:
            return second if len(second.path) < len(first.path) else first
        else:
            return first
