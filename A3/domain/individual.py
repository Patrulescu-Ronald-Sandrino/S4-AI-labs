import functools
from random import random, randint
from typing import Tuple, Optional, List

import utils
from domain.drone import Drone
from domain.map import Map


class Individual:
    def __init__(self, map: Map, drone: Drone, size: int = 0):
        self.__map = map
        self.__drone = drone
        self.__size = size
        self.__chromosome = self.__map.fix_chromosome([randint(0, 3) for _ in range(self.__size)], self.__drone.position)
        self.__fitness: int = -1

    def get_path(self) -> List[Tuple[int, int]]:
        path: List[Tuple[int, int]] = [(self.__drone.x, self.__drone.y)]
        for gene in self.__chromosome:
            last_x, last_y = path[-1]
            delta_x, delta_y = utils.DIRECTIONS[gene]
            path.append((last_x + delta_x, last_y + delta_y))

        return path

    @property
    def fitness(self) -> int:
        return self.__fitness

    def compute_fitness(self) -> int:
        # compute the fitness for the indivisual
        # and save it in self.__fitness
        position = (self.__drone.x, self.__drone.y)
        fittness: int = functools.reduce(lambda a, b: a + b, self.__map.read_udm_sensors(*position))
        number_of_moves: int = 0

        for gene in self.__chromosome:
            number_of_moves += 1
            delta_x, delta_y = utils.DIRECTIONS[gene]
            current_x, current_y = position
            position = (current_x + delta_x, current_y + delta_y)

            if self.__map.is_position_inside_map(position) and self.__map.at(position) != Map.Position.WALL:
                fittness += functools.reduce(lambda a, b: a + b, self.__map.read_udm_sensors(*position))
            else:
                fittness -= 25
            if number_of_moves == self.__drone.battery:
                break

        self.__fitness = fittness
        return self.__fitness

    def mutate(self, mutate_probability: float = utils.INDIVIDUAL_MUTATION_PROBABILITY) -> None:
        # performs swap mutation
        if random() < mutate_probability:
            # perform a mutation with respect to the representation
            first_gene_index, second_gene_index = utils.generate_different_random_numbers(0, len(self.__chromosome) - 1)
            self.__chromosome[first_gene_index], self.__chromosome[second_gene_index] = self.__chromosome[second_gene_index], self.__chromosome[first_gene_index]
            self.__chromosome = self.__map.fix_chromosome(self.__chromosome, self.__drone.position)

    def crossover(self, other_parent: 'Individual', crossover_probability: float = utils.INDIVIDUAL_CROSSOVER_PROBABILITY) -> Optional[Tuple['Individual', 'Individual']]:
        if random() < crossover_probability:
            offspring1, offspring2 = Individual(self.__map, self.__drone, self.__size), Individual(self.__map, self.__drone, self.__size)
            # perform the crossover between the self and the otherParent
            split_index = randint(int((self.__size - 1) / 4), int(3 * (self.__size - 1) / 4))
            offspring1.__chromosome = self.__map.fix_chromosome(self.__chromosome[:split_index] + other_parent.__chromosome[split_index:], self.__drone.position)
            offspring2.__chromosome = self.__map.fix_chromosome(other_parent.__chromosome[:split_index] + self.__chromosome[split_index:], self.__drone.position)
            return offspring1, offspring2

        return None
