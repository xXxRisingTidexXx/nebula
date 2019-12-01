from argparse import Namespace
from typing import Callable, Iterable, Any, Optional, Tuple


def check_namespace(namespace: Namespace) -> Tuple[str, str, int]:
    if namespace.housing not in {'primary', 'secondary'}:
        raise RuntimeError(
            f'Housing must be either primary or secondary, '
            f'but provided: {namespace.housing}'
        )
    k = int(namespace.k)
    if k <= 1:
        raise RuntimeError(f'K must be greater than 1, but provided: {k}')
    return namespace.locality, namespace.housing, k


def find(
    predicate: Callable,
    iterable: Iterable,
    default: Optional[Any] = None
) -> Optional[Any]:
    return next(filter(predicate, iterable), default)
