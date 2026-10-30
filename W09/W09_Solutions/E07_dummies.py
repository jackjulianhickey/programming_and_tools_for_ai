"""Drill. Turning words into numbers a distance can be computed on. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E07_dummies.py

No output means every test passed.

"Gentoo" is not a number, and there is no sensible distance between it and
"Adelie". One-hot encoding replaces the column with one column per value,
holding 1 where that was the value and 0 everywhere else. The lecture used
this on species and island.
"""

import pandas as pd

# Given: the same tiny table as E02.
PENGUINS = pd.DataFrame({
    "species": ["Adelie", "Adelie", "Gentoo", "Gentoo", "Chinstrap"],
    "island": ["Dream", "Biscoe", "Biscoe", "Biscoe", "Dream"],
    "bill_mm": [39.1, 40.3, 46.1, 50.0, 46.5],
    "mass_g": [3750.0, 3250.0, 4500.0, 5700.0, 3500.0],
})


def encode(df, column):
    """Replace one text column with a 0/1 column for each of its values.

    The new columns are named after the old column and the value, so
    "species" becomes "species_Adelie", "species_Chinstrap", "species_Gentoo".
    Use dtype=int: by default you get True and False, which are the same
    thing but print less clearly.

    >>> out = encode(PENGUINS, "species")
    >>> "species" in out.columns
    False
    >>> [c for c in out.columns if c.startswith("species_")]
    ['species_Adelie', 'species_Chinstrap', 'species_Gentoo']
    >>> out["species_Gentoo"].tolist()
    [0, 0, 1, 1, 0]

    The other columns are left alone:

    >>> out["bill_mm"].tolist()
    [39.1, 40.3, 46.1, 50.0, 46.5]

    And it works on any text column:

    >>> encode(PENGUINS, "island")["island_Dream"].tolist()
    [1, 0, 0, 0, 1]
    """
    return pd.get_dummies(df, columns=[column], dtype=int)


def n_new_columns(df, column):
    """How many columns would encoding `column` add, net of the one removed?

    One column goes, one per distinct value arrives.

    >>> n_new_columns(PENGUINS, "species")     # 3 species, minus the original
    2
    >>> n_new_columns(PENGUINS, "island")      # 2 islands, minus the original
    1
    """
    return df[column].nunique() - 1


# Write it once yourself, then use the built-in for the rest of your life:
# n_new_columns is only ever a sanity check. pandas already knows how wide
# the result is, and encode(df, column).shape[1] will tell you.
