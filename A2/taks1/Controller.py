import time
from random import randint
from typing import Tuple, Type, List

import pygame

from domain.Drone import Drone
from domain.Map import Map
from domain.PathSearcher import PathSearcher
from domain.constants import RED, DIRECTIONS, DUMMY_SEARCH_PATH


class Controller:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone()
        # TODO:
        #  IDEA
        #   1. use a "Singleton" Class for the algorithms
        #   2. create a class PathSearcher that is inherited by PathSearcherAStar and by PathSearcherGreedy
        #       - learn Python Polymorphism
        #       - replace in Controller.search_path() 'algorithm: str' with searcher: "instanceof(PathSearcher)"
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
        """
        generates a pair of distinct empty positions inside the map
        :param max_number_of_steps:
        :return:
        """
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

    def search_path_v2(self, searcher_class: Type[PathSearcher], start_x: int, start_y: int, end_x: int, end_y: int) -> Tuple[List[Tuple[int, int]], float]:
        searcher = searcher_class(start_x, start_y, end_x, end_y)
        return searcher.run(self.__map)

    def display_with_path(self, walls_color, path_color, path) -> pygame.Surface:
        image = self.__map.image(walls_color)

        mark = pygame.Surface((20, 20))
        mark.fill(path_color)

        for (x, y) in path:
            image.blit(mark, (y * 20, x * 20))

        return image

    @staticmethod
    def dummy_search() -> List[Tuple[int, int]]:
        # example of some path in assets/maps/test1.map from [5,7] to [7,11]
        return DUMMY_SEARCH_PATH

    def search_path_v1(self, algorithm: str, start_x: int, start_y: int, end_x: int, end_y: int) -> Tuple[List[Tuple[int, int]], float]:
        if algorithm not in self.algorithms:
            return [], -1

        if algorithm.__contains__("dummy_search"):
            return self.dummy_search(), 0

        start_time = time.time()

        found = False
        visited = dict()
        to_visit = [(start_x, start_y)]

        # TODO: define prev, nrSteps

        while len(to_visit) > 0 and not found:
            node = (x, y) = to_visit.pop(0)
            visited[node] = True

            if node == (end_x, end_y):
                found = True
            else:
                aux = []
                for (delta_x, delta_y) in DIRECTIONS:
                    new = (new_x, new_y) = x + delta_x, y + delta_y
                    if self.__map.is_position_valid(new_x, new_y) and new not in visited:
                        # TODO self.algorithms[algorithm]['function'](...)
                        pass
                to_visit.extend(aux)
                # TODO to_visit.sort(key=lambda position: self.algorithms[algorithm]['heuristic'](*position, end_x, end_y))

        end_time = time.time()
        interval = end_time - start_time
        path = [None] if found else []  # TODO: replace [None] with the build_path(...)

        return path, interval

    def greedy(self) -> None:
        # TODO
        pass

    def a_star(self) -> None:
        # TODO
        pass
