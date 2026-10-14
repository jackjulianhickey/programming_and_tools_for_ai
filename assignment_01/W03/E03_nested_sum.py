"""Drill. Recursion, on the simplest possible nested data.

Run the tests:

    python -m doctest W03/E03_nested_sum.py

No output means every test passed.
"""


def nested_sum(items):
    """Total every number in items, however deeply nested the lists are.

    Two cases, as always. An item is either a list, which we have to look
    inside, or a number, which we can just add.

    isinstance(x, list) is how you ask whether x is a list.

    >>> nested_sum([1, 2, 3])
    6
    >>> nested_sum([1, [2, 3], [4, [5]]])
    15
    >>> nested_sum([])
    0
    >>> nested_sum([[], [[]]])
    0
    >>> nested_sum([[[[7]]]])
    7
    """
    if not isinstance(items, list):
        return items

    return sum(nested_sum(x) for x in items)