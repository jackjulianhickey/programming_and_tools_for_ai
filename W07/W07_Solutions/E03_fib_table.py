"""Drill. Fibonacci from the bottom up. SOLUTION.

Run the tests:

    python -m doctest W07_Solutions/E03_fib_table.py

No output means every test passed.

The lecture's `fib_slow` is exponential because it asks the same questions over
and over. Fill a table instead, smallest first, so each answer is computed
once. Then notice how little of that table you actually needed.
"""
def fib_table(n):
    """Return the nth Fibonacci number, building a list from the bottom up.

    >>> [fib_table(i) for i in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> fib_table(35)
    9227465
    """
    F = [0, 1]
    for i in range(2, n + 1):
        F.append(F[i - 1] + F[i - 2])
    return F[n]


def fib_pair(n):
    """The same answer, keeping only the two values we still need.

    >>> [fib_pair(i) for i in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> fib_pair(35)
    9227465
    >>> all(fib_pair(i) == fib_table(i) for i in range(50))
    True
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# `fib_table` holds n numbers to return one. `fib_pair` holds two. This is the
# same saving we make for edit distance in E05, one dimension down: look at the
# recurrence, see how far back it actually reaches, and keep only that much.
