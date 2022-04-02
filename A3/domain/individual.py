from random import random
from typing import Tuple

import utils
from domain import gene
from domain.drone import Drone
from domain.map import Map


class Individual:
    def __init__(self, map: Map, drone: Drone, size: int = 0):
        self.__map = map
        self.__drone = drone
        self.__size = size
        self.__chromosome = [gene() for i in range(self.__size)]
        self.__fitness: float = -1

    @property
    def fitness(self) -> float:
        return self.__fitness

    def compute_fitness(self) -> float:
        # compute the fitness for the indivisual
        # and save it in self.__fitness
        pass

    def mutate(self, mutate_probability: float = utils.INDIVIDUAL_MUTATION_PROBABILITY):
        if random() < mutate_probability:
            pass
            # perform a mutation with respect to the representation

    def crossover(self, other_parent: 'Individual', crossover_probability: float = utils.INDIVIDUAL_CROSSOVER_PROBABILITY) -> Tuple['Individual', 'Individual']:
        offspring1, offspring2 = Individual(self.__map, self.__drone, self.__size), Individual(self.__map, self.__drone, self.__size)
        if random() < crossover_probability:
            pass
            # perform the crossover between the self and the otherParent

        return offspring1, offspring2
