import pickle
from random import random, randint

import numpy as np
import pygame
from typing import Tuple

from domain.constants import BLUE, WHITE


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, num_file="test.map"):
        with open(num_file, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def generate_position(self) -> tuple:
        """
        generates a random position inside the map
        :return:
        """
        return randint(0, self.n - 1), randint(0, self.m - 1)

    @staticmethod
    def is_cell_value_valid(value) -> bool:
        return value in [0, 1]

    def generate_typed_position(self, value: int = 0, max_number_of_steps: int = -1) -> tuple:
        """
        generates a random wall or a random empty position inside the map
        :param value: 0 - empty position, 1 - wall
        :param max_number_of_steps: non-null integer for fixed number, negative number for infinite loop
        :return:
        """
        if not self.is_cell_value_valid(value):
            return None, None

        steps_taken = 0
        while True:
            if 0 <= max_number_of_steps == steps_taken:
                return None, None
            x, y = randint(0, self.n - 1), randint(0, self.m - 1)
            steps_taken += 1
            if self.surface[x][y] == value:
                return x, y

    def generate_typed_positions_pair(self, first_value: int = 0, second_value: int = 0,
                                      max_number_of_steps: int = -1) -> \
            Tuple[tuple, tuple]:
        """
        Returns a pair of random different positions of given values
        (assuming that the values are valid
        and that they can be generated in the given number of steps)
        :param first_value:
        :param second_value:
        :param max_number_of_steps:
        :return:
        """


