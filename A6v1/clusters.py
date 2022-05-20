import csv
from typing import Set, List

from domain.cluster import Cluster


def read_points(filepath: str):
    points = []
    # with open('dataset.csv') as csv_file:
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # Complete appending point (row1, row2) to points list
            if row[0] == 'label':
                continue
            # point = (float(row[1]), float(row[2]))
            point = {'x': float(row[1]), 'y': float(row[2]), 'label': row[0]}
            points.append(point)
    return points


class Clusters:
    def __init__(self, input_filepath: str):
        self.__labels: Set[str] = set()
        self.__clusters: List[Cluster] = []
        self.__add_points_from_file(input_filepath)

    def __add_points_from_file(self, input_filepath: str):
        for point in read_points(input_filepath):
            self.add_point(point['x'], point['y'], point['label'])

    @property
    def number(self) -> int:
        return len(self.__clusters)

    def add_point(self, x: float, y: float, label: str):
        self.__labels.add(label)
        raise NotImplementedError('TODO')
