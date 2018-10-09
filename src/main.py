from collections import deque
from typing import Dict, List, Sequence

from decrypt import xor_pairwise
from decryption_state import PartiallyDecrypted
from extensions import empty, mean
from lexicon import BasicLexicon, Lexicon
from trie import Trie

def score_next_seq(
        seq: str,
        partial_encryptions: Sequence[PartiallyDecrypted])-> float:
    return mean([enc.score_next_seq(seq) for enc in partial_encryptions])

def decrypt(vocabulary: Lexicon, encrypted: Sequence[str]) -> Sequence[str]:
    ## TODO: implement
    return []

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

if __name__=='__main__':
    vocabulary: Lexicon = BasicLexicon(WORDS_BASIC_PATH)
    encrypted: List[str] = open(ENCRYPTED_PATH).readlines()
    print("vocabulary size: " + str(len(vocabulary)))
    # print("vocab starting with ande*: " + str(vocabulary("ande")))
    print("encrypted: " + ''.join(encrypted))
    # charset: str = get_charset(vocabulary)
    # print("charset:\n'" + charset + "'")
    pairwise_encrypted: Dict[int, Dict[int, str]] = xor_pairwise(encrypted)
    print("pairwise_encrypted: " + str(pairwise_encrypted))
    decrypt(vocabulary, encrypted)
