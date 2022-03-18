import abc
import time
from typing import Tuple, List, Any

import domain.Map
from domain.constants import DUMMY_SEARCH_PATH, DIRECTIONS


class PathSearcher:
    @staticmethod
    @abc.abstractmethod
    def get_name():
        raise NotImplementedError("PathSearcher.get_name() is pure virtual")

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, metaclass=abc.ABCMeta):
        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y
        self._path = []
        self._time = -1

    def run(self, detected_map: domain.Map) -> Tuple[List[Tuple[int, int]], float]:
        start_time = time.time()  # start counting the time passed
        self.__universal_run_prepare()  # set _found, _visited and _to_visit
        self.__searcher_run_prepare()  # set values specific to the PathSearcher instance

        while len(self._to_visit) > 0 and not self._found:
            node = (x, y) = self._to_visit.pop(0)
            self._visited[node] = True

            if node == (self._end_x, self._end_y):
                found = True
            else:
                aux = []
                for (delta_x, delta_y) in DIRECTIONS:
                    new_position = (new_x, new_y) = x + delta_x, y + delta_y
                    if detected_map.is_position_valid(new_x, new_y) and new_position not in self._visited:
                        self.__add()  # TODO: change call arguments

                self._to_visit.extend(aux)
                self.__sort()  # TODO: change call arguments

        self._path = [] if self._found else []  # TODO: replace first [] with build path
        end_time = time.time()  # stop counting the time passed
        self._time = end_time - start_time
        return self._path, self._time

    def __universal_run_prepare(self):
        self._found = False
        self._visited = dict()
        self._to_visit = [(self._start_x, self._start_y)]

    @abc.abstractmethod
    def __searcher_run_prepare(self):
        raise NotImplementedError("PathSearcher.__prepare_for_run() is pure virtual")

    @abc.abstractmethod
    def __add(self):
        raise NotImplementedError("PathSearcher.__add() is pure virtual")

    @abc.abstractmethod
    def __sort(self):
        raise NotImplementedError("PathSearcher.__sort() is pure virtual")

    @staticmethod
    def run_result_to_string(algorithm_name: str, path: list, search_time: float) -> str:
        result = str()

        result += 'Algorithm: ' + algorithm_name + '\n'
        result += 'Time: ' + str(search_time) + '\n'
        if len(path) == 0:
            result += "Path: doesn't exist\n"
        else:
            result += "Path\n" + str(path)

        return result

    def __str__(self) -> str:
        return self.run_result_to_string(self.get_name(), self._path, self._time)


class PathSearcherAStar(PathSearcher):
    @staticmethod
    def get_name():
        return "A*"

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        super().__init__(start_x, start_y, end_x, end_y)

    def __searcher_run_prepare(self):
        # TODO
        pass

    def __add(self):
        # TODO
        pass

    def __sort(self):
        # TODO
        pass


class PathSearcherGreedy(PathSearcher):
    @staticmethod
    def get_name():
        return "Greedy"

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        super().__init__(start_x, start_y, end_x, end_y)

    def __searcher_run_prepare(self):
        # TODO
        pass

    def __add(self):
        # TODO
        pass

    def __sort(self):
        # TODO
        pass


class PathSearcherDummy(PathSearcher):
    @staticmethod
    def get_name():
        return "dummy_search"

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        super().__init__(start_x, start_y, end_x, end_y)

    def run(self, detected_map: domain.Map) -> Tuple[List[Tuple[int, int]], float]:
        self._path = DUMMY_SEARCH_PATH
        self._time = 0

        return self._path, self._time

    def __searcher_run_prepare(self):
        pass

    def __add(self):
        pass

    def __sort(self):
        pass
