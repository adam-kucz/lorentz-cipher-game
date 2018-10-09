from collections import deque
from typing import Dict, List, Sequence

from cipher import Cipher, xor_pairwise
from decryption_state import PartiallyDecrypted
from extensions import empty, mean
from lexicon import BasicLexicon, Lexicon
from trie import Trie

def score_next_seq(
        seq: str,
        partial_encryptions: Sequence[PartiallyDecrypted])-> float:
    return mean([enc.score_next_seq(seq) for enc in partial_encryptions])

def decrypt(vocabulary: Lexicon, encrypted: Sequence[Cipher]) -> Sequence[str]:
    ## TODO: implement
    return []

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
MESSAGES_PATH: str = "../data/messages.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

if __name__=='__main__':
    vocabulary: Lexicon = BasicLexicon(WORDS_BASIC_PATH)
    print("vocabulary size: " + str(len(vocabulary)))
    # print("vocab starting with ande*: " + str(vocabulary("ande")))
    message_file_lines: List[str] = open(MESSAGES_PATH).readlines()
    key: Cipher = Cipher(message_file_lines[0][:-1])
    messages: List[str] = [line[:-1].lower() for line in message_file_lines[1:]]
    print("messages: " + '\n'.join(messages))
    encrypted: List[Cipher] = [Cipher(message) for message in messages]
    print("encrypted: " + '\n'.join((str(enc) for enc in encrypted)))
    # charset: str = get_charset(vocabulary)
    # print("charset:\n'" + charset + "'")
    pairwise_encrypted: Dict[int, Dict[int, Cipher]] = xor_pairwise(encrypted)
    print("pairwise_encrypted: " + str(pairwise_encrypted))
    decrypt(vocabulary, encrypted)
