"""Extension. Euclid's algorithm, 300 BC.

Run the tests:

    python -m doctest W01/E15_gcd.py

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


def gcd(a, b):
    """Return the greatest common divisor of a and b.

    Use iterate. The thing being transformed is a pair (a, b), not a single
    number. The transform turns (a, b) into (b, a % b). Stop when b is 0.
    The answer is then the first element of the pair.

    >>> gcd(48, 18)
    6
    >>> gcd(1071, 462)
    21
    >>> gcd(17, 5)
    1
    >>> gcd(12, 12)
    12
    >>> gcd(7, 0)
    7
    """
    return  # YOUR CODE HERE
