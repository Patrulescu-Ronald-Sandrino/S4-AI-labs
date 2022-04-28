import os.path
import sys
from random import random, randint
from typing import Set

from src.domain.drone import Drone
from src.domain.map import *
from src.domain.problem_constants import *
from src.service.solver import Solver, SolverTools


def get_map_creation_predicate() -> Callable[[int, int], Map.Cell]:
    random_sensors_positions: Set[Tuple[int, int]] = {(randint(0, MAP_ROWS - 1), randint(0, MAP_COLUMNS - 1)) for _ in range(MAP_SENSORS)}

    def map_creation_predicate(row: int, column: int) -> Map.Cell:
        if random_sensors_positions.__contains__((row, column)):
            return Map.Cell.SENSOR
        if random() < MAP_WALLS_FILL:
            return Map.Cell.WALL
        return Map.Cell.EMPTY

    return map_creation_predicate


def reallocate_drone(map_instance: Map, drone: Drone) -> None:
    try:
        if map_instance.surface[drone.row][drone.column] != Map.Cell.EMPTY:
            SolverTools.place_drone_on_empty_cell(map_instance, drone)
    except Exception as e:
        print(f'{e}')
        exit(1)


def print_info(map_instance: Map, drone: Drone) -> None:
    print(map_instance)
    for key, value in map_instance.compute_sensors_gains().items():
        print(f'{key}: {value}')
    print(map_instance.to_texttable())
    print(f'ROWS: {map_instance.rows} COLUMNS: {map_instance.columns} TOTAL: {map_instance.rows * map_instance.columns}')
    #
    walls = map_instance.find_cells(Map.Cell.WALL)  # is slow
    print(f'WALLS {len(walls)}: {walls}')
    sensors = map_instance.find_cells(Map.Cell.SENSOR)  # is slow
    print(f'SENSORS {len(sensors)}: {sensors}')
    print(f"Drone at: {drone.row}, {drone.column}")
    print(map_instance.compute_minimum_distances_between_sensors())


def main():
    # input preparation
    map_filename: str = os.path.join('data', 'map.txt')
    map_instance: Map = MapFactory.from_text_file(map_filename)
    # map_instance: Map = MapBuilder().from_predicate(get_map_creation_predicate(),  MAP_ROWS, MAP_COLUMNS).get()
    # MapWriter.to_text_file(map_instance, os.path.join('data', 'map.txt'))
    drone: Drone = Drone(*DRONE_POSITION, DRONE_ENERGY)
    reallocate_drone(map_instance, drone)  # reallocate the drone on an empty position, if necessary

    # info print
    print_info(map_instance, drone)

    # run the algorithm
    best_ant, duration = Solver(map_instance, drone).run(NUMBER_OF_EPOCHS, NUMBER_OF_ANTS, NUMBER_OF_ITERATIONS)

    # result print
    print(f'It took {duration} second/s')
    if best_ant is None:
        print(f'best ant -> None')
    else:
        print(f'best ant -> fitness: {best_ant.fitness} path: {best_ant.path}')


if __name__ == '__main__':
    main()


