import csv
import sys
from random import uniform
from typing import List, Tuple, Set

from matplotlib import pyplot as plt

from domain.centroid import Centroid
from domain.point import Point


class Solver:
    CLUSTERS = 4
    ITERATIONS = 1000

    def __init__(self, filename: str):
        self.filename: str = filename
        self.points: List[Point] = []
        self.centroids: Set[Centroid] = set()
        self.any_centroid_changed: bool = False

    def run(self):
        self.__prepare()

        for _ in range(Solver.ITERATIONS):
            print(f'running iteration {_}')
            self.any_centroid_changed: bool = False
            self.__run_iteration()
            if not self.any_centroid_changed:
                break
            self.display()

        # TODO: statistics and plotting
        self.print_info()

    def print_info(self):
        for centroid in self.centroids:
            print()
            print(f'centroid {round(centroid.x, 4)} {round(centroid.y, 4)}')
            print(f'len(points_indices) {len(centroid.points_indices)}')
            print(f'points_indices {centroid.points_indices}')

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

    def display(self):
        colours = ['red', 'green', 'blue', 'yellow']
        index = 0
        for centroid in self.centroids:
            plt.scatter(
                [self.points[point_index].x for point_index in centroid.points_indices],
                [self.points[point_index].y for point_index in centroid.points_indices],
                c=colours[index]
            )
            index += 1

        plt.scatter(
            [centroid.x for centroid in self.centroids],
            [centroid.y for centroid in self.centroids],
            c='black'
        )
        plt.show()

    # LEVEL 3

    def __read_points(self):
        with open(self.filename, 'r') as file:
            rows: List[str] = list(csv.reader(file))[1:]  # skip the 1st line (header line)

            # row[0] = label
            # row[1] = x
            # row[2] = y
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

