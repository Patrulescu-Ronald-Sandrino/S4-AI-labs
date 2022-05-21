

class Mean:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def remove_point(self, length: int, x: float, y: float):
        self.x = (self.x * (length + 1) - x) / length
        self.y = (self.y * (length + 1) - y) / length

    def add_point(self, length: int, x: float, y: float):
        self.x = (self.x * (length - 1) + x) / length
        self.y = (self.y * (length - 1) + y) / length
