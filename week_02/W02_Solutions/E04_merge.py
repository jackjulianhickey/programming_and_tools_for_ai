"""Drill. Building a new dict instead of changing an old one. SOLUTION.

Run the tests:

    python -m doctest W02_Solutions/E04_merge.py

No output means every test passed.
"""


def merge(d1, d2):
    """Return a new dict with the pairs of both. On a clash, d2 wins.

    Neither argument may be changed.

    >>> merge({"a": 1, "b": 2}, {"a": 17, "c": 3})
    {'a': 17, 'b': 2, 'c': 3}
    >>> merge({}, {"a": 1})
    {'a': 1}

    A doctest runs its lines in order, so we can check afterwards that the
    arguments really were left alone:

    >>> first = {"a": 1, "b": 2}
    >>> second = {"a": 17, "c": 3}
    >>> merge(first, second)
    {'a': 17, 'b': 2, 'c': 3}
    >>> first
    {'a': 1, 'b': 2}
    >>> second
    {'a': 17, 'c': 3}
    """
    out = {}
    for k in d1:
        out[k] = d1[k]  # a copy, not another name for the same dict
    for k in d2:
        out[k] = d2[k]  # d2's pairs win, because they are written second
    return out
