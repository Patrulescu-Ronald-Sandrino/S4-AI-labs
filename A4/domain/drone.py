from typing import Tuple


class Drone:
    def __init__(self, row: int, column: int, energy: int):
        self.row = row
        self.column = column
        self.energy = energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.row, self.column
