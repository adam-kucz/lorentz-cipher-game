from typing import Collection, Iterable, Sized, Union

def empty(x: Union[None,Sized,Iterable]) -> bool:
    if x == None:
        return True
    elif isinstance(x, Iterable):
        empty = object()
        return next(iter(x), empty) is empty
    elif isinstance(x, Sized):
        return len(x) == 0
    else:
        raise TypeError("empty(x): x must be Iterable or Sized")

def mean(ls: Collection) -> float:
    return sum(ls) / float(len(ls))
