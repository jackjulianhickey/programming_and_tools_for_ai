"""Composition. Edit distance in one row. SOLUTION.

Run the tests:

    python -m doctest W07_Solutions/E04_one_row.py

No output means every test passed.

The lecture showed that `D[i][j]` needs only two cells from the row above and
the one immediately to its left. So the whole table is never needed: two lists
are enough, the row we finished and the row we are building.

Your `levenshtein_row` must return exactly what `E01`'s `levenshtein` returns.

**Do not build a table.** The point of the exercise is the space, and a grid of
`(len(a)+1) x (len(b)+1)` cells gives the right answers while missing that
entirely. Nothing here checks. You are on your honour, and the interview is
where it gets asked about.
"""

from E01_editdist import levenshtein
def levenshtein_row(a, b):
    """Edit distance, holding only two rows at a time.

    >>> levenshtein_row("kitten", "sitting")
    3
    >>> levenshtein_row("ACGTACGTAC", "CGTACGTACA")
    2
    >>> levenshtein_row("", "abc")
    3
    >>> levenshtein_row("abc", "abc")
    0
    >>> levenshtein_row("", "")
    0

    It must agree with the lecture's table version everywhere:

    >>> pairs = [("kitten", "sitting"), ("flaw", "lawn"), ("", "abc")]
    >>> all(levenshtein_row(a, b) == levenshtein(a, b) for a, b in pairs)
    True
    """
    prev = list(range(len(b) + 1))          # row 0: the base case
    for i, x in enumerate(a, start=1):
        curr = [i]                          # column 0: the other base case
        for j, y in enumerate(b, start=1):
            cost = 0 if x == y else 1
            curr.append(min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]
