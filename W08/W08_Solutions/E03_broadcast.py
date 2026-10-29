"""Drill. Adding arrays whose shapes do not match. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E03_broadcast.py

No output means every test passed.

Numpy stretches a length-1 axis to fit, so a column of 4 and a row of 4 add
up to a 4 by 4 table. Nothing is copied: the stretching is a fiction Numpy
maintains while it reads the values.

Each function below should be one line of Numpy, with no loop.

QUESTION: in combine, c can be added just as it comes, but b cannot. Why
does one of them need reshaping and the other does not?
Answer in the comment at the bottom.
"""
import numpy as np


def combine(A, b, c, d):
    """Build the table z, where

        z[i, j] = A[i, j] + b[i] + c[j] + d

    A is 2-D with n rows and m columns, b has n entries, c has m entries,
    and d is a single number.

    >>> A = np.zeros((4, 4))
    >>> b = np.array([10.0, 20.0, 30.0, 40.0])
    >>> c = np.array([1.0, 2.0, 3.0, 4.0])
    >>> combine(A, b, c, 100.0)
    array([[111., 112., 113., 114.],
           [121., 122., 123., 124.],
           [131., 132., 133., 134.],
           [141., 142., 143., 144.]])
    >>> A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    >>> combine(A, np.array([0.0, 10.0]), np.array([0.0, 0.0, 100.0]), 1.0)
    array([[  2.,   3., 104.],
           [ 15.,  16., 117.]])
    """
    return A + b.reshape(-1, 1) + c + d


def times_table(n):
    """Return the n by n multiplication table.

    Make a row 1, 2, ..., n and a column of the same numbers, and multiply.

    >>> times_table(3)
    array([[1, 2, 3],
           [2, 4, 6],
           [3, 6, 9]])
    >>> print(times_table(5)[4, 4])
    25
    """
    row = np.arange(1, n + 1)
    return row.reshape(-1, 1) * row


# ANSWER:
# Shapes are lined up at the right-hand end. c has shape (m,), which lines up
# against the columns of A, which is what c[j] is supposed to vary along, so
# it needs nothing. b has shape (n,), and lined up at the right it would also
# fall on the columns -- the wrong axis, and an error unless n happens to
# equal m. Reshaping it to (n, 1) puts the n on the rows and leaves a 1 on the
# columns, so Numpy stretches b across each row instead.
