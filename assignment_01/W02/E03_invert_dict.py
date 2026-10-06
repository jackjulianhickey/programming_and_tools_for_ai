"""Drill. A dict comprehension.

Run the tests:

    python -m doctest W02/E03_invert_dict.py

No output means every test passed.

QUESTION: the last doctest below loses a pair. Why? Write your answer in
the comment at the bottom.
"""


def invert_dict(d):
    """Return a new dict with every key-value pair the other way round.

    Use a dict comprehension: {new_key: new_value for k, v in d.items()}.

    >>> invert_dict({"a": 1, "dog": 3, "giraffe": 7})
    {1: 'a', 3: 'dog', 7: 'giraffe'}
    >>> invert_dict({})
    {}

    Inverting twice gets you back where you started:

    >>> invert_dict(invert_dict({"a": 1}))
    {'a': 1}

    But not always:

    >>> invert_dict({"a": 1, "b": 1})
    {1: 'b'}
    """
    dict_inverted = {v: k for k, v in d.items()}
    return dict_inverted


# ANSWER: The last doctest loses a pair because dictionaries cannot have duplicate keys. 
# In the example `{"a": 1, "b": 1}`, both "a" and "b" have the same value of 1. 
# When inverting the dictionary, the key 1 can only map to one value, so it ends up mapping to 'b', which is the last key processed.
