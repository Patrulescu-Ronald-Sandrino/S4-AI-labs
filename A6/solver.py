import csv
import sys
from random import uniform
from typing import List, Tuple, Set, Dict

from matplotlib import pyplot as plt

from domain.centroid import Centroid
from domain.point import Point
from statistics_calculator import StatisticsCalculator
from statistics_printer import StatisticsPrinter


class Solver:
    CLUSTERS = 4
    ITERATIONS = 1000
    LABELS: Dict[str, None] = {label: None for label in ['A', 'B', 'C', 'D']}

    def __init__(self, filename: str):
        self.filename: str = filename
        self.points: List[Point] = []
        self.centroids: Set[Centroid] = set()
        self.any_centroid_changed: bool = False

    def run(self):
        self.__prepare()

        for _ in range(Solver.ITERATIONS):
            print(f'running iteration {_}')
            self.any_centroid_changed = False
            self.__run_iteration()
            if not self.any_centroid_changed:
                break
            self.__display_plot()

        self.__print_centroids_info()
        self.__compute_and_print_statistics()

    # LEVEL 2

    def __prepare(self):
        self.__read_points()
        x_bounds, y_bounds = self.__find_domain_bounds()
        self.__initialize_centroids(x_bounds, y_bounds)
        self.any_centroid_changed = True

    def __run_iteration(self):  # https://www.geeksforgeeks.org/k-means-clustering-introduction/
        for index, point in enumerate(self.points):

            centroid: Centroid = point.centroid
            new_centroid: Centroid = point.classify(self.centroids)
            
            if centroid is not None and new_centroid != centroid:
                centroid.remove_point(index, *point.xy)
            new_centroid.add_point(index, *point.xy)

            if new_centroid != centroid:
                self.any_centroid_changed = True
                point.centroid = new_centroid

    def __display_plot(self):
        colours = {'red', 'green', 'blue', 'yellow'}
        for centroid, color in zip(self.centroids, colours):
            plt.scatter(
                [self.points[point_index].x for point_index in centroid.points_indices],
                [self.points[point_index].y for point_index in centroid.points_indices],
                c=color
            )

        plt.scatter(
            [centroid.x for centroid in self.centroids],
            [centroid.y for centroid in self.centroids],
            c='black'
        )
        plt.show()

    def __print_centroids_info(self):
        for centroid in self.centroids:
            print(centroid)

    def __compute_and_print_statistics(self):
        results = StatisticsCalculator(Solver.LABELS, self.points, self.centroids).run()
        StatisticsPrinter(Solver.LABELS, self.centroids, *results).print()

    # LEVEL 3

    def __read_points(self):
        with open(self.filename, 'r') as file:
            rows: List[str] = list(csv.reader(file))[1:]  # skip the 1st line (header line)
            # indices:     0      1    2
            # line:     <label>, <x>, <y>
            self.points = [Point(row[1], row[2], row[0]) for row in rows]

    def __find_domain_bounds(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        x_min = y_min = sys.maxsize
        x_max = y_max = - sys.maxsize + 1

        for point in self.points:
            x_min = min(x_min, point.x)
            x_max = max(x_max, point.x)
            y_min = min(y_min, point.y)
            y_max = max(y_max, point.y)

        return (x_min, x_max), (y_min, y_max)

    def __initialize_centroids(self, x_bounds: Tuple[float, float], y_bounds: Tuple[float, float]):
        self.centroids = {Centroid(uniform(*x_bounds), uniform(*y_bounds)) for _ in range(Solver.CLUSTERS)}

    # LEVEL 4
