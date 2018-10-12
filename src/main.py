from typing import Dict, List

from cipher import Cipher
from full_decrypt import decrypt, xor_pairwise
from lexicon import Lexicon, BasicLexicon

if __name__ == '__main__':
    DATA_DIR: str = __file__ + "/../data"
    WORDS_BASIC_PATH: str = DATA_DIR + "/words-basic.txt"
    MESSAGES_PATH: str = DATA_DIR + "/messages.txt"
    ENCRYPTED_PATH: str = DATA_DIR + "/encrypted.txt"

    vocabulary: Lexicon = BasicLexicon(WORDS_BASIC_PATH)
    print("vocabulary size: " + str(len(vocabulary)))
    # print("vocab starting with ande*: " + str(vocabulary("ande")))
    message_file_lines: List[str] = open(MESSAGES_PATH).readlines()
    key: Cipher = Cipher(message_file_lines[0][:-1])
    messages: List[str] =\
        [line[:-1].lower() for line in message_file_lines[1:]]
    print("messages: " + '\n'.join(messages))
    encrypted: List[Cipher] = [Cipher(message) for message in messages]
    print("encrypted: " + '\n'.join((str(enc) for enc in encrypted)))
    # charset: str = get_charset(vocabulary)
    # print("charset:\n'" + charset + "'")
    pairwise_encrypted: Dict[int, Dict[int, Cipher]] = xor_pairwise(encrypted)
    print("pairwise_encrypted: " + str(pairwise_encrypted))
    decrypt(vocabulary, encrypted)
