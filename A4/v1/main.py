from v1.domain.drone import Drone
from v1.domain.map import Map
from v1.domain.problem_constants import *
from v1.service.solver import Solver


def main():
    map_: Map = Map(MAP_ROWS, MAP_COLUMNS)\
        .add_walls_random(MAP_ADD_WALLS_FILL)\
        .add_sensors_random(MAP_SENSORS)
    drone: Drone = Drone(DRONE_X, DRONE_Y, DRONE_BATTERY)

    solution, duration = Solver(map_, drone).run(ANTS, EPOCHS)

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
