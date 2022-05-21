from typing import Set, Tuple


class Centroid:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.points_indices: Set[int] = set()

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def remove_point(self, index: int, x: float, y: float):
        self.points_indices.remove(index)
        length = len(self.points_indices)
        self.x = (self.x * (length + 1) - x) / length
        self.y = (self.y * (length + 1) - y) / length

    def add_point(self, index: int, x: float, y: float):
        self.points_indices.add(index)
        length = len(self.points_indices)
        self.x = (self.x * (length - 1) + x) / length
        self.y = (self.y * (length - 1) + y) / length

    def __str__(self) -> str:
        result: str = f'Centroid:\n'

        # result += f'id: {id(self)}\n'
        # result += f'id: {hex(id(self))}\n'
        result += f'mean: {round(self.x, 4)} {round(self.y, 4)}\n'
        result += f'len(points_indices): {len(self.points_indices)}\n'
        result += f'points_indices: {self.points_indices}\n'
        
        return result

