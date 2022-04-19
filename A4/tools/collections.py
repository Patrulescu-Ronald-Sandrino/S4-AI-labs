from typing import List, Any, Callable


def flat_map(list_: List[Any], mapper: Callable[[Any], Any]) -> List[Any]:
    result: List[Any] = []

    for item in list_:
        result.extend(mapper(item))

    return result
