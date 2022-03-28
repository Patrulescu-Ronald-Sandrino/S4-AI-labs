import inspect
import random
import sys
import time
from typing import List, Tuple, Any

import numpy as np

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

    def __move_drone_on_empty_position(self):
        if self.__map.at((self.__drone.x, self.__drone.y)) == Map.Position.WALL:
            new_position = self.__map.generate_random_position_of_type(Map.Position.EMPTY)
            if not self.__map.is_position_inside_map(new_position):
                sys.stderr.write("[error][{}.{}()] Could not find an EMPTY Position inside the map\n".format(__class__, inspect.stack()[0].function))
                sys.exit(1)
            else:
                self.__drone.move(new_position)

    def iteration(self, args):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        pass
        
    def run(self, args):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics
        pass
    
    @property
    def map(self) -> Map:
        return self.__map

    def simulate_seed(self, seed):
        random.seed(seed)
        new_population: Population = Population()  # TODO
        self.__repository.add_population(new_population)  # TODO

        best_individual = None
        average: int = 0

        for generation in range(self.__generation_count):
            for iteration in range(self.__number_of_iterations):
                self.iteration(new_population)  # TODO
            new_population.set_individuals(new_population.selection(self.__population_size))  # TODO
            self.__repository.set_last_population(new_population)

            population_fitness = [individual.fitness() for individual in new_population.get_invdividuals()]  # TODO
            best_individual = new_population.selection(1)[0]
            average = np.average(population_fitness)

        return best_individual, average

    def solver(self, seed: int = DEFAULT_SEED) -> Tuple[List[Individual], List[Any], float]:
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        best_individuals: List[Individual] = []
        final_generation_averages: List[Any] = []

        start_time: float = time.time()
        for seed_value in range(1, seed + 1):
            final_generation_average, best_individual = self.simulate_seed(seed)  # TODO
            print(seed_value, str(final_generation_average), str(best_individual.get_fitness()))  # TODO
            best_individuals.append(best_individual)
            final_generation_averages.append(final_generation_average)
        end_time: float = time.time()

        return best_individuals, final_generation_averages, end_time - start_time

    @map.setter
    def map(self, new_map: Map) -> None:
        self.__map = new_map

    def set_parameters(self, population_size: int = DEFAULT_POPULATION_SIZE,
                       individual_size: int = DEFAULT_INDIVIDUAL_SIZE,
                       generation_count: int = DEFAULT_GENERATION_COUNT,
                       number_of_iterations: int = DEFAULT_NUMBER_OF_ITERATIONS):
        self.__population_size = population_size
        self.__individual_size = individual_size
        self.__generation_count = generation_count
        self.__number_of_iterations = number_of_iterations

       