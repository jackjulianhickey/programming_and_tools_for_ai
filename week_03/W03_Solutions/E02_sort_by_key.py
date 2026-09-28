"""Drill. sorted with a key, and the classic sort bug. SOLUTION.

Run the tests:

    python -m doctest W03_Solutions/E02_sort_by_key.py

No output means every test passed.

QUESTION: why does xs = xs.sort() throw away your list? Write your answer
in the comment at the bottom.
"""


def sort_by_mass(pairs):
    """Sort a list of (name, mass) tuples by mass, lightest first.

    Return a new list. The argument must not be changed.

    >>> sort_by_mass([("frame", 2200), ("spoke", 5), ("tyre", 320)])
    [('spoke', 5), ('tyre', 320), ('frame', 2200)]
    >>> sort_by_mass([])
    []

    >>> parts = [("frame", 2200), ("spoke", 5)]
    >>> sort_by_mass(parts)
    [('spoke', 5), ('frame', 2200)]
    >>> parts
    [('frame', 2200), ('spoke', 5)]
    """
    return sorted(pairs, key=lambda pair: pair[1])


def heaviest(pairs):
    """Return the name of the heaviest part.

    Use max with the same key, rather than sorting and taking the last one.

    >>> heaviest([("frame", 2200), ("spoke", 5), ("tyre", 320)])
    'frame'
    >>> heaviest([("spoke", 5)])
    'spoke'
    """
    return max(pairs, key=lambda pair: pair[1])[0]


# ANSWER: .sort() sorts the list in place and returns None, because it has
# already done its work on the list itself and has nothing left to hand back.
# Assigning that None over the name xs loses your only reference to the list,
# which is now sorted and unreachable. sorted() is the one that returns a new
# list. The rule is general: in Python, methods that change an object in place
# usually return None -- .append, .extend and .update all do the same.
