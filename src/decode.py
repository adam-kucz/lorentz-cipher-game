from collections import deque
from itertools import chain
from typing import Any, cast
from typing import Optional, Tuple, Union
from typing import Iterable, Iterator, Mapping, MutableMapping, Sequence
from typing import Generic, TypeVar

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

E = TypeVar('E')
V = TypeVar('V')

class Trie(Generic[E,V], MutableMapping[Iterable[E], V]):
    def __init__(self: Trie[E,V], val: Optional[V] = None) -> None:
        self.val: Optional[V] = val
        self.elems: MutableMapping[E,Trie[E,V]] = dict()
    
    def __iter__(self: Trie[E,V]) -> Iterator[Iterable[E]]:
        if self.val != None:
            yield iter([])
        for e, subtrie in self.elems.items():
            for elem in subtrie:
                yield chain([e], elem)
    
    def __getitem__(self: Trie[E,V], n: Iterable[E]) -> V:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            return self.elems[e][iterator]
        except StopIteration:
            if self.val != None:
                return cast(V, self.val)
            else:
                raise KeyError("no entry for key")
    
    def __setitem__(self: Trie[E,V], n: Iterable[E], v: V) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            if e not in self.elems:
                self.elems[e] = Trie()
            self.elems[e][n] = v
        except StopIteration:
            self.val = v
    
    def __delitem__(self: Trie[E,V], n: Iterable[E]) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            del self.elems[e][iterator]
        except StopIteration:
            if self.val != None:
                self.val = None
            else:
                raise KeyError("no entry for key")
    
    def __len__(self: Trie[E,V]) -> int:
        return (1 if self.val is not None else 0) \
            + sum(map(len, self.elems.values()))
    
    def __contains__(self: Trie[E,V], n: Any) -> bool:
        if isinstance(n, Iterable):
            iterator: Iterator[E] = iter(cast(Iterable[E], n))
            e: E = next(iterator)
            return e in self.elems and iterator in self.elems[e]
        else:
            return False
    
    def __repr__(self: Trie[E,V]) -> str:
        return "(" + repr(self.val) + ", " + repr(self.elems) + ")"

Char = str
Bits = int
Lexicon = Trie[Char,str]

WORD_SEPARATOR = " "

class PartiallyDecrypted:
    def __init__(
            self: PartiallyDecrypted,
            encrypted: str,
            lexicon: Lexicon) -> None:
        self.encrypted: str = encrypted
        self.pos: int = 0
        self.decrypted: str = ""
        self.lexicon: Lexicon = lexicon
    
    def score_next_seq(self: PartiallyDecrypted, seq: str) -> float:
        i: int = self.decrypted.rfind(WORD_SEPARATOR)
        if i == -1:
            i = 0
        relevant_enc = self.encrypted[i:]
        relevant_dec = self.decrypted[i:]
        return 0
    
def char_to_bits(c: Char) -> Bits:
    ## TODO: implement
    return 0

def bits_to_char(bits: Bits) -> Char:
    ## TODO: implement
    return '0'

def xor(encrypted1: str, encrypted2: str) -> str:
    bit_seq1: Iterable[Bits] = (char_to_bits(c) for c in encrypted1)
    bit_seq2: Iterable[Bits] = (char_to_bits(c) for c in encrypted2)
    bit_seq_out: Iterable[Bits] = (b1 ^ b2 for b1,b2 in zip(bit_seq1, bit_seq2))
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

def get_words_basic(filename: str) -> Lexicon:
    trie: Lexicon = Trie()
    with open(filename, 'r') as f:
        for line in f:
            word: str = line[:-1]
            trie[(c for c in word)] = word
    return trie

def score_next_seq(
        seq: str,
        partial_encryptions: Sequence[PartiallyDecrypted])-> float:
    s: float = sum(enc.score_next_seq(seq) for enc in partial_encryptions)
    l: int = len(partial_encryptions)
    return s / l

def decrypt(vocabulary: Lexicon, encrypted: Sequence[str]) -> Sequence[str]:
    ## TODO: implement
    return []

if __name__=='__main__':
    vocabulary: Lexicon = get_words_basic(WORDS_BASIC_PATH)
    encrypted: Sequence[str] = open(ENCRYPTED_PATH).readlines()
    decrypt(vocabulary, encrypted)
