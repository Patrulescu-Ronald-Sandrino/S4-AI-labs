import time
from random import randint
from typing import List, Optional, Tuple, Dict

import tools.collections
from tools.general import function_name
from v1.domain.ant import Ant
from v1.domain.drone import Drone
from v1.domain.map import Map, Direction


class Solver:
    def __init__(self, map_: Map, drone: Drone):
        self.__map: Map = map_
        self.__drone: Drone = drone
        self.__pheromone_matrix: List[List[Dict[Direction, List[float]]]] = []

    def prepare(self):
        self.__pheromone_matrix = self.__map.create_pheromone_matrix()

        # make sure the drone is on a free cell
        if self.__map.surface[self.__drone.row][self.__drone.column] != Map.CellType.EMPTY:
            empty_positions: List[Tuple[int, int]] = self.__map.find_all(Map.CellType.EMPTY)
            number_of_empty_positions: int = len(empty_positions)
            if number_of_empty_positions == 0:
                raise Exception(f'[{self.__class__.__name__}.{function_name()}()] Could not find an empty cell to place the drone. Try changing some values')

            self.__drone.row, self.__drone.column = empty_positions[randint(0, number_of_empty_positions - 1)]

    def epoch(self, number_of_ants: int) -> Optional[List[int]]:  # TODO
        ants_population = [Ant(self.__drone, self.__map) for _ in range(number_of_ants)]

        print(self.__drone.row, self.__drone.column)  # TODO [END] remove this
        return None

    def run(self, number_of_ants: int, number_of_epochs: int) -> Tuple[Optional[List[int]], float]:
        overall_best_solution: Optional[List[int]] = None

        self.prepare()

        start_time: float = time.time()
        for epoch in range(number_of_epochs):
            print(f" TODO epoch(). Running epoch {epoch}:", end=' ')  # TODO [END] remove this

            epoch_best_solution: Optional[List[int]] = self.epoch(number_of_ants)  # TODO the arguments to epoch()

            # TODO: compare epoch

        end_time: float = time.time()

        return overall_best_solution, end_time - start_time
