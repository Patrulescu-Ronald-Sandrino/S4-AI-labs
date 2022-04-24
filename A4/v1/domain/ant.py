from random import random, randint
from typing import List, Dict, Tuple, Optional

import tools.collections
from v1.domain.drone import Drone
from v1.domain.map import Direction, DIRECTION_DELTA, Map
from v1.domain.problem_constants import MAX_SENSOR_CAPACITY, ALPHA, BETA, Q0


class Ant:
    def __init__(self, drone: Drone, map_: Map):
        self.__path: Dict[Tuple[int, int], int] = {drone.position: 0}
        self.__battery = drone.energy
        self.__map = map_
        self.__fitness: int = 0
        self.__spent_energy = tools.collections.create_matrix(lambda row, column: 0, self.__map.rows, self.__map.columns)

    @property
    def path(self) -> Dict[Tuple[int, int], int]:
        return self.__path

    @property
    def fitness(self) -> int:
        return self.__fitness

    def __get_potential_neighbours(self, trace: List[List[Dict[Direction, List[float]]]]) -> Dict[Direction, Dict[Tuple[int, int], int]]:
        current_row, current_column = next(reversed(self.__path.values()))  # python get the last added value in a dictionary https://stackoverflow.com/a/63059166/17299754
        # potential_neighbours = {}  # type: Dict[Direction, Dict[Tuple[int, int], int]]
        potential_neighbours: Dict[Direction, Dict[Tuple[int, int], int]] = {}

        for direction in Direction:
            for energy_level in range(min(MAX_SENSOR_CAPACITY + 1, self.__battery)):  # TODO: maybe its self.__battery + 1 instead
                if tau := trace[current_row][current_column][direction] != 0:
                    delta_column, delta_row = DIRECTION_DELTA[direction]
                    next_position = next_row, next_column = current_row + delta_row, current_column + delta_column

                    if self.__spent_energy[next_row][next_column] <= energy_level and next_position not in self.__path:
                        potential_neighbours[direction] = {next_position: energy_level}

        return potential_neighbours

    @staticmethod
    def compute_transition_probability(pheromone_concentration: float, visibility: float) -> float:
        return (pheromone_concentration ** ALPHA) * (visibility ** BETA)

    @staticmethod
    def compute_transitions_probabilities(potential_neighbours: Dict[Direction, Dict[Tuple[int, int], int]], trace: List[List[Dict[Direction, List[float]]]]) -> Dict[Direction, Dict[Tuple[int, int], float]]:
        transition_probabilities: Dict[Direction, Dict[Tuple[int, int], float]] = {}

        for direction in potential_neighbours.keys():
            (row, column), energy_level = list(potential_neighbours[direction].items())[0]
            transition_probability: float = Ant.compute_transition_probability(trace[row][column][direction][energy_level], 1 / (energy_level + 1))

            transition_probabilities[direction] = {(row, column): transition_probability}

        return transition_probabilities

    @staticmethod
    def find_position_with_highest_transition_probability(transition_probabilities: Dict[Direction, Dict[Tuple[int, int], float]]) -> Optional[Tuple[Direction, Tuple[int, int]]]:
        position_with_highest_transition_probability: Optional[Tuple[Direction, Tuple[int, int]]] = None
        highest_transition_probability: int = -1

        for direction in transition_probabilities.keys():
            (row, column), transition_probability = list(transition_probabilities.items())[0]

            if transition_probability > highest_transition_probability:
                position_with_highest_transition_probability = direction, (row, column)
                highest_transition_probability = transition_probability

        return position_with_highest_transition_probability

    @staticmethod
    def transition_probabilities_as_list(transition_probabilities: Dict[Direction, Dict[Tuple[int, int], float]]) -> List[Tuple[Direction, Tuple[int, int], float]]:
        result: List[Tuple[Direction, Tuple[int, int], float]] = []

        for direction in transition_probabilities.keys():
            (row, column), transition_probability = list(transition_probabilities.items())[0]

            result.append((direction, (row, column), transition_probability))

        return result

    def move(self, trace: List[List[Dict[Direction, List[float]]]]) -> bool:
        potential_neighbours: Dict[Direction, Dict[Tuple[int, int], int]] = self.__get_potential_neighbours(trace)

        if len(potential_neighbours) == 0:
            return False

        transition_probabilities: Dict[Direction, Dict[Tuple[int, int], float]] = Ant.compute_transitions_probabilities(
            potential_neighbours, trace)

        next_path_move: Tuple[Tuple[int, int], int]
        if random() < Q0 and (result := Ant.find_position_with_highest_transition_probability(transition_probabilities)) is not None:
            direction, position = result
            next_path_move = position, potential_neighbours[direction][position]
        else:
            if Ant.find_position_with_highest_transition_probability(transition_probabilities) is None:
                print(f'[log] Ant.find_position_with_highest_transition_probability(transition_probabilities) failed')

            direction, position = Ant.roulette(Ant.transition_probabilities_as_list(transition_probabilities))
            next_path_move = position, potential_neighbours[direction][position]

        (row, column), energy = next_path_move
        self.__path[(row, column)] = energy
        self.__battery -= energy + 1
        self.__spent_energy[row][column] = energy
        self.__update_fitness()

        return True

    def __update_fitness(self) -> None:
        marked_sensors_map: List[List[int]] = tools.collections.create_matrix(lambda row, column: 0, self.__map.rows, self.__map.columns)

        for position, energy in self.__path.items():
            if self.__map.at(position) != Map.CellType.SENSOR:
                continue

            for direction in Direction:
                for energy_level in range(energy):
                    current_row, current_column = Map.shift_position(position, direction, energy_level)

                    if self.__map.surface[current_row][current_column] == Map.CellType.WALL:
                        break

                    marked_sensors_map[current_row][current_column] = 1

        self.__fitness = sum([sum(row) for row in marked_sensors_map])

    @staticmethod
    def roulette(transition_probabilities: List[Tuple[Direction, Tuple[int, int], float]]) -> Tuple[Direction, Tuple[int, int]]:
        probabilities_sum: float = sum(map(lambda entry: entry[2], transition_probabilities))

        if probabilities_sum == 0:
            return transition_probabilities[randint(0, len(transition_probabilities) - 1)][:2]

        cumulative_distribution_function: List[float] = [transition_probabilities[0][2] / probabilities_sum]
        for index in range(1, len(transition_probabilities)):
            cumulative_distribution_function.append((cumulative_distribution_function[index - 1] + transition_probabilities[index][2]) / probabilities_sum)

        random_value: float = random()
        index: int = 0
        while random_value > random():
            index += 1

            if index == len(transition_probabilities):
                return transition_probabilities[randint(0, len(transition_probabilities) - 1)][:2]

        return transition_probabilities[index][:2]
