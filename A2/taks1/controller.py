from random import randint
from typing import Tuple

import pygame

from domain.Drone import Drone
from domain.Map import Map
from domain.constants import RED


class Controller:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone()
        # self.algorithms = {'greedy': self.greedy, 'a_star': self.a_star}
        self.algorithms = {'dummy_search': self.dummy_search(), 'dummy_search2': self.dummy_search(), 'dummy_search3': self.dummy_search()}

    def load_map(self, map_filepath=None) -> None:
        """
        Loads a map - either random or given as a filepath string
        :param map_filepath:
        :return:
        """
        if map_filepath is None:
            self.__map.randomMap()
        else:
            self.__map.loadMap(map_filepath)

    def generate_path(self, max_number_of_steps: int = -1) -> Tuple[tuple, tuple]:
        def is_tuple_none(xy: tuple) -> bool:
            x, y = xy
            return (x, y) == (None, None)

        first_position = self.__map.generate_typed_position(0, max_number_of_steps)
        if is_tuple_none(first_position):
            return first_position, first_position
        while True:
            second_position = self.__map.generate_typed_position(0, max_number_of_steps)
            if is_tuple_none(second_position):
                return second_position, second_position
            if first_position != second_position:
                return first_position, second_position

    def search_path(self, algorithm: str, start_x: int, start_y: int, end_x: int, end_y: int) -> tuple:
        if algorithm not in self.algorithms:
            return None, None

        if algorithm.__contains__("dummy_search"):
            return self.dummy_search(), 0

        # TODO
        # TODO self.algorithms[algorithm](...)

        return [], None

    @staticmethod
    def dummy_search():
        # example of some path in assets/maps/test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    def greedy(self) -> None:
        # TODO
        pass

    def a_star(self) -> None:
        # TODO
        pass

    def display_with_path(self, walls_color, path_color, path) -> pygame.Surface:
        image = self.__map.image(walls_color)

        mark = pygame.Surface((20, 20))
        mark.fill(path_color)

        for (x, y) in path:
            image.blit(mark, (y * 20, x * 20))

        return image
