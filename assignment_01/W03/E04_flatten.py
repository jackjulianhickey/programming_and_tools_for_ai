"""Drill. The same walk, collecting instead of adding.

Run the tests:

    python -m doctest W03/E04_flatten.py

No output means every test passed.
"""


def flatten(items):
    """Return a flat list of every number in items, in the order they appear.

    Same two cases as nested_sum. The only difference is what you do with
    the answer from below: append adds one item, extend adds all the items
    of another list.

    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([1, [2, 3], [4, [5]]])
    [1, 2, 3, 4, 5]
    >>> flatten([])
    []
    >>> flatten([[], [[]]])
    []
    >>> flatten([[[[7]]]])
    [7]
    """    

    result = []
    if not isinstance(items, list):
        return[items]

    for x in items:
        result.extend(flatten(x))

    return result