from collections import deque
from itertools import chain
from typing import \
    Any, \
    cast, \
    Collection, \
    Dict, \
    Generic, \
    Iterable, \
    Iterator, \
    Mapping, \
    MutableMapping, \
    List, \
    Optional, \
    Sequence, \
    Sized, \
    Tuple, \
    TypeVar, \
    Union

E = TypeVar('E')
V = TypeVar('V')

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

class Trie(Generic[E,V], Dict[Iterable[E], V]):
    def __init__(self: 'Trie[E,V]', val: Optional[V] = None) -> None:
        self.val: Optional[V] = val
        self.elems: MutableMapping[E,Trie[E,V]] = dict()
    
    def __call__(self: 'Trie[E,V]', n: Iterable[E]) -> Optional['Trie[E,V]']:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            return self.elems[e](iterator) if e in self.elems else None
        except StopIteration:
            return self
        
    def __iter__(self: 'Trie[E,V]') -> Iterator[Iterable[E]]:
        if self.val != None:
            yield iter([])
        for e, subtrie in self.elems.items():
            for elem in subtrie:
                yield chain([e], elem)
    
    def __getitem__(self: 'Trie[E,V]', n: Iterable[E]) -> V:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            return self.elems[e][iterator]
        except StopIteration:
            if self.val != None:
                return cast(V, self.val)
            else:
                raise KeyError("no entry for key")
    
    def __setitem__(self: 'Trie[E,V]', n: Iterable[E], v: V) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            if e not in self.elems:
                self.elems[e] = Trie[E,V]()
            self.elems[e][n] = v
        except StopIteration:
            self.val = v
    
    def __delitem__(self: 'Trie[E,V]', n: Iterable[E]) -> None:
        try:
            iterator: Iterator[E] = iter(n)
            e: E = next(iterator)
            del self.elems[e][iterator]
        except StopIteration:
            if self.val != None:
                self.val = None
            else:
                raise KeyError("no entry for key")
    
    def __len__(self: 'Trie[E,V]') -> int:
        return (1 if self.val is not None else 0) \
            + sum(map(len, self.elems.values()))
    
    def __contains__(self: 'Trie[E,V]', n: Any) -> bool:
        if isinstance(n, Iterable):
            iterator: Iterator[E] = iter(cast(Iterable[E], n))
            e: E = next(iterator)
            return e in self.elems and iterator in self.elems[e]
        else:
            return False
    
    def __repr__(self: 'Trie[E,V]') -> str:
        return "(" + repr(self.val) + ", " + repr(self.elems) + ")"

Char = str

class Lexicon(Trie[Char,str]):
    def score_word(self: 'Lexicon', word: str) -> float:
        return 1 if word in self else 0
    
    def score_seq(self: 'Lexicon', seq: str) -> float:
        return 1 if not(empty(self(seq))) else 0

WORD_SEPARATOR = ' '

class PartiallyDecrypted:
    def __init__(
            self: 'PartiallyDecrypted',
            encrypted: str,
            lexicon: Lexicon) -> None:
        self.encrypted: str = encrypted
        self.pos: int = 0
        self.decrypted: str = ""
        self.lexicon: Lexicon = lexicon
    
    def score_next_seq(self: 'PartiallyDecrypted', seq: str) -> float:
        i: int = self.decrypted.rfind(WORD_SEPARATOR)
        if i == -1:
            i = 0
        encrypted_by_seq: str = self.encrypted[self.pos : self.pos+len(seq)]
        newly_decrypted: str = self.decrypted[i:] + xor(encrypted_by_seq, seq)
        decrypted_words: Sequence[str] = newly_decrypted.split(WORD_SEPARATOR)
        scores: Sequence[float] = \
            [self.lexicon.score_word(w) for w in decrypted_words[:-1]] \
            + [self.lexicon.score_seq(decrypted_words[-1])]
        return mean(scores)

Bits = int

## TODO: replace hardcoded functions
## probably with higher level
CHARSET: str = WORD_SEPARATOR + '&l1530b9xy2cn,ho-/7r8wgza.s6\'jkf4ume!qvpitd'
CODES: Iterable[Tuple[Char,Bits]] = \
    [(CHARSET[i], i) for i in range(len(CHARSET))]
#     [(' ' if i == 0 else chr(ord('a') - 1 + i), i) \
#      for i in range(1 + ord('z') - ord('a') + 1)]
CHAR_TO_BITS: Mapping[Char,Bits] = dict(CODES)
BITS_TO_CHAR: Mapping[Bits,Char] = dict((i,c) for (c,i) in CODES)

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

def xor_pairwise(encrypted: Sequence[str]) -> Mapping[int, Mapping[int, str]]:
    result: MutableMapping[int, MutableMapping[int, str]] = dict()
    for i1, msg1 in enumerate(encrypted):
        d: MutableMapping[int,str] = dict()
        for i2, msg2 in filter(lambda t: t[0] != i1, enumerate(encrypted)):
            d[i2] = xor(msg1, msg2)
        result[i1] = d
    return result

def get_words_basic(filename: str) -> Lexicon:
    trie: Lexicon = Lexicon()
    with open(filename, 'r') as f:
        for line in f:
            word: str = line[:-1].lower()
            trie[(c for c in word)] = word
    return trie

def score_next_seq(
        seq: str,
        partial_encryptions: Sequence[PartiallyDecrypted])-> float:
    return mean([enc.score_next_seq(seq) for enc in partial_encryptions])

def decrypt(vocabulary: Lexicon, encrypted: Sequence[str]) -> Sequence[str]:
    ## TODO: implement
    return []

def get_charset(lexicon: Lexicon) -> str:
    return ''.join(set(c for char_iter in lexicon for c in char_iter))

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

if __name__=='__main__':
    vocabulary: Lexicon = get_words_basic(WORDS_BASIC_PATH)
    encrypted: List[str] = open(ENCRYPTED_PATH).readlines()
    print("vocabulary size: " + str(len(vocabulary)))
    # print("vocab starting with ande*: " + str(vocabulary("ande")))
    print("encrypted: " + ''.join(encrypted))
    # charset: str = get_charset(vocabulary)
    # print("charset:\n'" + charset + "'")
    pairwise_encrypted: Mapping[int, Mapping[int, str]] = xor_pairwise(encrypted)
    print("pairwise_encrypted: " + str(pairwise_encrypted))
    decrypt(vocabulary, encrypted)
