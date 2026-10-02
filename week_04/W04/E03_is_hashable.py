"""Drill. Ask an object whether it could be a dictionary key.

Run the tests:

    python -m doctest W04/E03_is_hashable.py

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
    except:
        return False


# ANSWER: The reason is it holds an object that is mutable and so the values of the list can change and are mutable.