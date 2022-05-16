from typing import Callable, TypeVar, Dict, Set, Any

T = TypeVar('T')


def create_dictionary_matrix(predicate: Callable[[int, int], T], rows: int, columns: int) -> Dict[int, Dict[int, T]]:
    return {row: {column: predicate(row, column) for column in range(columns)} for row in range(rows)}


def n_th_in_set(set_: Set[T], index: int) -> T:  # TODO END remove if unused
    if index >= len(set_):
        raise ValueError("Out of the set's range")
    for i, value in enumerate(set_):
        if i == index:
            return value


def last_key(dict_: Dict[T, Any]) -> T:
    """
    returns the last key from a dictionary (last = last inserted, https://stackoverflow.com/a/16125343)
    :param dict_:
    :return:
    source: https://stackoverflow.com/questions/16125229/last-key-in-python-dictionary
    """
    return list(dict_)[-1]
