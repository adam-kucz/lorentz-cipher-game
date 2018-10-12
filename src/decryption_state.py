from typing import cast, Optional, Sequence

from .cipher import Cipher, WORD_SEPARATOR
from .extensions import mean
from .lexicon import Lexicon


class PartiallyDecrypted:
    def __init__(
            self: 'PartiallyDecrypted',
            encrypted: Cipher,
            lexicon: Lexicon) -> None:
        self.encrypted: Cipher = encrypted
        self.pos: int = 0
        self.decrypted: str = ""
        self.lexicon: Lexicon = lexicon

    def score_next_seq(self: 'PartiallyDecrypted', seq: Cipher) -> float:
        i: int = self.decrypted.rfind(WORD_SEPARATOR)
        if i == -1:
            i = 0
        p: int = self.pos
        encrypted_by_seq: Cipher = self.encrypted[p:p + len(seq)]
        decryption_candidate: Optional[str] = (encrypted_by_seq ^ seq).word
        if decryption_candidate is None:
            return 0
        newly_decrypted: str = \
            self.decrypted[i:] + cast(str, decryption_candidate)
        decrypted_words: Sequence[str] = newly_decrypted.split(WORD_SEPARATOR)
        scores: Sequence[float] = \
            [self.lexicon.score_word(w) for w in decrypted_words[:-1]] \
            + [self.lexicon.score_seq(decrypted_words[-1])]
        return mean(scores)
