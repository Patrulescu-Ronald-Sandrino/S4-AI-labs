from typing import Set, Tuple


class Centroid:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.points_indices: Set[int] = set()

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def remove_point(self, index: int, x: float, y: float):
        self.points_indices.remove(index)
        length = len(self.points_indices)
        self.x = (self.x * (length + 1) - x) / length
        self.y = (self.y * (length + 1) - y) / length

    def add_point(self, index: int, x: float, y: float):
        self.points_indices.add(index)
        length = len(self.points_indices)
        self.x = (self.x * (length - 1) + x) / length
        self.y = (self.y * (length - 1) + y) / length

