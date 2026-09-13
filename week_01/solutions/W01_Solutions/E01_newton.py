"""Drill. Nothing to write here: the only job is to run this file. SOLUTION.

This is Newton's algorithm from the lecture, complete. Run its tests:

    python -m doctest W01_Solutions/E01_newton.py

No output means every test passed. That silence is the whole point: doctest
only speaks up when something is wrong.

Now make it speak. Change the 1.414214 below to 1.5, run it again, and read
what it prints -- expected, got, and the line it came from. Then change it
back. That is the output you will be reading all semester.
"""


def newton_sqrt(x, tol=1e-10):
    """Return the square root of x.

    Start from a guess, and repeatedly average it with x divided by it. One
    of those two is too small and the other too large, so their average is
    closer than at least one of them.

    >>> round(newton_sqrt(2), 6)
    1.414214
    >>> round(newton_sqrt(16), 6)
    4.0
    >>> newton_sqrt(0)
    0.0
    >>> round(newton_sqrt(73.7), 6)
    8.58487
    """
    if x < 0:
        raise ValueError(f"Square root undefined for input {x}")
    if x == 0:
        return 0.0
    g = float(x)
    while True:
        g = (g + x / g) / 2
        if abs(g * g - x) < tol:
            break
    return g
