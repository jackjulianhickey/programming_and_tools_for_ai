"""Drill. Nothing to write here: the only job is to run this file. SOLUTION.

This is the whole search program from the lecture, complete: the river
crossing of Parts 1 to 3, and the Connemara road map of Part 4. Run its tests:

    python -m doctest W06_Solutions/E01_river.py

No output means every test passed.

Then run it as a program, which prints the seven crossings:

    python W06_Solutions/E01_river.py

and try the variants the lecture used:

    python W06_Solutions/E01_river.py --explicit   # search the typed-out graph
    python W06_Solutions/E01_river.py --dfs        # depth-first, not breadth-first
    python W06_Solutions/E01_river.py --states     # all 16 states, safe or not
    python W06_Solutions/E01_river.py --route Galway Roundstone

Read `bfs_graph` and `bfs` side by side. They differ in one line, and that
line is the whole idea of the week: a graph you look up in a dict, and a
graph that is computed on demand and never exists all at once.

Then read `bfs_graph` and `dijkstra` side by side. They differ in the
container: a queue that hands back the state found first, and a heap that
hands back the state reached most cheaply.
"""

import heapq
from collections import deque

# A state says which bank each of the four things is on: farmer, wolf, goat,
# cabbage, in that order, each "L" or "R". So "LLLL" is everything on the left
# bank, which is where we start, and "RRRR" is the goal.
ITEMS = "FWGC"
START = "LLLL"
GOAL = "RRRR"

# The ten safe states and their crossings, typed out by hand. `successors`
# below computes exactly this, which is the point of Part 2: we would rather
# not type it.
RIVER_GRAPH = {
    "LLLL": ["RLRL"],
    "RLRL": ["LLLL", "LLRL"],
    "LLRL": ["RLRL", "RRRL", "RLRR"],
    "RRRL": ["LLRL", "LRLL"],
    "LRLL": ["RRRL", "RRLR"],
    "RLRR": ["LLRL", "LLLR"],
    "LLLR": ["RLRR", "RRLR"],
    "RRLR": ["LRLL", "LLLR", "LRLR"],
    "LRLR": ["RRLR", "RRRR"],
    "RRRR": ["LRLR"],
}

# Part 4's graph: Connemara, roughly, with driving times in minutes. The value
# is a dict rather than a list, because each neighbour now carries a weight.
# Every road appears twice, once from each end, because you can drive it
# either way; `check_symmetric` is there to catch any possible typo.
#
# Note that `bfs_graph` runs on this graph unchanged, without a word about
# weights: iterating a dict gives its keys, so `for nxt in graph[state]` walks
# the neighbours either way. It answers the wrong question, which is the point
# of Part 4.
ROADS = {
    "Galway":      {"Spiddal": 25, "Oughterard": 25},
    "Spiddal":     {"Galway": 25, "Rossaveal": 20},
    "Rossaveal":   {"Spiddal": 20, "Carna": 35},
    "Carna":       {"Rossaveal": 35, "Roundstone": 25},
    "Roundstone":  {"Carna": 25, "Recess": 18, "Clifden": 20},
    "Oughterard":  {"Galway": 25, "MaamCross": 15, "Cong": 30},
    "MaamCross":   {"Oughterard": 15, "Recess": 12, "Leenaun": 20},
    "Recess":      {"MaamCross": 12, "Roundstone": 18, "Clifden": 20},
    "Leenaun":     {"MaamCross": 20, "Cong": 35, "Letterfrack": 25},
    "Cong":        {"Oughterard": 30, "Leenaun": 35},
    "Letterfrack": {"Leenaun": 25, "Clifden": 15},
    "Clifden":     {"Recess": 20, "Roundstone": 20, "Letterfrack": 15},
}


def is_safe(state):
    """Is this state safe, ie does nothing get eaten while the farmer is away?

    The wolf eats the goat, and the goat eats the cabbage, unless the farmer
    is on that bank to stop it.

    >>> is_safe("LLLL")
    True
    >>> is_safe("RLLL")      # farmer alone on the right: wolf, goat, cabbage left
    False
    >>> is_safe("RLRL")      # farmer takes the goat: wolf and cabbage are fine
    True
    """
    farmer, wolf, goat, cabbage = state # each item either "L" or "R"
    if goat == wolf and farmer != goat:
        return False
    if goat == cabbage and farmer != goat:
        return False
    return True


def successors(state):
    """Yield every safe state one crossing away from `state`.

    The farmer always crosses, alone or with one thing from the same bank.

    >>> list(successors("LLLL"))     # only the goat may go first
    ['RLRL']
    >>> list(successors("RLRL"))     # row back alone, or bring the goat back
    ['LLRL', 'LLLL']

    It is a generator, so nothing is computed until somebody asks:

    >>> type(successors("LLLL")).__name__
    'generator'
    """
    farmer, wolf, goat, cabbage = state
    there = "R" if farmer == "L" else "L"    # the bank the boat is heading for

    # The four possible crossings, written out one at a time. The farmer always
    # moves to the other bank, and so does whatever comes along -- and a thing
    # can only come along if it is on the farmer's bank to begin with.
    crossings = [there + wolf + goat + cabbage]           # the farmer, alone
    if wolf == farmer:
        crossings.append(there + there + goat + cabbage)  # ... with the wolf
    if goat == farmer:
        crossings.append(there + wolf + there + cabbage)  # ... with the goat
    if cabbage == farmer:
        crossings.append(there + wolf + goat + there)     # ... with the cabbage

    for crossed in crossings:
        if is_safe(crossed):
            yield crossed


def path_to(came_from, state):
    """Walk the predecessor pointers back from `state` to build the path.

    `came_from` maps each state to the state we reached it from. The start
    maps to None, which is where the walk stops.

    >>> path_to({"a": None, "b": "a", "c": "b"}, "c")
    ['a', 'b', 'c']
    >>> path_to({"a": None}, "a")
    ['a']
    """
    path = [state]
    while came_from[path[-1]] is not None:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def bfs_graph(graph, start, goal):
    """Shortest path from start to goal, in a graph given as a dict.

    >>> bfs_graph(RIVER_GRAPH, START, GOAL)
    ['LLLL', 'RLRL', 'LLRL', 'RRRL', 'LRLL', 'RRLR', 'LRLR', 'RRRR']

    None if there is no route at all:

    >>> bfs_graph({"a": ["b"], "b": ["a"], "z": []}, "a", "z") is None
    True
    """
    frontier = deque([start])
    # One dict does two jobs: it remembers how we got to each state, and being
    # in it at all is what "visited" means.
    came_from = {start: None}
    while frontier:
        state = frontier.popleft()
        if state == goal:
            return path_to(came_from, state)
        for nxt in graph[state]:
            if nxt not in came_from:
                came_from[nxt] = state
                frontier.append(nxt)
    return None


def bfs(successors, start, goal):
    """Shortest path from start to goal, in a graph computed on demand.

    The only difference from `bfs_graph` is `successors(state)` in place of
    `graph[state]`. The graph is never built, and never needs to fit in
    memory.

    >>> bfs(successors, START, GOAL)
    ['LLLL', 'RLRL', 'LLRL', 'RRRL', 'LRLL', 'RRLR', 'LRLR', 'RRRR']

    Seven crossings, which is the known answer:

    >>> len(bfs(successors, START, GOAL)) - 1
    7
    """
    frontier = deque([start])
    came_from = {start: None}
    while frontier:
        state = frontier.popleft()
        if state == goal:
            return path_to(came_from, state)
        for nxt in successors(state):
            if nxt not in came_from:
                came_from[nxt] = state
                frontier.append(nxt)
    return None


def dfs(successors, start, goal):
    """A path from start to goal, depth first. Two characters different.

    `frontier.pop()` instead of `frontier.popleft()`: take the state we saw
    most recently rather than the one we saw longest ago. A queue becomes a
    stack, breadth-first becomes depth-first, and the path is no longer the
    shortest one.

    >>> dfs(successors, START, GOAL)
    ['LLLL', 'RLRL', 'LLRL', 'RLRR', 'LLLR', 'RRLR', 'LRLR', 'RRRR']

    On this graph it happens to find the other seven-crossing solution, so
    look at `--dfs` on a bigger problem before believing that DFS is fine.
    """
    frontier = [start]
    came_from = {start: None}
    while frontier:
        state = frontier.pop()
        if state == goal:
            return path_to(came_from, state)
        for nxt in successors(state):
            if nxt not in came_from:
                came_from[nxt] = state
                frontier.append(nxt)
    return None


def describe(state):
    """A readable picture of one state: left bank, river, right bank.

    >>> describe("LLLL")
    'FWGC ~ '
    >>> describe("RLRL")
    'WC ~ FG'
    """
    left = "".join(x for x, side in zip(ITEMS, state) if side == "L")
    right = "".join(x for x, side in zip(ITEMS, state) if side == "R")
    return f"{left} ~ {right}"


def crossing(before, after):
    """Name the crossing that turns `before` into `after`.

    >>> crossing("LLLL", "RLRL")
    'farmer takes the goat  -->'
    >>> crossing("RLRL", "LLLL")
    '<--  farmer takes the goat'
    """
    moved = [ITEMS[i] for i in range(1, len(ITEMS)) if before[i] != after[i]]
    names = {"W": "the wolf", "G": "the goat", "C": "the cabbage"}
    what = f"takes {names[moved[0]]}" if moved else "rows back alone"
    if after[0] == "R":
        return f"farmer {what}  -->"
    return f"<--  farmer {what}"


# ------------------------------------------------- and now with weights ---


def roads_from(town):
    """Yield (neighbouring town, minutes) pairs: the successor function for ROADS.

    A dict of dicts is already this shape --- `.items()` on the inner dict is
    exactly a run of (neighbour, weight) pairs.

    >>> sorted(roads_from("Galway"))
    [('Oughterard', 25), ('Spiddal', 25)]
    """
    return ROADS[town].items()


def road_time(route):
    """How long does this route take, in minutes?

    >>> road_time(["Galway", "Oughterard", "MaamCross"])
    40
    >>> road_time(["Galway"])
    0
    """
    return sum(ROADS[a][b] for a, b in zip(route, route[1:]))


class PriorityQueue:
    """A heap, wrapped up so that nothing outside this class mentions `heapq`.

    Push items with a priority; `pop` always hands back the smallest one.

    >>> pq = PriorityQueue()
    >>> pq.push("Clifden", 72)
    >>> pq.push("Recess", 52)
    >>> len(pq)
    2
    >>> pq.pop()
    ('Recess', 52)

    It is an ordinary priority queue, with no opinions about the items in it.
    The same item may go in twice, and an item may go back in after it has
    come out --- both of which some other algorithm will want, even though
    Dijkstra does not:

    >>> pq.push("Recess", 90)
    >>> pq.push("Recess", 40)
    >>> [pq.pop() for _ in range(3)]
    [('Recess', 40), ('Clifden', 72), ('Recess', 90)]

    `__len__` makes `while pq:` work, exactly as it does for a `deque`:

    >>> bool(pq), len(pq)
    (False, 0)
    >>> pq.pop()
    Traceback (most recent call last):
        ...
    IndexError: pop from an empty PriorityQueue
    """

    def __init__(self):
        # heapq keeps a list *partly* sorted: enough that the smallest item is
        # always at the front, and not a scrap more.
        self._heap = []
        self._count = 0

    def push(self, item, priority):
        """Put `item` in, to come out when nothing cheaper is waiting."""
        # The count breaks ties, so two items of equal priority come out in
        # the order they went in -- and so the items themselves never have to
        # be comparable. This is the recipe in the heapq documentation.
        heapq.heappush(self._heap, (priority, self._count, item))
        self._count += 1

    def pop(self):
        """Take the cheapest item waiting, as (item, priority).

        The pair is (item, priority) to match `push(item, priority)`. Inside,
        the heap holds (priority, count, item), because that is what makes it
        sort -- but that is this class's business, not its caller's.
        """
        if not self._heap:
            raise IndexError("pop from an empty PriorityQueue")
        priority, _, item = heapq.heappop(self._heap)
        return item, priority

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return f"PriorityQueue({len(self)} waiting)"


def dijkstra(successors, start, goal):
    """The cheapest route from start to goal, and what it costs.

    `bfs` with the `deque` replaced by a `PriorityQueue`: take the state we
    can reach most cheaply, not the one we happened to find first. Like `bfs`
    it takes a **function**, so the graph never has to exist --- except that
    each neighbour now arrives with the cost of getting to it.

    The other change is what `came_from` remembers. BFS stores only which
    state it came from, because with every move costing the same, the first
    route to a state is the best one and there is nothing to compare against.
    Here a later route can be cheaper, so we store the cost alongside, and a
    state goes back on the frontier whenever we better it.

    >>> dijkstra(roads_from, "Galway", "Roundstone")
    (70, ['Galway', 'Oughterard', 'MaamCross', 'Recess', 'Roundstone'])

    BFS finds a route of the same four roads that takes half an hour longer,
    because it is answering "fewest roads", not "least time":

    >>> road_time(bfs_graph(ROADS, "Galway", "Roundstone"))
    105

    A dict of dicts can be handed over as a function, the same way Part 3
    handed over `RIVER_GRAPH`:

    >>> dijkstra(lambda town: ROADS[town].items(), "Galway", "Clifden")
    (72, ['Galway', 'Oughterard', 'MaamCross', 'Recess', 'Clifden'])

    >>> dijkstra(roads_from, "Galway", "Galway")
    (0, ['Galway'])
    >>> dijkstra(roads_from, "Letterfrack", "Rossaveal")
    (95, ['Letterfrack', 'Clifden', 'Roundstone', 'Carna', 'Rossaveal'])
    """
    frontier = PriorityQueue()
    frontier.push(start, 0)
    came_from = {start: (None, 0)}
    while frontier:
        node, cost = frontier.pop()
        if node == goal:
            # path_to wants predecessors on their own, so drop the costs.
            steps = {where: prev for where, (prev, _) in came_from.items()}
            return cost, path_to(steps, node)
        for nxt, weight in successors(node):
            if (nxt not in came_from
                    or cost + weight < came_from[nxt][1]):
                came_from[nxt] = (node, cost + weight)
                frontier.push(nxt, cost + weight)
    return None, None


def check_symmetric(graph):
    """Every road should appear from both ends, with the same time.

    >>> check_symmetric(ROADS)
    True
    >>> check_symmetric({"a": {"b": 1}, "b": {"a": 2}})
    Traceback (most recent call last):
        ...
    ValueError: a -- b does not match
    """
    for a, out in graph.items():
        for b, weight in out.items():
            if graph[b].get(a) != weight:
                raise ValueError(f"{a} -- {b} does not match")
    return True


if __name__ == "__main__":
    import argparse
    from itertools import product

    # argparse is not on the syllabus. You never have to write anything like
    # this; it is here so that every variant in the lecture can be run.
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--explicit", action="store_true",
                   help="search RIVER_GRAPH, the version typed out by hand")
    p.add_argument("--dfs", action="store_true",
                   help="depth-first instead of breadth-first")
    p.add_argument("--states", action="store_true",
                   help="print all 16 states, and which of them are safe")
    p.add_argument("--route", nargs=2, metavar=("FROM", "TO"),
                   help="leave the river: fewest roads and quickest, on ROADS")
    args = p.parse_args()

    if args.states:
        for bits in product("LR", repeat=len(ITEMS)):
            state = "".join(bits)
            mark = "safe" if is_safe(state) else "EATEN"
            print(f"{state}   {describe(state):>9}   {mark}")
        raise SystemExit

    if args.route:
        check_symmetric(ROADS)
        start, goal = args.route
        fewest = bfs_graph(ROADS, start, goal)
        cost, quickest = dijkstra(roads_from, start, goal)
        print(f"fewest roads:  {len(fewest) - 1} roads, "
              f"{road_time(fewest)} min")
        print("   " + " -> ".join(fewest))
        print(f"quickest:      {len(quickest) - 1} roads, {cost} min")
        print("   " + " -> ".join(quickest))
        raise SystemExit

    if args.explicit:
        path = bfs_graph(RIVER_GRAPH, START, GOAL)
    elif args.dfs:
        path = dfs(successors, START, GOAL)
    else:
        path = bfs(successors, START, GOAL)

    print(f"{describe(path[0]):>9}")
    for before, after in zip(path, path[1:]):
        print(f"{describe(after):>9}    {crossing(before, after)}")
    print(f"\n{len(path) - 1} crossings")
