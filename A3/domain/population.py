from typing import List, Tuple

from domain.drone import Drone
from domain.individual import Individual
from domain.map import Map


class Population:
    def __init__(self, map: Map, drone: Drone, population_size: int = 0, individual_size: int = 0):
        self.__population_size = population_size
        self.__individuals = [Individual(map, drone, individual_size) for _ in range(population_size)]
        # TODO: MAYBE self.evaluate()

    @property
    def individuals(self) -> List[Individual]:
        return self.__individuals[:]

    def evaluate(self) -> List[Tuple[Individual, float]]:
        # evaluates the population
        return [(individual, individual.compute_fitness()) for individual in self.__individuals]

    def selection(self, k: int = 0) -> List[Individual]:
        # perform a selection of k individuals from the population
        # and returns that selection
        self.evaluate()
        return sorted(self.__individuals, key=lambda individual: individual.compute_fitness(), reverse=True)[:k]

    def set_individuals(self, individuals: List[Individual]) -> None:
        self.__individuals = individuals

    def get_individuals(self) -> List[Individual]:
        return self.__individuals

    def add_individual(self, individual: Individual) -> None:
        self.__individuals.append(individual)


