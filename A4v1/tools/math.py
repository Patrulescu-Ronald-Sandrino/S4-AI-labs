

# def in_range(value: float, lowest: float, highest: float) -> bool:
#     return lowest <= value <= highest
from typing import Tuple


def out_of_range(value: int, lowest: int, highest: int) -> bool:
    return value < lowest or value > highest

