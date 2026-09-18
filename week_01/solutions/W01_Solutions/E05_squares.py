"""Drill. Building a list with append. SOLUTION.

Run the tests:

    python -m doctest W01_Solutions/E05_squares.py

No output means every test passed.
"""


def squares(n):
    """Return a list of the squares of 1 up to and including n.

    >>> squares(4)
    [1, 4, 9, 16]
    >>> squares(1)
    [1]
    >>> squares(0)
    []
    """
    result = []
    for i in range(1, n + 1):
        result.append(i * i)
    return result
