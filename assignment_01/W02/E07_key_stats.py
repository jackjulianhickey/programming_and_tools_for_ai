"""Composition. How un-random is a sequence of keypresses? SOLUTION.

Run the tests:

    python -m doctest W02/E07_key_stats.py

No output means every test passed.

The oracle beats you because your typing has structure. These two functions
measure two kinds of structure directly, without any model at all.

QUESTION: for a genuinely random sequence, what would you expect switch_rate
to be? Write your answer in the comment at the bottom.
"""


def longest_run(history):
    """Return the length of the longest run of one repeated key.

    A run is a stretch of the same character. In "ffdff" the runs are
    "ff", "d", "ff", so the longest is 2.

    >>> longest_run("ffdff")
    2
    >>> longest_run("fffff")
    5
    >>> longest_run("fdfdfd")
    1
    >>> longest_run("f")
    1

    An empty history has no runs at all:

    >>> longest_run("")
    0
    """

    if not history:
        return 0
    
    longest = 1
    current = 1
    for i in range(1, len(history)):
        if history[i] == history[i - 1]:
            current += 1
        else:
            current = 1
        if current > longest:
            longest = current

    return longest


def switch_rate(history):
    """Return the fraction of keypresses that differed from the one before.

    Count the places where the key changed, and divide by the number of
    places where it could have changed, which is one less than the length.

    >>> switch_rate("fdfdfd")     # changes every time
    1.0
    >>> switch_rate("ffffff")     # never changes
    0.0
    >>> switch_rate("ffdd")       # one change out of three chances
    0.3333333333333333
    >>> round(switch_rate("fdfdff"), 2)
    0.8

    A sequence with no pairs in it has no chances to change, so there is
    nothing to average and we say 0.0 rather than dividing by zero:

    >>> switch_rate("f")
    0.0
    >>> switch_rate("")
    0.0
    """
    if not history or (len(history) == 1):
        return 0.0

    switches = 0
    for i in range(1, len(history)):
        if history[i] != history[i-1]:
            switches += 1
    
    return switches / (len(history)-1)


# ANSWER: 50% as then the ability of predicting the next keystroke can go either way.