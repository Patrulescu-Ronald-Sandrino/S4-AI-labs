import time
from random import randint
from typing import Optional, Tuple, List

from src.domain.ant import Ant
from src.domain.drone import Drone
from src.domain.map import Map


class Solver:
    def __init__(self, map_instance: Map, drone: Drone):
        self.__map: Map = map_instance
        self.__drone: Drone = drone

    def epoch(self, number_of_ants: int, number_of_iterations: int) -> Optional[Ant]:
        raise NotImplementedError("TODO")
        # TODO: move ants

        # TODO: update pheromone matrix

        # TODO: find best ant

        # TODO: update pheromone matrix based on best ant

        # TODO: return best ant

    def run(self, number_of_epochs: int, number_of_ants: int, number_of_iterations: int) -> Tuple[Optional[Ant], float]:
        best_ant: Optional[Ant] = None

        start_time: float = time.time()
        for epoch_number in range(1, number_of_epochs + 1):
            print(f'[epoch {epoch_number}/{number_of_epochs}] ' + '-' * 30)  # TODO END remove

            epoch_best_ant = self.epoch(number_of_ants, number_of_iterations)
            best_ant = Ant.get_best(best_ant, epoch_best_ant)

            if best_ant is not None:  # TODO END remove
                if id(best_ant) != id(epoch_best_ant):
                    print(f'RAISED to fitness: {best_ant.fitness} path: {best_ant.path}')
                else:
                    print(f'Not changed')
            else:
                print(f'best_ant: None')

            print(f'[epoch {epoch_number}/{number_of_epochs}] ' + '-' * 30)  # TODO END remove
        end_time: float = time.time()

        return best_ant, end_time - start_time


class SolverTools:
    @staticmethod
    def place_drone_on_empty_cell(map_instance: Map, drone: Drone) -> None:
        if map_instance.value_at(drone.position) == Map.Cell.EMPTY:
            raise Exception("Drone already on an empty cell!")

        empty_cells: List[Tuple[int, int]] = map_instance.find_cells(Map.Cell.EMPTY)
        if len(empty_cells) == 0:
            raise Exception("No empty cells were found to place the drone!")

        drone.position = empty_cells[randint(0, len(empty_cells) - 1)]
