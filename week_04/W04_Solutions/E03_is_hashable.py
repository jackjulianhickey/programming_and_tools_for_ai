"""Drill. Ask an object whether it could be a dictionary key. SOLUTION.

Run the tests:

    python -m doctest W04_Solutions/E03_is_hashable.py

No output means every test passed.

QUESTION: the last two tests below are the interesting ones. Why is a tuple
hashable when it holds numbers but not when it holds a list? Write your answer
in the comment at the bottom.
"""


def is_hashable(x):
    """Return True if `hash(x)` works, and False if it raises.

    There is no way to ask an object this question except by trying it, so
    try it: call `hash` inside a `try`, and catch the `TypeError`.

    The immutable built-ins are hashable:

    >>> is_hashable(3)
    True
    >>> is_hashable("cat")
    True
    >>> is_hashable((1, 2))
    True
    >>> is_hashable(None)
    True

    The mutable ones are not:

    >>> is_hashable([1, 2])
    False
    >>> is_hashable({"a": 1})
    False
    >>> is_hashable({1, 2})
    False

    And a tuple is only as hashable as the things inside it:

    >>> is_hashable((1, (2, 3)))
    True
    >>> is_hashable((1, [2, 3]))
    False
    """
    try:
        hash(x)
        return True
    except TypeError:
        return False


# ANSWER: a tuple hashes by combining the hashes of its contents, so it can
# only be hashed if every item in it can. (1, [2, 3]) contains a list, the
# list has no hash, and so neither has the tuple. The rule underneath is that
# hashing is a promise: an object's hash must never change while it is being
# used as a key. Anything you can modify in place cannot make that promise,
# and a container inherits the problem from whatever it holds.
