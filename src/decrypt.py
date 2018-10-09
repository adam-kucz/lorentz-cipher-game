from typing import Iterable, Dict, Sequence, Tuple

from decryption_state import WORD_SEPARATOR
from lexicon import Char

Bits = int

## TODO: replace hardcoded functions
## probably with higher level
CHARSET: str = WORD_SEPARATOR + '&l1530b9xy2cn,ho-/7r8wgza.s6\'jkf4ume!qvpitd'
CODES: Iterable[Tuple[Char,Bits]] = \
    [(CHARSET[i], i) for i in range(len(CHARSET))]
#     [(' ' if i == 0 else chr(ord('a') - 1 + i), i) \
#      for i in range(1 + ord('z') - ord('a') + 1)]
CHAR_TO_BITS: Dict[Char,Bits] = dict(CODES)
BITS_TO_CHAR: Dict[Bits,Char] = dict((i,c) for (c,i) in CODES)

def char_to_bits(c: Char) -> Bits:
    return CHAR_TO_BITS[c]

def bits_to_char(bits: Bits) -> Char:
    return BITS_TO_CHAR[bits]

def xor(encrypted1: str, encrypted2: str) -> str:
    bit_seq1: Iterable[Bits] = (char_to_bits(c) for c in encrypted1.lower())
    bit_seq2: Iterable[Bits] = (char_to_bits(c) for c in encrypted2.lower())
    bit_seq_out: Iterable[Bits] = (b1 ^ b2 for b1,b2 in zip(bit_seq1, bit_seq2))
    str_out: str = ''.join(bits_to_char(bits) for bits in bit_seq_out)
    return str_out

def xor_pairwise(encrypted: Sequence[str]) -> Dict[int, Dict[int, str]]:
    result: Dict[int, Dict[int, str]] = dict()
    for i1, msg1 in enumerate(encrypted):
        d: Dict[int,str] = dict()
        for i2, msg2 in filter(lambda t: t[0] != i1, enumerate(encrypted)):
            d[i2] = xor(msg1, msg2)
        result[i1] = d
    return result
