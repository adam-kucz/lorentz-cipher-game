#!/usr/bin/env python3

from typing import List

from lorentzgame.cipher import Cipher
from lorentzgame.decryption import Decryption
from lorentzgame.lexicon import Lexicon, BasicLexicon

if __name__ == '__main__':
    DATA_DIR: str = "/home/acalc79/Code/lorentz-cipher-game/data"
    WORDS_BASIC_PATH: str = DATA_DIR + "/words-basic.txt"
    MESSAGES_PATH: str = DATA_DIR + "/messages.txt"
    ENCRYPTED_PATH: str = DATA_DIR + "/encrypted.txt"

    vocabulary: Lexicon = BasicLexicon(WORDS_BASIC_PATH)
    print("vocabulary size: " + str(len(vocabulary)))
    message_file_lines: List[str] = open(MESSAGES_PATH).readlines()
    key: Cipher = Cipher(message_file_lines[0][:-1])
    messages: List[str] =\
        [line[:-1].lower() for line in message_file_lines[1:]]
    print("messages: " + '\n'.join(messages))
    encrypted: List[Cipher] = [Cipher(message) for message in messages]
    print("encrypted: " + '\n'.join((str(enc) for enc in encrypted)))
    d: Decryption = Decryption(vocabulary, encrypted)
    print(d.plaintext)
