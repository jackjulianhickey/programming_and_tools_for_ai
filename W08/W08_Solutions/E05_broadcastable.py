"""Composition. Deciding whether two arrays can be broadcast together. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E05_broadcastable.py

No output means every test passed.

Numpy's rule is short. Line the two shapes up at the *right* hand end, and
pad the shorter one with 1s on the left. Two axes are compatible if they are
equal, or if either of them is 1. If every pair is compatible the arrays can
be broadcast together; if any pair is not, Numpy raises an error.

So (4, 1) and (1, 4) are fine, and so are (3, 5) and (5,), but (3, 5) and
(3,) are not: lined up at the right, 5 and 3 disagree and neither is 1.

Write the rule out yourself. You only need the shapes, never the values.
"""
import numpy as np


def is_broadcastable(X, Y):
    """Can X and Y be added together, using Numpy's broadcasting rules?

    >>> is_broadcastable(np.zeros((4, 1)), np.zeros((1, 4)))
    True
    >>> is_broadcastable(np.zeros((3, 5)), np.zeros(5))
    True
    >>> is_broadcastable(np.zeros((3, 5)), np.zeros(3))
    False
    >>> is_broadcastable(np.zeros((2, 3, 4)), np.zeros((3, 1)))
    True
    >>> is_broadcastable(np.zeros((2, 3)), np.zeros((4, 3)))
    False
    """
    for n, m in zip(reversed(X.shape), reversed(Y.shape)):
        if n != m and n != 1 and m != 1:
            return False
    return True

