"""Drill. defaultdict, for collecting rather than counting. SOLUTION.

Run the tests:

    python -m doctest W02_Solutions/E06_group_by.py

No output means every test passed.
"""

from collections import defaultdict


def group_by_first_letter(words):
    """Group words by their first letter, keeping the order they came in.

    Use a defaultdict for this. 
    Return a plain dict, not a defaultdict, so that it prints tidily:
    dict(d) makes an ordinary dict out of any dict.

    >>> group_by_first_letter(["apple", "avocado", "banana"])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    >>> group_by_first_letter([])
    {}
    >>> group_by_first_letter(["one"])
    {'o': ['one']}
    """
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)
