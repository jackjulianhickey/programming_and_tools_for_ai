"""Composition. How far is everywhere, in moves? SOLUTION.

Run the tests:

    python -m doctest W06/E04_hops.py

No output means every test passed.

One BFS answers "how far is the goal?" for every goal at once, because a
state is first reached along a shortest path to it. Keep the distance instead
of the predecessor and you get the whole table for the price of one search.

QUESTION: `hops_from` records a distance for a state the first time it sees
that state, and never changes it afterwards. Why is that safe here, and what
would go wrong on `ROADS` if the numbers we wanted were minutes rather than
roads? Write your answer in the comment at the bottom.
"""

from collections import deque

from E01_river import ROADS, START, successors


def hops_from(successors, start):
    """How many moves each reachable state is from `start`, as a dict.

    `start` itself is 0. Everything else is one more than the state it was
    first reached from.

    >>> hops_from(successors, START)["RRRR"]
    7
    >>> hops_from(successors, START)["RLRL"]
    1

    Four roads from Galway to Clifden, whichever way you go:

    >>> hops_from(lambda town: ROADS[town], "Galway")["Clifden"]
    4
    >>> hops_from(lambda n: {"a": "b", "b": "a"}[n], "a") == {"a": 0, "b": 1}
    True
    """
    frontier = deque([start])
    hops = {start: 0}

    while frontier:
        state = frontier.popleft()

        for nxt in successors(state):
            if nxt not in hops:
                hops[nxt] = hops[state]+1
                frontier.append(nxt)
    return hops


def farthest_hops(successors, start):
    """The distance to the state that is hardest to reach from `start`.

    >>> farthest_hops(successors, START)
    7
    >>> farthest_hops(lambda town: ROADS[town], "Galway")
    4
    """
    return max(hops_from(successors, start).values())


# ANSWER: It's because BFS moves outwards in circles so the first time we see a state will be the shortest number of moves.
# It is not weighted. With roads a path with 2 roads might take more time that a path with more roads.
