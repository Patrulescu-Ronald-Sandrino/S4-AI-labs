from v1.domain.drone import Drone
from v1.domain.map import Map
from v1.domain.problem_constants import *
from v1.service.solver import Solver


def main():
    map_: Map = Map(MAP_ROWS, MAP_COLUMNS)\
        .add_walls_random(MAP_ADD_WALLS_FILL)\
        .add_sensors_random(MAP_SENSORS)
    # print(map_.to_texttable())
    # print(map_.find_all(Map.CellType.SENSOR))
    # print(map_.compute_sensors_gains())
    # for key, value in map_.compute_sensors_gains(5).items():
    #     print(key, value)
    # return
    drone: Drone = Drone(DRONE_X, DRONE_Y, DRONE_BATTERY)

    solution, duration = Solver(map_, drone).run(NUMBER_OF_ANTS, NUMBER_OF_EPOCHS)

    print(f'Drone\'s position: {drone.row} {drone.column}')
    print(f'It took {duration} seconds')
    if solution:
        print(f"Solution size: {len(solution)}")
    print(f"Solution: {solution}")


if __name__ == "__main__":
    main()


"""
TODO:
    1. copy compute sensors_gain


"""
