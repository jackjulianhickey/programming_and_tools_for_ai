"""Drill. Boolean masks, and doing the sum along one axis. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E04_axis_masks.py

No output means every test passed.

Two ideas, both from the lecture. Comparing an array to a number gives an
array of True and False, which you can count with sum or use as an index.
And every summarising method takes an axis: axis=0 goes down the columns,
axis=1 goes along the rows.

Each function below should be one line of Numpy, with no loop.
"""
import numpy as np


def count_above(x, t):
    """Count how many entries of x are greater than t.

    >>> x = np.array([1, 5, 3, 9, 2])
    >>> count_above(x, 2)
    3
    >>> count_above(x, 100)
    0
    """
    return int(np.sum(x > t))


def values_above(x, t):
    """Return just the entries of x greater than t, in their original order.

    >>> x = np.array([1, 5, 3, 9, 2])
    >>> values_above(x, 2)
    array([5, 3, 9])
    >>> values_above(x, 4)
    array([5, 9])
    """
    return x[x > t]


def column_means(X):
    """Return the mean of each column of the 2-D array X.

    >>> X = np.array([[1.0, 2.0, 3.0], [3.0, 4.0, 9.0]])
    >>> column_means(X)
    array([2., 3., 6.])
    >>> column_means(np.array([[10.0, 20.0]]))
    array([10., 20.])
    """
    return X.mean(axis=0)


def row_maxes(X):
    """Return the largest value in each row of the 2-D array X.

    >>> X = np.array([[1.0, 2.0, 3.0], [9.0, 4.0, 0.0]])
    >>> row_maxes(X)
    array([3., 9.])
    >>> row_maxes(np.array([[-1.0, -5.0]]))
    array([-1.])
    """
    return X.max(axis=1)
