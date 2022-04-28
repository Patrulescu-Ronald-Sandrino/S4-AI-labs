from typing import Callable, TypeVar, Dict


T = TypeVar('T')


def create_dictionary_matrix(predicate: Callable[[int, int], T], rows: int, columns: int) -> Dict[int, Dict[int, T]]:
    return {row: {column: predicate(row, column) for column in range(columns)} for row in range(rows)}
