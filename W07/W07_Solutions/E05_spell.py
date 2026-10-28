"""Composition. Spelling suggestions. SOLUTION.

Run the tests:

    python -m doctest W07_Solutions/E05_spell.py

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
    ranked = sorted(words, key=lambda w: (levenshtein(word, w), w))
    return ranked[:n]


# ANSWER: ties are the normal case, not a corner case. "cet" is one edit from
# "cat", and then "bat", "car", "cart" and "cast" are all two edits away.
# `sorted` is stable, so sorting on distance alone leaves those four in
# whatever order the dictionary happened to list them, and the same call on the
# same words returns a different answer if someone reorders the file. That is a
# problem with the function and not only with the test: a caller cannot rely on
# an answer that depends on something they did not think was part of the input.
# Adding the word to the key breaks every tie the same way every time. Being
# able to doctest it is the symptom, not the reason. A real spellchecker breaks
# ties by which word is more common, which is more useful than alphabetical and
# just as deterministic.
