from typing import List

from domain.point import Point, LabeledPoint


class Cluster:
    def __init__(self, x: float, y: float):
        self.__centroid: Point = Point(x, y)
        self.__points: List[LabeledPoint] = []

    @property
    def centroid(self) -> Point:
        return self.__centroid

    @property
    def points(self) -> List[LabeledPoint]:
        return self.__points[:]

    def add_point(self, x: float, y: float, label: str):
        self.__points.append(LabeledPoint(x, y, label))

    def recompute_centroid(self):
        raise NotImplementedError('TODO')

    def compute_labels_occurrences(self):
        raise NotImplementedError('TODO')