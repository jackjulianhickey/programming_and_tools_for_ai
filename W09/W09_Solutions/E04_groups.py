"""Drill. Splitting a table into groups and summarising each one. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E04_groups.py

No output means every test passed.

groupby is the single most useful thing pandas does. Say which column to
split on, then say what to work out for each group.
"""

import pandas as pd

# Given: the same tiny table as E02.
PENGUINS = pd.DataFrame({
    "species": ["Adelie", "Adelie", "Gentoo", "Gentoo", "Chinstrap"],
    "island": ["Dream", "Biscoe", "Biscoe", "Biscoe", "Dream"],
    "bill_mm": [39.1, 40.3, 46.1, 50.0, 46.5],
    "mass_g": [3750.0, 3250.0, 4500.0, 5700.0, 3500.0],
})


def group_sizes(df, by):
    """How many rows are in each group? Return a plain dict.

    >>> group_sizes(PENGUINS, "species") == {"Adelie": 2, "Chinstrap": 1,
    ...                                      "Gentoo": 2}
    True
    >>> group_sizes(PENGUINS, "island") == {"Biscoe": 3, "Dream": 2}
    True
    """
    return df.groupby(by).size().to_dict()


def group_means(df, by, column):
    """The mean of `column` within each group, rounded to 1 place, as a dict.

    >>> group_means(PENGUINS, "species", "mass_g") == {"Adelie": 3500.0,
    ...     "Chinstrap": 3500.0, "Gentoo": 5100.0}
    True
    >>> group_means(PENGUINS, "island", "bill_mm") == {"Biscoe": 45.5,
    ...                                                "Dream": 42.8}
    True
    """
    return df.groupby(by)[column].mean().round(1).to_dict()
