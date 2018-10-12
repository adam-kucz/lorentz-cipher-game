from itertools import chain
from typing import Iterable, Optional, Sequence

from .cipher import Cipher, WORD_SEPARATOR
from .partial_decrypt import PartialDecrypt  #, MAX_SCORE
from .extensions import mean
from .lexicon import Lexicon, Char
from .trie import Trie


class Decryption:
    def __init__(self: 'Decryption', vocab: Lexicon,
                 encrypted: Iterable[Cipher]) -> None:
        self.vocab: Lexicon = vocab
        self.decryptions: Iterable[PartialDecrypt] = \
            [PartialDecrypt(c, vocab) for c in encrypted]
        self.target: int = max(chain([0], map(len, encrypted)))
        self.key: Cipher = Cipher()

    @property
    def plaintext(self: 'Decryption') -> Sequence[Optional[str]]:
        while len(self.key) < self.target:
            cipher: Cipher = self.best_next_cipher
            self.key += cipher
            for d in self.decryptions:
                d.decrypt_next_with(cipher)
        return map(lambda s: s.decrypted, self.decryptions)

    def score_next_seq(self: 'Decryption', seq: Cipher) -> float:
        return mean([enc.score_next_seq(seq) for enc in self.decryptions])

    @property
    def all_candidates(self: 'Decryption') -> Iterable[Cipher]:
        for candidate in self.decryptions:  # type: PartialDecrypt
            subtree: Optional[Trie[Char, str]] = self.vocab(candidate.prefix)
            if subtree is None:
                continue
            l: int = len(candidate.prefix)
            for word in subtree.values():  # type: str
                yield Cipher(word[l:] + WORD_SEPARATOR)

    @property
    def best_next_cipher(self: 'Decryption') -> Cipher:
        best_score: float = float('-inf')
        best_cipher: Cipher = Cipher()
        for cipher in self.all_candidates:  # type: Cipher
            score: float = self.score_next_seq(cipher)
            if score > best_score:
                best_score = score
                best_cipher = cipher
            elif score == best_score and len(cipher) > len(best_cipher):
                best_cipher = cipher
        return best_cipher
