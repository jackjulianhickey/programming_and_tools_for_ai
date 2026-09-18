"""Composition. Rotation, in one line, with slicing. SOLUTION.

Run the tests:

    python -m doctest W01_Solutions/E11_rotate.py

No output means every test passed.
"""


def rotate(s, k):
    """Move the first k items of s to the end.

    This is the trick that made the cipher easy in the lecture. It works on
    a list as well as a string. If k is bigger than s, wrap around.

    >>> rotate("abcdef", 2)
    'cdefab'
    >>> rotate("abcdef", 0)
    'abcdef'
    >>> rotate([1, 2, 3, 4], 1)
    [2, 3, 4, 1]
    >>> rotate("abc", 3)
    'abc'
    >>> rotate("abc", 4)
    'bca'
    >>> rotate("", 2)
    ''
    """
    if not s:
        return s
    k = k % len(s)
    return s[k:] + s[:k]
