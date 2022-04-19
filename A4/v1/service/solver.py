import time
from random import randint
from typing import List, Optional, Tuple

from tools.general import function_name
from v1.domain.drone import Drone
from v1.domain.map import Map


class Solver:
    def __init__(self, map_: Map, drone: Drone):
        self.__map: Map = map_
        self.__drone: Drone = drone
        self.__trace: List[List[float]] = []

    def prepare(self):
        self.__trace = Solver.get_new_trace(self.__map.rows * self.__map.columns)

        # make sure the drone is on a free cell
        if self.__map.surface[self.__drone.row][self.__drone.column] != Map.CellType.EMPTY:
            empty_positions: List[Tuple[int, int]] = self.__map.find_all(Map.CellType.EMPTY)
            number_of_empty_positions: int = len(empty_positions)
            if number_of_empty_positions == 0:
                raise Exception(f'[{self.__class__.__name__}.{function_name()}()] Could not find an empty cell to place the drone. Try changing some values')

            self.__drone.row, self.__drone.column = empty_positions[randint(0, number_of_empty_positions - 1)]

    def epoch(self) -> Optional[List[int]]:
        print(self.__drone.row, self.__drone.column)
        return None  # TODO

    def run(self, ants: int, epochs: int) -> Tuple[Optional[List[int]], float]:
        overall_best_solution: Optional[List[int]] = None

        self.prepare()

        start_time: float = time.time()
        for epoch in range(epochs):
            print(f" TODO epoch(). Running epoch {epoch}:", end=' ')
            epoch_best_solution: Optional[List[int]] = self.epoch()  # TODO the arguments to epoch()
            # TODO: compare epoch

        end_time: float = time.time()

        return overall_best_solution, end_time - start_time

    @staticmethod
    def get_new_trace(size: int) -> List[List[float]]:
        return [[1.0 for _ in range(size)] for _ in range(size)]
