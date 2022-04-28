from typing import Tuple


class Drone:
    def __init__(self, row: int, column: int, energy: int):
        self.row = row
        self.column = column
        self.__energy = energy

    @property
    def energy(self) -> int:
        return self.__energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.row, self.column

    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self.row, self.column = position
