from typing import Set, Tuple

from domain.mean import Mean


class Centroid:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.points_indices: Set[int] = set()
        self.mean: Mean = Mean(0, 0)

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def remove_point(self, index: int, x: float, y: float):
        self.points_indices.remove(index)
        self.mean.remove_point(len(self.points_indices), x, y)

    def add_point(self, index: int, x: float, y: float):
        self.points_indices.add(index)
        self.mean.add_point(len(self.points_indices), x, y)

