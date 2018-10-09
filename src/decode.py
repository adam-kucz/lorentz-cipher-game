from collections import deque
from itertools import chain
from typing import cast
from typing import Optional, Tuple, Union
from typing import Deque, Iterator, Mapping, MutableMapping, Sequence
from typing import Generic, TypeVar

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

Char = str
Bits = int
E = TypeVar('E')
V = TypeVar('V')
Lexicon = Trie[Char,str]

class Trie(Generic[E,V]):
    def __init__(self: Trie[E,V], val: Optional[V] = None) -> None:
        self.val: Optional[V] = val
        self.elems: Mapping[E,Trie[E,V]] = dict()
        
    def __iter__(self: Trie[E,V]) -> Iterator[Tuple[Deque[E],V]]:
        if self.val != None:
            yield (deque(), cast(V, self.val))
        for e, trie in self.elems.items():
            for dq, v in trie:
                dq.appendleft(e)
                yield (dq, v)

    def __getitem__(self: Trie[E,V], n: Iterator[E]) -> V:
        try:
            e: E = next(n)
            return self.elems[e][n]
        except StopIteration:
            if self.val != None:
                return cast(V, self.val)
            else:
                raise KeyError("no entry for key")

    def __setitem__(self: Trie[E,V], n: Iterator[E], v: V) -> None:
        try:
            e: E = next(n)
            self.elems[e][n] = v
        except StopIteration:
            self.val = v
            
def get_words_basic(filename: str) -> Lexicon:
    trie: Lexicon = Trie()
    with open(filename, 'r') as f:
        for line in f:
            word: str = line[:-1]
            trie[(c for c in word)] = word
    return trie

def char_to_bits(c: Char) -> Bits:
    ## TODO: implement
    return 0

def bits_to_char(bits: Bits) -> Char:
    ## TODO: implement
    return '0'

def xor(encrypted1: str, encrypted2: str) -> str:
    bit_seq1: Iterator[Bits] = (char_to_bits(c) for c in encrypted1)
    bit_seq2: Iterator[Bits] = (char_to_bits(c) for c in encrypted2)
    bit_seq_out: Iterator[Bits] = (b1 ^ b2 for b1,b2 in zip(bit_seq1, bit_seq2))
    str_out: str = ''.join(bits_to_char(bits) for bits in bit_seq_out)
    return str_out

def xor_pairwise(encrypted: Sequence[str]) -> Mapping[int, Mapping[int, str]]:
    result: MutableMapping[int, MutableMapping[int, str]] = dict()
    for i1, msg1 in enumerate(encrypted):
        d: MutableMapping[int,str] = dict()
        for i2, msg2 in filter(lambda t: t[0] != i1, enumerate(encrypted)):
            d[i2] = xor(msg1, msg2)
        result[i1] = d
    return result

def score_decryption(word: str, encrypted: Sequence[str]) -> float:
    ## TODO: implement
    return 0

def decrypt(vocabulary: Lexicon, encrypted: Sequence[str]) -> Sequence[str]:
    ## TODO: implement
    return []

if __name__=='__main__':
    vocabulary: Lexicon = get_words_basic(WORDS_BASIC_PATH)
    encrypted: Sequence[str] = open(ENCRYPTED_PATH).readlines()
    decrypt(vocabulary, encrypted)
