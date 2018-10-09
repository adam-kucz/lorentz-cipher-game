from typing import Sequence

from decrypt import xor
from extensions import mean
from lexicon import Lexicon

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
