# -*- coding: utf-8 -*-
import random
from enum import Enum, IntEnum

# Creating some colors
from typing import Tuple


class Color(Enum):
    BLUE = (0, 0, 255)
    GRAY_BLUE = (50, 120, 120)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


# define directions
class Directions(IntEnum):
    UP = 0
    DOWN = 2
    LEFT = 1
    RIGHT = 3


# define indexes variations
DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

# define map size
MAP_HEIGHT = 20
MAP_WIDTH = 20
MAP_RANDOM_FILL = 0.2

DRONE_START_POSITION = (5, 5)

DEFAULT_SCREEN_DIMENSION = (400, 400)

DEFAULT_POPULATION_SIZE = 75
DEFAULT_INDIVIDUAL_SIZE = 40
DEFAULT_GENERATION_COUNT = 20
DEFAULT_NUMBER_OF_ITERATIONS = 94

DEFAULT_SEED = 10

NUMBER_OF_RUNS_FOR_STATISTICS = 30

INDIVIDUAL_MUTATION_PROBABILITY = 0.05
INDIVIDUAL_CROSSOVER_PROBABILITY = 0.8


def not_implemented(*args, **kwargs):  # TODO remove after finishing the UI
    print("Not implemented!")


class IO:
    @staticmethod
    def read_int(prompt_message: str = "Enter integer: ", failure_message: str = "Error! Input cannot be converted to "
                                                                                 "int. ") -> int:
        while True:
            try:
                return int(input(prompt_message))
            except ValueError as e:
                print(failure_message + "ValueError message: ", e)


def random_int(start: int, end: int) -> int:
    return random.randint(start, end)


def generate_different_random_numbers(start: int, end: int, max_number_of_iterations: int = 10 ** 6) -> Tuple[int, int]:
    first: int = random_int(start, end)
    second: int = random_int(start, end)
    iterations_done: int = 0

    while first != second and iterations_done <= max_number_of_iterations:
        iterations_done += 1
        second = random_int(start, end)

    return first, second
