from typing import Sequence

from .cipher import Cipher
from .decryption_state import PartiallyDecrypted
from .extensions import mean
from .lexicon import Lexicon

def score_next_seq(
        seq: Cipher,
        partial_encryptions: Sequence[PartiallyDecrypted])-> float:
    return mean([enc.score_next_seq(seq) for enc in partial_encryptions])

def decrypt(vocabulary: Lexicon, encrypted: Sequence[Cipher]) -> Sequence[str]:
    ## TODO: implement
    return []
