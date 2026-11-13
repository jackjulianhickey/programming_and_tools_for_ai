"""Extension. Each algorithm on the other one's data.

Run the tests:

    python -m doctest W07/E06_wrong_tool.py

No output means every test passed.

Levenshtein is for symbols and DTW is for numbers. Nothing stops you running
either on the other kind of data, and what goes wrong is worth understanding:
each algorithm has an assumption built into it, and the assumption only shows
itself when it is false.

Write both functions, then answer the questions from what the doctests show.

QUESTION 1: `levenshtein` compares items with `==`, and two measured floats are
almost never exactly equal. What does the distance degenerate to? Does `tol`
really fix it?

QUESTION 2: `dtw_symbols("bookkeeper", "bokeper")` is 0.0, meaning DTW calls
the misspelling a perfect match. Explain why, and say whether DTW could ever be
used for spellchecking. Write your answers in the comments at the bottom.
"""

INF = float("inf")
INF = float("inf")


def levenshtein_tol(a, b, tol):
    """Edit distance on numbers, counting two values equal if within tol.

    >>> levenshtein_tol([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], 0.0)
    0
    >>> levenshtein_tol([1.0, 2.0, 3.0], [1.05, 2.0, 3.0], 0.0)
    1
    >>> levenshtein_tol([1.0, 2.0, 3.0], [1.05, 2.0, 3.0], 0.1)
    0
    >>> levenshtein_tol([1.0, 2.0, 3.0], [1.0, 1.0, 2.0, 3.0], 0.1)
    1
    >>> levenshtein_tol([1.0], [999.0], 0.1)
    1
    """
    D = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        D[i][0] = i
    for j in range(len(b) + 1):
        D[0][j] = j

    for i in range(1, len(a) + 1):
        for x in range(1, len(b) + 1):
            cost = 0 if abs(a[i - 1] - b[x - 1]) <= tol else 1
            D[i][x] = min(
               D[i - 1][x] + 1,
               D[i][x - 1] + 1,
               D[i - 1][x - 1] + cost 
            )
         
    return D[-1][-1]


def dtw_symbols(a, b):
    """DTW on symbols, costing 0 for a match and 1 for a mismatch.

    >>> dtw_symbols("abc", "abc")
    0.0
    >>> dtw_symbols("abc", "xyz")
    3.0
    >>> dtw_symbols("aab", "ab")
    0.0
    >>> dtw_symbols("bookkeeper", "bokeper")
    0.0
    """

    D = [[INF] * (len(b) + 1) for _ in range(len(a) + 1)]
    D[0][0] = 0.0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = cost + min(
                D[i - 1][j],
                D[i][j - 1],
                D[i - 1][j - 1]
            )
    return D[-1][-1]


# ANSWER 1: When no two floats are exactly equal the cost will always be 1 resulting the lengths of the sequences.
# Tol ensures that they are within a set tolerance limit so that floating points
# can be compared without the subtraction of these values
# needing to fall to zero which might not be possible because of floating points. 
# Tol doesn't really solve the problem as magnitude is ignored giving the same cost no matter the values.


# ANSWER 2: DTW doesn't see repeated chars because of its design. It lacks a deletion
# and cannot see double letters at all because of how it streches it's checking. This makes it
# entirely unsuitable as a spell checker.