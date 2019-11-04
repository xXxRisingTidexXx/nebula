from typing import Callable, Iterable, Any, Optional


def find(
    predicate: Callable,
    iterable: Iterable,
    default: Optional[Any] = None
) -> Optional[Any]:
    return next(filter(predicate, iterable), default)
