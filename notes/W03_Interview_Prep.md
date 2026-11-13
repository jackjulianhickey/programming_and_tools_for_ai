# Week 03 Interview Prep — Higher-Order Functions, Recursion, Trees & Generators

← Back to [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Source Directory:** [`assignment_01/W03/`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03)  
**Core Week 03 Themes:** Key functions (`sorted` / `max` with `lambda`), in-place mutation vs returning new objects, structural recursion over nested lists and JSON Bill-of-Materials (BOM) trees, eager list comprehensions vs lazy generators (`yield` / `yield from`), passing state *down* a recursion (`prefix`), and non-mutating functional tree updates (`repriced`).

> **Why Week 03 Matters for 8–10 Marks:** Recursion, call-stack depth (`O(d)`), lazy generator evaluation, and non-mutating tree copying (`E06`–`E08`) are prime 8–10 mark interview territory. Expect the interviewer to ask you to trace recursive frames by hand, distinguish a `generator` object from a `list`, and prove why `repriced` does not mutate the caller's input tree.

---

## Table of Contents

1. [Summary Complexity & Difficulty Matrix](#summary-complexity--difficulty-matrix)
2. [Reference Context — `E01_bom.py` (Given Code)](#reference-context--e01_bompy-given-code)
3. [`E02_sort_by_key.py` — `sort_by_mass` & `heaviest`](#e02_sort_by_keypy--sort_by_mass--heaviest)
4. [`E03_nested_sum.py` — `nested_sum`](#e03_nested_sumpy--nested_sum)
5. [`E04_flatten.py` — `flatten`](#e04_flattenpy--flatten)
6. [`E05_count_parts.py` — `count_parts` & `deepest`](#e05_count_partspy--count_parts--deepest)
7. [`E06_apply_fn.py` — `apply_fn_to_list` & `apply_fn_to_list_gen`](#e06_apply_fnpy--apply_fn_to_list--apply_fn_to_list_gen)
8. [`E07_part_paths.py` — `part_paths` & `find_part`](#e07_part_pathspy--part_paths--find_part)
9. [`E08_bom_json.py` — `load_bom`, `repriced` & `save_bom`](#e08_bom_jsonpy--load_bom-repriced--save_bom)
10. [Week 03 Watchlist — Subtle Quirks in Your Submitted Code](#week-03-watchlist--subtle-quirks-in-your-submitted-code)

---

## Summary Complexity & Difficulty Matrix

*(Let `n` = length of input sequence, `N` = total nodes in tree/nested list, `L` = number of leaf nodes, `d` = maximum tree depth, `b` = max branching factor, `S` = string path length.)*

| Exercise File | Functions | Difficulty Tier | Time Complexity | Auxiliary Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| [E01_bom.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py) | [`unit_mass`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L57-L78), [`parts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L81-L97) | Reference (Given) | `O(N)` | `O(d)` call/generator stack |
| [E02_sort_by_key.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py) | [`sort_by_mass`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L14-L30) | Warm-up | `O(n log n)` | `O(n)` (new sorted list) |
| [E02_sort_by_key.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py) | [`heaviest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L33-L43) | Warm-up | `O(n)` | `O(1)` |
| [E03_nested_sum.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E03_nested_sum.py) | [`nested_sum`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E03_nested_sum.py#L11-L33) | Warm-up / Moderate | `O(N)` | `O(d)` call + generator frames |
| [E04_flatten.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py) | [`flatten`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py#L11-L37) | Moderate | `O(N + L * d)` (`O(N^2)` worst skew) | `O(L + d)` (`O(L)` output + `O(d)` stack) |
| [E05_count_parts.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py) | [`count_parts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py#L27-L44), [`deepest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py#L47-L63) | Moderate | `O(N)` | `O(d)` call + generator frames |
| [E06_apply_fn.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py) | [`apply_fn_to_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L24-L47) | Moderate | `O(n)` (assuming `fn` is `O(1)`) | `O(n)` (eager output list) |
| [E06_apply_fn.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py) | [`apply_fn_to_list_gen`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L50-L74) | Hard (8–10 Mark Target) | `O(1)` at call; `O(1)` per `next()` | `O(1)` (lazy generator state) |
| [E07_part_paths.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py) | [`part_paths`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L27-L63) | Hard (8–10 Mark Target) | `O(N * S + L * d)` | `O(L * S + d * S)` |
| [E07_part_paths.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py) | [`find_part`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L66-L94) | Hard (8–10 Mark Target) | `O(d * (b + S))` | `O(d * S)` (recursive string slices) |
| [E08_bom_json.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py) | [`load_bom`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L30-L41), [`save_bom`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L73-L96) | Moderate | `O(N)` (JSON serialization) | `O(N)` (`load_bom`) / `O(d)` (`save_bom`) |
| [E08_bom_json.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py) | [`repriced`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L44-L70) | Hard (8–10 Mark Target) | `O(N)` | `O(N)` new tree (`O(d)` call stack) |

---

## Reference Context — `E01_bom.py` (Given Code)

**File:** [E01_bom.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py) | **Data:** [bicycle.json](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/data/bicycle.json)

Every tree exercise in Week 03 (`E05`, `E07`, `E08`) operates on the **Bill of Materials (BOM)** tree introduced in [E01_bom.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py). Make sure you know its exact data shape cold:

### 1. The Two Node Shapes in a BOM Tree
Every node is a Python `dict`, and every subtree is itself a valid BOM:
- **Bought part (Leaf / Base Case):** Has `"name"`, `"qty"`, `"material"`, `"mass"` (and `"cost"` in [bicycle.json](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/data/bicycle.json)), and **no `"children"` key**.
  - Example: `{"name": "spoke", "qty": 32, "material": "steel", "mass": 5, "cost": 0.40}`
- **Built assembly (Internal Node / Recursive Case):** Has `"name"`, `"qty"`, and `"children"` (a `list` of child node dicts), and **no `"mass"`, `"material"`, or `"cost"` key**.
  - Example: `bicycle` (`qty: 1`, 5 children: `wheel`, `frame`, `handlebar`, `saddle`, `chain`), where `wheel` (`qty: 2`) itself has 4 leaf children (`rim`, `spoke`, `hub`, `tyre`).

### 2. Key Functions in `E01_bom.py`
- [`everything`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L37-L43) & [`is_steel`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L46-L54): Predicate functions (`dict -> bool`) passed into `unit_mass` via its `keep` parameter. Notice `is_steel(node)` accesses `node["material"]` directly — it never crashes on `bicycle` or `wheel` (which have no `"material"` key) **only because** `unit_mass` calls `keep(node)` *inside* the leaf base case!
- [`unit_mass`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L57-L78):
  ```python
  def unit_mass(node, keep=everything):
      if "mass" in node:
          return node["mass"] if keep(node) else 0
      return sum(c["qty"] * unit_mass(c, keep) for c in node["children"])
  ```
  - **Crucial detail (`unit_mass` ignores `node["qty"]` at the top level):** Calling `unit_mass(wheel)` returns `1060` (`380 + 32*5 + 200 + 320`), **not** `2120`, even though `wheel["qty"] == 2`! Why? Because `unit_mass` computes the mass of **one** unit of `node`; the parent (`bicycle`) is responsible for multiplying `c["qty"] * unit_mass(c, keep)`. If `unit_mass` also multiplied by `node["qty"]`, quantities would get squared down the tree!
- [`parts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L81-L97):
  ```python
  def parts(node):
      if "children" not in node:
          yield node
      else:
          for c in node["children"]:
              yield from parts(c)
  ```
  - **Recursive generator:** Yields the `8` leaf `dict`s left-to-right, one at a time, lazily.
  - **Why `yield from parts(c)` instead of `yield parts(c)`?** Because `parts(c)` returns a `generator` object! Writing `yield parts(c)` would yield nested generator objects instead of the leaf dictionaries inside them. `yield from` delegates iteration to the sub-generator and forwards every item it yields directly to the caller.
  - **Why `len(parts(bicycle))` fails:** Generators compute items on demand and do not know how many items they will yield ahead of time (`TypeError: object of type 'generator' has no len()`). You must materialize `list(parts(bicycle))` first or count lazily with `sum(1 for _ in parts(bicycle))`.

---

## `E02_sort_by_key.py` — `sort_by_mass` & `heaviest`

- **File:** [E02_sort_by_key.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E02_sort_by_key.py))
- **Symbols:** [`sort_by_mass`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L14-L30), [`heaviest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L33-L43)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def sort_by_mass(pairs):
    return sorted(pairs, key=lambda p:p[1])


def heaviest(pairs):
    return max(pairs, key=lambda p:p[1])[0]


# ANSWER: sort returns none so by assigning xs to the return value of sort(xs) you are changing the value to none
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:**
  - `sort_by_mass`: *"It uses Python's built-in `sorted()` with a `lambda` key function that extracts index `1` (the mass) from each `(name, mass)` tuple, returning a brand-new list ordered from lightest to heaviest without mutating `pairs`."*
  - `heaviest`: *"It scans `pairs` in a single linear pass using `max()` with the same `lambda p: p[1]` key to find the tuple with the largest mass, then indexes `[0]` to return just the part's string name."*
- **Line-by-Line & Variable Breakdown:**
  - `pairs` (parameter): Expected to be an iterable (typically `list[tuple[str, int | float]]`) of `(name, mass)` pairs.
  - `lambda p: p[1]` (anonymous key function): Called **once per element** (the *decorate-sort-undecorate* / Schwartzian transform pattern in CPython). Here `p` stands for a single `(name, mass)` pair, and `p[1]` selects its numeric mass for comparison instead of Python's default tuple comparison (which would sort alphabetically by `p[0]` first!).
  - `[0]` at the end of [`heaviest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L43): `max(...)` returns the winning *tuple* (e.g. `('frame', 2200)`), not the key value `2200`; indexing `[0]` extracts `'frame'`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `pairs`: `Iterable[tuple[str, int | float]]`
  - `p` (inside `lambda`): `tuple[str, int | float]`
  - `sort_by_mass(pairs)` return type: always `list[tuple[str, int | float]]` (even if `pairs` was a `tuple` or generator!).
  - `heaviest(pairs)` return type: `str` (specifically the type of element `0` of the winning tuple).
- **Concrete Step-by-Step Trace:**
  - Call `heaviest([("frame", 2200), ("spoke", 5), ("tyre", 320)])`:
    1. `max` evaluates key `p[1]` on `("frame", 2200)` → `2200` (current best item: `("frame", 2200)`).
    2. Evaluates key on `("spoke", 5)` → `5 > 2200` is `False`.
    3. Evaluates key on `("tyre", 320)` → `320 > 2200` is `False`.
    4. `max(...)` returns `("frame", 2200)`.
    5. `("frame", 2200)[0]` evaluates to `'frame'`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty list `[]`:**
     - `sort_by_mass([])` → returns `[]` cleanly.
     - `heaviest([])` → raises **`ValueError: max() iterable argument is empty`** because `max()` has no `default` argument and nothing to index `[0]` on!
  2. **Tied masses, e.g. `[("handlebar", 300), ("chain", 300)]`:**
     - `sort_by_mass` → returns `[('handlebar', 300), ('chain', 300)]`. Because Python's Timsort is **stable** and the `key` function only returns `p[1]`, Python **never** compares `"handlebar"` vs `"chain"` — it preserves their original input order!
     - `heaviest` → returns `'handlebar'` (`max()` strictly uses `>` on keys, so the **first** maximum wins).
  3. **All negative numbers, e.g. `[("a", -50), ("b", -10)]`:**
     - Both work properly (`heaviest` returns `'b'`), unlike manual loops buggy enough to initialize `best_mass = 0`.
  4. **Malformed element `[("frame",)]` (1-tuple) or `[("frame", None)]`:**
     - 1-tuple raises `IndexError: tuple index out of range` inside `lambda`.
     - `None` mass with >1 item raises `TypeError: '<' not supported between instances of 'NoneType' and 'int'` (note: on a *1-element* list `[("frame", None)]`, both `sorted` and `max` actually succeed without doing any `<` comparison!).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - `sort_by_mass`: **Time `O(n log n)`** worst/average case (`O(n)` best case on already-sorted input thanks to Timsort run detection); **Space `O(n)`** for the newly returned `list` plus key array.
  - `heaviest`: **Time `O(n)`** (exactly `n` key evaluations and `n - 1` comparisons); **Space `O(1)`** auxiliary memory.
- **Alternative Comparison:**
  - Why not implement `heaviest(pairs)` as `sort_by_mass(pairs)[-1][0]`?
    1. Asymptotically slower: `O(n log n)` time and `O(n)` memory instead of `O(n)` time and `O(1)` memory.
    2. Subtle tie-breaking difference: on `[("handlebar", 300), ("chain", 300)]`, `max(...)[0]` returns `'handlebar'` (the first tied item), whereas `sorted(...)[-1][0]` returns `'chain'` (the last tied item)!
  - Alternative to `lambda p: p[1]`: `from operator import itemgetter; itemgetter(1)` runs in C rather than creating a Python stack frame per call, giving slightly lower constant-factor overhead.
- **Embedded File Question (`# ANSWER` on [Line 46](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L46)):**
  - *Question:* Why does `xs = xs.sort()` throw away your list?
  - *Your written answer:* `# ANSWER: sort returns none so by assigning xs to the return value of sort(xs) you are changing the value to none`
  - **Interview Polish (Watch the syntax slip!):** Your conceptual explanation is spot-on, **but watch out**: in your comment you wrote `sort(xs)` instead of `xs.sort()`. There is **no** built-in `sort(xs)` function in Python (`NameError`). Say explicitly: *"`list.sort()` is a method (`xs.sort()`) that mutates the list in-place and returns `None` — following Python's convention for in-place mutators like `.append()`, `.extend()`, and `.reverse()` so callers don't mistake mutation for copying. Rebinding `xs = xs.sort()` overwrites the variable `xs` with `None`, losing the reference to the newly sorted list."*

### Likely Interview Q&A
1. **Q: If two parts have the same mass `300`, does `sort_by_mass` sort them alphabetically by name as a tie-breaker?**  
   **A:** No! Because `key=lambda p: p[1]` hands Timsort *only* the integer `300`, Timsort never compares the tuple strings `p[0]`. Because Timsort is a **stable** sort, tied elements stay in their exact original order. If I wanted alphabetical tie-breaking, I would use `key=lambda p: (p[1], p[0])`.
2. **Q: How many times is `lambda p: p[1]` called when sorting `n` items — `O(n)` times or `O(n log n)` times?**  
   **A:** Exactly `n` times (`O(n)`), not `O(n log n)`! Python computes and caches the `key` value once per element before running the `O(n log n)` comparisons.
3. **Q: What happens if someone passes a generator `(x for x in pairs)` into `sort_by_mass` and `heaviest`?**  
   **A:** Both work! Both `sorted()` and `max()` accept any iterable (consuming the generator once). Just note that if the same generator object were passed to `sort_by_mass` and then to `heaviest`, the second call would see an exhausted (empty) generator and raise `ValueError`.

---

## `E03_nested_sum.py` — `nested_sum`

- **File:** [E03_nested_sum.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E03_nested_sum.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E03_nested_sum.py))
- **Symbol:** [`nested_sum`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E03_nested_sum.py#L11-L33)
- **Difficulty Tier:** `Warm-up / Moderate`

### Your Submitted Code
```python
def nested_sum(items):
    if not isinstance(items, list):
        return items

    return sum(nested_sum(x) for x in items)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"This function treats arbitrarily nested lists as a tree where numbers are leaves and lists are internal nodes. If `items` is not a `list` (base case), it returns the number itself; otherwise (recursive case), it lazily sums the recursive `nested_sum(x)` of every element `x` inside `items`."*
- **Line-by-Line & Variable Breakdown:**
  - `if not isinstance(items, list): return items` (Lines 30–31): **Base case** checked on entry. When `nested_sum` recurses down onto a bare number (e.g. `4`), `isinstance(4, list)` is `False`, so `4` is returned directly.
  - `return sum(nested_sum(x) for x in items)` (Line 33): **Recursive case**. Iterates over each child `x` of the list `items` using a generator expression, recursively totals `x`, and feeds those sub-totals into `sum()` (whose default `start` value is `0`, automatically handling empty lists `[]`!).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `items`: `list | int | float` (recursive union type: `NestedList = int | float | list[NestedList]`)
  - `(nested_sum(x) for x in items)`: `generator` yielding `int | float`
  - Return type: `int | float` (specifically `int` `0` for empty lists, or numeric sum).
- **Concrete Step-by-Step Trace on `nested_sum([1, [2, 3]])`:**
  1. `nested_sum([1, [2, 3]])`: `isinstance(..., list)` is `True` → enters `sum(...)`.
     - `x = 1` → calls `nested_sum(1)` → not a list → returns `1`. Running `sum`: `0 + 1 = 1`.
     - `x = [2, 3]` → calls `nested_sum([2, 3])` → is a list → enters inner `sum(...)`:
       - `x = 2` → `nested_sum(2)` returns `2`.
       - `x = 3` → `nested_sum(3)` returns `3`.
       - Inner `sum` returns `5`.
     - Outer `sum`: `1 + 5 = 6` → returns `6`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty or deeply nested empty lists `[]` or `[[], [[]]]`:**
     - `nested_sum([])`: generator yields nothing, `sum(())` returns `0`.
     - `nested_sum([[], [[]]])`: `nested_sum([]) -> 0`, `nested_sum([[]]) -> sum([0]) -> 0`, outer `sum([0, 0]) -> 0`.
  2. **A bare number at the top level, e.g. `nested_sum(42)`:**
     - Your code returns `42` cleanly! *(Contrast: the official solution loops `for item in items:` immediately without checking `items`, so `nested_sum(42)` in the official solution raises `TypeError: 'int' object is not iterable`!)*
  3. **A tuple or string inside the list, e.g. `nested_sum([1, (2, 3)])` or `nested_sum(["a", "b"])`:**
     - `isinstance((2, 3), list)` is `False`, so `nested_sum((2, 3))` returns `(2, 3)`, and `sum` tries `1 + (2, 3)` → **`TypeError: unsupported operand type(s) for +: 'int' and 'tuple'`**.
     - For `["a", "b"]`, `sum` starts at integer `0` and tries `0 + "a"` → **`TypeError: unsupported operand type(s) for +: 'int' and 'str'`**.
  4. **1,000+ levels of nesting (`[[[...]]]`)**:
     - Hits CPython's call-stack guard (`sys.getrecursionlimit()`, default `1000`) and raises **`RecursionError`**.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - **Time:** **`O(N)`** where `N` is the total number of list containers + leaf numbers across all levels. Every node is visited once.
  - **Space:** **`O(d)`** where `d` is the maximum nesting depth. Crucially, because you wrote `sum(nested_sum(x) for x in items)` with a **generator expression** rather than `sum([nested_sum(x) for x in items])` with a list comprehension, no intermediate lists are built at each level — at most `d` function frames and `d` suspended generator frames exist simultaneously on the stack!
- **Comparison with [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E03_nested_sum.py#L30-L36):**
  - The official solution checks `if isinstance(item, list):` *before* recursing inside an explicit `for item in items:` loop, avoiding recursive calls on leaf numbers (`1` call vs `4` calls on `[1, 2, 3]`).
  - Your version is shorter (3 lines vs 7 lines), mirrors `unit_mass`'s node-first recursion pattern, and handles scalar top-level inputs gracefully, at the tiny constant cost of one extra function call per leaf number.

### Likely Interview Q&A
1. **Q: Why does `nested_sum([[], [[]]])` return `0` when you never wrote `0` anywhere in your code?**  
   **A:** Built-in `sum(iterable, start=0)` defaults its starting accumulator to `0`. An empty list `[]` produces zero elements from `(nested_sum(x) for x in items)`, so `sum` returns `0`, and parent lists sum those zeros to `0`.
2. **Q: What is the difference in memory complexity between `sum(nested_sum(x) for x in items)` and `sum([nested_sum(x) for x in items])`?**  
   **A:** With the generator expression, memory is strictly `O(d)` (nesting depth), even if a list has a million numbers `[1, 2, ..., 1_000_000]` (`d = 1`). With brackets `[...]`, Python builds an eager million-element list in RAM before summing, increasing auxiliary space from `O(d)` to `O(N)`.

---

## `E04_flatten.py` — `flatten`

- **File:** [E04_flatten.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E04_flatten.py))
- **Symbol:** [`flatten`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py#L11-L37)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def flatten(items):
    result = []
    if not isinstance(items, list):
        return[items]

    for x in items:
        result.extend(flatten(x))

    return result
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"This recursively flattens arbitrarily nested lists into a single 1D list preserving left-to-right order. If `items` is a single non-list value, it wraps it in a one-element list `[items]`; otherwise, it loops through `items` and uses `.extend()` to append all flattened elements from each child into `result`."*
- **Line-by-Line & Variable Breakdown:**
  - `result = []` (Line 30): Accumulator list collecting flattened items at the current nesting level. *(Self-critique ready for interview: placing `result = []` after line 32 would be cleaner because on the base case `return [items]`, `result` is created and immediately discarded!)*
  - `if not isinstance(items, list): return [items]` (Lines 31–32): Base case. Must return a **list** `[items]` (not bare `items`!) because the caller passes the return value into `result.extend(...)`, which requires an iterable!
  - `result.extend(flatten(x))` (Line 35): Unpacks every element returned by `flatten(x)` onto the end of `result`. Using `.append(flatten(x))` here would re-nest sublists instead of flattening them!

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `items`: `list | Any` (non-list leaf values)
  - `result`: `list`
  - Return type: always `list`
- **Concrete Step-by-Step Trace on `flatten([1, [2, 3]])`:**
  1. `flatten([1, [2, 3]])`: `result = []`. Is a list → enters loop:
     - `x = 1`: calls `flatten(1)` → not a list → returns `[1]`. `result.extend([1])` → `result` is `[1]`.
     - `x = [2, 3]`: calls `flatten([2, 3])` → inner `result = []`:
       - `x = 2` → `flatten(2)` returns `[2]` → inner `result` becomes `[2]`.
       - `x = 3` → `flatten(3)` returns `[3]` → inner `result` becomes `[2, 3]`.
       - Returns `[2, 3]`.
     - Outer `result.extend([2, 3])` → outer `result` becomes `[1, 2, 3]`.
  2. Returns `[1, 2, 3]`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Deeply nested empties `[[], [[]]]`:**
     - `flatten([])` skips the `for` loop and returns `[]`. `result.extend([])` adds nothing → returns `[]`!
  2. **Strings inside the list, e.g. `flatten(["abc", ["de"]])`:**
     - Because `isinstance("abc", list)` is `False`, strings are treated as **atomic leaves** (not split into characters!) and it returns `['abc', 'de']`. *(Notice why checking `isinstance(items, list)` is much safer here than trying to iterate arbitrary iterables, because in Python strings are iterable of 1-char strings, which would cause infinite recursion on `"a"`!)*
  3. **Input mutation check:** Does `flatten` mutate `items` or any inner list? **No** — it constructs fresh `result` lists and never mutates `items`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity (8–10 Mark Nuance!):**
  - Let `N` be total list nodes + leaf elements, `L` be the number of leaves, and `d` be maximum depth.
  - **On shallow / bounded-depth lists (`d = O(1)`):** Time is **`O(N)`**. Specifically, on a flat list `[1, 2, ..., n]`, each `.extend([x])` is `O(1)` amortized, giving **`O(n)`** total time (whereas writing `result = result + flatten(x)` would copy `result` every iteration and degrade even a flat list to **`O(n^2)`**!).
  - **On deeply nested lists:** Because each recursive level builds its own `result` list and the parent copies all elements up via `result.extend(...)`, a leaf at depth `k` gets copied `k` times on the way back up! Total time is **`O(N + L * d)`**, which in a degenerate chain of depth `d = N` (e.g. `[[[[1], 2], 3], 4]`) reaches **`O(N^2)`**.
  - **Space:** **`O(L + d)`** peak memory (`O(d)` stack frames + active intermediate sublists summing to `O(L)`).
- **How to Achieve Strict `O(N)` Even on Deeply Skewed Inputs (Alternatives):**
  1. **Shared accumulator list passed down:** Define helper `_walk(sub, out)` that calls `out.append(sub)` at leaves, mutating a **single** list `out` across the entire traversal — every leaf is appended once (`O(N)` time, `O(L + d)` space).
  2. **Recursive generator (`yield` / `yield from`):**
     ```python
     def flatten_gen(items):
         if not isinstance(items, list):
             yield items
         else:
             for x in items:
                 yield from flatten_gen(x)
     ```
     Calling `list(flatten_gen(items))` runs in `O(N)` time (or `O(N * d)` in CPython `yield from` chaining without bytecode flattening, though only `O(d)` memory during lazy iteration!).
  3. **Comparison with [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E04_flatten.py#L29-L35):** The official solution checks `if isinstance(item, list): out.extend(flatten(item)) else: out.append(item)` — avoiding creating `L` temporary single-element `[items]` lists and avoiding allocating `result = []` before the base case check.

### Likely Interview Q&A
1. **Q: On line 30, you wrote `result = []` before `if not isinstance(items, list): return [items]`. Does that hurt anything?**  
   **A:** Correctness-wise no, and asymptotically no (`O(1)` per leaf), but every leaf call allocates an empty `list` `result` that is immediately thrown away on line 32, plus a second 1-element list `[items]`. Moving `result = []` below the `if` statement (or checking `isinstance(x, list)` in the loop and calling `result.append(x)` like the official solution) eliminates those extra allocations.
2. **Q: Why did you use `result.extend(flatten(x))` instead of `result.append(flatten(x))` or `result = result + flatten(x)`?**  
   **A:** `.append()` inserts the returned list as a single nested element rather than unpacking its items. `+` creates a brand-new list copy of `result` on every iteration, turning a flat `n`-element list from `O(n)` into `O(n^2)` time! `.extend()` mutates `result` in-place in amortized `O(len(chunk))` time.

---

## `E05_count_parts.py` — `count_parts` & `deepest`

- **File:** [E05_count_parts.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E05_count_parts.py))
- **Symbols:** [`count_parts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py#L27-L44), [`deepest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py#L47-L63)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def count_parts(node):
    if "children" not in node:
        return 1
    return  sum(x["qty"] * count_parts(x) for x in node["children"])


def deepest(node):
    if "children" not in node:
        return 0

    return 1 + max(deepest(x) for x in node["children"])
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:**
  - `count_parts`: *"It counts the total physical bought parts inside one unit of `node` by returning `1` at any leaf part and summing `child['qty'] * count_parts(child)` across all children of an assembly."*
  - `deepest`: *"It computes the height (maximum edge depth) of the BOM tree rooted at `node`: a leaf part has depth `0`, and an assembly node has depth `1` plus the maximum depth among its children."*
- **Line-by-Line & Variable Breakdown:**
  - `if "children" not in node:` (Lines 42, 60): Distinguishes a bought leaf part from a built assembly node.
  - `x["qty"] * count_parts(x)` (Line 44): Multiplies how many physical parts live inside *one* child `x` by how many copies of `x` go into `node` (e.g., `2` wheels × `35` parts per wheel = `70` wheel parts). Notice `count_parts` has the **exact same recursive shape** as [`unit_mass`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py#L57-L78), with `1` replacing `node["mass"]`!
  - `1 + max(deepest(x) for x in node["children"])` (Line 63): Post-order aggregation where `+ 1` counts the edge from `node` down to its deepest child, and `qty` is irrelevant because having 2 wheels doesn't make the hierarchy deeper!

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `node` / `x`: `dict[str, Any]`
  - `count_parts(node)` return type: `int`
  - `deepest(node)` return type: `int` (`>= 0`)
- **Concrete Step-by-Step Trace on `bicycle`:**
  - `count_parts(bicycle)`:
    - `wheel`: `1*1 (rim) + 32*1 (spoke) + 1*1 (hub) + 1*1 (tyre) = 35`. Multiplied by `wheel["qty"] == 2` → `70`.
    - `frame` (`1*1`), `handlebar` (`1*1`), `saddle` (`1*1`), `chain` (`1*1`) → `4`.
    - Total: `70 + 4 = 74`.
  - `deepest(bicycle)`:
    - `rim`, `spoke`, `hub`, `tyre` each return `0`.
    - `wheel` returns `1 + max(0, 0, 0, 0) = 1`.
    - `frame`, `handlebar`, `saddle`, `chain` each return `0`.
    - `bicycle` returns `1 + max(1, 0, 0, 0, 0) = 2`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **An assembly node with an empty children list `{"name": "box", "qty": 1, "children": []}` (KEY EDGE CASE!):**
     - `count_parts` → `"children" not in node` is `False` → `sum` over empty generator returns **`0`**!
     - `deepest` → `"children" not in node` is `False` → calls `max()` on an empty generator → **raises `ValueError: max() iterable argument is empty`**! *(Fix if empty children lists were valid: `if not node.get("children"): return 0`.)*
  2. **A child with `"qty": 0`:**
     - `count_parts` contributes `0 * count_parts(x) = 0` physical parts, while `deepest` *still* counts that child's structural depth in `max(...)`!
  3. **A single leaf part `spoke` (`qty: 32`):**
     - `count_parts(spoke)` returns **`1`**, NOT `32`, because `count_parts` asks *"how many parts inside **one** of `node`"*, just like `unit_mass`!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - Both `count_parts` and `deepest` visit every node in the tree once: **Time `O(N)`** where `N` is the number of nodes in the BOM tree (`10` dict nodes for `bicycle`, NOT `74` — notice we multiply by `32` in `O(1)` arithmetic rather than visiting `spoke` 32 times!).
  - **Space `O(d)`** where `d` is tree height (`d = 2` for `bicycle`), since both `sum(...)` and `max(...)` consume generator expressions lazily (`O(1)` space per active stack frame).
- **Comparison with [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E05_count_parts.py#L42-L62):** Identical logic and complexity (only loop variable `x` vs `c`). Also note: in [`E08_bom_json.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L23-L27), you could even express `count_parts(node)` using higher-order functions if leaves had a key, or generalize `unit_mass(node, value_fn)` where `count_parts` passes `lambda _: 1`!

### Likely Interview Q&A
1. **Q: Why did `len(list(parts(bicycle)))` in `E01` give `8`, whereas `count_parts(bicycle)` gives `74`?**  
   **A:** `parts(bicycle)` yields each unique leaf dictionary in the JSON tree once, ignoring `"qty"` (so `"wheel"` is walked once and `"spoke"` is yielded once = 8 BOM lines). `count_parts(bicycle)` multiplies by `"qty"` at every assembly edge (`2` wheels × `32` spokes = `64` physical spokes alone), giving `74` physical items.
2. **Q: Does `count_parts(bicycle)` take `O(74)` time or `O(10)` time? What if `"spoke"` had `"qty": 10_000_000`?**  
   **A:** `O(10)` — i.e., `O(N)` in the number of **tree nodes**, completely independent of `"qty"` values! Even if `"qty"` were `10,000,000`, `x["qty"] * count_parts(x)` is a single integer multiplication (`O(1)`), not `10,000,000` loop iterations.

---

## `E06_apply_fn.py` — `apply_fn_to_list` & `apply_fn_to_list_gen`

- **File:** [E06_apply_fn.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E06_apply_fn.py))
- **Symbols:** [`naturals`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L16-L21), [`apply_fn_to_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L24-L47), [`apply_fn_to_list_gen`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L50-L74)
- **Difficulty Tier:** `Hard (8–10 Mark Target)` (Eager vs Lazy Evaluation & Generators)

### Your Submitted Code
```python
def apply_fn_to_list(fn, L):
    # new_list = []
    # for x in L:
    #     new_list.append(fn(x))

    # return new_list
    return list(fn(x) for x in L)


def apply_fn_to_list_gen(fn, g):
    yield from (fn(x) for x in g) 


# ANSWER: the first one would get stuck in a loop as it tries to process all elements immediately. The second one processes elements one by when and only when requested.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:**
  - `apply_fn_to_list`: *"This is an eager higher-order `map`: it takes a one-argument function `fn` and an iterable `L`, immediately applies `fn(x)` to every element in `L`, and materializes all results into a new `list` in memory before returning."*
  - `apply_fn_to_list_gen`: *"This is a lazy generator version of `map`: calling it does zero work upfront and immediately returns a `generator` object that delegates via `yield from` to compute `fn(x)` one item at a time only when `next()` is requested."*
- **Line-by-Line & Variable Breakdown (Know Your Exact Syntax Choices!):**
  - `fn` (parameter): First-class callable (`Callable[[T], U]`), such as built-in `len`, unbound method `str.upper`, or a `lambda`.
  - `return list(fn(x) for x in L)` (Line 47): **Important distinction!** `(fn(x) for x in L)` is a **generator expression** passed into the `list()` constructor, which eagerly consumes it into a `list`. *(The docstring asked for a list comprehension `[fn(x) for x in L]` — be ready to distinguish the two if asked!)*
  - `yield from (fn(x) for x in g)` (Line 74): Because `yield from` is a `yield` keyword inside `def`, Python compiles `apply_fn_to_list_gen` as a **generator function**. When called, its body does not execute at all until the first `next()`. Then it creates the inner generator `(fn(x) for x in g)` and transparently yields each computed `fn(x)` on demand.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `fn`: `Callable[[Any], Any]`
  - `L` / `g`: `Iterable[Any]` (can be a `list`, `tuple`, `range`, `iterator`, or infinite `generator` like `naturals()`)
  - `apply_fn_to_list(fn, L)` return type: `list`
  - `apply_fn_to_list_gen(fn, g)` return type: `generator` (`types.GeneratorType`)
- **Concrete Step-by-Step Trace on `squares = apply_fn_to_list_gen(lambda x: x * x, naturals())`:**
  1. `nat = naturals()`: executes **0 lines** of `naturals`; returns generator `nat` paused at top of `naturals`.
  2. `squares = apply_fn_to_list_gen(lambda..., nat)`: executes **0 lines** of `apply_fn_to_list_gen`; returns generator `squares` paused before line 74. (`fn` has been called **0 times**!)
  3. First `next(squares)`:
     - `squares` enters line 74, creates inner generator `(fn(x) for x in nat)`, and `yield from` calls `next()` on it.
     - Inner generator calls `next(nat)` → `naturals()` sets `n = 0` and hits `yield n`, pausing at line 20 and yielding `0`.
     - Inner generator computes `0 * 0 = 0` and yields `0` out through `yield from` → caller receives `0`!
  4. Second `next(squares)`:
     - Resumes `naturals()` after line 20 → `n += 1` (`n = 1`), loops `while True`, hits `yield 1` → inner computes `1 * 1 = 1` → caller receives `1`!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Iterating `squares` twice (`list(g)` then `list(g)` on a finite `g`):**
     - Generators are **single-pass iterators**! If `res = apply_fn_to_list_gen(len, ["a", "bb"])`, the first `list(res)` returns `[1, 2]`, and a second `list(res)` returns **`[]`** because `res` is exhausted! By contrast, the `list` returned by `apply_fn_to_list` can be iterated arbitrarily many times.
  2. **`fn` raises an exception on the 3rd element (e.g. `1 / x` on `[2, 1, 0, 4]`):**
     - `apply_fn_to_list(lambda x: 1/x, [2, 1, 0, 4])` crashes **immediately** when called (`ZeroDivisionError`), returning nothing.
     - `gen = apply_fn_to_list_gen(lambda x: 1/x, [2, 1, 0, 4])` succeeds at call time, yields `0.5` on 1st `next(gen)`, yields `1.0` on 2nd `next(gen)`, and only raises `ZeroDivisionError` on the **3rd** `next(gen)`! If the caller only needed the first 2 items, it **never crashes**!
  3. **`apply_fn_to_list(lambda x: x*x, naturals())`:**
     - Never returns: `list(...)` pulls items from `naturals()` in an infinite loop, growing the internal list array until Python runs out of RAM (`MemoryError`) or you interrupt it (`KeyboardInterrupt`).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity (assuming `fn` takes `O(1)` time and space):**
  - `apply_fn_to_list`: **Time `O(n)`**, **Space `O(n)`** (must store all `n` results simultaneously).
  - `apply_fn_to_list_gen`:
    - Calling `apply_fn_to_list_gen(fn, g)`: **Time `O(1)`**, **Space `O(1)`**.
    - Advancing one step `next(...)`: **Time `O(1)`**, **Space `O(1)`**.
    - Consuming `k` items from an infinite stream: **Time `O(k)`**, **Space `O(1)`** (if processed one by one without storing in a list!).
- **Comparison with [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_03/W03_Solutions/E06_apply_fn.py#L42-L71) & Built-in `map`:**
  1. In `apply_fn_to_list`, the official solution wrote `[fn(x) for x in L]` (a true **list comprehension**), whereas you wrote `list(fn(x) for x in L)` (`list()` around a **generator expression**). Both are `O(n)` time and `O(n)` space, though `[fn(x) for x in L]` has a smaller constant factor in CPython because it avoids allocating a generator object, avoids repeated generator frame suspension/resumption, and can pre-allocate list capacity when `L` defines `__len__`.
  2. In `apply_fn_to_list_gen`, the official solution wrote:
     ```python
     for x in g:
         yield fn(x)
     ```
     Your `yield from (fn(x) for x in g)` is functionally identical and equally lazy (`O(1)` memory), just creating two generator frames (the outer generator function delegating to the inner generator expression) instead of one! Note also that `return (fn(x) for x in g)` (without `yield from`) would *also* return a single generator object!
  3. Built-in `map(fn, g)` in Python 3 is implemented in C as a lazy iterator just like `apply_fn_to_list_gen`.
- **Embedded File Question (`# ANSWER` on [Line 89](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L89)):**
  - *Your written answer:* `# ANSWER: the first one would get stuck in a loop as it tries to process all elements immediately. The second one processes elements one by when and only when requested.` *(minor typo: "one by when" → "one by one")*.
  - **Interview Polish:** Mention **both** non-termination **and** memory exhaustion (`MemoryError`): `apply_fn_to_list` uses **eager evaluation** — it must exhaust `L` and store every element in RAM before returning, so on an infinite generator like `naturals()` it loops until memory runs out. `apply_fn_to_list_gen` uses **lazy evaluation** — returning a generator immediately in `O(1)` space and computing elements on-demand one `next()` at a time.

### Likely Interview Q&A
1. **Q: Look at line 47 (`return list(fn(x) for x in L)`). Is `(fn(x) for x in L)` a list comprehension?**  
   **A:** Technically no — `(fn(x) for x in L)` is a **generator expression**, which I passed to `list()` to materialize eagerly! A true list comprehension is `[fn(x) for x in L]`. Both are `O(n)` time and `O(n)` space, though `[fn(x) for x in L]` is slightly faster because it skips creating and stepping an intermediate generator object.
2. **Q: On line 74, what would change if you wrote `yield (fn(x) for x in g)` instead of `yield from (fn(x) for x in g)`?**  
   **A:** Huge bug! `yield (...)` would make `squares` a 1-element generator whose single yielded item is *another generator object*, rather than yielding `0, 1, 4, 9, ...`! `yield from` unpacks/delegates to the sub-generator so its values come straight out to the caller.
3. **Q: Why does `str.upper` work when passed as `fn` in `apply_fn_to_list(str.upper, ["ab", "cd"])`?**  
   **A:** In Python, functions and methods are first-class objects. `str.upper` accessed on the `str` class is a function taking one `str` argument (`self`), so calling `str.upper("ab")` is equivalent to `"ab".upper()` and returns `'AB'`.

---

## `E07_part_paths.py` — `part_paths` & `find_part`

- **File:** [E07_part_paths.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py) *(Extension Exercise — no official solution file released)*
- **Symbols:** [`part_paths`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L27-L63), [`find_part`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L66-L94)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def part_paths(node, prefix=""):
    part = (f"{prefix}/{node['name']}") if prefix else node["name"]
    if "children" not in node:
        return [part]

    paths = []
    for child in node["children"]:
        paths.extend(part_paths(child, part))
    return paths


def find_part(node, path):
    parts = path.split('/')
    if parts[0] != node["name"]:
        raise KeyError(f"{path}")

    if len(parts) == 1:
        return node

    for child in node.get("children", []):
        if child["name"] == parts[1]:
            remaining_path = "/".join(parts[1:])
            try:
                return find_part(child, remaining_path)
            except KeyError:
                raise KeyError(path)
    raise KeyError(path)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:**
  - `part_paths`: *"Unlike `unit_mass` which only aggregates answers upward, `part_paths` passes the accumulated ancestor string `prefix` **down** the tree as an optional parameter, returning `[part]` at each leaf and extending all child path lists back up."*
  - `find_part`: *"It navigates down a BOM tree along a `'/'`-separated path by verifying `parts[0]` matches the current node's name, returning `node` when one segment remains, or recursing on the matching child with the remaining path while re-wrapping any nested `KeyError` with the full path."*
- **Line-by-Line & Variable Breakdown:**
  - **`part_paths`:**
    - `prefix=""` (Line 27): Default parameter representing the ancestor path accumulated so far; external callers omit it so it starts empty `""`.
    - `part = (f"{prefix}/{node['name']}") if prefix else node["name"]` (Line 56): Computes this node's path relative to where the search started. The `if prefix else` guard prevents a leading slash like `"/bicycle"` on the root call where `prefix == ""`!
    - `if "children" not in node: return [part]` (Lines 57–58): Base case — only **bought leaf parts** are included in the output list (notice assembly paths like `"bicycle/wheel"` are *not* returned on their own, only passed down as `part` into children!).
    - `paths.extend(part_paths(child, part))` (Line 62): Passes `part` down as the child's `prefix` and flattens the child's returned list of leaf paths into `paths`.
  - **`find_part`:**
    - `parts = path.split('/')` (Line 80): Splits e.g. `"bicycle/wheel/hub"` into `['bicycle', 'wheel', 'hub']`.
    - `if parts[0] != node["name"]: raise KeyError(f"{path}")` (Lines 81–82): Guards the root of the current subtree — if the first segment doesn't match `node["name"]`, this path doesn't live here.
    - `if len(parts) == 1: return node` (Lines 84–85): Base case! Notice this returns **any** matching node — either a leaf (`"bicycle/wheel/hub"`) **or** an internal assembly (`"bicycle"` or `"bicycle/wheel"`), as tested by `find_part(bicycle, "bicycle")`!
    - `for child in node.get("children", []):` (Line 87): Safely handles searching below a leaf node (where `"children"` is absent, `.get("children", [])` returns `[]` instead of crashing with `KeyError: 'children'`, so execution falls through to line 94 `raise KeyError(path)`!).
    - **Why lines 90–93 (`try: return find_part(child, remaining_path) except KeyError: raise KeyError(path)`) exist:** This is a **super important detail**! When recursing on `wheel` with `remaining_path = "wheel/axle"`, if `"axle"` is missing, the recursive call raises `KeyError('wheel/axle')` — which lost the `"bicycle/"` prefix! Catching `KeyError` and raising `KeyError(path)` restores the caller's full path (`KeyError: 'bicycle/wheel/axle'`).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `part_paths`: `node: dict`, `prefix: str` → `part: str`, `paths: list[str]` → returns `list[str]`.
  - `find_part`: `node: dict`, `path: str` → `parts: list[str]`, `remaining_path: str` → returns `dict` (the matching BOM node) or raises `KeyError`.
- **Concrete Step-by-Step Trace:**
  1. **`part_paths(wheel)`** (where `wheel = bicycle["children"][0]`):
     - Call `part_paths(wheel, prefix="")`: `prefix` is falsy → `part = "wheel"`. Has `"children"` → loops over `rim`, `spoke`, `hub`, `tyre`:
       - `part_paths(rim, "wheel")`: `prefix` is truthy → `part = "wheel/rim"`. Leaf → returns `['wheel/rim']`.
       - Same for `spoke`, `hub`, `tyre` → `paths` becomes `['wheel/rim', 'wheel/spoke', 'wheel/hub', 'wheel/tyre']`.
  2. **`find_part(bicycle, "bicycle/wheel/axle")`:**
     - Frame 1 (`node=bicycle`, `path="bicycle/wheel/axle"`): `parts=['bicycle','wheel','axle']`. `parts[0]=='bicycle'` OK. Matches child `wheel` (`parts[1]`), sets `remaining_path="wheel/axle"`, calls `find_part(wheel, "wheel/axle")`.
     - Frame 2 (`node=wheel`, `path="wheel/axle"`): `parts=['wheel','axle']`. `parts[0]=='wheel'` OK. Scans `rim`, `spoke`, `hub`, `tyre` — none equals `'axle'`. Loops ends → line 94 raises `KeyError('wheel/axle')`.
     - Back in Frame 1: `except KeyError:` catches `KeyError('wheel/axle')` and line 93 raises `KeyError('bicycle/wheel/axle')`!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty path `find_part(bicycle, "")`:**
     - `"".split('/')` returns `['']` (a 1-element list containing empty string, NOT `[]`!). `parts[0]` is `'' != 'bicycle'` → raises `KeyError('')`.
  2. **Leading or trailing slash `find_part(bicycle, "/bicycle")` or `find_part(bicycle, "bicycle/")`:**
     - `"/bicycle".split('/')` → `['', 'bicycle']` → `parts[0]` is `'' != 'bicycle'` → raises `KeyError('/bicycle')`.
     - `"bicycle/".split('/')` → `['bicycle', '']` → `len(parts) == 2`, searches children for `child["name"] == ""`, fails → raises `KeyError('bicycle/')`.
  3. **Path continues past a leaf, e.g. `find_part(bicycle, "bicycle/frame/bolt")`:**
     - Frame 1 matches `frame` and calls `find_part(frame, "frame/bolt")`. Inside Frame 2, `frame.get("children", [])` safely returns `[]` (no crash on missing `"children"` key!), loop does 0 iterations, raises `KeyError('frame/bolt')`, re-wrapped by Frame 1 as `KeyError('bicycle/frame/bolt')`!
  4. **Duplicate sibling names (Subtle Quirk!):**
     - Suppose an assembly had *two* children both named `"wheel"`, and only the *second* `"wheel"` contained `"disc"`. In `find_part`, when the first `"wheel"` fails and raises `KeyError`, lines 92–93 immediately `raise KeyError(path)` instead of continuing the `for` loop to check the second `"wheel"`! (Fine for BOM trees where sibling part names under one assembly are distinct, and worth mentioning if asked!)

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - `part_paths`: Visits all `N` nodes, creating a path string of length `O(S)` at each node and extending `L` leaf path references up `d` levels → **Time `O(N * S + L * d)`**, **Space `O(L * S + d * S)`**.
  - `find_part`: At each of the `d` steps along the path, `path.split('/')` and `"/".join(parts[1:])` copy the remaining string of length `O(S)` (`d` times → `O(d * S)` string work), and the loop scans up to `b` sibling children (`O(d * b)`). Total **Time `O(d * (b + S))`**, **Space `O(d * S)`** on the call stack. (Note: it only descends down **one** matching branch — it does **not** visit the whole `O(N)` tree when names are unique!)
- **Alternative Comparison (Iterative `find_part` & Generator `part_paths`):**
  - If you wrote `find_part` **iteratively** by splitting `parts = path.split('/')` **once** upfront and walking `curr = child` in a `for step in parts[1:]:` loop:
    1. You eliminate repeated `split`/`join` at every depth, improving time to **`O(S + d * b)`** and auxiliary space to **`O(S)`** (`O(1)` stack frames)!
    2. Because the original `path` parameter stays in the same function scope, `raise KeyError(path)` works directly at any depth without needing `try / except` exception re-wrapping!
  - Similarly, `part_paths` could be written as a recursive generator (`yield part` / `yield from part_paths(child, part)`), dropping auxiliary list-copying overhead to `O(d * S)`.

### Likely Interview Q&A
1. **Q: Why did you need `try ... except KeyError: raise KeyError(path)` on lines 90–93 of `find_part`?**  
   **A:** Because each recursive call passes `remaining_path = "/".join(parts[1:])`, which strips off the current node's name! If a lookup fails deeper in the tree, the inner call only knows `remaining_path` (like `'wheel/axle'`), so it raises `KeyError('wheel/axle')`. Catching and re-raising `KeyError(path)` restores the caller's full path (`'bicycle/wheel/axle'`).
2. **Q: Why did you write `node.get("children", [])` on line 87 instead of `node["children"]`?**  
   **A:** If the caller passes a path that tries to go *inside* a leaf part — like `"bicycle/frame/screw"` — `frame` is a bought part with no `"children"` key. `node["children"]` would raise `KeyError('children')` instead of `KeyError('bicycle/frame/screw')`! Using `.get("children", [])` safely treats leaves as having zero children so line 94 raises `KeyError(path)`.
3. **Q: Why does `part_paths` have `if prefix else node["name"]` on line 56?**  
   **A:** On the initial top-level call, `prefix` defaults to `""`. Without the `if prefix` check, `f"{prefix}/{node['name']}"` would put a leading slash at the front (`"/bicycle/wheel/rim"` instead of `"bicycle/wheel/rim"`).

---

## `E08_bom_json.py` — `load_bom`, `repriced` & `save_bom`

- **File:** [E08_bom_json.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py) *(Extension Exercise — no official solution file released)*
- **Symbols:** [`unit_total`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L23-L27) *(given)*, [`load_bom`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L30-L41), [`repriced`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L44-L70), [`save_bom`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L73-L96)
- **Difficulty Tier:** `Hard (8–10 Mark Target)` (Shallow vs Deep Copy, Immutability & JSON I/O)

### Your Submitted Code
```python
def load_bom(filename):
    with open (DATA / filename) as f:
        bom = json.load(f)
    return bom


def repriced(node, material, factor):
    new_node = dict(node) 
    if "children" in node:
        new_node["children"] = [repriced(child, material, factor) for child in node["children"]]
    if node.get("material") == material:
        new_node["cost"] = node["cost"] * factor
    return new_node


def save_bom(bom, path):
    with open((DATA / path), "w") as f:
        json.dump(bom, f, indent=4)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:**
  - `load_bom` / `save_bom`: *"They deserialize a BOM dictionary tree from JSON (`json.load`) and serialize a BOM tree back out to formatted JSON (`json.dump(..., indent=4)`) using `with open(...)` context managers so file handles always close safely."*
  - `repriced`: *"It performs a functional (non-mutating) tree update: at every node it creates a shallow copy `dict(node)`, replaces `"children"` with a new list of recursively `repriced` child dicts, updates `"cost"` if `"material"` matches, and returns the brand-new tree leaving the original untouched."*
- **Line-by-Line & Variable Breakdown (`repriced`):**
  - `new_node = dict(node)` (Line 65): Creates a **new dictionary** copying all top-level key-value bindings of `node` (`"name"`, `"qty"`, `"mass"`, `"cost"`, etc.).
  - `if "children" in node:` (Line 66) → `new_node["children"] = [repriced(child, material, factor) for child in node["children"]]` (Line 67): **Why `dict(node)` alone wasn't enough!** After line 65, `new_node["children"]` still pointed to the **exact same `list` object** as `node["children"]`! Rebinding `new_node["children"]` to a fresh list comprehension of recursive `repriced(...)` calls ensures every list and every child dict down the entire tree is newly allocated.
  - `if node.get("material") == material:` (Line 68): Uses `.get("material")` instead of `node["material"]` because assembly nodes (`bicycle`, `wheel`) do not have a `"material"` key! If they match `material`, line 69 updates `new_node["cost"] = node["cost"] * factor` on `new_node` (never touching `node`).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `load_bom(filename: str | Path) -> dict[str, Any]`
  - `repriced(node: dict, material: str, factor: int | float) -> dict[str, Any]`
  - `save_bom(bom: dict, path: str | Path) -> None` (note: no `return` statement, so returns `None`!)
- **Concrete Step-by-Step Trace on `dearer = repriced(bom, "steel", 1.10)`:**
  1. `repriced(bicycle, "steel", 1.10)`:
     - `new_node = dict(bicycle)` (new dict; `"children"` temporarily aliases `bicycle["children"]`).
     - `"children" in bicycle` is `True` → builds new list calling `repriced` on `wheel`, `frame`, `handlebar`, `saddle`, `chain`:
       - On `spoke` (`material: "steel"`, `cost: 0.40`): `new_node = dict(spoke)` (no `"children"`). `spoke.get("material") == "steel"` is `True` → `new_node["cost"] = 0.40 * 1.10 = 0.44`. Original `spoke["cost"]` remains `0.40`!
       - On `rim` (`material: "aluminium"`, `cost: 24.0`): `new_node = dict(rim)`, `"aluminium" == "steel"` is `False` → `cost` stays `24.0`.
       - On `wheel`: gets new `"children"` list of those 4 new dicts; `wheel.get("material")` is `None != "steel"`.
     - `bicycle` gets new `"children"` list of 5 new dicts.
  2. `unit_total(bom, key="cost")` is still `279.6`; `round(unit_total(dearer, key="cost"), 2)` is `295.46` (`144.60` of steel × `0.10` = `+14.46`... wait: steel cost in `bicycle.json` is `2*(32*0.40 + 12.00) + 95.00 + 14.00 = 2*24.80 + 109.00 = 158.60`; `158.60 * 0.10 = 15.86`; `279.60 + 15.86 = 295.46`!).
- **"What If the Caller Passed...?" (Edge Cases — READ #1 & #2 CAREFULLY!):**
  1. **CRITICAL QUIRK IN `save_bom` ([Line 95](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L95)): `with open((DATA / path), "w") as f:`!**
     - *Why did the doctest pass when `path = Path(tempfile.mkdtemp()) / "dearer.json"`?*  
       Because in Python's `pathlib`, joining any path with an **absolute** path on the right (`DATA / Path("/tmp/.../dearer.json")`) **discards the left-hand path `DATA`** and evaluates to `Path("/tmp/.../dearer.json")`!
     - *What if a caller passes a **relative** path, like `save_bom(dearer, "out.json")`?*  
       Then `DATA / "out.json"` writes to `assignment_01/W03/data/out.json` instead of `./out.json` in the current working directory! Writing `with open(path, "w") as f:` directly (without `DATA /`) is cleaner when the parameter is a full `path` rather than a `filename` inside `DATA`. Knowing this `pathlib` rule cold turns a potential gotcha into an impressive technical explanation!
  2. **`repriced(bom, None, 1.10)` (Passing `material=None`):**
     - On `bicycle` (an assembly node with no `"material"` key and no `"cost"` key!), `node.get("material")` returns `None`! Then `None == None` evaluates to **`True`**, and line 69 executes `node["cost"] * factor`, raising **`KeyError: 'cost'`**! *(Guarding `if "cost" in node and node.get("material") == material:` or putting `elif` after `if "children" in node:` avoids this completely!)*
  3. **`factor = 0` or negative `factor`:**
     - Sets all matching material costs to `0.0` (e.g., modeling free/subsidized material) without error.
  4. **Floating-point representation (`0.40 * 1.10`):**
     - In IEEE-754 binary float, `0.4 * 1.1` is `0.44000000000000006`, which is why the doctest uses `round(unit_total(dearer, key="cost"), 2)`!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - `repriced`: Visits each of the `N` nodes in the BOM tree once, performing an `O(k)` shallow dictionary copy (`k <= 5` keys per node, so `O(1)`) at each node. **Time `O(N)`**, **Space `O(N)`** for the newly returned tree + **`O(d)`** recursion stack frames.
  - `load_bom` / `save_bom`: **Time `O(N)`** to parse/serialize JSON; `load_bom` allocates **`O(N)`** dicts/lists, while `save_bom` streams to disk using **`O(d)`** recursion stack inside `json.dump`.
- **Alternative Comparison (`repriced` vs `copy.deepcopy`):**
  - *Alternative:* Call `new_tree = copy.deepcopy(node)` first, and then mutate `new_tree` in-place with a recursive helper.
  - *Trade-off:* Both are `O(N)` time and `O(N)` space, **but** your structural single-pass `repriced` walks the tree **once** instead of **twice** (`deepcopy` walk + reprice walk), doesn't need to maintain `deepcopy`'s internal memoization hash table (`memo` dict tracking object IDs for cycle detection), and makes the immutability guarantee explicit right in the code!
  - *Structural Sharing Bonus:* Could unmodified subtrees (e.g., `"saddle"`, made of `"plastic"`) be reused without copying? If the tree is treated as strictly immutable, yes (persistent data structures / structural sharing); however, copying every dict guarantees the caller can later mutate `dearer` without ever affecting `bom`.

### Likely Interview Q&A
1. **Q: On line 65 you wrote `new_node = dict(node)`. Why didn't `new_node = node` work, and why wasn't `new_node = dict(node)` by itself enough without line 67?**  
   **A:** `new_node = node` just creates a second variable referencing the *same* dict object, so any edit mutates `bom`. `new_node = dict(node)` makes a **shallow copy** of the top-level dict, so changing `new_node["cost"]` on a leaf is safe — *however*, on an assembly node, `new_node["children"]` still points to the **same list of child dicts** as `node["children"]`! Line 67 replaces `new_node["children"]` with a brand-new list of recursively copied child dicts, giving us a full deep copy of the tree structure in one pass.
2. **Q: Why do we use `with open(...) as f:` in `load_bom` and `save_bom` instead of `f = open(...)` followed by `f.close()`?**  
   **A:** `with` invokes the file's **context manager** (`__enter__` and `__exit__`), guaranteeing the OS file descriptor is flushed and closed immediately when leaving the block — *even if* `json.load` or `json.dump` raises an exception mid-flight!
3. **Q: Why did `save_bom(dearer, path)` work in the doctest even though you wrote `DATA / path` on line 95 and `path` was in `/tmp`?**  
   **A:** In `pathlib`, the `/` operator checks whether the right-hand path is absolute. Since `tempfile.mkdtemp()` returns an absolute path, `DATA / path` discards `DATA` and evaluates to `path`! However, for relative paths `DATA / path` would save inside `W03/data/`, so `open(path, "w")` directly would be cleaner for general paths.

---

## Week 03 Watchlist — Subtle Quirks in Your Submitted Code

Review these 6 points for 60 seconds right before walking into the interview — if the lecturer probes any of them, already knowing the answer turns a trap into easy top marks:

1. **[`E02_sort_by_key.py` L46](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py#L46):** Your `# ANSWER` comment says `sort(xs)` instead of `xs.sort()`. Clarify verbally that `.sort()` is a **list method** (`xs.sort()`), whereas `sorted(xs)` is the built-in function.
2. **[`E04_flatten.py` L30](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py#L30):** `result = []` runs *before* the base-case `if not isinstance(items, list): return [items]`, allocating an unused empty list on every leaf call. Also remember that copying lists up `d` levels costs `O(N + L * d)` time.
3. **[`E05_count_parts.py` L63](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py#L63):** If an assembly node has `"children": []` (empty list), `deepest` raises `ValueError: max() iterable argument is empty`.
4. **[`E06_apply_fn.py` L47 & L74](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L47):** `list(fn(x) for x in L)` wraps a **generator expression** in `list()` (vs list comprehension `[fn(x) for x in L]`), and `yield from (fn(x) for x in g)` delegates to an inner generator expression (vs `for x in g: yield fn(x)`). Know both forms!
5. **[`E07_part_paths.py` L88–L93](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L88-L93):** Remember *why* `try ... except KeyError: raise KeyError(path)` is there (re-attaching stripped path prefixes on error), and note that splitting/joining at each recursive call costs `O(d * S)` string work vs `O(S)` iteratively.
6. **[`E08_bom_json.py` L68 & L95](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L68):** `repriced(bom, None, 1.1)` would match `node.get("material") == None` on assembly nodes and raise `KeyError: 'cost'`; and `DATA / path` in `save_bom` only wrote to `tempfile` because `pathlib` ignores `DATA` when `path` is absolute!
