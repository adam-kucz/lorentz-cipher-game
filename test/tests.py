import unittest
from unittest import TestCase
from os import path
from typing import Dict, List

from ..src.cipher import Cipher, xor_pairwise
from ..src.full_decrypt import decrypt
from ..src.lexicon import Lexicon, BasicLexicon

DATA_DIR: str = path.dirname(__file__) + "/../data"
WORDS_BASIC_PATH: str = DATA_DIR + "/words-basic.txt"
MESSAGES_PATH: str = DATA_DIR + "/messages.txt"
ENCRYPTED_PATH: str = DATA_DIR + "/encrypted.txt"

class TestLorentz(TestCase):

    def test_blankkey(self: 'TestCase') -> None:
        vocabulary: Lexicon = BasicLexicon(WORDS_BASIC_PATH)
        print("vocabulary size: " + str(len(vocabulary)))
        # print("vocab starting with ande*: " + str(vocabulary("ande")))
        with open(MESSAGES_PATH) as f: # type: TextIO
            message_file_lines: List[str] = f.readlines()
        key: Cipher = Cipher(message_file_lines[0][:-1])
        messages: List[str] =\
            [line[:-1].lower() for line in message_file_lines[1:]]
        print("messages:\n" + '\n'.join(messages))
        encrypted: List[Cipher] = \
            [Cipher(message) ^ key for message in messages]
        print("encrypted:\n" + '\n'.join((str(enc) for enc in encrypted)))
        # charset: str = get_charset(vocabulary)
        # print("charset:\n'" + charset + "'")
        pairwise_encrypted: Dict[int, Dict[int, Cipher]] = \
            xor_pairwise(encrypted)
        print("pairwise_encrypted: " + str(pairwise_encrypted))
        decrypt(vocabulary, encrypted)

if __name__ == '__main__':
    unittest.main()
