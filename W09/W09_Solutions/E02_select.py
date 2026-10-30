"""Drill. Getting rows and columns out of a table. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E02_select.py

No output means every test passed.

A DataFrame is a table: named columns, each holding one kind of thing, and
rows that line up across them. Everything this week starts here.
"""

import pandas as pd

# Given: a tiny table to practise on. Five penguins, four of the columns the
# lecture used.
PENGUINS = pd.DataFrame({
    "species": ["Adelie", "Adelie", "Gentoo", "Gentoo", "Chinstrap"],
    "island": ["Dream", "Biscoe", "Biscoe", "Biscoe", "Dream"],
    "bill_mm": [39.1, 40.3, 46.1, 50.0, 46.5],
    "mass_g": [3750.0, 3250.0, 4500.0, 5700.0, 3500.0],
})


def column_list(df, name):
    """Return one column of df as an ordinary Python list.

    >>> column_list(PENGUINS, "species")
    ['Adelie', 'Adelie', 'Gentoo', 'Gentoo', 'Chinstrap']
    >>> column_list(PENGUINS, "mass_g")
    [3750.0, 3250.0, 4500.0, 5700.0, 3500.0]
    """
    return df[name].tolist()


def heavier_than(df, grams):
    """Return the rows of df whose mass_g is greater than grams.

    The result is a DataFrame, not a list, so it still has all its columns.

    >>> heavier_than(PENGUINS, 4000)["species"].tolist()
    ['Gentoo', 'Gentoo']
    >>> heavier_than(PENGUINS, 3600)["species"].tolist()
    ['Adelie', 'Gentoo', 'Gentoo']

    Nothing qualifies, and that is an empty table rather than an error:

    >>> len(heavier_than(PENGUINS, 10000))
    0
    """
    return df[df["mass_g"] > grams]
