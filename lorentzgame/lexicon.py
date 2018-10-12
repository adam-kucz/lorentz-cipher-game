from typing import TextIO  # noqa

from .extensions import empty
from .trie import Trie


class Char(str):
    def __init__(self: 'Char', c: str) -> None:
        if len(c) != 1:
            raise ValueError("Char must be a single character, not '" + c + "'")
        super().__init__(c)


class Lexicon(Trie[Char, str]):

    MAX_WORD_SCORE: float = 1
    
    def score_word(self: 'Lexicon', word: str) -> float:
        return 1 if word in self else 0

    MAX_SEQ_SCORE: float = 1
    
    def score_seq(self: 'Lexicon', seq: str) -> float:
        return 1 if not(empty(self(seq))) else 0

    def get_charset(self: 'Lexicon') -> str:
        return ''.join(set(c for char_iter in self for c in char_iter))


class BasicLexicon(Lexicon):
    def __init__(self: 'Lexicon', filename: str) -> None:
        super().__init__()
        with open(filename, 'r') as f:  # type: TextIO
            for line in f:  # type: str
                word: str = line[:-1].lower()
                self[(c for c in word)] = word
