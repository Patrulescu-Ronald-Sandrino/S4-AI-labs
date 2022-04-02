import inspect
import random
import sys
import time
from typing import List, Tuple, Any

import numpy as np

import utils
from domain.drone import Drone
from domain.individual import Individual
from repository import *
from utils import *


class Controller:
    def __init__(self, repository: Repository):
        self.__repository = repository
        self.__map = Map().random_map()
        self.__drone = Drone(*DRONE_START_POSITION)
        self.__move_drone_on_empty_position()

        self.__population_size: int = DEFAULT_POPULATION_SIZE
        self.__individual_size: int = DEFAULT_INDIVIDUAL_SIZE
        self.__generation_count: int = DEFAULT_GENERATION_COUNT
        self.__number_of_iterations: int = DEFAULT_NUMBER_OF_ITERATIONS

        self.__best_individuals: List[Individual] = []
        self.__averages: List[float] = []
        self.__duration: float = 0

    @property
    def map(self) -> Map:
        return self.__map

    @map.setter
    def map(self, new_map: Map) -> None:
        self.__map = new_map
        
    def __move_drone_on_empty_position(self):
        if self.__map.at((self.__drone.x, self.__drone.y)) == Map.Position.WALL:
            new_position = self.__map.generate_random_position_of_type(Map.Position.EMPTY)
            if not self.__map.is_position_inside_map(new_position):
                sys.stderr.write("[error][{}.{}()] Could not find an EMPTY Position inside the map\n".format(__class__, inspect.stack()[0].function))
                sys.exit(1)
            else:
                self.__drone.move(new_position)
    
    def set_parameters(self, population_size: int = DEFAULT_POPULATION_SIZE,
                       individual_size: int = DEFAULT_INDIVIDUAL_SIZE,
                       generation_count: int = DEFAULT_GENERATION_COUNT,
                       number_of_iterations: int = DEFAULT_NUMBER_OF_ITERATIONS):
        self.__population_size = population_size
        self.__individual_size = individual_size
        self.__generation_count = generation_count
        self.__number_of_iterations = number_of_iterations

    def iteration(self, population: Population):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        individuals: List[Individual] = population.get_individuals()

        first_parent_index, second_parent_index = utils.generate_different_random_numbers(0, len(individuals) - 1)
        first_parent: Individual = individuals[first_parent_index]
        second_parent: Individual = individuals[first_parent_index]

        # TODO crossover
        # TODO mutate

    def __perform_generation_iterations(self, population: Population, iterations: int = DEFAULT_NUMBER_OF_ITERATIONS):
        for iteration in range(self.__number_of_iterations):
            self.iteration(population)  # TODO
        population.set_individuals(population.selection(self.__population_size))
        self.__repository.set_last_population(population)

    def run(self, current_seed: int) -> Tuple[Individual, float]:
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        # return the results and the info for statistics
        random.seed(current_seed)
        population: Population = Population(self.__map, self.__drone, self.__population_size, self.__individual_size)
        self.__repository.add_population(population)

        best_individual: Individual = None  # type: ignore

        for generation in range(self.__generation_count):
            self.__perform_generation_iterations(population, DEFAULT_NUMBER_OF_ITERATIONS)

            best_individual = population.selection(1)[0]  # NOTE: selection also performs fitness evaluation

        last_fitness_average: float = np.average([individual.fitness for individual in population.get_individuals()])

        return best_individual, last_fitness_average

    def solver(self, seed: int = DEFAULT_SEED) -> Tuple[List[Individual], List[float], float]:
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        best_individuals = []  # type: List[Individual]
        averages: List[float] = []

        start_time: float = time.time()
        for current_seed in range(1, seed + 1):
            best_individual, average = self.run(current_seed)
            best_individuals.append(best_individual)
            averages.append(average)
        end_time: float = time.time()

        return best_individuals, averages, end_time - start_time

    def get_results(self) -> Tuple[List[Individual], List[float], float]:
        return self.__best_individuals, self.__averages, self.__duration
