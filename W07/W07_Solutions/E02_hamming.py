"""Drill. Counting the positions where two sequences disagree. SOLUTION.

Run the tests:

    python -m doctest W07_Solutions/E02_hamming.py

No output means every test passed.

Hamming distance is the first thing anyone tries, and the lecture spent Part 1
showing where it breaks. Write it, then write the version that copes with two
different lengths.
"""

from itertools import zip_longest
def hamming(a, b):
    """Count the positions where a and b differ, ignoring any extra tail.

    >>> hamming("ACGT", "ACGT")
    0
    >>> hamming("ACGTACGTAC", "ACGTTCGTAC")
    1
    >>> hamming("ACGTACGTAC", "CGTACGTACA")
    10
    """
    return sum(x != y for x, y in zip(a, b))


def hamming_padded(a, b):
    """Count differing positions, counting each unmatched item as a difference.

    >>> hamming_padded("ACGT", "ACGT")
    0
    >>> hamming_padded("abc", "abcde")
    2
    >>> hamming_padded("", "abc")
    3
    >>> hamming_padded("abc", "")
    3
    """
    return sum(x != y for x, y in zip_longest(a, b))


# `zip` stops at the shorter of the two, so `hamming` silently ignores
# everything past the end of it: hamming("abc", "abcde") is 0. That is why the
# lecture said Hamming cannot compare sequences of different lengths at all.
# `itertools.zip_longest` pads the shorter one with None instead, and None
# equals nothing, so every unmatched item counts as a difference.
