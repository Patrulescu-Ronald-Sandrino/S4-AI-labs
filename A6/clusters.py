from typing import Dict

from domain.cluster import Cluster


class Clusters:
    def __init__(self):
        self.__clusters: Dict[str, Cluster] = {}

    @property
    def number(self) -> int:
        return len(self.__clusters)

    def add_point(self, label: str, ):