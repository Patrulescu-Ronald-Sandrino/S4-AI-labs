import os.path
from random import random, randint
from typing import Set

from src.domain.map import *
from src.domain.problem_constants import *


def get_map_creation_predicate() -> Callable[[int, int], Map.Cell]:
    random_sensors_positions: Set[Tuple[int, int]] = {(randint(0, MAP_ROWS - 1), randint(0, MAP_COLUMNS - 1)) for _ in range(MAP_SENSORS)}

    def map_creation_predicate(row: int, column: int) -> Map.Cell:
        if random_sensors_positions.__contains__((row, column)):
            return Map.Cell.SENSOR
        if random() < MAP_WALLS_FILL:
            return Map.Cell.WALL
        return Map.Cell.EMPTY

    return map_creation_predicate


def main():
    map_filename: str = os.path.join('data', 'map.txt')
    map_instance: Map = MapFactory.from_text_file(map_filename)
    # map_instance: Map = MapBuilder().from_predicate(get_map_creation_predicate(),  MAP_ROWS, MAP_COLUMNS).get()
    # MapWriter.to_text_file(map_instance, os.path.join('data', 'map.txt'))
    print(map_instance)
    print(map_instance.to_texttable())
    print(f'ROWS: {map_instance.rows} COLUMNS: {map_instance.columns} TOTAL: {map_instance.rows * map_instance.columns}')
    # walls = map_instance.find_cells(Map.Cell.WALL)  # is slow
    # print(f'WALLS {len(walls)}: {walls}')
    # sensors = map_instance.find_cells(Map.Cell.SENSOR)  # is slow
    # print(f'SENSORS {len(sensors)}: {sensors}')
    # print(f'SENSORS: {map_instance.find_cells(Map.Cell.SENSOR)}')


if __name__ == '__main__':
    main()


