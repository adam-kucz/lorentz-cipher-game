from typing import Iterable, Set, TextIO  # noqa

from .extensions import empty
from .trie import Trie


class SingleChar(str):
    """Single character of a string"""
    def __init__(self: 'SingleChar', c: str) -> None:
        if len(c) != 1:
            raise ValueError("Char must be a single character, " +
                             "not '" + c + "'")
        super().__init__(c)


Char = SingleChar


def unpack(string: str) -> Iterable[Char]:
    """
    Unpack a string into an iterable of characters.

    :param string: str: string to convert
    :returns: Iterable[Char]: an iterable over characters in string
    """
    return map(Char, string)


class Lexicon(Trie[Char, str]):
    """Lexicon of known words represented as a trie"""

    MAX_WORD_SCORE: float = 1

    def score_word(self: 'Lexicon', word: str) -> float:
        """
        Assign a score to the given word.

        :param word: str: word to score using this lexicon
        :returns: float: score of word
        """
        return 1 if unpack(word) in self else 0

    MAX_SEQ_SCORE: float = 1

    def score_seq(self: 'Lexicon', seq: str) -> float:
        """
        Assign a score to the given word prefix.

        :param seq: str: word prefix to score
        :returns: float: score of seq
        """
        return 1 if not(empty(self(unpack(seq)))) else 0

    def get_charset(self: 'Lexicon') -> Set[Char]:
        """
        Get a set of all characters in this lexicon

        :returns: Set[Char]: all characters present
        """
        return set(c for char_iter in self for c in char_iter)

    def prune_to_charset(self: 'Lexicon', charset: Set[Char]) -> None:
        """
        Remove words that contain characters from outside given charset.

        :param charset: Set[Char]: set of acceptable characters
        """
        # TODO: implement
        pass
        # def prune_tree()
        # for char in self.elems:
        #     if char not in charset:
        #         del self.elems[char]
        #     else:
        #         self.elems[char].prune_to_charset(charset)


class BasicLexicon(Lexicon):
    """ """
    def __init__(self: 'Lexicon', filename: str) -> None:
        super().__init__()
        with open(filename, 'r') as f:  # type: TextIO
            for line in f:  # type: str
                word: str = line[:-1].lower()
                self[unpack(word)] = word


WORD_SEPARATOR = ' '
CHARSET: Set[Char] = \
    set(map(Char,
            WORD_SEPARATOR + '&l1530b9xy2cn,ho-/7r8wgza.s6\'jkf4ume!qvpitd'))
