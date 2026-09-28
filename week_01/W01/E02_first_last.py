"""Drill. Indexing, and returning a tuple.

Run the tests:

    python -m doctest W01/E02_first_last.py

No output means every test passed.
"""


def first_last(L):
    """Return a tuple of the first and last items of L.

    This works on anything you can index: a list, a tuple, a string.

    >>> first_last([1, 2, 3])
    (1, 3)
    >>> first_last(["a", "b"])
    ('a', 'b')
    >>> first_last([7])
    (7, 7)
    >>> first_last("hello")
    ('h', 'o')
    """

    return (L[0], L[-1])
