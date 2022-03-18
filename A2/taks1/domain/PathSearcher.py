import abc
import time
from typing import Tuple, List, Any, Dict

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
        self._found = False
        self._prev = dict()
        self._path = []
        self._time = -1

    @staticmethod
    def previous_dictionary_to_path(previous: Dict[Tuple[int, int], Tuple[int, int]], final_x: int, final_y: int) -> \
            List[Tuple[int, int]]:
        reversed_path = []
        current = final_x, final_y

        while previous[current] != (None, None):
            reversed_path.append(current)
            current = previous[current]

        reversed_path.append(current)  # add the last value for current (which should be (start_x, start_y))

        reversed_path.reverse()
        path = reversed_path

        return path

    def _universal_run_prepare(self):
        start = (self._start_x, self._start_y)

        self._found = False
        self._visited = dict()
        self._to_visit = [start]
        self._prev = {start: (None, None)}

    @abc.abstractmethod
    def run(self, detected_map: domain.Map):
        raise NotImplementedError("PathSearcher.run() is pure virtual")

    def _run(self, detected_map: domain.Map, searcher_run_prepare, add_to_queue, sort_queue) -> Tuple[
        List[Tuple[int, int]], float]:
        start_time = time.time()  # start counting the time passed
        self._universal_run_prepare()  # set _found, _visited and _to_visit
        searcher_run_prepare()  # set values specific to the PathSearcher instance

        while len(self._to_visit) > 0 and not self._found:
            current_node = (x, y) = self._to_visit.pop(0)
            self._visited[current_node] = True

            if current_node == (self._end_x, self._end_y):
                self._found = True
            else:
                aux = []
                for (delta_x, delta_y) in DIRECTIONS:
                    new_node = (new_x, new_y) = x + delta_x, y + delta_y
                    if detected_map.is_position_valid(new_x, new_y) and new_node not in self._visited:
                        add_to_queue(aux, current_node, new_node)

                self._to_visit.extend(aux)
                sort_queue()

        self._path = self.previous_dictionary_to_path(self._prev, self._end_x, self._end_y) if self._found else []
        end_time = time.time()  # stop counting the time passed
        self._time = end_time - start_time
        return self._path, self._time

    @staticmethod
    def heuristic_manhattan_distance(start: Tuple[int, int], end: Tuple[int, int]) -> int:
        (start_x, start_y) = start
        (end_x, end_y) = end
        return abs(start_x - end_x) + abs(start_y - end_y)

    @abc.abstractmethod
    def _searcher_run_prepare(self):
        raise NotImplementedError("PathSearcher.__prepare_for_run() is pure virtual")

    @abc.abstractmethod
    def _add_to_queue(self, aux: List[Tuple[int, int]], current_node: Tuple[int, int], new_node: Tuple[int, int]):
        raise NotImplementedError("PathSearcher.__add_to_queue() is pure virtual")

    @abc.abstractmethod
    def _sort_queue(self):
        raise NotImplementedError("PathSearcher.__sort_queue() is pure virtual")

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
        self._number_of_steps = dict()

    def run(self, detected_map: domain.Map):
        return self._run(detected_map, self._searcher_run_prepare, self._add_to_queue, self._sort_queue)

    def _searcher_run_prepare(self):
        self._number_of_steps = {(self._start_x, self._start_y): 0}

    def _add_to_queue(self, aux: List[Tuple[int, int]], current_node: Tuple[int, int], new_node: Tuple[int, int]):
        # TODO
        if new_node in self._to_visit and self._number_of_steps[new_node] > self._number_of_steps[current_node] + 1:
            self._to_visit.remove(new_node)
        aux.append(new_node)
        self._prev[new_node] = current_node
        self._number_of_steps[new_node] = 1 + self._number_of_steps[current_node]

    def _sort_queue(self):
        end = (self._end_x, self._end_y)
        self._to_visit.sort(key=lambda coordinates: self._number_of_steps[coordinates] + self.heuristic_manhattan_distance(coordinates, end))


class PathSearcherGreedy(PathSearcher):
    @staticmethod
    def get_name():
        return "Greedy"

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        super().__init__(start_x, start_y, end_x, end_y)

    def run(self, detected_map: domain.Map) -> Tuple[List[Tuple[int, int]], float]:
        return self._run(detected_map, self._searcher_run_prepare, self._add_to_queue, self._sort_queue)

    def _searcher_run_prepare(self):
        pass

    def _add_to_queue(self, aux: List[Tuple[int, int]], current_node: Tuple[int, int],
                      new_node: Tuple[int, int]) -> None:
        aux.append(new_node)
        self._prev[new_node] = current_node

    def _sort_queue(self):
        end = (self._end_x, self._end_y)
        self._to_visit.sort(key=lambda coordinates: self.heuristic_manhattan_distance(coordinates, end))


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

    def _searcher_run_prepare(self):
        pass

    def _add_to_queue(self, aux: List[Tuple[int, int]], current_node: Tuple[int, int], new_node: Tuple[int, int]):
        pass

    def _sort_queue(self):
        pass
