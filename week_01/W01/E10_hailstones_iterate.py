"""Composition. The same problem, using iterate.

Run the tests:

    python -m doctest W01/E10_hailstones_iterate.py

No output means every test passed.
"""

# Given: the iterate function from the lecture, with one addition -- a limit on
# the number of steps, so that a wrong transform gives up instead of hanging.
# You do not need to change it.
def iterate(x, transform, done, max_steps=10000):
    """Apply transform to x over and over, until done(x) is true."""
    for _ in range(max_steps):
        if done(x):
            return x
        x = transform(x)
    raise RuntimeError("iterate: gave up after too many steps")


def hailstone_step(n):
    """Return the next hailstone number after n.

    >>> hailstone_step(10)
    5
    >>> hailstone_step(7)
    22
    >>> hailstone_step(1)
    4
    """
    return n // 2 if n % 2 == 0 else 3 * n + 1


def reaches_one(n):
    """Return True if n is 1, that is, if the sequence is finished.

    With both pieces written, iterate can run the whole thing:

    >>> reaches_one(1)
    True
    >>> reaches_one(2)
    False
    >>> iterate(27, hailstone_step, reaches_one)
    1
    """
    return  True if n == 1 else False
