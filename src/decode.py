import random
from typing import List

WORDS_BASIC_PATH: str = "../data/words-basic.txt"
ENCRYPTED_PATH: str = "../data/encrypted.txt"

def get_words_basic(filename: str) -> List[str]:
    return [line[:-1] for line in open(filename, 'r')]

def decrypt(vocabulary: List[str], encrypted: List[str]) -> List[str]:
    return []

if __name__=='__main__':
    vocabulary: List[str] = get_words_basic(WORDS_BASIC_PATH)
    encrypted: List[str] = open(ENCRYPTED_PATH).readlines()
    decrypt(vocabulary, encrypted)
