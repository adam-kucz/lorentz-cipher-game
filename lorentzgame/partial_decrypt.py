from typing import cast, Optional, Sequence

from .cipher import Cipher, WORD_SEPARATOR
from .extensions import mean
from .lexicon import Lexicon


class PartialDecrypt:
    def __init__(
            self: 'PartialDecrypt',
            encrypted: Cipher,
            lexicon: Lexicon) -> None:
        self.encrypted: Cipher = encrypted
        self.decrypted: str = ""
        self.lexicon: Lexicon = lexicon

    @property
    def pos(self: 'PartialDecrypt') -> int:
        return len(self.decrypted)
    
    @property
    def prefix(self: 'PartialDecrypt') -> str:
        return self.decrypted.rsplit(WORD_SEPARATOR, 1)[1]

    def __get_decrypt_next_str(self: 'PartialDecrypt',
                              seq: Cipher) -> Optional[str]:
        i: int = self.decrypted.rfind(WORD_SEPARATOR)
        if i == -1:
            i = 0
        p: int = self.pos
        encrypted_by_seq: Cipher = self.encrypted[p:p + len(seq)]
        decryption_candidate: Optional[str] = (encrypted_by_seq ^ seq).word
        if decryption_candidate is None:
            return None
        return self.decrypted[i:] + cast(str, decryption_candidate)

    def decrypt_next_with(self: 'PartialDecrypt', seq: Cipher) -> None:
        string: Optional[str] = self.__get_decrypt_next_str(seq)
        if string is not None:
            self.decrypted += string
        else:
            raise ValueError("Invalid key for decryption")

    MAX_SCORE: float = max(Lexicon.MAX_SEQ_SCORE, Lexicon.MAX_WORD_SCORE)
    
    def score_next_seq(self: 'PartialDecrypt', seq: Cipher) -> float:
        newly_decrypted: str = self.__get_decrypt_next_str(seq)
        decrypted_words: Sequence[str] = newly_decrypted.split(WORD_SEPARATOR)
        scores: Sequence[float] = \
            [self.lexicon.score_word(w) for w in decrypted_words[:-1]] \
            + [self.lexicon.score_seq(decrypted_words[-1])]
        return mean(scores)
