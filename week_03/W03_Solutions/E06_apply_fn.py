"""Composition. Write map yourself, twice: eagerly, then lazily. SOLUTION.

Run the tests:

    python -m doctest W03_Solutions/E06_apply_fn.py

No output means every test passed.

QUESTION: the second version works on an endless sequence and the first one
does not. Why? Write your answer in the comment at the bottom.
"""


# Given: an endless generator, to prove a point at the end. It never stops, so
# never call list() on it.
def naturals():
    """Yield 0, 1, 2, 3, ... for ever."""
    n = 0
    while True:
        yield n
        n += 1


def apply_fn_to_list(fn, L):
    """Return a new list holding fn(x) for every x in L.

    One line, with a list comprehension. `fn` is a function passed as an
    argument, like `keep` in the lecture and `key` in `sorted`.

    >>> apply_fn_to_list(len, ["a", "bb", "ccc"])
    [1, 2, 3]
    >>> apply_fn_to_list(str.upper, ["ab", "cd"])
    ['AB', 'CD']

    The function can be anything that takes one argument:

    >>> apply_fn_to_list(lambda x: x * x, [1, 2, 3, 4])
    [1, 4, 9, 16]
    >>> apply_fn_to_list(len, [])
    []
    """
    return [fn(x) for x in L]


def apply_fn_to_list_gen(fn, g):
    """Yield fn(x) for every x that g yields. The lazy version.

    `g` is any iterable, and this is itself a generator: nothing is computed
    until somebody asks. So there is no comprehension and no list here, just
    a loop and a `yield`.

    >>> list(apply_fn_to_list_gen(len, ["a", "bb", "ccc"]))
    [1, 2, 3]
    >>> list(apply_fn_to_list_gen(str.upper, iter(["ab", "cd"])))
    ['AB', 'CD']

    Calling it computes nothing at all:

    >>> squares = apply_fn_to_list_gen(lambda x: x * x, naturals())
    >>> type(squares).__name__
    'generator'

    And now the point. `naturals()` never ends, so `apply_fn_to_list` could
    never return -- but this one hands over squares for as long as we ask:

    >>> [next(squares) for _ in range(6)]
    [0, 1, 4, 9, 16, 25]
    """
    for x in g:
        yield fn(x)


# Python has both of these built in, as `map`. It is the lazy one: `map` returns
# an object that computes nothing until you iterate it, exactly like
# apply_fn_to_list_gen. Wrap it in `list()` when you want the eager one.
#
#     >>> list(map(len, ["a", "bb", "ccc"]))
#     [1, 2, 3]
#
# Write it once yourself, then use the built-in for the rest of your life. Most
# Python programmers would use a comprehension for the eager case anyway, and
# keep `map` for the lazy one.


# ANSWER: apply_fn_to_list has to finish building the whole list before it can
# return anything, and naturals() never finishes, so the call would never come
# back -- it would fill memory until the program died. apply_fn_to_list_gen
# returns a generator immediately and does the work one item at a time, only
# when asked, so it never needs to know how long the sequence is. Laziness is
# what makes an endless sequence usable at all.
