from __future__ import annotations

from typing import Optional, Tuple, Dict, List

from src.domain.drone import Drone


class Ant:
    def __init__(self, size: int, drone: Drone):
        self.__size: int = size
        self.__path: Dict[Tuple[int, int]] = {}
        self.__fitness: int = 0

        self.__start: Tuple[int, int] = drone.position
        self.__battery: int = drone.energy

    @property
    def path(self) -> Dict[Tuple[int, int]]:
        return self.__path

    @property
    def fitness(self) -> int:
        return self.__fitness

    def get_potential_next_sensors(self):
        raise NotImplementedError("TODO")

    def move(self, pheromone_matrix: Dict[Tuple[int, int], Dict[Tuple[int, int], float]], distances: Dict[Tuple[int, int], Dict[Tuple[int, int], float]], q0: float, alpha: float, beta: float) -> bool:
        # TODO: get potential next positions
        # TODO: if none exists => return False


        return True

    @staticmethod
    def get_best(first: Optional[Ant], second: Optional[Ant]) -> Optional[Ant]:
        if first is None:
            return second
        if second is None:
            return first
        if first.fitness > second.fitness:
            return first
        elif first.fitness == second.fitness:
            return first if len(first.path) < len(second.path) else second
        else:
            return second
