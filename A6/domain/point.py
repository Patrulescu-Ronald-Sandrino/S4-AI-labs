from typing import Optional, Tuple, Set

from domain.centroid import Centroid
from tools.math import euclidean_distance


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
        return min(centroids, key=lambda centroid: euclidean_distance(self.xy, centroid.xy))
