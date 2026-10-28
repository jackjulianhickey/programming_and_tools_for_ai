"""Composition. Spelling suggestions.

Run the tests:

    python -m doctest W07/E05_spell.py

No output means every test passed.

A spellchecker offers the dictionary words closest to what you typed. That is
edit distance, run once for every word in the dictionary. A real word list has
100,000 entries, which is why we wanted the cheap version in E04: once your
`levenshtein_row` works, it drops straight in here.

QUESTION: `suggest` sorts on `(distance, word)` rather than on `distance`
alone. What would change if it sorted on `distance` alone, and is that a
problem with the function or only with the test? Write your answer in the
comment at the bottom.
"""

from E01_editdist import levenshtein
from E04_one_row import levenshtein_row
# Given: a small word list, so the doctests need no real dictionary.
WORDS = ["cat", "cart", "car", "cast", "case", "bat", "dog"]


def suggest(word, words, n=3):
    """Return the n words closest to `word`, nearest first.

    >>> suggest("cet", WORDS)
    ['cat', 'bat', 'car']
    >>> suggest("dat", WORDS)
    ['bat', 'cat', 'car']
    >>> suggest("cat", WORDS, n=1)
    ['cat']
    >>> suggest("cat", [])
    []
    """
    pairs = [(levenshtein_row(word, w), w) for w in words]

    pairs.sort()

    return [w for dist, w in pairs[:n]]


# ANSWER: If it is sorted based on distance only then words with a the same distance
# are not sorted alphabetically and may not match the order of the doctests.                                                                                                                                                                                                                                                                                                                                                                                                                                                  
