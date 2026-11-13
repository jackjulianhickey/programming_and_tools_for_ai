"""Drill. Missing values, and the two different things to do about them. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E05_missing.py

No output means every test passed.

Real tables have holes in them. Pandas writes a hole as NaN, which is a
float meaning "not a number", and it is not equal to anything -- including
itself -- so you cannot test for it with ==. Use .isna() instead.

QUESTION: the lecture dropped the penguins whose sex was not recorded, but
filled in nothing. Why is filling in a missing *measurement* reasonable,
while filling in a missing *label* is not? Answer in the comment at the
bottom of this file.
"""

import pandas as pd

# Given: the same tiny table, with three values missing.
PENGUINS = pd.DataFrame({
    "species": ["Adelie", "Adelie", "Gentoo", "Gentoo", "Chinstrap"],
    "bill_mm": [39.1, None, 46.1, 50.0, 46.5],
    "mass_g": [3750.0, 3250.0, None, 5700.0, None],
})


def count_missing(df):
    """How many values are missing in each column? Return a plain dict.

    >>> count_missing(PENGUINS) == {"species": 0, "bill_mm": 1, "mass_g": 2}
    True
    >>> count_missing(PENGUINS[["species", "bill_mm"]]) == {"species": 0,
    ...                                                     "bill_mm": 1}
    True
    """
    return df.isna().sum().to_dict()


def drop_missing(df, column):
    """Return only the rows where `column` has a value.

    >>> drop_missing(PENGUINS, "mass_g")["species"].tolist()
    ['Adelie', 'Adelie', 'Gentoo']
    >>> drop_missing(PENGUINS, "bill_mm")["species"].tolist()
    ['Adelie', 'Gentoo', 'Gentoo', 'Chinstrap']
    """
    return df.dropna(subset=[column])


def fill_with_median(df, column):
    """Return a copy of df with the holes in `column` filled by its median.

    The median is worked out from the values that are there. Filling changes
    the table, so work on a copy: a function that quietly rewrites its own
    argument is a function nobody can use twice.

    >>> fill_with_median(PENGUINS, "mass_g")["mass_g"].tolist()
    [3750.0, 3250.0, 3750.0, 5700.0, 3750.0]
    >>> fill_with_median(PENGUINS, "bill_mm")["bill_mm"].tolist()
    [39.1, 46.3, 46.1, 50.0, 46.5]

    The original is untouched:

    >>> count_missing(PENGUINS)["mass_g"]
    2
    """
    filled = df.copy()
    filled[column] = filled[column].fillna(filled[column].median())
    return filled


# ANSWER: a missing measurement is a missing *input*. Filling it with the
# median is a guess, and a guess that is wrong only makes the model's job
# harder -- we can still check afterwards how well the model did. A missing
# label is the *answer*. If we invent one and then mark the model against it,
# we are marking it against our own guess rather than against the truth, and
# a high score would mean only that the model had learned to agree with us.
