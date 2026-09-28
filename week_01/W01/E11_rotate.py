"""Composition. Rotation, in one line, with slicing.

Run the tests:

    python -m doctest W01/E11_rotate.py

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
    return s[k % len(s):] + s[:k % len(s)] if s else s 
# k % len(s) is used to handle wrapping around. 
# The if s else s is used to handle the case where s is an empty string or list, in which case we just return s.
# For example, if s = "abcdef" and k = 2, then k % len(s) = 2 % 6 = 2, so we take the slice s[2:] which is "cdef" and the slice s[:2] which is "ab", and concatenate them to get "cdefab".
# If s = "abc" and k = 4, then k % len(s) = 4 % 3 = 1, so we take the slice s[1:] which is "bc" and the slice s[:1] which is "a", and concatenate them to get "bca".
