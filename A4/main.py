import functools
import os.path

from domain.drone import Drone
from domain.map import Map
from domain.problem_constants import *
from gui import GUI
from service.solver import Solver


def main():
    # map_: Map = Map(MAP_ROWS, MAP_COLUMNS)\
    #     .add_walls_random(MAP_ADD_WALLS_FILL)\
    #     .add_sensors_random(MAP_SENSORS)

    map_: Map = Map()
    map_.from_file_text(os.path.join('data', 'map.txt'))
    # print(f'{map_.rows} {map_.columns}')
    # print(map_.__str__())

    # print(map_.to_texttable())
    # print(map_.find_all(Map.CellType.SENSOR))
    # print(map_.compute_sensors_gains())
    # for key, value in map_.compute_sensors_gains(5).items():
    #     print(key, value)
    # return
    drone: Drone = Drone(DRONE_X, DRONE_Y, DRONE_BATTERY)
    print(map_.to_texttable())

    print(f"Sensors: {map_.find_all(Map.CellType.SENSOR)}")

    solution, duration = Solver(map_, drone).run(NUMBER_OF_ANTS, NUMBER_OF_EPOCHS)

    print(f'Drone\'s position: {drone.row} {drone.column}')
    print(f'It took {duration} seconds')
    if solution is not None:
        print(f"Solution size: {len(solution.path)}")
        print(f"Solution: {solution.path}")

        # GUI(map_, solution.path).run()
    else:
        print(f"Solution:", solution)


if __name__ == "__main__":
    main()


"""
TODO:
    1. update self.__fitness value in Ant.move()
    2. implement Solver.epoch()


"""
