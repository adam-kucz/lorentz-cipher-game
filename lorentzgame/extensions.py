from typing import \
    Collection, \
    Iterable, \
    Optional, \
    Sized, \
    TypeVar, \
    Union

A = TypeVar('A')


def unsafe_first(ls: Iterable[A]) -> bool:
    """

    :param ls: Iterable[A]: 

    """
    try:
        return next(iter(ls))
    except StopIteration:
        raise ValueError("Cannot take first element of empty iterable")


def first(ls: Iterable[A]) -> Optional[A]:
    """

    :param ls: Iterable[A]: 

    """
    try:
        return unsafe_first(ls)
    except ValueError:
        return None


def empty(x: Union[None, Sized, Iterable]) -> bool:
    """

    :param x: Union[None: 
    :param Sized: 
    :param Iterable]: 

    """
    if x is None:
        return False
    if isinstance(x, Iterable):
        return first(x) is not None
    return len(x) > 0


def mean(ls: Collection) -> float:
    """

    :param ls: Collection: 

    """
    return sum(ls) / float(len(ls))

# @overload # pylint: disable=undefined-variable
# def mapdict(d: MutableMapping[K, A], f: Callable[[A], B]) -> Dict[K, B]: \
#     # pylint: disable=unused-argument
#     pass
# @overload # pylint: disable=undefined-variable
# def mapdict(d: Mapping[K, A], f: Callable[[A], B]) -> Mapping[K, B]: \
#     # pylint: disable=function-redefined, unused-argument
#     pass

# def mapdict(d: Mapping[K, A], f: Callable[[A], B]) -> Dict[K, B]: \
#     # pylint: disable=function-redefined
#     newpairs: Iterable[Tuple[K, B]] = ((k, f(d[k])) for k in d)
#     if isinstance(d, MutableMapping[K, A]):
#         d.update(newpairs)
#         return d
#     return dict(newpairs)
