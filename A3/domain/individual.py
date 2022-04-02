from random import random, randint
from typing import Tuple, Optional

import utils
from domain import gene
from domain.drone import Drone
from domain.map import Map


class Individual:
    def __init__(self, map: Map, drone: Drone, size: int = 0):
        self.__map = map
        self.__drone = drone
        self.__size = size
        self.__chromosome = [randint(0, 3) for _ in range(self.__size)]
        self.__fitness: float = -1

    @property
    def fitness(self) -> float:
        return self.__fitness

    def compute_fitness(self) -> float:
        # compute the fitness for the indivisual
        # and save it in self.__fitness
        pass
        raise NotImplementedError

    def mutate(self, mutate_probability: float = utils.INDIVIDUAL_MUTATION_PROBABILITY) -> None:
        # performs swap mutation
        if random() < mutate_probability:
            # perform a mutation with respect to the representation
            first_gene_index, second_gene_index = utils.generate_different_random_numbers(0, len(self.__chromosome) - 1)
            self.__chromosome[first_gene_index], self.__chromosome[second_gene_index] = self.__chromosome[second_gene_index], self.__chromosome[first_gene_index]

    def crossover(self, other_parent: 'Individual', crossover_probability: float = utils.INDIVIDUAL_CROSSOVER_PROBABILITY) -> Optional[Tuple['Individual', 'Individual']]:
        if random() < crossover_probability:
            offspring1, offspring2 = Individual(self.__map, self.__drone, self.__size), Individual(self.__map, self.__drone, self.__size)
            # perform the crossover between the self and the otherParent
            split_index = randint(int((self.__size - 1) / 4), int(3 * (self.__size - 1) / 4))
            offspring1.__chromosome = self.__chromosome[:split_index] + other_parent.__chromosome[split_index:]
            offspring2.__chromosome = other_parent.__chromosome[:split_index] + self.__chromosome[split_index:]
            return offspring1, offspring2

        return None
