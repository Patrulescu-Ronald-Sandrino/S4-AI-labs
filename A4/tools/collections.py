from typing import List, Any, Callable, TypeVar

T = TypeVar('T')


def flat_map(list_: List[List[T]], predicate: Callable[[List[T]], List[Any]]) -> List[Any]:
    result: List[Any] = []

    for item in list_:
        result.extend(predicate(item))

    return result


def create_matrix(predicate: Callable[[int, int], T], rows: int, columns: int = None) -> List[List[T]]:
    return [[predicate(row, column) for column in range(rows if columns is None else columns)] for row in range(rows)]
