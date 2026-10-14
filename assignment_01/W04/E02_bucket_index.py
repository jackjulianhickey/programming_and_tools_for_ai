"""Drill. The one line the whole week rests on.

Run the tests:

    python -m doctest W04/E02_bucket_index.py

No output means every test passed.
"""


def bucket_index(key, capacity):
    """Which bucket does `key` belong in, when there are `capacity` of them?

    Two steps: `hash` turns the key into an int, which may be huge or
    negative, and `%` folds it into 0, 1, ..., capacity - 1.

    Integers hash to themselves, so these are easy to check by hand:

    >>> bucket_index(3, 8)
    3
    >>> bucket_index(11, 8)
    3
    >>> bucket_index(11, 16)
    11

    The answer is always a legal bucket number, whatever the key:

    >>> bucket_index(-3, 8)
    5
    >>> all(0 <= bucket_index(k, 8) < 8 for k in range(-50, 50))
    True
    >>> all(0 <= bucket_index(w, 5) < 5 for w in ["cat", "dog", "emu"])
    True

    Note `bucket_index(11, 8)` and `bucket_index(11, 16)` differ. That is why
    growing a table means re-filing every pair, and not just copying them.
    """
    
    return hash(key) % capacity


# Note `%` never returns a negative number in Python, even for a negative
# left-hand side, which is exactly what we need for a list index. (One oddity
# if you go looking: hash(-1) is -2, not -1. CPython reserves -1 to mean "an
# error happened" inside the C code, so it quietly returns -2 instead.)
