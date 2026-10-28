"""Drill. Nothing to write here: the only job is to run this file. SOLUTION.

This is the whole program from the lecture: the edit-distance table of Part 2,
the traceback of Part 3, and dynamic time warping from Part 4. Run its tests:

    python -m doctest W07_Solutions/E01_editdist.py

No output means every test passed.

Then run it as a program:

    python W07_Solutions/E01_editdist.py                  # kitten -> sitting
    python W07_Solutions/E01_editdist.py cat cart         # any pair of words
    python W07_Solutions/E01_editdist.py --fib 30         # the trap, timed
    python W07_Solutions/E01_editdist.py --dtw            # two walking speeds

Read `fib_slow` and `fib_cached` side by side. They differ in one line, and
that line takes thirty million calls down to thirty-one.

Then read `edit_table` and `dtw`. They differ in what a step costs and in what
the edges of the table say, and in nothing else.
"""

import sys
import time
from functools import cache

INF = float("inf")


# ---------------------------------------------------------------- Part 2 ----

def fib_slow(n):
    """Fibonacci, straight from the definition. Correct, and exponential.

    >>> [fib_slow(i) for i in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


@cache
def fib_cached(n):
    """The same function, with the answers remembered.

    >>> [fib_cached(i) for i in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> fib_cached(35)
    9227465
    """
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


def edit_table(a, b):
    """The table of edit distances between every pair of prefixes.

    `D[i][j]` is the distance from the first `i` characters of `a` to the
    first `j` characters of `b`, so the answer is in the bottom-right corner.

    >>> edit_table("kitten", "sitting")[-1][-1]
    3
    >>> edit_table("", "abc")[-1][-1]
    3
    >>> edit_table("abc", "abc")[-1][-1]
    0
    """
    D = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        D[i][0] = i                      # delete i characters
    for j in range(len(b) + 1):
        D[0][j] = j                      # insert j characters
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = min(D[i - 1][j] + 1,          # delete a[i-1]
                          D[i][j - 1] + 1,          # insert b[j-1]
                          D[i - 1][j - 1] + cost)   # keep or substitute
    return D


def levenshtein(a, b):
    """The edit distance between two sequences.

    >>> levenshtein("kitten", "sitting")
    3
    >>> levenshtein("ACGTACGTAC", "CGTACGTACA")
    2
    >>> levenshtein("", "")
    0
    """
    return edit_table(a, b)[-1][-1]


# ---------------------------------------------------------------- Part 3 ----

def edits(a, b):
    """The actual edits, recovered by walking back through the table.

    >>> edits("kitten", "sitting")
    ['substitute k -> s', 'substitute e -> i', 'insert g']
    >>> edits("ACGTACGTAC", "CGTACGTACA")
    ['delete A', 'insert A']
    >>> edits("abc", "abc")
    []
    """
    D = edit_table(a, b)
    i, j, steps = len(a), len(b), []
    while i > 0 or j > 0:
        cost = 0 if i and j and a[i - 1] == b[j - 1] else 1
        if i and j and D[i][j] == D[i - 1][j - 1] + cost:
            if cost:
                steps.append(f"substitute {a[i - 1]} -> {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i and D[i][j] == D[i - 1][j] + 1:
            steps.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            steps.append(f"insert {b[j - 1]}")
            j -= 1
    steps.reverse()
    return steps


# ---------------------------------------------------------------- Part 4 ----

def dtw(a, b):
    """Dynamic time warping: the same table, for sequences of numbers.

    A step costs the difference between two values rather than 0 or 1, and
    there is no deleting, only stretching. So a sequence held longer in the
    middle is free, and the two need not be the same length.

    >>> dtw([0, 1, 3, 6, 3, 1, 0], [0, 1, 1, 3, 6, 6, 3, 1, 0])
    0.0
    >>> dtw([0, 1, 3, 6, 3, 1, 0], [0, 0, 1, 3, 6, 3, 1])
    1.0
    >>> dtw([1, 2], [1, 2])
    0.0
    """
    D = [[INF] * (len(b) + 1) for _ in range(len(a) + 1)]
    D[0][0] = 0.0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = abs(a[i - 1] - b[j - 1])
            D[i][j] = cost + min(D[i - 1][j], D[i][j - 1], D[i - 1][j - 1])
    return D[-1][-1]


# ------------------------------------------------------------------ main ----

SLOW = [0, 1, 3, 6, 3, 1, 0]
FAST = [0, 1, 1, 3, 6, 6, 3, 1, 0]


def main(argv):
    if argv[:1] == ["--fib"]:
        n = int(argv[1]) if len(argv) > 1 else 30
        t = time.perf_counter()
        fib_slow(n)
        slow = time.perf_counter() - t
        t = time.perf_counter()
        fib_cached.cache_clear()
        fib_cached(n)
        fast = time.perf_counter() - t
        print(f"fib({n}) = {fib_cached(n)}")
        print(f"  from the definition: {slow:8.3f} s")
        print(f"  with the cache:      {fast:8.6f} s")
        return
    if argv[:1] == ["--dtw"]:
        print(f"a = {SLOW}")
        print(f"b = {FAST}     the same shape, held longer in the middle")
        print(f"dtw(a, b) = {dtw(SLOW, FAST)}")
        return
    a, b = (argv + ["kitten", "sitting"])[:2] if len(argv) < 2 else argv[:2]
    n = levenshtein(a, b)
    print(f"{a} -> {b}: {n} edit{'' if n == 1 else 's'}")
    for step in edits(a, b):
        print(f"  {step}")


if __name__ == "__main__":
    main(sys.argv[1:])
