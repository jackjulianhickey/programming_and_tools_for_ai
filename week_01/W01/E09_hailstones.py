"""Composition. Hailstone sequences.

Run the tests:

    python -m doctest W01/E09_hailstones.py

No output means every test passed.
"""

# hailstones returns a sequence of numbers starting at n and ending at 1, where each number is
# generated from the previous number by the following rules:
# - if the previous number is even, the next number is half of the previous number
# - if the previous number is odd, the next number is 3 times the previous number + 1

def hailstones(n):
    """Return the hailstone sequence starting at n and ending at 1.

    If n is even, the next number is n/2. If n is odd, it is 3n+1.

    >>> hailstones(1)
    [1]
    >>> hailstones(10)
    [10, 5, 16, 8, 4, 2, 1]
    >>> hailstones(7)[:6]
    [7, 22, 11, 34, 17, 52]
    >>> len(hailstones(27))
    112
    """
    result = []
    while n != 1:
        result.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = (3 * n) + 1
    result.append(1)

    return result


# longest_hailstone returns the number n < limit that generates the longest hailstone sequence, along with the length of that sequence.
# In other words using the hailstones function and the limit, find the number n < limit that generates the longest sequence of numbers and it's length.

def longest_hailstone(limit):
    """Return (n, length) for the longest hailstone sequence with n < limit.

    >>> longest_hailstone(10)
    (9, 20)
    >>> longest_hailstone(100)
    (97, 119)
    >>> longest_hailstone(1000)
    (871, 179)
    """
    result = (0, 0)
    for n in range(1, limit):
        ret = len(hailstones(n))
        if ret > result[1]:
            result = (n, ret)
    
    return  result
