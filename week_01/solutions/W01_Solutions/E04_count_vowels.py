"""Drill. Looping over a string. SOLUTION.

Run the tests:

    python -m doctest W01_Solutions/E04_count_vowels.py

No output means every test passed.
"""


def count_vowels(s):
    """Return the number of vowels in s. Upper case counts too.

    >>> count_vowels("hello")
    2
    >>> count_vowels("xyz")
    0
    >>> count_vowels("AEIOU")
    5
    >>> count_vowels("")
    0
    """
    count = 0
    for c in s.lower():
        if c in "aeiou":
            count += 1
    return count
