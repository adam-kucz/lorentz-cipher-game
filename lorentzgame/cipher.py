from typing import \
    Any, \
    cast, \
    Dict, \
    Iterable, \
    Iterator, \
    List, \
    Optional, \
    Sequence, \
    Tuple, \
    Union

from .lexicon import Char

## TODO: place it somewhere else where it fits better
WORD_SEPARATOR = ' '

class Bits:
    def __init__(self: 'Bits', n: int = 0) -> None:
        self.__n = n

    def __repr__(self: 'Bits') -> str:
        return '{:02x}'.format(self.__n)

    def __str__(self: 'Bits') -> str:
        return '0x' + str(self)

    def __xor__(self: 'Bits', other: 'Bits') -> 'Bits':
        return Bits(int(self) ^ int(other))

    def __int__(self: 'Bits') -> int:
        return self.__n

## TODO: replace hardcoded functions
## probably with higher level
CHARSET: str = WORD_SEPARATOR + '&l1530b9xy2cn,ho-/7r8wgza.s6\'jkf4ume!qvpitd'
CODES: Iterable[Tuple[Char, Bits]] = \
    [(CHARSET[i], Bits(i)) for i in range(len(CHARSET))]
#     [(' ' if i == 0 else chr(ord('a') - 1 + i), i) \
#      for i in range(1 + ord('z') - ord('a') + 1)]
CHAR_TO_BITS: Dict[Char, Bits] = dict(CODES)
BITS_TO_CHAR: Dict[Bits, Char] = dict((i, c) for (c, i) in CODES)


class Cipher(Sequence[Bits]):
    def __init__(self: 'Cipher',
                 src: Union[str, Iterable[Bits], None] = None) -> None:
        if src is None:
            self.seq: List[Bits] = []
        elif isinstance(src, str):
            self.seq: List[Bits] = [self.__char_to_bits(c) for c in src]
        else:
            self.seq: List[Bits] = list(cast(Iterable[Bits], src))

    @staticmethod
    def __char_to_bits(c: Char) -> Bits:
        return CHAR_TO_BITS[c]

    @staticmethod
    def __bits_to_char(b: Bits) -> Char:
        return BITS_TO_CHAR[b]

    @property
    def word(self: 'Cipher') -> Optional[str]:
        try:
            return ''.join(self.__bits_to_char(b) for b in self.seq)
        except KeyError:
            return None

    def __xor__(self: 'Cipher', other: 'Cipher') -> 'Cipher':
        return Cipher(b1 ^ b2 for b1, b2 in zip(self, other))

    def __len__(self: 'Cipher') -> int:
        return len(self.seq)

    def __getitem__(self: 'Cipher', i: Union[int, slice]) -> Any:
        return self.seq[i]

    def __iter__(self: 'Cipher') -> Iterator[Bits]:
        return iter(self.seq)

    def __add__(self: 'Cipher', other: 'Cipher') -> 'Cipher':
        return Cipher(self.seq + other.seq)

    def __str__(self: 'Cipher') -> str:
        return '0x' + ''.join(repr(bits) for bits in self.seq)

    def __repr__(self: 'Cipher') -> str:
        return str(self)


def xor_pairwise(encrypted: Iterable[Cipher]) -> Dict[int, Dict[int, Cipher]]:
    result: Dict[int, Dict[int, Cipher]] = dict()
    for i1, msg1 in enumerate(encrypted):  # type: int, Cipher
        d: Dict[int, Cipher] = dict()
        other_msgs: Iterable[Tuple[int, Cipher]] = \
            filter(lambda t: t[0] != i1, # pylint: disable=cell-var-from-loop
                   enumerate(encrypted))
        for i2, msg2 in other_msgs:  # type: int, Cipher
            d[i2] = msg1 ^ msg2
        result[i1] = d
    return result
