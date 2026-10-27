"""Drill. Read a graph out of a dict, whatever shape the dict is. SOLUTION.

Run the tests:

    python -m doctest W06_Solutions/E02_neighbours.py

No output means every test passed.

`E01_river.py` has two graphs in it, and they are not stored the same way.
`RIVER_GRAPH` maps a state to a *list* of states; `ROADS` maps a town to a
*dict* of town -> minutes. All three functions here work on both, because
iterating a dict gives you its keys.
"""

from E01_river import RIVER_GRAPH, ROADS


def neighbours(graph, node):
    """Which nodes is `node` joined to? Sorted, so the answer is predictable.

    An empty list if we have never heard of the node, rather than a KeyError.

    >>> neighbours(ROADS, "Galway")
    ['Oughterard', 'Spiddal']
    >>> neighbours(RIVER_GRAPH, "LLRL")
    ['RLRL', 'RLRR', 'RRRL']
    >>> neighbours(ROADS, "Dublin")
    []
    """
    return sorted(graph.get(node, []))


def is_edge(graph, a, b):
    """Is there an edge from `a` to `b`?

    >>> is_edge(ROADS, "Galway", "Oughterard")
    True
    >>> is_edge(ROADS, "Galway", "Clifden")
    False
    >>> is_edge(ROADS, "Dublin", "Galway")
    False
    """
    return b in neighbours(graph, a)


def degree(graph, node):
    """How many edges does `node` have?

    >>> degree(ROADS, "Roundstone")
    3
    >>> degree(RIVER_GRAPH, "LLLL")
    1
    """
    return len(neighbours(graph, node))
