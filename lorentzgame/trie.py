from itertools import chain
from typing import \
    cast, \
    Generic, \
    Iterable, \
    Iterator, \
    MutableMapping, \
    Optional, \
    TypeVar

E = TypeVar('E')
V = TypeVar('V')

class Trie(Generic[E, V], MutableMapping[Iterable[E], V]):
    def __init__(self: 'Trie[E,V]', val: Optional[V] = None) -> None:
        self.val: Optional[V] = val
        self.elems: MutableMapping[E, Trie[E, V]] = dict()

    def __call__(self: 'Trie[E,V]', n: Iterable[E]) -> Optional['Trie[E,V]']:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            return self.elems[e](iterator) if e in self.elems else None
        except StopIteration:
            return self

    def __iter__(self: 'Trie[E,V]') -> Iterator[Iterable[E]]:
        if self.val is not None:
            yield ()
        for e, subtrie in self.elems.items(): # type: E, Trie[E,V]
            for elem in subtrie: # type: Iterable[E]
                yield tuple(chain([e], elem))

    def __getitem__(self: 'Trie[E,V]', n: Iterable[E]) -> V:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            return self.elems[e][iterator]
        except StopIteration:
            if self.val is None:
                raise KeyError("no entry for key")
            return cast(V, self.val)

    def __setitem__(self: 'Trie[E,V]', n: Iterable[E], v: V) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            if e not in self.elems:
                self.elems[e] = Trie[E, V]()
            self.elems[e][iterator] = v
        except StopIteration:
            self.val = v

    def __delitem__(self: 'Trie[E,V]', n: Iterable[E]) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            del self.elems[e][iterator]
        except StopIteration:
            if self.val is None:
                raise KeyError("no entry for key")
            self.val = None

    def __len__(self: 'Trie[E,V]') -> int:
        return (1 if self.val is not None else 0) \
            + sum(map(len, self.elems.values()))

    def __contains__(self: 'Trie[E,V]', n: object) -> bool:
        if isinstance(n, Iterable):
            iterator: Iterator[E] = iter(cast(Iterable[E], n))
            e: E = next(iterator)
            return e in self.elems and iterator in self.elems[e]
        return False

    def __repr__(self: 'Trie[E,V]') -> str:
        return "(" + repr(self.val) + ", " + repr(self.elems) + ")"
