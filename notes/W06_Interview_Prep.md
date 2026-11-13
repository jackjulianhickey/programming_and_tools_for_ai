# Week 6 Interview Prep: Graphs, Implicit State Spaces & Shortest-Path Search

[<- Back to Master Interview Playbook](./README.md)

**Core Topics:** Explicit vs. Implicit Graphs, Adjacency Representations (`dict` of `list`s vs. `dict` of `dict`s), Generators as Successor Functions, Breadth-First Search (`deque`), Depth-First Search (`list` stack), Predecessor Backtracking, Binary Min-Heaps (`heapq` & `PriorityQueue`), and Dijkstra's Shortest-Path Algorithm.

> **Why Week 6 Matters for 8–10 Marks:** Week 6 is one of the highest-yield weeks in the entire CT5148 portfolio for testing **all three interview pillars** (`Explain`, `Trace`, `Analyse`). Expect questions on why `deque.popleft()` beats `list.pop(0)`, why visited states are recorded *when pushing* rather than *when popping*, when BFS finds optimal paths vs. when Dijkstra is required, why infinite implicit graphs break `connected` or `dfs`, and why calling `dijkstra` inside a loop in `E06` is `O(V * (V + E) log V)` instead of `O((V + E) log V)`.

---

## Table of Contents

1. [Week 6 Exercise Summary Table](#1-week-6-exercise-summary-table)
2. [Reference Context: `E01_river.py` (Given Code)](#2-reference-context-e01_riverpy-given-code)
3. [`E02_neighbours.py` — Reading Explicit Graph Dicts](#3-e02_neighbourspy--reading-explicit-graph-dicts)
4. [`E03_reachable.py` — Exhaustive State-Space Exploration](#4-e03_reachablepy--exhaustive-state-space-exploration)
5. [`E04_hops.py` — Unweighted Single-Source Shortest Distances](#5-e04_hopspy--unweighted-single-source-shortest-distances)
6. [`E05_calculator.py` — BFS on an Infinite Implicit Graph](#6-e05_calculatorpy--bfs-on-an-infinite-implicit-graph)
7. [`E06_route.py` — BFS ("Fewest Roads") vs. Dijkstra ("Least Time")](#7-e06_routepy--bfs-fewest-roads-vs-dijkstra-least-time)
8. [Week 6 Master Comparison Cheat Sheet (BFS vs. DFS vs. Dijkstra)](#8-week-6-master-comparison-cheat-sheet-bfs-vs-dfs-vs-dijkstra)

---

## 1. Week 6 Exercise Summary Table

Let `V` be the number of reachable vertices/states, `E` the number of edges/transitions, and `d` the out-degree of a single queried vertex (`d <= V`). For implicit trees/graphs with branching factor `b` and solution depth `k`, `V` explored up to depth `k` is `O(b^k)`.

| Exercise File | Functions | Difficulty Tier | Time Complexity (Your Code) | Space Complexity (Your Code) |
| :--- | :--- | :--- | :--- | :--- |
| [E01_river.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py) | [`bfs_graph`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L154-L177), [`bfs`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L180-L205), [`dfs`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L208-L232), [`PriorityQueue`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L290-L353), [`dijkstra`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L356-L404) | Reference (Given) | BFS/DFS: `O(V + E)`<br>Dijkstra: `O((V + E) log E)` | BFS/DFS: `O(V)`<br>Dijkstra: `O(V + E)` |
| [E02_neighbours.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py) | [`neighbours`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L18-L35)<br>[`is_edge`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L38-L50)<br>[`degree`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L53-L66) | Warm-up | `neighbours`: `O(d log d)`<br>`is_edge`: `O(1)` (`dict`) / `O(d)` (`list`)<br>`degree`: `O(d)` *(could be `O(1)`)* | `neighbours`: `O(d)`<br>`is_edge`: `O(1)`<br>`degree`: `O(1)` |
| [E03_reachable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py) | [`reachable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py#L19-L48)<br>[`connected`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py#L50-L62) | Moderate | `reachable`: `O(V + E)`<br>`connected`: `O(V + E)` *(no early exit!)* | `O(V)` |
| [E04_hops.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py) | [`hops_from`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L24-L52)<br>[`farthest_hops`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L55-L63) | Moderate | `hops_from`: `O(V + E)`<br>`farthest_hops`: `O(V + E)` | `O(V)` |
| [E05_calculator.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py) | [`calc_successors`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L33-L43)<br>[`presses`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L46-L54)<br>[`fewest_presses`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L57-L67) | **Hard (8–10 Mark Target)** | `calc_successors`: `O(1)`<br>`presses` / `fewest_presses`: `O(3^k)` worst-case up to optimal depth `k` (`O(V_k)` states reached) | `O(3^k)` worst-case (`O(V_k)` in `came_from` & `frontier`) |
| [E06_route.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py) | [`time_lost`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L17-L35)<br>[`quickest_times`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L38-L60) | **Hard (8–10 Mark Target)** | `time_lost`: `O((V + E) log E)`<br>`quickest_times`: `O(V * (V + E) log E)` *(runs `dijkstra` `V` times!)* | `O(V + E)` |

---

## 2. Reference Context: `E01_river.py` (Given Code)

**File:** [E01_river.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py)

Every exercise in Week 6 imports data structures, graphs, or search routines directly from [E01_river.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py). You must be comfortable explaining any part of `E01` if asked how your functions work under the hood.

### 2.1 Two Explicit Graph Shapes (`RIVER_GRAPH` vs. `ROADS`)
- **`RIVER_GRAPH`** ([`RIVER_GRAPH`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L43-L54), `dict[str, list[str]]`): Unweighted adjacency list of the 10 safe states (out of $2^4 = 16$ total `"L"`/`"R"` strings for Farmer, Wolf, Goat, Cabbage). States are 4-character strings (`"LLLL"` to `"RRRR"`), which are **immutable and hashable**, so they can serve as `dict` keys and `set` members.
- **`ROADS`** ([`ROADS`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L65-L78), `dict[str, dict[str, int]]`): Weighted undirected Connemara road network (12 towns, driving times in minutes). Because iterating over a Python `dict` yields its **keys**, `for nxt in graph[state]:` works identically on both `RIVER_GRAPH` and `ROADS` — though on `ROADS` it silently ignores the minute weights!

### 2.2 Explicit Graph Lookup vs. Implicit Graph Generation
Compare [`bfs_graph`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L154-L177) and [`bfs`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L180-L205):
- Line 173 in `bfs_graph`: `for nxt in graph[state]:` (requires the entire graph to exist in memory upfront).
- Line 201 in `bfs`: `for nxt in successors(state):` (computes neighbours **lazily on demand** via a function/generator like [`successors`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L102-L133)).
- **Why this matters:** In AI search (Rubik's cube with $\sim 4.3 \times 10^{19}$ states, chess, or `E05`'s **infinite** calculator graph), building `graph` as a `dict` is impossible. Passing a `successors` function lets `bfs` materialize only the states it actually visits. Conversely, any explicit `dict` graph `G` can be turned into a successor function with `lambda node: G[node]`.

### 2.3 `came_from` & `path_to`: One Dict Doing Two Jobs
- In [`bfs_graph`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L168), `came_from = {start: None}` acts simultaneously as:
  1. **The `visited` set** (`if nxt not in came_from:` is an `O(1)` average hash lookup preventing cycles and duplicate frontier entries).
  2. **The parent-pointer tree** mapping each reached state to the state that first discovered it.
- [`path_to`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L136-L151) reconstructs the route by walking backwards from `goal` until hitting the sentinel `None` at `start`, using `path.append(...)` (`O(1)` amortized) followed by `path.reverse()` (`O(L)`), avoiding `path.insert(0, ...)` which would shift elements and take `O(L^2)`.

### 2.4 `bfs` (`deque`) vs. `dfs` (`list`)
- [`bfs`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L180-L205) uses `collections.deque` (a doubly-linked list of fixed-size blocks) so `frontier.append(nxt)` (right) and `frontier.popleft()` (left, FIFO) are both **`O(1)`**. Using a Python `list` with `frontier.pop(0)` would shift every remaining element left in `O(V)` time per pop, degrading BFS from `O(V + E)` to `O(V^2 + E)`.
- [`dfs`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L208-L232) uses a plain `list` as a LIFO stack (`append` + `pop()` from the right end, both `O(1)` amortized). It finds *a* path (on finite graphs), **not** guaranteed to be shortest, and can diverge infinitely on infinite graphs even when a 1-step solution exists.

### 2.5 `PriorityQueue` (`heapq`) & `dijkstra`
- [`PriorityQueue`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L290-L353) wraps Python's min-heap module `heapq`.
  - **Why `(priority, self._count, item)` on line 334?** Python compares tuples lexicographically element-by-element. If two items tie on `priority`, comparing `self._count` (a strictly increasing integer `0, 1, 2, ...`) does **two crucial jobs**: (1) breaks ties in FIFO insertion order, and (2) ensures Python **never** compares `item` against `item` (which would crash with `TypeError` if states were `dict`s or custom objects without `<`).
  - `push` and `pop` each run in **`O(log H)`** where `H` is the current heap size.
- [`dijkstra`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L356-L404):
  - `came_from` stores `(predecessor, best_cost_so_far)` pairs: `came_from = {start: (None, 0)}`.
  - **Edge relaxation & Lazy Deletion ([lines 400–403](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L400-L403)):** Unlike BFS, the first path discovered to `nxt` may not be the cheapest! Whenever `cost + weight < came_from[nxt][1]`, Dijkstra updates `came_from[nxt]` and calls `frontier.push(nxt, cost + weight)`. Because `heapq` has no `O(log V)` `decrease_key` operation, the older higher-cost entry `(old_cost, old_count, nxt)` stays inside `self._heap` as a **stale entry** ("lazy deletion").
  - **Subtle detail in `E01`'s `dijkstra`:** Notice `dijkstra` checks `if node == goal:` **when popping** ([line 395](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L395)), *never* when pushing, because `goal` might be pushed early via an expensive fewer-road route and improved later via a cheaper multi-road route before `goal` reaches the top of the min-heap. Also note `E01` does not write `if cost > came_from[node][1]: continue` after `pop()`; for non-negative edge weights, popping a stale `(node, cost)` still preserves correctness because `cost > came_from[node][1]` cannot beat already-relaxed neighbour costs, though adding `if cost > came_from[node][1]: continue` avoids redundant `successors(node)` expansions.

---

## 3. `E02_neighbours.py` — Reading Explicit Graph Dicts

- **File:** [E02_neighbours.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py)
- **Functions:** [`neighbours`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L18-L35), [`is_edge`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L38-L50), [`degree`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L53-L66)
- **Difficulty Tier:** Warm-up

### Your Code

```python
from E01_river import RIVER_GRAPH, ROADS


def neighbours(graph, node):
    L = []
    if node not in graph:
        return L
    for nxt in graph[node]:
        L.append(nxt)
    return sorted(L)


def is_edge(graph, a, b):
    if a not in graph:
        return False
    return True if b in graph[a] else False


def degree(graph, node):
    num = 0
    if node not in graph:
        return num
    for edge in graph[node]:
        num+=1
    return num
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** These three helper functions inspect an explicit adjacency-dictionary graph—returning a node's sorted neighbour list, testing whether a directed edge `(a, b)` exists, and counting a node's outgoing edges—while returning safe defaults (`[]`, `False`, `0`) for unknown nodes instead of raising `KeyError`. All three work unchanged on both unweighted (`dict` of `list`s) and weighted (`dict` of `dict`s) graphs because iterating or checking `in` on a Python `dict` operates on its keys.
- **Line-by-Line & Variable Breakdown:**
  - **In [`neighbours`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L18-L35):**
    - `L = []` (line 30): Accumulator list initialized empty so it can be returned immediately on line 32 if `node not in graph`. *(Interview self-awareness note: `L` is a capital single-letter name for "list"; if asked about naming, say a descriptive lowercase name like `adj` or `result`—or the one-liner `return sorted(graph.get(node, []))`—follows PEP 8 better.)*
    - `if node not in graph: return L` (lines 31–32): `O(1)` average hash-table guard against `KeyError` when `node` (e.g., `"Dublin"`) is absent.
    - `for nxt in graph[node]: L.append(nxt)` (lines 33–34): Iterates over `graph[node]`. When `graph` is `RIVER_GRAPH`, `graph[node]` is a `list[str]`; when `graph` is `ROADS`, `graph[node]` is a `dict[str, int]` and iterating yields its town-name keys (`nxt` = "next state/node").
    - `return sorted(L)` (line 35): Returns a new sorted `list` via Timsort for deterministic output regardless of insertion order.
  - **In [`is_edge`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L38-L50):**
    - `if a not in graph: return False` (lines 48–49): Guards `graph[a]` when source `a` is unknown.
    - `return True if b in graph[a] else False` (line 50): Tests membership of `b` in `graph[a]`. **Code quirk to know:** `b in graph[a]` *already* evaluates to `bool` (`True` or `False`), so the conditional expression `True if ... else False` is redundant; `return a in graph and b in graph[a]` is idiomatic. However, **algorithmically your `is_edge` beats the official solution** (`return b in neighbours(graph, a)`), which unnecessarily copies and *sorts* all neighbours in `O(d log d)` before scanning!
  - **In [`degree`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py#L53-L66):**
    - `num = 0` (line 61): Counter for outgoing edges, returned immediately (`0`) if `node not in graph`.
    - `for edge in graph[node]: num += 1` (lines 64–65): Counts each neighbour key/element `edge` in `graph[node]`. *(Note: `edge` is actually the neighbouring vertex name rather than a `(u, v)` tuple, and `len(graph[node])` would retrieve this count in `O(1)` instead of `O(d)`.)*

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `graph`: `dict[Hashable, Iterable[Hashable]]` (specifically `dict[str, list[str]]` for `RIVER_GRAPH` or `dict[str, dict[str, int]]` for `ROADS`).
  - `node`, `a`, `b`: `Hashable` (here `str`).
  - Local variables: `L` is `list[str]`; `nxt` and `edge` are `str`; `num` is `int`.
  - Return types: `neighbours` -> `list` (e.g., `list[str]`); `is_edge` -> `bool`; `degree` -> `int`.
- **Concrete Step-by-Step Trace (`neighbours(ROADS, "Galway")` & `is_edge(ROADS, "Galway", "Clifden")`):**
  1. `neighbours(ROADS, "Galway")`: `L = []`. `"Galway" not in ROADS` is `False`. `ROADS["Galway"]` is `{'Spiddal': 25, 'Oughterard': 25}`. Loop appends `'Spiddal'`, then `'Oughterard'` -> `L = ['Spiddal', 'Oughterard']`. `sorted(L)` returns `['Oughterard', 'Spiddal']`.
  2. `is_edge(ROADS, "Galway", "Clifden")`: `"Galway" not in ROADS` is `False`. `"Clifden" in {'Spiddal': 25, 'Oughterard': 25}` performs an `O(1)` dict key lookup -> `False` -> ternary returns `False`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Unknown node (`"Dublin"`):** `neighbours(ROADS, "Dublin")` -> `[]`; `is_edge(ROADS, "Dublin", "Galway")` -> `False`; `degree(ROADS, "Dublin")` -> `0`. No `KeyError` is raised.
  2. **Isolated node (`graph = {"Island": {}}`):** `"Island" in graph` is `True`, loop runs `0` times -> `neighbours` returns `[]`, `is_edge` returns `False`, `degree` returns `0`.
  3. **Directed graph asymmetry (`graph = {"a": ["b"], "b": []}`):** `is_edge(graph, "a", "b")` returns `True`, while `is_edge(graph, "b", "a")` returns `False`; `degree(graph, "a")` returns `1` (**out-degree**), while `degree(graph, "b")` returns `0` (incoming edges are not counted unless stored symmetrically).
  4. **Unhashable node (`neighbours(ROADS, ["Galway"])`) or Mixed neighbour types (`{"a": [1, "b"]}`):** Passing `["Galway"]` raises `TypeError: unhashable type: 'list'` at `if node not in graph:`. If a node's neighbour collection mixes incomparable types (`[1, "b"]`), `sorted(L)` raises `TypeError: '<' not supported between instances of 'str' and 'int'`, whereas `is_edge` and `degree` still succeed!

### Pillar 3 — Analyse (Complexity & Algorithmic Comparisons)

- **Time Complexity (let `d` be the out-degree of the queried node):**
  - `neighbours`: `O(d log d)` — `O(1)` average dict lookup + `O(d)` copy loop + `O(d log d)` Timsort.
  - `is_edge`: **`O(1)` average** when `graph[a]` is a `dict` (like `ROADS`, hash lookup on keys) or `set`, and **`O(d)`** when `graph[a]` is a `list` (like `RIVER_GRAPH`, linear scan).
  - `degree`: **`O(d)`** in your code due to the explicit `for edge in graph[node]: num += 1` loop. Replacing lines 61–66 with `return len(graph[node]) if node in graph else 0` reduces it to **`O(1)`** because Python `list` and `dict` objects store their element count in C header metadata.
- **Space Complexity:**
  - `neighbours`: `O(d)` auxiliary space for `L` and the sorted copy (note `L.sort(); return L` would sort `L` in-place rather than allocating a second `d`-element list, though still `O(d)` overall).
  - `is_edge` and `degree`: `O(1)` auxiliary space.
- **Data Structure Comparison (Adjacency Dict-of-Lists vs. Dict-of-Dicts/Sets vs. Adjacency Matrix):**
  - `dict` of `list`s (`RIVER_GRAPH`): `O(V + E)` space, `O(d)` `is_edge`, fast iteration.
  - `dict` of `dict`s (`ROADS`): `O(V + E)` space, **`O(1)`** `is_edge` + weight lookup, fast iteration.
  - `V x V` Adjacency Matrix: `O(V^2)` space (wasteful on sparse road maps), `O(1)` `is_edge`, but `O(V)` just to list a node's neighbours!

### Likely Interview Q&A

1. **Q: Why do all three functions work on both `RIVER_GRAPH` (values are `list`s) and `ROADS` (values are `dict`s) without `isinstance` checks?**
   - **A:** Because both `list` and `dict` implement Python's iterable and container protocols (`__iter__` and `__contains__`), and for a `dict` both operate on its **keys**—which in `ROADS` are the neighbouring town names, matching the elements of `RIVER_GRAPH`'s lists.
2. **Q: Look at line 50: `return True if b in graph[a] else False`. Can you simplify that, and how fast is `b in graph[a]`?**
   - **A:** Yes—`b in graph[a]` already returns a `bool`, so `return b in graph[a]` (or replacing the whole function with `return a in graph and b in graph[a]`) is cleaner. On `ROADS`, `graph[a]` is a `dict`, so `b in graph[a]` is `O(1)` average hash lookup; on `RIVER_GRAPH`, `graph[a]` is a `list`, so it's `O(d)` linear scan.
3. **Q: Why is your `degree` function `O(d)`, and how could you make it `O(1)`?**
   - **A:** My `for` loop walks every neighbour and increments `num`, taking `O(d)` time. Since Python `list` and `dict` store their length internally, `len(graph.get(node, ()))` returns the degree in `O(1)` constant time.

---

## 4. `E03_reachable.py` — Exhaustive State-Space Exploration

- **File:** [E03_reachable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py)
- **Functions:** [`reachable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py#L19-L48), [`connected`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py#L50-L62)
- **Difficulty Tier:** Moderate

### Your Code

```python
from collections import deque

from E01_river import ROADS, START, successors


def reachable(successors, start):
    frontier = deque([start])
    visited = {start}

    while frontier:
        state = frontier.popleft()

        for nxt in successors(state):
            if nxt not in visited:
                visited.add(nxt)
                frontier.append(nxt)
    return visited

def connected(successors, a, b):
    return True if b in reachable(successors, a) else False
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `reachable` performs an exhaustive Breadth-First Search on an implicit graph—removing the goal test from `bfs` so it explores until the `deque` frontier runs empty—and returns the complete `set` of states reachable from `start`. `connected` composes `reachable` to test whether target state `b` lies anywhere in `a`'s reachable component.
- **Line-by-Line & Variable Breakdown:**
  - `frontier = deque([start])` (line 38): FIFO queue seeded with `start`, holding discovered states whose outgoing transitions have not yet been expanded.
  - `visited = {start}` (line 39): A `set` (not `{}` which would be an empty `dict`!) recording every state seen so far. Because we don't need paths or distances here, a `set` is lighter and clearer than `E01`'s `came_from` `dict`. `start` is included immediately because 0 moves reaches `start`.
  - `while frontier:` / `state = frontier.popleft()` (lines 41–42): Continues until no unexpanded states remain, popping the oldest queued state in `O(1)` time.
  - `for nxt in successors(state):` (line 44): Calls the caller-supplied `successors` function/generator to lazily produce adjacent states.
  - `if nxt not in visited:` -> `visited.add(nxt)` -> `frontier.append(nxt)` (lines 45–47): **Critical invariant:** `nxt` is added to `visited` *at the moment it is enqueued*, NOT when it is later popped! This guarantees each reachable state enters `frontier` **at most once**.
  - `return True if b in reachable(successors, a) else False` (line 62): Computes the full reachable `set` from `a` and checks `O(1)` set membership of `b`. *(Same style note as `E02`: `return b in reachable(successors, a)` is already a `bool`.)*

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `successors`: `Callable[[T], Iterable[T]]` (e.g., generator function `successors(state)` or `lambda town: ROADS[town]`).
  - `start`, `a`, `b`: `T` (must be `Hashable`, e.g., `str` or `int`, because it is stored in `set` `visited`).
  - `frontier`: `collections.deque[T]`; `visited`: `set[T]`; `state`, `nxt`: `T`.
  - Return types: `reachable` -> `set[T]`; `connected` -> `bool`.
- **Concrete Step-by-Step Trace (`reachable` on River Graph first 3 pops from `"LLLL"`):**
  1. **Init:** `frontier = deque(['LLLL'])`, `visited = {'LLLL'}`.
  2. **Pop 1 (`state = 'LLLL'`):** `successors('LLLL')` yields `'RLRL'`. Not in `visited` -> `visited = {'LLLL', 'RLRL'}`, `frontier = deque(['RLRL'])`.
  3. **Pop 2 (`state = 'RLRL'`):** `successors('RLRL')` yields `'LLRL'`, `'LLLL'`. `'LLRL'` added (`visited` size 3, `frontier = deque(['LLRL'])`); `'LLLL'` already in `visited` (skipped, avoiding `LLLL <-> RLRL` infinite 2-cycle!).
  4. **Pop 3 (`state = 'LLRL'`):** `successors('LLRL')` yields `'RLRL'` (seen, skipped), `'RRRL'` (added), `'RLRR'` (added). `frontier = deque(['RRRL', 'RLRR'])`, `visited` size 5.
  5. Continues until all 10 safe states are in `visited` and `frontier` is empty; returns the 10-element `set`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **`a == b` on an unreachable/unsafe state (`connected(successors, "LLRR", "LLRR")`)**: `visited` is initialized to `{"LLRR"}` on line 39 before checking safety of `start`, so `"LLRR" in reachable(...)` returns **`True`** (0 steps from `"LLRR"` to itself). Meanwhile `connected(successors, "LLLL", "LLRR")` returns **`False`** because `successors` only ever yields states passing `is_safe`.
  2. **Infinite implicit graph (`connected(calc_successors, 0, 2)` using `E05`'s calculator!)**: **CRITICAL INTERVIEW TRAP!** Even though `2` is just **1 press away** from `0`, `connected` calls `reachable(calc_successors, 0)` first, which has **no goal check / early exit**, so it tries to materialize all infinitely many even integers and **hangs forever until `MemoryError`**! By contrast, `bfs(calc_successors, 0, 2) is not None` returns `True` in 1 step!
  3. **Directed graph (`G = {"a": ["b"], "b": []}`):** `connected(lambda x: G[x], "a", "b")` is `True`, whereas `connected(lambda x: G[x], "b", "a")` is `False` (`reachable` is directed reachability, not symmetric!).
  4. **Unknown start node with dict lambda (`reachable(lambda t: ROADS[t], "Dublin")`):** `frontier.popleft()` pops `"Dublin"`, then `successors("Dublin")` evaluates `ROADS["Dublin"]` and raises `KeyError: 'Dublin'`.

### Pillar 3 — Analyse (Complexity & Algorithmic Comparisons)

- **Time Complexity:**
  - `reachable`: **`O(V + E)`** where `V` is the number of states reachable from `start` and `E` is the total number of outgoing transitions yielded across those `V` states. Every reachable state is enqueued and popped exactly once (`O(V)`), and each yielded transition performs an `O(1)` average hash lookup in `visited` (`O(E)`).
  - `connected`: **`O(V + E)` in EVERY case** (best case AND worst case!), because `reachable(successors, a)` always explores the entire connected component of `a` before `b in ...` is tested! If you instead stopped as soon as `nxt == b` (like `bfs`), best-case time drops to `O(1)` while worst-case (when `b` is unreachable) remains `O(V + E)`.
- **Space Complexity:** **`O(V)`** — `visited` stores all `V` reachable states, and `frontier` holds at most `V` states at once.
- **BFS vs. DFS for `reachable`:**
  - If you replaced `frontier = deque([start])` and `popleft()` with `frontier = [start]` and `pop()` (iterative DFS), **`reachable` would return the exact same `set` in the exact same `O(V + E)` time and `O(V)` space!** Because `set` is unordered and there is no goal or distance being tracked, exploration order (breadth-first vs. depth-first) does not change the final reachable set on any finite graph.

### Likely Interview Q&A

1. **Q: What would go wrong if we moved `visited.add(state)` up to right after `state = frontier.popleft()` instead of adding `nxt` inside the `for` loop?**
   - **A:** It would still return the right set on finite graphs, **but** the same unpopped node `nxt` could be pushed onto `frontier` multiple times by different neighbours before finally being popped. On dense graphs that inflates `frontier` space from `O(V)` to `O(E)` and does redundant loop work (and in `E04`'s `hops_from`, overwriting distances on later pushes would corrupt shortest-hop counts!).
2. **Q: Why did `doctest` line 33 wrap `ROADS` in `lambda town: ROADS[town]` instead of passing `ROADS` directly?**
   - **A:** Because `reachable` expects a **callable** `successors(state)` (an implicit graph interface), and a `dict` is subscriptable (`ROADS[town]`), not callable (`ROADS(town)` raises `TypeError: 'dict' object is not callable`). The `lambda` adapts a `dict` lookup into a 1-argument function.
3. **Q: When is `b in reachable(successors, a)` much worse than `bfs(successors, a, b) is not None`?**
   - **A:** Whenever `b` is close to `a` inside a huge—or infinite—state space! `bfs` stops as soon as `b` is reached, whereas `reachable` exhaustively explores the entire component first (and never terminates on an infinite graph like `E05`). Only if you needed to answer *thousands* of connectivity queries from the *same* `a` on a finite graph would precomputing `S = reachable(successors, a)` once and checking `b in S` in `O(1)` per query win.

---

## 5. `E04_hops.py` — Unweighted Single-Source Shortest Distances

- **File:** [E04_hops.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py)
- **Functions:** [`hops_from`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L24-L52), [`farthest_hops`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L55-L63)
- **Difficulty Tier:** Moderate (with high-value Embedded Question!)

### Your Code

```python
from collections import deque

from E01_river import ROADS, START, successors


def hops_from(successors, start):
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
    return max(hops_from(successors, start).values())


# ANSWER: It's because BFS moves outwards in circles so the first time we see a state will be the shortest number of moves.
# It is not weighted. With roads a path with 2 roads might take more time that a path with more roads.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `hops_from` runs a single exhaustive BFS from `start` to build a dictionary mapping every reachable state to the minimum number of moves (edges) needed to reach it. `farthest_hops` then takes the maximum value in that dictionary to report how many moves away the hardest-to-reach state is (the vertex *eccentricity* of `start`).
- **Line-by-Line & Variable Breakdown:**
  - `hops = {start: 0}` (line 43): Just like `came_from` in `E01`, one `dict` does **two jobs**: membership in `hops` (`if nxt not in hops:`) acts as the `O(1)` `visited` check, while `hops[state]` stores the integer shortest-path distance from `start` (`0` moves to reach `start`).
  - `hops[nxt] = hops[state]+1` (line 50): Dynamic/inductive update—since `nxt` has never been seen before and is reached in one transition from `state`, its shortest move count is `hops[state] + 1`.
  - `return max(hops_from(successors, start).values())` (line 63): Extracts the `dict_values` view of all shortest hop distances and returns the largest integer in `O(V)` time.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `successors`: `Callable[[T], Iterable[T]]`; `start`: `T` (`Hashable`).
  - `frontier`: `collections.deque[T]`; `hops`: `dict[T, int]`.
  - Return types: `hops_from` -> `dict[T, int]`; `farthest_hops` -> `int`.
- **Concrete Step-by-Step Trace (`hops_from` on `{"a": ["b", "c"], "b": ["c", "d"], "c": ["d"], "d": []}` from `"a"`):**
  1. **Init:** `frontier = deque(['a'])`, `hops = {'a': 0}`.
  2. **Pop `'a'` (hop `0`):** Neighbours `'b'`, `'c'`. Both unseen -> `hops['b'] = 1`, `hops['c'] = 1`; `frontier = deque(['b', 'c'])`.
  3. **Pop `'b'` (hop `1`):** Neighbours `'c'`, `'d'`. `'c'` is **already in `hops`** (at hop `1`, NOT overwritten with `2`!); `'d'` unseen -> `hops['d'] = 2`; `frontier = deque(['c', 'd'])`.
  4. **Pop `'c'` (hop `1`):** Neighbour `'d'` already in `hops` (skipped). `frontier = deque(['d'])`.
  5. **Pop `'d'` (hop `2`):** No neighbours. `frontier` empty -> returns `{'a': 0, 'b': 1, 'c': 1, 'd': 2}`. `farthest_hops` -> `max([0, 1, 1, 2])` = `2`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Isolated start vertex (`successors = lambda _: []`):** `hops` starts as `{start: 0}`, loop pops `start`, sees 0 neighbours, returns `{start: 0}`. Crucially, `farthest_hops` calls `max([0])` and safely returns **`0`** (it can **never** hit `ValueError: max() iterable argument is empty` because `start` is always in `hops`!).
  2. **Disconnected graph:** Unreachable nodes never appear as keys in `hops`. Looking up an unreachable key (`hops_from(...)[unreachable]`) raises `KeyError`, and `farthest_hops` returns the max distance within `start`'s connected component (not `inf`).
  3. **What if `deque.popleft()` were accidentally replaced with `frontier.pop()` (DFS)?** Trace the exact graph above (`a -> b, c`, `b -> d`, `c -> d`, plus `b -> e -> d`): DFS could discover a node via a deep detour *first* and permanently lock in a non-minimal hop count in `hops`! `hops[nxt] = hops[state] + 1` **only** computes shortest distances because `frontier` is a FIFO queue!

### Pillar 3 — Analyse (Complexity, Comparisons & Embedded `# ANSWER`)

- **Time Complexity:**
  - `hops_from`: **`O(V + E)`** — **one** search computes shortest distances to **all `V` states simultaneously**! Compare this directly with `E06`'s `quickest_times`: if you instead called `bfs(successors, start, goal)` separately for every state, it would cost `O(V * (V + E))`!
  - `farthest_hops`: **`O(V + E)`** (`O(V + E)` for `hops_from` + `O(V)` for `max(...)`).
- **Space Complexity:** **`O(V)`** for the `hops` dictionary and `frontier` deque.
- **Embedded File Question (`# ANSWER` Review & Upgrade):**
  - *Question ([lines 13–16](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L13-L16)):* Why is it safe for `hops_from` to record a state's distance the first time it sees it and never change it, and what would go wrong on `ROADS` if we wanted minutes rather than roads?
  - *Your written answer ([lines 66–67](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L66-L67)):* Solid intuition ("moves outwards in circles" and "2 roads might take more time than a path with more roads").
  - **10/10 Spoken Upgrade for the Interview:**
    1. **Why BFS's first-seen distance is optimal:** Because every move costs `+1` and `frontier` is FIFO, the queue maintains a **monotonic two-layer invariant**—at any moment `frontier` holds only states at distance $d$ followed by states at distance $d + 1$. Therefore, the first time `nxt` is reached (from a state at distance $d$), no state popped later can have distance $< d$, so no path can reach `nxt` in fewer than $d + 1$ moves.
    2. **Two concrete `ROADS` counterexamples where minutes break this:**
       - **Fewer roads, MORE minutes (`Spiddal` -> `Clifden`):** BFS finds the **4-road** coastal route (`Spiddal -> Rossaveal -> Carna -> Roundstone -> Clifden` = $20 + 35 + 25 + 20 = 100\text{ min}$) first and locks in `Clifden`, missing the **5-road** inland route (`Spiddal -> Galway -> Oughterard -> MaamCross -> Recess -> Clifden` = $25 + 25 + 15 + 12 + 20 = 97\text{ min}$)!
       - **Equal roads, wrong tie-break (`Galway` -> `Roundstone`):** Both routes are **4 roads**, so whichever 4-road route BFS expands first (`Spiddal` coastal = **105 min**) blocks the second 4-road route (`Oughterard` inland = **70 min**)! That's why weighted graphs require Dijkstra's `PriorityQueue` + relaxation (`cost + weight < best[nxt]`).

### Likely Interview Q&A

1. **Q: Why does `hops_from` compute distances to *every* reachable state in `O(V + E)`, no slower asymptotically than finding a single farthest goal?**
   - **A:** Because in the worst case, a single-goal BFS already visits all `V` vertices and traverses all `E` edges. Recording `hops[nxt] = hops[state] + 1` in `O(1)` as we go harvests the shortest distance to every state in that single pass.
2. **Q: Could `farthest_hops` avoid `max(hops.values())` altogether?**
   - **A:** Yes! Because BFS pops states in monotonically non-decreasing order of hop distance (`0, 1, 1, 2, ...`), the **very last `state` popped** from `frontier` is guaranteed to have the maximum hop distance `hops[state]`! Calling `max(...)` is `O(V)` so total complexity is still `O(V + E)`, and `max(hops_from(...).values())` cleanly reuses `hops_from`.

---

## 6. `E05_calculator.py` — BFS on an Infinite Implicit Graph

- **File:** [E05_calculator.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py)
- **Functions:** [`calc_successors`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L33-L43), [`presses`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L46-L54), [`fewest_presses`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L57-L67)
- **Difficulty Tier:** **Hard (8–10 Mark Target)**

### Your Code

```python
from E01_river import bfs


def calc_successors(n):
    yield n * 3
    yield n + 2
    yield n - 2


def presses(target):
    return bfs(calc_successors, 0, target)


def fewest_presses(target):
    return len(presses(target)) - 1


# ANSWER: Because we start at 0 we can only add 2 or subtract 2 to make a difference. 
# When we multiple this by 3 we will only ever reach even numbers.
# Here the space is infinite and the frontier will continue to grow without ever hitting 101.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** We model the three-button calculator (`* 3`, `+ 2`, `- 2`) as an **infinite implicit state-space graph** where each integer on the display is a vertex and each button press is a directed unweighted edge. Passing the generator `calc_successors` into `E01`'s `bfs` finds the shortest sequence of display values from `0` to `target` without ever constructing the infinite graph in memory.
- **Line-by-Line & Variable Breakdown:**
  - `def calc_successors(n):` with three `yield` statements (lines 33–43): A **generator function**. Calling `calc_successors(n)` returns a lazy `generator` object that yields `n * 3`, then `n + 2`, then `n - 2` one at a time on demand.
  - **Why a state is just the `int` `n` (and NOT the button history):** Multiple button histories produce the same display value (e.g., `0 -> +2 -> *3 -> 6` in 2 presses vs. `0 -> +2 -> +2 -> +2 -> 6` in 3 presses, or `0 -> *3 -> 0` in 1 press). Making the state `n` collapses equivalent histories via `if nxt not in came_from:` in `bfs`, pruning huge redundant subtrees!
  - `bfs(calc_successors, 0, target)` (line 54): Reuses `E01`'s implicit `bfs` starting at `0` (`int` is immutable and hashable, so it works seamlessly in `came_from` alongside `"LLLL"` strings!).
  - `len(presses(target)) - 1` (line 67): **Fencepost rule**—a path list `[0, 2, 6, 8, 10]` has `5` states (including the initial `0` before any button is pressed) and therefore `5 - 1 = 4` transitions (button presses).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `n`, `target`: `int`.
  - `calc_successors(n)`: returns `Iterator[int]` (`generator` yielding 3 `int`s).
  - `presses(target)`: returns `list[int]` (when `target` is an even `int`; never returns for unreachable targets because the graph is infinite!).
  - `fewest_presses(target)`: returns `int`.
- **Concrete Step-by-Step Trace (`presses(6)`):**
  1. **Init in `bfs`:** `frontier = deque([0])`, `came_from = {0: None}`.
  2. **Pop `0` (depth 0):** `0 != 6`. `calc_successors(0)` yields:
     - `0` (`0 in came_from` -> skipped! Self-loop `0 * 3 == 0` harmlessly ignored!)
     - `2` (unseen -> `came_from[2] = 0`, enqueue `2`)
     - `-2` (unseen -> `came_from[-2] = 0`, enqueue `-2`)
     - Now `frontier = deque([2, -2])`.
  3. **Pop `2` (depth 1):** `2 != 6`. `calc_successors(2)` yields `6`, `4`, `0`:
     - `6` -> `came_from[6] = 2`, enqueue `6`
     - `4` -> `came_from[4] = 2`, enqueue `4`
     - `0` -> already in `came_from`, skipped.
     - Now `frontier = deque([-2, 6, 4])`. *(Notice `6` is in `came_from`, and `bfs` tests `state == goal` on pop!)*
  4. **Pop `-2` (depth 1):** `-2 != 6`. Yields `-6` (enqueued), `0` (seen), `-4` (enqueued). `frontier = deque([6, 4, -6, -4])`.
  5. **Pop `6` (depth 2):** `6 == 6`! Calls `path_to(came_from, 6)` -> walks `6 -> 2 -> 0 -> None`, reverses -> returns `[0, 2, 6]`. `fewest_presses(6)` returns `len([0, 2, 6]) - 1 = 2`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **`target = 0`:** `frontier.popleft()` pops `0`; `0 == 0` immediately on the first iteration before calling `calc_successors`! `presses(0)` returns `[0]`, and `fewest_presses(0)` returns `1 - 1 = 0`.
  2. **Negative even integer (`target = -6`):** Works completely! `0 -> -2 -> -6` returns `[0, -2, -6]` and `fewest_presses(-6) == 2`, because `- 2` and `* 3` explore negative even numbers symmetrically.
  3. **Odd integer (`target = 101`) or `float` (`target = 2.0` vs `2.5`):**
     - `target = 101` or `2.5`: **Infinite loop -> `MemoryError`!** `frontier` and `came_from` grow without bound across all even integers and never hit `101` or `2.5`. (Note: if `bfs` ever returned `None` on a *finite* graph for an unreachable target, `len(None) - 1` on line 67 would raise `TypeError: object of type 'NoneType' has no len()`!)
     - `target = 2.0`: Subtle Python quirk! In Python, `2 == 2.0` is `True` (`int` and `float` compare equal by value!), so `presses(2.0)` **terminates** and returns `[0, 2]` (`list[int]`)!
  4. **What if we replaced `bfs` with `dfs(calc_successors, 0, 2)`?!**
     - **KILLER INTERVIEW TRACE:** Even though `2` is **1 button press away**, `dfs(calc_successors, 0, 2)` **NEVER TERMINATES**! Why? At `0`, `calc_successors(0)` pushes `2` then `-2` onto the stack. `dfs` pops `-2` (LIFO!), which pushes `-6` then `-4`; popping `-4` pushes `-12`; popping `-12` pushes `-36, -10, -14`, plunging forever into negative numbers (`0 -> -2 -> -4 -> -12 -> -14 -> -16 -> ...`) while `2` sits untouched at index `0` of the stack forever! This proves **DFS is incomplete on infinite graphs**, whereas **BFS is complete** (guaranteed to find any reachable goal at finite depth $k$).

### Pillar 3 — Analyse (Complexity, Comparisons & Embedded `# ANSWER`)

- **Time & Space Complexity:**
  - `calc_successors(n)`: `O(1)` time and `O(1)` space.
  - `presses(target)` / `fewest_presses(target)`: Let $k$ be the minimum number of presses to reach an even `target` (note $k = O(\log |\text{target}|)$ because repeatedly multiplying by 3 and adjusting by $\pm 2$ builds numbers in base 3!). With branching factor $b = 3$, BFS explores at most $1 + 3 + 3^2 + \dots + 3^k = O(3^k)$ states before popping `target` (and significantly fewer in practice due to duplicate-state pruning in `came_from`, e.g., for `target = 100`, $k = 7$, $3^7 = 2187$, and `came_from` actually visits fewer than 700 integers!). Both **time** and **space** are **`O(b^k)` = `O(3^k)`** (or **`O(V_k)`** where `V_k` is the number of distinct states within $k$ steps of `0`), and $\infty$ if `target` is odd.
- **Embedded File Question (`# ANSWER` Review & Mathematical Proof):**
  - *Question ([lines 25–27](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L25-L27)):* Why does `fewest_presses(100)` return in a fraction of a second, while `fewest_presses(101)` never returns?
  - *Your written answer ([lines 70–72](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L70-L72)):* Spot-on! Spotlights both **even parity invariance** and the **infinite state space**.
  - **Crisp Mathematical Proof if Asked to Formalize:**
    - **Parity Invariant:** Let $P(n)$ be the property "$n$ is an even integer" ($n \equiv 0 \pmod 2$).
      1. *Base case:* Start state $0 = 2(0)$ is even.
      2. *Inductive step:* If $n = 2m$ is even, all three successors are even: $3n = 2(3m)$, $n + 2 = 2(m + 1)$, and $n - 2 = 2(m - 1)$.
    - Hence the connected component of $0$ is strictly $2\mathbb{Z}$ (all even integers—every even integer $2m$ is reachable via $|m|$ presses of `+2` or `-2`). Because $101 \equiv 1 \pmod 2$, $101 \notin 2\mathbb{Z}$, and because $2\mathbb{Z}$ is infinite, `frontier` never empties, so `bfs` never reaches `return None`.
    - *Follow-up: How would you fix `presses` for odd integers?* Add `if target % 2 != 0: return None` (and handle `None` in `fewest_presses`)—an `O(1)` domain-invariant check before launching search!

### Likely Interview Q&A

1. **Q: Why does `presses(100)` find `[0, 2, 4, 12, 36, 34, 102, 100]`—notice it overshoots to `102` and subtracts `2`! Could a greedy algorithm find that?**
   - **A:** A naive greedy strategy ("stay below `100` and get as close as possible") would do `0 -> 2 -> 6 -> 18 -> 54 -> ...` and get stuck adding `+2` twenty-three times! Going `36 -> 34` (`-2`, temporarily moving *farther* from `100`!) so that `34 * 3 = 102` lands one `-2` away from `100` shows why exhaustive shortest-path search (`bfs`) beats myopic greedy choices.
2. **Q: Why must `calc_successors` be a function/generator here instead of a dictionary like `RIVER_GRAPH`?**
   - **A:** Because $\mathbb{Z}$ is infinite—a dictionary mapping every integer to its three neighbours would require infinite memory and never finish building before `bfs` even started.

---

## 7. `E06_route.py` — BFS ("Fewest Roads") vs. Dijkstra ("Least Time")

- **File:** [E06_route.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py)
- **Functions:** [`time_lost`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L17-L35), [`quickest_times`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L38-L60)
- **Difficulty Tier:** **Hard (8–10 Mark Target)**

### Your Code

```python
from E01_river import ROADS, bfs_graph, dijkstra, road_time, roads_from


def time_lost(start, goal):
    fewest_roads = bfs_graph(ROADS, start, goal)
    fewest_roads_time = road_time(fewest_roads)

    quickest_roads_time, quickest_path = dijkstra(roads_from, start, goal)
    return fewest_roads_time - quickest_roads_time


def quickest_times(start):
    # time_to = {}
    # for town in ROADS:
    #     time, path = dijkstra(roads_from, start, town)
    #     time_to[town] = time

    # return time_to
    return {town: dijkstra(roads_from, start, town)[0] for town in ROADS}
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `time_lost` quantifies in minutes the penalty of choosing an unweighted "fewest roads" route (`bfs_graph`) over a weighted "minimum driving time" route (`dijkstra`) on Connemara's `ROADS` map. `quickest_times` uses a dictionary comprehension to map every town in `ROADS` to its minimum driving time from `start`.
- **Line-by-Line & Variable Breakdown:**
  - `fewest_roads = bfs_graph(ROADS, start, goal)` (line 31): Runs unweighted BFS on `ROADS` (`dict` of `dict`s), returning a `list[str]` of towns with the minimum number of road segments, ignoring minute weights.
  - `fewest_roads_time = road_time(fewest_roads)` (line 32): Passes that town list to `E01`'s [`road_time`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py#L279-L287) (`sum(ROADS[a][b] for a, b in zip(route, route[1:]))`) to sum the actual driving minutes of the BFS route.
  - `quickest_roads_time, quickest_path = dijkstra(roads_from, start, goal)` (line 34): Unpacks the `(cost, path)` tuple returned by `dijkstra`. *(Minor style note: `quickest_path` is unused, so Python convention often names it `_` as in `quickest_roads_time, _ = ...`.)*
  - `return fewest_roads_time - quickest_roads_time` (line 35): Returns the non-negative difference in minutes (`0` when BFS happens to pick an optimal-time route).
  - `return {town: dijkstra(roads_from, start, town)[0] for town in ROADS}` (line 60): Dictionary comprehension iterating over all 12 town keys in `ROADS`, running `dijkstra` to `town`, and indexing `[0]` to keep just the `cost` integer (concise version of your commented-out accumulator loop on lines 54–59).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `start`, `goal`: `str` (town names in `ROADS`).
  - `fewest_roads`, `quickest_path`: `list[str]` (or `None` if unreachable).
  - `fewest_roads_time`, `quickest_roads_time`: `int`.
  - Return types: `time_lost` -> `int`; `quickest_times` -> `dict[str, int]`.
- **Concrete Step-by-Step Trace (`time_lost("Galway", "Roundstone")` vs. `time_lost("Spiddal", "Clifden")`):**
  - **Case A — `time_lost("Galway", "Roundstone")` (`35`):**
    1. `bfs_graph(ROADS, "Galway", "Roundstone")`: `ROADS["Galway"]` has keys `'Spiddal'`, then `'Oughterard'`. Both coastal and inland routes take **4 roads**, and because `'Spiddal'` was inserted first in `ROADS["Galway"]`, BFS discovers `'Roundstone'` via `'Carna'` first: `['Galway', 'Spiddal', 'Rossaveal', 'Carna', 'Roundstone']`.
    2. `road_time(fewest_roads)` = $25 + 20 + 35 + 25 = 105$ minutes.
    3. `dijkstra(roads_from, "Galway", "Roundstone")`: Pops cheaper inland nodes (`Oughterard` at `25`, `MaamCross` at `40`, `Recess` at `52`, `Roundstone` at `70`) well before `Carna` (`80`) can push `Roundstone` (`105`). Returns `(70, ['Galway', 'Oughterard', 'MaamCross', 'Recess', 'Roundstone'])`.
    4. Returns $105 - 70 = 35$.
  - **Case B — `time_lost("Spiddal", "Clifden")` (`3` — true road-count vs. time trade-off!):**
    1. `bfs_graph` picks the **4-road** coastal route `['Spiddal', 'Rossaveal', 'Carna', 'Roundstone', 'Clifden']` -> `road_time` = $20 + 35 + 25 + 20 = 100$ min.
    2. `dijkstra` picks the **5-road** inland route `['Spiddal', 'Galway', 'Oughterard', 'MaamCross', 'Recess', 'Clifden']` -> `cost` = $25 + 25 + 15 + 12 + 20 = 97$ min.
    3. Returns $100 - 97 = 3$.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **`start == goal` (`time_lost("Galway", "Galway")`)**: `bfs_graph` returns `['Galway']`; `zip(['Galway'], [])` is empty so `road_time(['Galway'])` returns `0`; `dijkstra` returns `(0, ['Galway'])`; returns `0 - 0 = 0`. *(Quirky edge case: `time_lost("Dublin", "Dublin")` ALSO returns `0` without `KeyError`, because both `bfs_graph` and `dijkstra` test `state == goal` on the popped `start` node before ever looking it up in `ROADS`!)*
  2. **Unknown `start` with `start != goal` (`time_lost("Dublin", "Galway")`):** `bfs_graph` pops `"Dublin"`, sees `"Dublin" != "Galway"`, evaluates `ROADS["Dublin"]`, and raises `KeyError: 'Dublin'`.
  3. **Disconnected town (`"Aran": {}` added to `ROADS`, `time_lost("Galway", "Aran")`):** `bfs_graph` returns `None`, and line 32 `road_time(None)` attempts `None[1:]`, raising **`TypeError: 'NoneType' object is not subscriptable`**! Meanwhile in `quickest_times("Galway")`, `dijkstra` returns `(None, None)` so `quickest_times` safely maps `"Aran": None`!
  4. **Can `time_lost(start, goal)` EVER return a negative number?** **Never** (when edge weights are non-negative): `fewest_roads` is *a* valid path from `start` to `goal`, and `dijkstra` returns the global minimum cost over *all* paths from `start` to `goal`, so `fewest_roads_time >= quickest_roads_time` always holds!

### Pillar 3 — Analyse (Complexity & The Big 8–10 Mark Optimization Question!)

- **Time Complexity:**
  - `time_lost`: `O(V + E)` for `bfs_graph` + `O(V)` for `road_time` + `O((V + E) log E)` for `dijkstra` = **`O((V + E) log E)`** (which equals `O((V + E) log V)` on simple graphs since $E \le V^2 \implies \log E \le 2 \log V$).
  - `quickest_times` **(YOUR CODE — EXPECT THIS QUESTION!):** Your dict comprehension calls `dijkstra(roads_from, start, town)` **once for each of the `V` towns in `ROADS`**, giving **`O(V * (V + E) log V)`**! On `ROADS` (`V = 12`), 12 searches take microseconds, and because `E06` only imported `dijkstra` (which requires a `goal`) and not `PriorityQueue`, composing `dijkstra` was the intended short solution.
  - **How to optimize `quickest_times` by a factor of `V` to `O((V + E) log V)`:**
    Compare `quickest_times` with `E04`'s [`hops_from`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L24-L52)! Just as removing `if state == goal:` from `bfs` let **one** BFS compute shortest hop counts to *every* vertex at once, removing `if node == goal:` from `dijkstra` and letting the `PriorityQueue` run until empty computes shortest driving times from `start` to **all `V` towns in ONE single-source Dijkstra pass** (`O((V + E) log V)`):
    ```python
    frontier = PriorityQueue()
    frontier.push(start, 0)
    best = {start: 0}
    while frontier:
        node, cost = frontier.pop()
        if cost > best[node]:      # skip stale lazy-deleted heap entries!
            continue
        for nxt, weight in roads_from(node):
            if nxt not in best or cost + weight < best[nxt]:
                best[nxt] = cost + weight
                frontier.push(nxt, cost + weight)
    return best
    ```
- **Space Complexity:** `O(V + E)` during `dijkstra` (for `came_from` of size `O(V)` and up to `O(E)` lazy-deletion entries in `PriorityQueue`), and `O(V)` for the returned `dict`.

### Likely Interview Q&A

1. **Q: Look at line 60 of `E06_route.py`. How many times does `dijkstra` run for `quickest_times("Galway")`, and is that wasteful?**
   - **A:** It runs `len(ROADS) = 12` times (`V` times), repeating the inner frontier expansions from `"Galway"` on every call for `O(V * (V + E) log V)` total time. Because Dijkstra is inherently a **single-source, all-destinations** algorithm, running a single `PriorityQueue` search with the early `node == goal` stop removed computes the entire `dict` in one `O((V + E) log V)` pass—just like `hops_from` did for unweighted BFS in `E04`.
2. **Q: Why does Dijkstra fail if an edge has a negative weight (say `-50` minutes)?**
   - **A:** Dijkstra's correctness relies on the greedy invariant that when the minimum-cost node `(node, cost)` is **popped** from the priority queue, no unexplored detour through a higher-cost frontier node can ever come back and make `node` cheaper. That requires every future edge to add $\ge 0$ cost! With a negative edge (especially to `goal` or in a negative cycle), `goal` can be popped early with a suboptimal cost while a currently more expensive path later traverses `-50` and beats it (or loops forever around a negative cycle). You would need Bellman-Ford (`O(V * E)`) instead.
3. **Q: Why did `time_lost("Galway", "Roundstone")` return `35` even though BOTH routes had 4 roads?**
   - **A:** Because BFS treats all 4-road routes as tied, and breaks ties purely by neighbour iteration order (`'Spiddal'` appears before `'Oughterard'` in `ROADS["Galway"]`). If `'Oughterard'` had been listed first in `ROADS["Galway"]`, `time_lost("Galway", "Roundstone")` would have been `0`—whereas `time_lost("Spiddal", "Clifden")` (`3` minutes: 4 coastal roads at 100 min vs. 5 inland roads at 97 min) would *still* be `3` regardless of dictionary key order!

---

## 8. Week 6 Master Comparison Cheat Sheet (BFS vs. DFS vs. Dijkstra)

| Property | Breadth-First Search (`bfs`) | Depth-First Search (`dfs`) | Dijkstra's Algorithm (`dijkstra`) |
| :--- | :--- | :--- | :--- |
| **Frontier Container** | FIFO Queue (`collections.deque`) | LIFO Stack (`list`) | Min-Heap (`PriorityQueue` via `heapq`) |
| **Add / Remove Ops** | `append(x)` / `popleft()` — both `O(1)` | `append(x)` / `pop()` — both `O(1)` | `push(x, p)` / `pop()` — both `O(log H)` |
| **State Revisited?** | Never updated once in `came_from` | Never updated once in `came_from` | Re-pushed if `cost + w < came_from[nxt][1]` |
| **Complete? (Finds path if one exists)** | **Yes** (even on infinite graphs, if branching factor `b` is finite) | **Yes on finite graphs; NO on infinite graphs** (can plunge down infinite branch) | **Yes** (if edge weights $\ge \epsilon > 0$; even on infinite graphs) |
| **Optimal? (Shortest path)** | **Yes for unweighted / uniform-cost** (minimizes *hop count*) | **No** (returns first path stumbled upon) | **Yes for non-negative weights ($w \ge 0$)** (minimizes *total weight*) |
| **Negative Weights?** | Not applicable (unweighted) | Not applicable | **Fails!** (Greedy pop invariant breaks) |
| **Time Complexity** | `O(V + E)` | `O(V + E)` | `O((V + E) log V)` |
| **Space Complexity** | `O(V)` | `O(V)` (`came_from` stores all visited) | `O(V + E)` (with lazy heap deletion) |
