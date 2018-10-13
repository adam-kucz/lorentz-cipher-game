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

from .lexicon import Char, unpack, CHARSET


class HexInt:
    """Code symbol in binary format"""
    def __init__(self: 'HexInt', n: int = 0) -> None:
        self.__n = n

    def __repr__(self: 'HexInt') -> str:
        return '{:02x}'.format(self.__n)

    def __str__(self: 'HexInt') -> str:
        return '0x' + str(self)

    def __xor__(self: 'HexInt', other: 'HexInt') -> 'HexInt':
        return HexInt(int(self) ^ int(other))

    def __int__(self: 'HexInt') -> int:
        return self.__n


Bits = HexInt

# TODO: replace hardcoded functions
# probably with higher level
CODES: Iterable[Tuple[Char, Bits]] = \
    [(c, Bits(i)) for i, c in enumerate(CHARSET)]
CHAR_TO_BITS: Dict[Char, Bits] = dict(CODES)
BITS_TO_CHAR: Dict[Bits, Char] = dict((i, c) for (c, i) in CODES)


class Cipher(Sequence[Bits]):
    """ a cipher """
    def __init__(self: 'Cipher',
                 src: Union[str, Iterable[Bits], None] = None) -> None:
        if src is None:
            self.seq: List[Bits] = []
        elif isinstance(src, str):
            self.seq: List[Bits] = list(map(self.__char_to_bits, unpack(src)))
        else:
            self.seq: List[Bits] = list(cast(Iterable[Bits], src))

    @staticmethod
    def __char_to_bits(char: Char) -> Bits:
        return CHAR_TO_BITS[char]

    @staticmethod
    def __bits_to_char(bits: Bits) -> Char:
        return BITS_TO_CHAR[bits]

    @property
    def string(self: 'Cipher') -> Optional[str]:
        """
        Interpret the cipher as a string

        :returns: Optional[str]: string of this cipher if possible,
        None otherwise
        """
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
