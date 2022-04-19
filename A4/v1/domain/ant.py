from typing import List


class Ant:
    def __init__(self):  # TODO
        self.__path: List = []
        pass

    def fitness(self) -> float:
        return len(self.__path)  # TODO

    def move(self):  # TODO
        pass