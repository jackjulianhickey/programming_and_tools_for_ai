"""Drill. Summarising a column down to one or two numbers. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E03_summary.py

No output means every test passed.
"""

import pandas as pd

# Given: the same tiny table as E02.
PENGUINS = pd.DataFrame({
    "species": ["Adelie", "Adelie", "Gentoo", "Gentoo", "Chinstrap"],
    "island": ["Dream", "Biscoe", "Biscoe", "Biscoe", "Dream"],
    "bill_mm": [39.1, 40.3, 46.1, 50.0, 46.5],
    "mass_g": [3750.0, 3250.0, 4500.0, 5700.0, 3500.0],
})


def column_range(df, name):
    """Return (smallest, largest) of one column, as a tuple.

    >>> print(*column_range(PENGUINS, "mass_g"))
    3250.0 5700.0
    >>> print(*column_range(PENGUINS, "bill_mm"))
    39.1 50.0
    """
    return df[name].min(), df[name].max()


def column_mean(df, name):
    """Return the mean of one column, rounded to 2 decimal places.

    >>> print(column_mean(PENGUINS, "mass_g"))
    4140.0
    >>> print(column_mean(PENGUINS, "bill_mm"))
    44.4
    """
    return round(df[name].mean(), 2)


def spread(df, name):
    """Return the standard deviation of one column, rounded to 2 places.

    Pandas divides by n - 1, not n, which is the usual convention for a
    sample. Numpy's std divides by n unless you tell it otherwise, so the
    two disagree by a little; this is a famous source of confusion.

    >>> print(spread(PENGUINS, "bill_mm"))
    4.57
    >>> print(spread(PENGUINS, "mass_g"))
    989.57
    """
    return round(df[name].std(), 2)
