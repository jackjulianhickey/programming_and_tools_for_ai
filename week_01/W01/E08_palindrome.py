"""Drill. Slicing with a step.

Run the tests:

    python -m doctest W01/E08_palindrome.py

No output means every test passed.
"""


def is_palindrome(s):
    """Return True if s reads the same forwards and backwards.

    >>> is_palindrome('racecar')
    True
    >>> is_palindrome('hello')
    False
    >>> is_palindrome('a')
    True
    >>> is_palindrome('')
    True
    >>> is_palindrome('ab')
    False
    >>> is_palindrome('abcba')
    True
    """
    return s==s[::-1]
