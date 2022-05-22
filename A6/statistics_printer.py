from typing import Set, Dict, Optional, List

import texttable

from domain.centroid import Centroid
from domain.point import Point


class StatisticsPrinter:
    def __init__(self,
                 labels: Dict[str, None],
                 centroids: Set[Centroid],
                 occurrences: Dict[str, Dict[Centroid, int]],
                 labels_to_centroids: Dict[str, Optional[Centroid]],
                 statistics: Dict[str, List[float]]):

        self.__labels = labels
        self.__centroids: Set[Centroid] = centroids
        self.__occurrences: Dict[str, Dict[Centroid, int]] = occurrences
        self.__labels_to_centroids: Dict[str, Optional[Centroid]] = labels_to_centroids
        self.__statistics: Dict[str, List[float]] = statistics

    def print(self):
        print(self.__get_occurrences_texttable().draw())
        print()
        print(self.__get_labels_texttable().draw())
        print()
        # print(self.__get_statistics_texttable().draw())
        print()

    # LEVEL 2

    def __get_occurrences_texttable(self) -> texttable.Texttable:
        table = texttable.Texttable()

        table.set_cols_width([20 for _ in range(len(self.__labels) + 1)])
        self.__add_centroid_headers_rows(table, self.__centroids)
        for label, label_occurrences_per_centroid in self.__occurrences.items():
            table.add_row([label] + [str(self.__occurrences[label][centroid]) for centroid in self.__centroids])

        return table
    
    def __get_labels_texttable(self) -> texttable.Texttable:
        table: texttable.Texttable = texttable.Texttable()

        table.set_cols_align(['c' for _ in range(len(self.__centroids) + 1)])
        table.set_cols_width([18 for _ in range(len(self.__centroids) + 1)])
        self.__add_centroid_headers_rows(table, self.__centroids)
        centroids_to_labels: Dict[Optional[Centroid], str] = {centroid: label for label, centroid in self.__labels_to_centroids.items()}
        table.add_row(['label'] + [centroids_to_labels[centroid] for centroid in self.__centroids])

        return table

    def __get_statistics_texttable(self) -> texttable.Texttable:
        table: texttable.Texttable = texttable.Texttable()
        header: List[str] = ['', 'accuracy', 'precision', 'rappel', 'score']

        table.set_cols_align(['c' for _ in range(len(header))])
        table.add_row(header)
        for row_name, row_data in self.__statistics.items():
            table.add_row([row_name] + row_data)

        return table

    # LEVEL 3

    def __add_centroid_headers_rows(self, table, centroids):
        # the following line is required to print the id's as int, not in scientific notation
        # @search: texttable printing big numbers in scientific notation
        #   https://stackoverflow.com/questions/16362093/python-converts-long-number-to-float-i-believe-example-x-xxxeyy
        table.set_cols_dtype(['a'] + ['i' for _ in range(len(self.__labels))])
        table.add_row(['id'] + [f'{id(centroid)}' for centroid in centroids])
        table.set_cols_dtype(['a'] + ['a' for _ in range(len(self.__labels))])  # revert columns types to automatic
        table.add_row(['hex(id)'] + [f'{hex(id(centroid))}' for centroid in centroids])
        table.add_row(['mean'] + [f'({round(centroid.x, 4)}, {round(centroid.y, 4)})' for centroid in centroids])
