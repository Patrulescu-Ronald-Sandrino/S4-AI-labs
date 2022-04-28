from __future__ import annotations

from typing import Optional


class Ant:
    def __init__(self):
        self.__path = None  # TODO: add type
        self.__fitness: int = 0

    @property
    def path(self):  # TODO: add return type
        return self.__path

    @property
    def fitness(self) -> int:
        return self.__fitness

    @staticmethod
    def get_best(first: Optional[Ant], second: Optional[Ant]) -> Optional[Ant]:
        if first is None:
            return second
        if second is None:
            return first
        if first.fitness > second.fitness:
            return first
        elif first.fitness == second.fitness:
            return first if len(first.path) < len(second.path) else second
        else:
            return second
