from typing import Optional, Tuple, Set

from domain.centroid import Centroid


class Point:
    def __init__(self, x: str, y: str, label: str):
        self.x: float = float(x)
        self.y: float = float(y)
        self.label: str = label
        self.centroid: Optional[Centroid] = None

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def classify(self, centroids: Set[Centroid]) -> Centroid:
        return min(centroids, key=lambda centroid: self.euclidean_distance(centroid.xy))

    def euclidean_distance(self, other_coordinates: Tuple[float, float]) -> float:
        other_x, other_y = other_coordinates
        return ((self.x - other_x) ** 2 + (self.y - other_y) ** 2) ** 1/2
