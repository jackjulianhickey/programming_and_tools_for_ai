"""Composition. How far is everywhere, in moves? SOLUTION.

Run the tests:

    python -m doctest W06_Solutions/E04_hops.py

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
    distance = {start: 0}
    frontier = deque([start])
    while frontier:
        state = frontier.popleft()
        for nxt in successors(state):
            if nxt not in distance:
                distance[nxt] = distance[state] + 1
                frontier.append(nxt)
    return distance


def farthest_hops(successors, start):
    """The distance to the state that is hardest to reach from `start`.

    >>> farthest_hops(successors, START)
    7
    >>> farthest_hops(lambda town: ROADS[town], "Galway")
    4
    """
    return max(hops_from(successors, start).values())


# ANSWER: BFS takes states off the frontier in order of distance, so the first
# time a state is seen it is being seen along a shortest path -- any later
# route to it is at least as long, and there is nothing to improve. That
# argument uses the fact that every move costs exactly 1. Minutes are not all
# 1: Galway to Roundstone is four roads either way, but 70 minutes one way and
# 105 the other, so the first arrival is no longer the best one and a figure
# written down early would be wrong. That is exactly the case Dijkstra's
# algorithm handles, by taking the cheapest-so-far state next instead of the
# shallowest.
