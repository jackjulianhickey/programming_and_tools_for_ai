"""Drill. Python has sum() built in, but not product(). SOLUTION.

Run the tests:

    python -m doctest W01_Solutions/E07_product.py

No output means every test passed.
"""


def product(L):
    """Return the product of the numbers in L.

    The sum of an empty list is 0, but the product of an empty list is 1.

    >>> product([1, 1, 1])
    1
    >>> product([1, 2, 3])
    6
    >>> product([])
    1
    >>> product([2, 3, 4])
    24
    """
    result = 1
    for x in L:
        result *= x
    return result
