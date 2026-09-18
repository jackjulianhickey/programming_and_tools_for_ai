"""Drill. Looking up a key that might not be there. SOLUTION.

Run the tests:

    python -m doctest W02_Solutions/E02_get_or.py

No output means every test passed.
"""


def get_or(d, key, default):
    """Return d[key] if key is present, and default if it is not.

    Remember that `in` asks about keys, never values, and that a missing
    key raises KeyError rather than returning None.

    Python has this built in, as d.get(key, default). Write it once
    yourself, then use the built-in for the rest of your life.

    >>> scores = {"ann": 7, "bob": 3}
    >>> get_or(scores, "ann", 0)
    7
    >>> get_or(scores, "cara", 0)
    0
    >>> get_or({}, "ann", "no score")
    'no score'

    A value that is present is returned even if it is falsy:

    >>> get_or({"ann": 0}, "ann", 99)
    0
    """
    if key in d:
        return d[key]
    return default
