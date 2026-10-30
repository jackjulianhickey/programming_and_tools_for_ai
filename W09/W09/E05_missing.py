"""Drill. Missing values, and the two different things to do about them.

Run the tests:

    python -m doctest W09/E05_missing.py

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
    df_copy = df.copy()
    median = df_copy[column].median()
    df_copy[column] = df_copy[column].fillna(median)
    return df_copy


# ANSWER: (the QUESTION is at the top of this file)
