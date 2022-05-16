from typing import Tuple


MAP_ROWS: int = 20
MAP_COLUMNS: int = 20
MAP_WALLS_FILL: float = 0.2
# MAP_SENSORS: int = 7
MAP_SENSORS: int = 8
MAX_SENSOR_CAPACITY: int = 5


DRONE_POSITION: Tuple[int, int] = 7, 12
# DRONE_ENERGY: int = 100
DRONE_ENERGY: int = 200


# NUMBER_OF_EPOCHS: int = 25
NUMBER_OF_EPOCHS: int = 100
# NUMBER_OF_ANTS: int = 80
NUMBER_OF_ANTS: int = MAP_SENSORS * 4
NUMBER_OF_ITERATIONS: int = DRONE_ENERGY  # TODO: if -1, then stop when battery runs out

# ALPHA: float = 0.8
# BETA: float = 1.5
# Q0: float = 0.05
# RHO: float = 0.5
ALPHA: float = 1.9
BETA: float = 0.9
Q0: float = 0.05
RHO: float = 0.5

