from __future__ import annotations

from typing import Tuple


class Point:
    def __init__(self, x: float, y: float):
        self.__x: float = x
        self.__y: float = y

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

