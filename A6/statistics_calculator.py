from typing import Dict, List, Set, Tuple, Optional

from sklearn.metrics import precision_score, recall_score, adjusted_rand_score

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
        label_to_centroid: Dict[str, Optional[Centroid]] = self.compute_clusters_labels(occurrences)
        statistics: Dict[str, List[float]] = self.__compute_statistics(label_to_centroid)
        
        return occurrences, label_to_centroid, statistics

    def __compute_occurrences_in_clusters(self):
        occurrences: Dict[str, Dict[Centroid, int]] = {label: {centroid: 0 for centroid in self.centroids} for label in
                                                       self.labels}
        for point in self.points:
            occurrences[point.label][point.centroid] += 1

        return occurrences

    def compute_clusters_labels(self, occurrences: Dict[str, Dict[Centroid, int]]):  # TODO: refactor due to the special case
        label_to_centroid: Dict[str, Optional[Centroid]] = {label: None for label in self.labels}

        for label in self.labels:
            while max(self.centroids, key=lambda centroid: occurrences[label][centroid]) in label_to_centroid.values():
                occurrences[label][max(self.centroids, key=lambda centroid: occurrences[label][centroid])] = -1
            label_to_centroid[label] = max(self.centroids, key=lambda centroid: occurrences[label][centroid])

        return label_to_centroid

    def __compute_statistics(self, label_to_centroid: Dict[str, Optional[Centroid]]) -> Dict[str, List[float]]:
        # {<label>: [<accuracy>, <precision>, <rappel>, <score>]}
        results: Dict[str, List[float]] = {label: [0 for _ in range(4)] for label in list(self.labels) + ['AVG']}
        count: int = len(self.points)

        # for label in label_to_centroid.keys():  # TODO: compute_statistics
        #     centroid: Centroid = label_to_centroid[label]
        #     accuracy_count: int = 0
        #     precision_count: int = 0
        #     rappel_count: int = 0

        results = {label: [j * 1.1 for j in range(4)] for label in list(self.labels) + ['AVG']}
        return results

    def print_overall_statistics(self):
        true_labels: List[str] = []
        predicted_labels: List[str] = []
        number_of_correct_predictions: int = 0

        for label, centroid in self.compute_clusters_labels(self.__compute_occurrences_in_clusters()).items():
            for point_index in centroid.points_indices:
                point: Point = self.points[point_index]

                true_labels.append(point.label)
                predicted_labels.append(label)
                number_of_correct_predictions += point.label == label

        print(f'Accuracy: {number_of_correct_predictions / len(self.points)}')
        print(f'Precision: {precision_score(true_labels, predicted_labels, labels=["A", "B", "C", "D"], average="micro")}')
        print(f'Rappel: {recall_score(true_labels, predicted_labels, labels=["A", "B", "C", "D"], average="micro")}')
        print(f'Score: {adjusted_rand_score(predicted_labels, true_labels)}')


