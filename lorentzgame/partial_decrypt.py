from typing import cast, Collection, Optional, Sequence

from .cipher import Cipher, WORD_SEPARATOR
from .extensions import mean
from .lexicon import Lexicon, Char, unpack


class PartialDecrypt:
    """ """
    def __init__(
            self: 'PartialDecrypt',
            encrypted: Cipher,
            lexicon: Lexicon) -> None:
        self.encrypted: Cipher = encrypted
        self.decrypted: str = ""
        self.lexicon: Lexicon = lexicon

    @property
    def pos(self: 'PartialDecrypt') -> int:
        """

        :param self: 'PartialDecrypt': 

        """
        return len(self.decrypted)

    @property
    def prefix(self: 'PartialDecrypt') -> Collection[Char]: \
        # pylint: disable=unsubscriptable-object
        return tuple(unpack(self.decrypted.rsplit(WORD_SEPARATOR, 1)[1]))

    def __get_decrypt_next_str(self: 'PartialDecrypt',
                               seq: Cipher) -> Optional[str]:
        """

        :param self: 'PartialDecrypt') -> Collection[Char]: \# pylint: disable:  (Default value = unsubscriptable-objectreturn tuple(unpack(self.decrypted.rsplit(WORD_SEPARATOR)
        :param 1)[1]))__get_decrypt_next_str(self: 'PartialDecrypt': 
        :param seq: Cipher: 

        """
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
        """

        :param self: 'PartialDecrypt': 
        :param seq: Cipher: 

        """
        string: Optional[str] = self.__get_decrypt_next_str(seq)
        if string is not None:
            self.decrypted += string
        else:
            raise ValueError("Invalid key for decryption")

    MAX_SCORE: float = max(Lexicon.MAX_SEQ_SCORE, Lexicon.MAX_WORD_SCORE)

    def score_next_seq(self: 'PartialDecrypt', seq: Cipher) -> float:
        """

        :param self: 'PartialDecrypt': 
        :param seq: Cipher: 

        """
        newly_decrypted: Optional[str] = self.__get_decrypt_next_str(seq)
        if newly_decrypted is None:
            return 0
        decrypted_words: Sequence[str] = newly_decrypted.split(WORD_SEPARATOR)
        scores: Sequence[float] = \
            [self.lexicon.score_word(w) for w in decrypted_words[:-1]] \
            + [self.lexicon.score_seq(decrypted_words[-1])]
        return mean(scores)
