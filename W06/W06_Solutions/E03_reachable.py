"""Composition. Search with no goal: where could we possibly get to? SOLUTION.

Run the tests:

    python -m doctest W06_Solutions/E03_reachable.py

No output means every test passed.

`bfs` stops as soon as it finds the goal. Take the goal away and let it run to
exhaustion, and what you have explored is the whole connected part of the
graph. That is how you find out how big a state space really is.
"""

from collections import deque

from E01_river import ROADS, START, successors


def reachable(successors, start):
    """Every state reachable from `start`, as a set. `start` itself counts.

    Breadth-first search with the goal test removed: keep a frontier and a
    visited set, and stop when the frontier runs dry.

    The river has sixteen states on paper and ten that are safe, and every
    safe one can actually be reached:

    >>> len(reachable(successors, START))
    10

    A dict is not a successor function, but a `lambda` turns it into one:

    >>> len(reachable(lambda town: ROADS[town], "Galway"))
    12
    >>> sorted(reachable(lambda n: {"a": "b", "b": "a", "c": ""}[n], "c"))
    ['c']
    """
    seen = {start}
    frontier = deque([start])
    while frontier:
        state = frontier.popleft()
        for nxt in successors(state):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def connected(successors, a, b):
    """Is there any route at all from `a` to `b`?

    >>> connected(successors, "LLLL", "RRRR")
    True

    "LLRR" is the wolf and the goat left alone together. It is a state you can
    write down, and there is no way to reach it:

    >>> connected(successors, "LLLL", "LLRR")
    False
    """
    return b in reachable(successors, a)
