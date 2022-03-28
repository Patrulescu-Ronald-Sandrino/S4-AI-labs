import inspect
import sys

from domain.drone import Drone
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
                sys.stderr.write("[error][{}.{}()] Could not find an EMPTY Position inside the map".format(__class__, inspect.stack()[0].function))
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
    
    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        
        # create the population,
        # run the algorithm
        # return the results and the statistics
        pass

    @property
    def map(self) -> Map:
        return self.__map

    @map.setter
    def map(self, new_map: Map) -> None:
        self.__map = new_map

    def set_parameters(self, population_size, individual_size, generation_count, number_of_iterations):
        self.__population_size = population_size
        self.__individual_size = individual_size
        self.__generation_count = generation_count
        self.__number_of_iterations = number_of_iterations

       