from typing import Dict, List, Set, Tuple, Optional

from domain.centroid import Centroid
from domain.point import Point


class StatisticsCalculator:
    def __init__(self,
                 labels: Dict[str, None],
                 points: List[Point],
                 centroids: Set[Centroid]):

        self.labels: Dict[str, None] = labels
        self.points: List[Point] = points
        self.centroids: Set[Centroid] = centroids

    def run(self) -> Tuple[Dict[str, Dict[Centroid, int]], Dict[str, Optional[Centroid]], Dict[str, List[float]]]:
        
        occurrences: Dict[str, Dict[Centroid, int]] = self.__compute_occurrences_in_clusters()
        label_to_centroid: Dict[str, Optional[Centroid]] = self.__compute_clusters_labels(occurrences)
        statistics: Dict[str, List[float]] = self.__compute_statistics(label_to_centroid)
        
        return occurrences, label_to_centroid, statistics

    def __compute_occurrences_in_clusters(self):
        occurrences: Dict[str, Dict[Centroid, int]] = {label: {centroid: 0 for centroid in self.centroids} for label in
                                                       self.labels}
        for point in self.points:
            occurrences[point.label][point.centroid] += 1

        return occurrences

    def __compute_clusters_labels(self, occurrences: Dict[str, Dict[Centroid, int]]):  # TODO: refactor due to the special case
        label_to_centroid: Dict[str, Optional[Centroid]] = {label: None for label in self.labels}

        for label in self.labels:
            while max(self.centroids, key=lambda centroid: occurrences[label][centroid]) in label_to_centroid.values():
                occurrences[label][max(self.centroids, key=lambda centroid: occurrences[label][centroid])] = -1
            label_to_centroid[label] = max(self.centroids, key=lambda centroid: occurrences[label][centroid])

        return label_to_centroid

    def __compute_statistics(self, label_to_centroid: Dict[str, Optional[Centroid]]):
        # TODO
        return {label: [j * 1.1 for j in range(4)] for label in list(self.labels) + ['AVG']}