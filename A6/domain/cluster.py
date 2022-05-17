from typing import List

from domain.point import Point


class Cluster:
    def __init__(self, label: str, x: float, y: float):
        self.__label: str = label
        self.__centroid: Point = Point(x, y)
        self.__points: List[Point] = []

    @property
    def label(self) -> str:
        return self.__label

    @property
    def centroid(self) -> Point:
        return self.__centroid

    @property
    def points(self) -> List[Point]:
        return self.__points[:]

    def add_point(self, x: float, y: float):
        self.__points.append(Point(x, y))

    def recompute_centroid(self):
        pass