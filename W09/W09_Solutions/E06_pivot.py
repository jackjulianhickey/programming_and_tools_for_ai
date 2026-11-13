"""Composition. Turning a long list of results into a table. SOLUTION.

Run the tests:

    python -m doctest W09_Solutions/E06_pivot.py

No output means every test passed.

This is the step the lecture program takes at the end. Results come out of
an experiment *long* -- one row per run, one column per thing you varied --
because that shape is easy to write and easy to add to. Tables in papers are
*wide*. pivot_table is how you get from one to the other.
"""

import pandas as pd

# Given: four runs of some experiment, in the long shape.
RUNS = pd.DataFrame({
    "metric": ["euclidean", "euclidean", "manhattan", "manhattan"],
    "setting": ["norm on", "norm off", "norm on", "norm off"],
    "accuracy": [0.90, 0.75, 0.86, 0.70],
})


def wide(df, index, columns, values):
    """Swing one column out across the top of the table.

    index says what goes down the side, columns what goes across the top,
    and values what fills the middle.

    >>> wide(RUNS, "setting", "metric", "accuracy").to_dict()
    {'euclidean': {'norm off': 0.75, 'norm on': 0.9}, 'manhattan': {'norm off': 0.7, 'norm on': 0.86}}

    Swap the two round and the table is transposed:

    >>> wide(RUNS, "metric", "setting", "accuracy").to_dict()
    {'norm off': {'euclidean': 0.75, 'manhattan': 0.7}, 'norm on': {'euclidean': 0.9, 'manhattan': 0.86}}
    """
    return df.pivot_table(index=index, columns=columns, values=values)


def best_by(df, group, column):
    """Which group has the highest mean `column`?

    >>> best_by(RUNS, "metric", "accuracy")
    'euclidean'
    >>> best_by(RUNS, "setting", "accuracy")
    'norm on'
    """
    return df.groupby(group)[column].mean().idxmax()
