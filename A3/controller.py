import datetime
import functools
import inspect
import math
import random
import sys
import time
from typing import List, Tuple, Any, Optional

import numpy
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

    def iteration(self, population: Population) -> None:
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        individuals: List[Individual] = population.get_individuals()

        first_parent_index, second_parent_index = utils.generate_different_random_numbers(0, len(individuals) - 1)
        # print("parent indices: ", first_parent_index, second_parent_index)
        first_parent: Individual = individuals[first_parent_index]
        second_parent: Individual = individuals[first_parent_index]

        # crossover
        offsprings: Optional[Tuple[Individual, Individual]] = first_parent.crossover(second_parent, INDIVIDUAL_CROSSOVER_PROBABILITY)
        if not offsprings:
            return

        # mutate
        (offspring1, offspring2) = offsprings
        offspring1.mutate(INDIVIDUAL_MUTATION_PROBABILITY)
        offspring2.mutate(INDIVIDUAL_MUTATION_PROBABILITY)

        # add the fittest offspring to population
        fittest_offspring = offspring1 if offspring1.compute_fitness() > offspring2.compute_fitness() else offspring2
        population.add_individual(fittest_offspring)

    def __perform_generation_iterations(self, population: Population, iterations: int = DEFAULT_NUMBER_OF_ITERATIONS):
        for iteration in range(self.__number_of_iterations):
            self.iteration(population)
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
            # pop = [(index, individual.fitness) for index, individual in enumerate(population.individuals)]
            # print("seed: {}, gen: {}, best_individual: {}, population: {}".format(current_seed, generation, best_individual.compute_fitness(), pop))

        last_fitness_average: float = np.average([individual.fitness for individual in population.get_individuals()])
        # print("last_fitness_average = ", last_fitness_average)
        # print([individual._Individual__chromosome for individual in population.get_individuals()])
        # print([individual.fitness for individual in population.get_individuals()])
        sum = functools.reduce(lambda a, b: a + b, [individual.fitness for individual in population.get_individuals()])
        # print(sum)
        # print("last_fitness_average (using the formula) = ", sum / len(population.get_individuals()))
        return best_individual, last_fitness_average

    def solver(self, seed: int = DEFAULT_SEED) -> Tuple[List[Individual], List[float], float]:
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        best_individuals = []  # type: List[Individual]
        averages: List[float] = []

        start_time: float = time.time()
        align = math.floor(math.log(max(seed, 1), 10)) + 1
        # print("{:>{}}{:>8}{:>8}".format("Seed", align, "Average", "Best fitness"))
        print("{:>12}{:>12}{:>15}".format("Seed", "Average", "Best fitness"))
        for current_seed in range(1, seed + 1):
            best_individual, average = self.run(current_seed)
            # print("{:>{}}{:8.2f}{:8.2f}".format(current_seed, align, average, best_individual.fitness))
            print("{:>12}{:12.2f}{:15.2f}".format(current_seed, average, best_individual.fitness))
            best_individuals.append(best_individual)
            averages.append(average)
        end_time: float = time.time()
        duration: float = end_time - start_time

        self.__best_individuals, self.__averages, self.__duration = best_individuals, averages, duration
        self.__best_individuals.sort(key=lambda individual: individual.fitness, reverse=True)
        # print("Individual.individuals_to_str(self.__best_individuals)", Individual.individuals_to_str(self.__best_individuals))
        self.log_statistics_to_file(seed)
        return best_individuals, averages, duration

    def get_results(self) -> Tuple[List[Individual], List[float], float]:
        return self.__best_individuals, self.__averages, self.__duration

    def statistics_to_str(self) -> str:
        result: str = ""
        result += "Population size = %d\n" % self.__population_size
        result += "Individual size = %d\n" % self.__individual_size
        result += "Generation count = %d\n" % self.__generation_count
        result += "Number of iterations = %d\n" % self.__number_of_iterations
        result += "Mutation probability = %.2f\n" % INDIVIDUAL_MUTATION_PROBABILITY
        result += "Crossover probability = %.2f\n" % INDIVIDUAL_CROSSOVER_PROBABILITY
        result += "Last generation average = %.2f\n" % self.__averages[-1]
        result += "Best fitness = %.2f\n" % (self.__best_individuals[0].fitness if len(self.__best_individuals) > 0 else "None")
        result += "Best path = %s\n" % (self.__best_individuals[0].get_path() if len(self.__best_individuals) > 0 else "None")
        result += "Duration = %s\n" % self.__duration
        result += "Average of averages = %.3f\n" % numpy.average(self.__averages)
        result += "std. dev. of averages = %.3f\n" % numpy.std(self.__averages)

        return result

    def log_statistics_to_file(self,
                               last_seed: int,
                               filepath="results/results.txt") -> None:
        result: str = ""
        result += "%s:\n" % datetime.datetime.now()
        result += "Seeds = [%d, %d]\n" % (1, last_seed)
        result += self.statistics_to_str()

        try:
            with open(filepath, 'a') as file:
                file.write(result + "\n")
        except OSError as e:
            sys.stderr.write("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, e))
            raise Exception("Failed to log statistics to file")
