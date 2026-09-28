"""Drill. The accumulator pattern.

Run the tests:

    python -m doctest W01/E06_cumsum.py

No output means every test passed.
"""


def cumsum(L):
    """Return the cumulative sum of L. A tuple input still returns a list.

    >>> cumsum([1, 2, 3])
    [1, 3, 6]
    >>> cumsum([5, 5, 5])
    [5, 10, 15]
    >>> cumsum([])
    []
    >>> cumsum([5])
    [5]
    >>> cumsum((5, 5, 5))
    [5, 10, 15]
    """
    total = 0
    result = []
    for i in L:
        total += i
        result.append(total)

    return result
