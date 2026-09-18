"""Drill. A dict comprehension. SOLUTION.

Run the tests:

    python -m doctest W02_Solutions/E03_invert_dict.py

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
    return {v: k for k, v in d.items()}


# ANSWER: keys are unique, but values need not be. Both "a" and "b" have the
# value 1, so both produce the key 1 in the inverted dict, and the second
# write overwrites the first. Nothing goes wrong and nothing is reported --
# the dict just comes out shorter. Inverting is only safe when the values are
# unique, and it is your job, not Python's, to know that they are.
