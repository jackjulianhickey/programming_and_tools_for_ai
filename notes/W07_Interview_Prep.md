# Week 7 Interview Prep: Dynamic Programming, Edit Distance & Dynamic Time Warping

[<- Back to Master Interview Playbook](./README.md)

**Core Topics:** Overlapping Subproblems, Top-Down Memoization (`@functools.cache`) vs. Bottom-Up Tabulation vs. Rolling-State Space Optimization (`O(1)` scalars / `O(m)` single row), DP Traceback, Lexicographic Tuple Sorting & Stability, Hamming Distance (`zip` / `zip_longest`), Levenshtein Edit Distance, and Dynamic Time Warping (DTW).

> **Why Week 7 Matters for 8–10 Marks:** Week 7 is the classic Dynamic Programming & Algorithmic Trade-offs week. Even the docstring of `E04_one_row.py` explicitly warns: *"You are on your honour, and the interview is where it gets asked about."* Expect pointed questions on how `prev_row` and `curr_row` map to the 2D recurrence, what capability you **lose** when discarding the DP table (`edits` traceback!), why tie-breaking in `E05_spell.py` is a **function correctness issue** (not just a doctest quirk—watch out, your comment in `E05` only mentioned doctests!), and why Levenshtein and DTW fail catastrophically on each other's data in `E06_wrong_tool.py`.

---

## Table of Contents

1. [Week 7 Exercise Summary Table](#1-week-7-exercise-summary-table)
2. [Reference Context: `E01_editdist.py` (Given Code)](#2-reference-context-e01_editdistpy-given-code)
3. [`E02_hamming.py` — Positional Mismatch & `zip` vs. `zip_longest`](#3-e02_hammingpy--positional-mismatch--zip-vs-zip_longest)
4. [`E03_fib_table.py` — Bottom-Up Tabulation vs. `O(1)` Rolling Pair](#4-e03_fib_tablepy--bottom-up-tabulation-vs-o1-rolling-pair)
5. [`E04_one_row.py` — Space-Optimized Levenshtein Distance (`O(m)` Space)](#5-e04_one_rowpy--space-optimized-levenshtein-distance-om-space)
6. [`E05_spell.py` — Dictionary Spellchecking & Deterministic Tie-Breaking](#6-e05_spellpy--dictionary-spellchecking--deterministic-tie-breaking)
7. [`E06_wrong_tool.py` — Levenshtein on Floats vs. DTW on Symbols](#7-e06_wrong_toolpy--levenshtein-on-floats-vs-dtw-on-symbols)
8. [Week 7 Master Comparison Cheat Sheets (DP Strategies & Distance Metrics)](#8-week-7-master-comparison-cheat-sheets-dp-strategies--distance-metrics)

---

## 1. Week 7 Exercise Summary Table

Let `n = len(a)` and `m = len(b)` for sequence comparisons, `n` be the index for Fibonacci, and `W = len(words)` with max dictionary word length `M` and query length `L` for spellchecking.

| Exercise File | Functions | Difficulty Tier | Time Complexity (Your Code) | Space Complexity (Your Code) |
| :--- | :--- | :--- | :--- | :--- |
| [E01_editdist.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py) | [`fib_slow`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L33-L39), [`fib_cached`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L42-L51), [`edit_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L54-L78), [`levenshtein`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L81-L91), [`edits`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L96-L121), [`dtw`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L126-L146) | Reference (Given) | `fib_slow`: `O(2^n)`<br>`fib_cached`: `O(n)`<br>`edit_table` / `dtw`: `O(n * m)` | `fib_slow` / `fib_cached`: `O(n)`<br>`edit_table` / `dtw`: `O(n * m)` |
| [E02_hamming.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py) | [`hamming`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py#L15-L25)<br>[`hamming_padded`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py#L28-L40) | Warm-up | `hamming`: `O(min(n, m))`<br>`hamming_padded`: `O(max(n, m))` | `O(1)` *(lazy generator expressions)* |
| [E03_fib_table.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py) | [`fib_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L13-L26)<br>[`fib_pair`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L29-L42) | Warm-up / Moderate | `fib_table`: `O(n)`<br>`fib_pair`: `O(n)` | `fib_table`: `O(n)`<br>`fib_pair`: `O(1)` *(word model)* |
| [E04_one_row.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py) | [`levenshtein_row`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py#L22-L57) | **Hard (8–10 Mark Target)** | `O(n * m)` | `O(m)` *(two rows of length `m + 1`; `O(min(n, m))` if inputs swapped)* |
| [E05_spell.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py) | [`suggest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L26-L42) | Moderate / Hard | `O(W * L * M + W log W)` | `O(W + M)` |
| [E06_wrong_tool.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py) | [`levenshtein_tol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L29-L59)<br>[`dtw_symbols`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L62-L85) | **Hard (8–10 Mark Target)** | `O(n * m)` | `O(n * m)` |

---

## 2. Reference Context: `E01_editdist.py` (Given Code)

**File:** [E01_editdist.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py)

Every exercise in Week 7 builds on or contrasts with the four core ideas in [E01_editdist.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py):

### 2.1 Overlapping Subproblems: `fib_slow` vs. `fib_cached`
- [`fib_slow`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L33-L39): `fib_slow(n - 1) + fib_slow(n - 2)` spawns a binary call tree of size $2 F_{n+1} - 1 = \Theta(\varphi^n)$ where $\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618$ (bounded above by `O(2^n)`), because identical subproblems like `fib_slow(2)` are recomputed millions of times (`29,860,703` calls for `n = 35`!). Call-stack depth is `O(n)`.
- [`fib_cached`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L42-L51): Adding `@cache` (`functools.cache`, an unbounded hash-map memoizer keyed on `(n,)`) ensures each of `0, 1, ..., n` is computed **at most once**, dropping time to **`O(n)`** (`31` unique subproblems for `n = 30`). However, it still uses **`O(n)` space** for both the cache dictionary and the recursion stack (and hits `RecursionError` around `n = 1000` if cold!).

### 2.2 Levenshtein Edit Distance (`edit_table` & `levenshtein`)
- [`edit_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L54-L78) builds an `(n + 1) x (m + 1)` grid `D` where `D[i][j]` is the minimum edits transforming prefix `a[:i]` (first `i` chars) into prefix `b[:j]` (first `j` chars).
- **Why `[[0] * (len(b) + 1) for _ in range(len(a) + 1)]` ([line 67](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L67))?** Writing `[[0] * (m + 1)] * (n + 1)` would make every row a reference to the **exact same list**, so setting `D[1][0] = 1` would mutate column `0` of every row!
- **Base cases:** `D[i][0] = i` (delete `i` chars from `a[:i]` to reach `""`) and `D[0][j] = j` (insert `j` chars into `""` to reach `b[:j]`).
- **Recurrence ([lines 74–77](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L74-L77)):** Note the **`i - 1` / `j - 1` index shift** because row/col `0` is the empty prefix `""`, so the `i`-th character of `a` sits at `a[i - 1]`:
  $$D[i][j] = \min\Bigl(\underbrace{D[i - 1][j] + 1}_{\text{delete } a[i-1]},\; \underbrace{D[i][j - 1] + 1}_{\text{insert } b[j-1]},\; \underbrace{D[i - 1][j - 1] + \text{cost}}_{\text{keep (0) or substitute (1)}}\Bigr)$$

### 2.3 Reconstructing the Alignment (`edits` Traceback)
- [`edits`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L96-L121) starts at `(i, j) = (len(a), len(b))` and walks backwards to `(0, 0)` in **`O(n + m)`** steps, checking which of the three predecessor cells (`D[i-1][j-1] + cost`, `D[i-1][j] + 1`, or `D[i][j-1] + 1`) equals `D[i][j]`, appending edit descriptions in reverse order, and calling `steps.reverse()`.
- **Crucial insight for `E04`:** `edits` **requires the entire `O(n * m)` table `D` in memory**! Once you throw away old rows in `E04_one_row.py`, you still get the distance `D[n][m]`, *but you can no longer walk back through `D` to print the edits!*

### 2.4 Dynamic Time Warping (`dtw`) vs. `edit_table`
Compare [`dtw`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L126-L146) against `edit_table`—they differ in **only two places**:
1. **Border Initialization ([lines 140–141](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L140-L141)):** Every cell starts at `INF = float("inf")` **except `D[0][0] = 0.0`**. `D[i][0] = INF` ($i > 0$) and `D[0][j] = INF` ($j > 0$) forbid dropping unaligned leading elements: `a[0]` *must* pair with `b[0]`, and `a[-1]` *must* pair with `b[-1]`.
2. **Recurrence & Step Cost ([lines 144–145](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L144-L145)):**
   $$D[i][j] = |a[i - 1] - b[j - 1]| + \min\bigl(D[i - 1][j],\; D[i][j - 1],\; D[i - 1][j - 1]\bigr)$$
   There is **no `+ 1` deletion/insertion penalty**! Moving right (`D[i][j - 1]`) or down (`D[i - 1][j]`) **stretches** (re-matches) `a[i - 1]` or `b[j - 1]` against another sample, paying `|a[i - 1] - b[j - 1]|`—which is **`0.0`** when a signal holds a steady value longer!

---

## 3. `E02_hamming.py` — Positional Mismatch & `zip` vs. `zip_longest`

- **File:** [E02_hamming.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py)
- **Functions:** [`hamming`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py#L15-L25), [`hamming_padded`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py#L28-L40)
- **Difficulty Tier:** Warm-up

### Your Code

```python
from itertools import zip_longest
def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def hamming_padded(a, b):
    return sum(x != y for x, y in zip_longest(a, b))
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `hamming` counts index-by-index character mismatches up to the shorter sequence's length using `zip`, while `hamming_padded` uses `itertools.zip_longest` so every trailing element of a longer sequence also counts as a mismatch. Both pass a lazy generator expression directly to `sum`, computing the count in a single `O(1)`-memory pass.
- **Line-by-Line & Variable Breakdown:**
  - `zip(a, b)` (line 25): Lazily yields `(x, y)` pairs `(a[0], b[0]), (a[1], b[1]), ...`, stopping as soon as **either** `a` or `b` runs out of elements.
  - `x != y` (lines 25 & 40): Evaluates to a `bool` (`True` when elements differ, `False` when equal). Because `bool` subclasses `int` in Python (`True == 1`, `False == 0`), `sum(...)` adds `1` for every `True` and `0` for every `False`.
  - `zip_longest(a, b)` (line 40): Lazily pairs elements until the **longer** iterable is exhausted, padding the shorter iterable with default `fillvalue=None`. For string inputs, no character equals `None`, so every padded `(char, None)` or `(None, char)` pair evaluates `x != y` to `True` (`+1`).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `a`, `b`: `Iterable[Any]` (not just `str`—works on `list`, `tuple`, or even one-shot generators!).
  - `x`, `y`: element types of `a`, `b` (or `None` during `zip_longest` padding).
  - `x != y for ...`: `generator` yielding `bool`s.
  - Return type: `int` (`sum` starts at `0`, an `int`, so even when empty it returns `0`, never `bool`).
- **Concrete Step-by-Step Trace (`hamming("abc", "axcde")` vs. `hamming_padded("abc", "axcde")`):**
  - `hamming("abc", "axcde")`: `zip` yields `('a','a') -> False`, `('b','x') -> True`, `('c','c') -> False`, then stops! Ignores `'d'`, `'e'`. `sum` returns **`1`**.
  - `hamming_padded("abc", "axcde")`: `zip_longest` yields the same 3 pairs (`False, True, False`) **plus** `(None, 'd') -> True` and `(None, 'e') -> True`. `sum` returns **`3`**.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Both empty (`hamming("", "")` / `hamming_padded("", "")`):** Generator yields 0 items; `sum(())` returns `0`.
  2. **Prefix trap (`hamming("abc", "abcde")`):** Returns **`0`**! `hamming` claims two distinct strings have zero distance because `zip` silently truncates `"de"`.
  3. **1-character shift (`hamming("ACGTACGTAC", "CGTACGTACA")`):** Returns **`10`** (maximum possible disagreement!), whereas `levenshtein` is only **`2`** (`delete A` at front, `insert A` at end). Hamming is rigid one-to-one alignment and cannot re-synchronize after an insertion or deletion.
  4. **WICKED HIDDEN EDGE CASE — `None` inside a list (`hamming_padded([1, None], [1])`)!**
     - Look at line 45's comment: *"None equals nothing, so every unmatched item counts as a difference."* That's true for **strings** (`'a' != None`), **but what if `a = [1, None]` and `b = [1]`?!**
     - `zip_longest([1, None], [1])` pads `b` with `fillvalue=None`, yielding `(1, 1)` and `(None, None)`! Since `None != None` is **`False`**, `hamming_padded([1, None], [1])` returns **`0`** instead of **`1`**!
     - *How to make it bulletproof for ANY iterable including `None`?* Pass a unique private sentinel object: `_SENTINEL = object()` and `zip_longest(a, b, fillvalue=_SENTINEL)` (`object()` is only `==` to itself!). Spotting that in an interview is guaranteed 10/10 material!

### Pillar 3 — Analyse (Complexity & Algorithmic Comparisons)

- **Time Complexity:**
  - `hamming(a, b)`: **`O(min(n, m))`** element comparisons.
  - `hamming_padded(a, b)`: **`O(max(n, m))`** element comparisons.
- **Space Complexity:** **`O(1)` auxiliary space** for both! Because `sum(x != y for ...)` uses a **generator expression** (no square brackets `[...]`) and both `zip` and `zip_longest` are C iterators yielding one pair at a time, no `O(n)` list is ever materialized in memory. (Writing `sum([x != y for ...])` with brackets would waste `O(n)` memory!)
- **Comparison (Hamming vs. Levenshtein):**
  - Hamming runs in **`O(n)` time and `O(1)` space**, vs. Levenshtein's **`O(n * m)` time and `O(min(n, m))` space**. Use Hamming when positions are fixed and insertions/deletions are impossible (e.g., fixed-length binary error-correcting codes, aligned SNP alleles of equal length); use Levenshtein whenever characters can be inserted or deleted (text typos, unaligned DNA reads).

### Likely Interview Q&A

1. **Q: What type does `x != y` produce, and why doesn't `sum(...)` complain about summing booleans?**
   - **A:** `x != y` produces a `bool`, and in Python `bool` is a subclass of `int` (`issubclass(bool, int)` is `True`) where `True` has integer value `1` and `False` has integer value `0`. Starting from `0`, `sum` adds `1` per `True`.
2. **Q: Why didn't you write `hamming(a, b) + abs(len(a) - len(b))` for `hamming_padded`?**
   - **A:** For sequences like `str` and `list`, `hamming(a, b) + abs(len(a) - len(b))` actually works in `O(min(n, m))` time (even faster when one string is short and the other is huge, AND immune to the `None` bug!). However, `len(...)` fails with `TypeError` on lazy iterators/generators that don't support `__len__`, whereas `zip_longest` works on any iterable.

---

## 4. `E03_fib_table.py` — Bottom-Up Tabulation vs. `O(1)` Rolling Pair

- **File:** [E03_fib_table.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py)
- **Functions:** [`fib_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L13-L26), [`fib_pair`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L29-L42)
- **Difficulty Tier:** Warm-up / Moderate

### Your Code

```python
def fib_table(n):
    if n == 0:
        return 0
    table = [0, 1]
    for i in range(2, n+1):
        table.append(table[i-1] + table[i-2])
    return table[n]


def fib_pair(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `fib_table` computes the $n$-th Fibonacci number via bottom-up tabulation, filling a list from base cases `0` and `1` up to index `n` so each subproblem is solved once without recursion. `fib_pair` observes that `F(i)` only ever looks two steps back (`F(i-1)` and `F(i-2)`), sliding just two variables `a` and `b` forward in `O(1)` space—the exact 1D prototype for `E04`'s two-row edit distance!
- **Line-by-Line & Variable Breakdown:**
  - `if n == 0: return 0` (lines 21–22): Early return for `n = 0`. *(Good detail to know: even if you deleted lines 21–22—as in the official solution—`table = [0, 1]`, `range(2, 1)` is empty, and `return table[0]` still returns `0`!)*
  - `table = [0, 1]` & `for i in range(2, n+1): table.append(table[i-1] + table[i-2])` (lines 23–25): Seeds $F_0 = 0, F_1 = 1$, then computes $F_2, F_3, \dots, F_n$ in topological dependency order so `table[i-1]` and `table[i-2]` are guaranteed already computed when index `i` runs.
  - `a, b = 0, 1` (line 39): **Loop invariant:** after `k` iterations of the `for _ in range(n):` loop, `a == F(k)` and `b == F(k + 1)`. At `k = 0` (before the loop), `a = F(0) = 0` and `b = F(1) = 1`.
  - `a, b = b, a + b` (line 41): Python **tuple unpacking** evaluates the entire right-hand side `(b, a + b)` using the *old* `a` and `b` before rebinding either name—advancing `(F(k), F(k+1))` to `(F(k+1), F(k+2))` without needing a `temp` variable!
  - `return a` (line 42): Why `return a` and NOT `return b`? Because after `n` iterations (`k = n`), the invariant says `a == F(n)` while `b == F(n + 1)`!

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:** `n`: `int`; `table`: `list[int]`; `i`, `_`, `a`, `b`: `int`; return type: `int`.
- **Concrete Step-by-Step Trace (`fib_pair(4)`):**
  - Start (`k = 0`): `a = 0`, `b = 1`
  - Iter 1 (`k = 1`): `a, b = 1, 0 + 1` -> `a = 1, b = 1`
  - Iter 2 (`k = 2`): `a, b = 1, 1 + 1` -> `a = 1, b = 2`
  - Iter 3 (`k = 3`): `a, b = 2, 1 + 2` -> `a = 2, b = 3`
  - Iter 4 (`k = 4`): `a, b = 3, 2 + 3` -> `a = 3, b = 5`
  - Returns `a` = **`3`** ($F_4 = 3$).
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **`n = 0` and `n = 1`:**
     - `fib_table(0)` hits `if n == 0: return 0` -> `0`; `fib_pair(0)` runs `range(0)` (0 times) -> returns `a = 0`.
     - `fib_table(1)`: `range(2, 2)` is empty -> returns `table[1] = 1`; `fib_pair(1)` runs 1 time (`a, b = 1, 1`) -> returns `a = 1`.
  2. **TRICKY TRACE — Negative integer (`n = -1` vs. `n = -3`)!**
     - What does your `fib_table(-1)` return?! `n == 0` is `False` -> `table = [0, 1]` -> `range(2, 0)` is empty -> **`return table[-1]` indexes from the END of `[0, 1]` and silently returns `1`!** For `n = -2` it returns `0`, and for `n = -3` it raises `IndexError: list index out of range`!
     - What does your `fib_pair(-1)` return?! `range(-1)` is empty -> loop runs 0 times -> **returns `0`!** (They disagree on `n = -1`!)
  3. **Large `n` (`n = 2000`):** Both `fib_table(2000)` and `fib_pair(2000)` succeed effortlessly, whereas `E01`'s `@cache` recursive `fib_cached(2000)` crashes with **`RecursionError: maximum recursion depth exceeded`** on a cold cache!

### Pillar 3 — Analyse (Complexity & Algorithmic Comparisons)

- **Time & Space Complexity:**
  - `fib_table(n)`: **`O(n)`** time (`n - 1` additions and `O(1)` amortized list appends) and **`O(n)`** space (list of `n + 1` integers).
  - `fib_pair(n)`: **`O(n)`** time (`n` additions) and **`O(1)`** space (2 variable bindings in the standard unit-cost word RAM model). *(Bonus 10/10 nuance: because $F_n \approx \varphi^n / \sqrt{5}$ requires $\Theta(n)$ bits in Python's arbitrary-precision `int`, adding two $n$-bit integers at the bit level actually costs $\Theta(n^2)$ bit operations total and $\Theta(n)$ bits to hold `a` and `b`—vs. $\Theta(n^2)$ bits for `fib_table`!)*
- **Top-Down Memoization (`fib_cached`) vs. Bottom-Up Tabulation (`fib_table`) vs. Rolling State (`fib_pair`):**
  - Top-down `@cache`: easiest to write from a recurrence, computes *only* reachable subproblems, but pays function-call overhead, `O(n)` dict memory, and `O(n)` call-stack depth (`RecursionError` risk).
  - Bottom-up `fib_table`: iterative (no recursion limit, fast contiguous list indexing), `O(n)` memory; handy if you will query *many* `F(k)` values later.
  - Rolling `fib_pair`: optimal `O(1)` state count when you only want the final value `F(n)`. (Even faster for huge `n`: $2 \times 2$ matrix exponentiation / fast doubling computes $F_n$ in `O(log n)` multiplications!)

### Likely Interview Q&A

1. **Q: Why did `fib_pair` return `a` instead of `b`, and what would `return b` compute?**
   - **A:** `a` starts at `F(0) = 0` and steps forward `n` times, so after `n` iterations `a` holds `F(n)` while `b` holds `F(n + 1)`. Returning `b` would be off by one (`fib(n + 1)`), failing `n = 0` (`1` instead of `0`).
2. **Q: What happens in `a, b = b, a + b` if you wrote it on two lines without a temporary variable (`a = b` then `b = a + b`)?**
   - **A:** `a = b` would overwrite `a` first, so `b = a + b` would compute `b + b = 2 * b` (powers of 2!) instead of Fibonacci numbers. Tuple assignment evaluates `(b, a + b)` before mutating `a`.

---

## 5. `E04_one_row.py` — Space-Optimized Levenshtein Distance (`O(m)` Space)

- **File:** [E04_one_row.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py)
- **Function:** [`levenshtein_row`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py#L22-L57)
- **Difficulty Tier:** **Hard (8–10 Mark Target — Explicitly Flagged in Docstring for Interview!)**

### Your Code

```python
from E01_editdist import levenshtein
def levenshtein_row(a, b):
    prev_row = list(range(len(b) + 1))

    for i in range (1, len(a) + 1):
        curr_row = [0] * (len(b) + 1)
        curr_row[0] = i

        for x in range(1, len(b) + 1):
            cost = 0 if a[i -1] == b[x - 1] else 1
            curr_row[x] = min (
                prev_row[x] + 1,
                curr_row[x - 1] + 1,
                prev_row[x - 1] + cost
            )
        prev_row = curr_row
    return prev_row[-1]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `levenshtein_row` computes the exact Levenshtein edit distance between `a` and `b` in `O(len(b))` memory instead of `O(len(a) * len(b))` by keeping only two 1D lists at any moment: `prev_row` (row `i - 1` of the DP table) and `curr_row` (row `i` currently being filled left-to-right). Once row `i` finishes, `prev_row = curr_row` promotes it to become the "row above" for iteration `i + 1`, letting Python garbage-collect the older row.
- **Line-by-Line & Variable Breakdown:**
  - `prev_row = list(range(len(b) + 1))` (line 43): Initializes **row `0`** of the DP table `[0, 1, 2, ..., len(b)]`, representing the `j` insertions needed to turn `""` (`a[:0]`) into `b[:j]`.
  - `for i in range(1, len(a) + 1):` (line 45): Outer loop stepping down one row per character of `a` (`a[i - 1]`).
  - `curr_row = [0] * (len(b) + 1)` & `curr_row[0] = i` (lines 46–47): Allocates a **fresh** list for row `i` and sets its column-0 base case (`i` deletions to turn `a[:i]` into `""`).
  - `for x in range(1, len(b) + 1):` (line 49): Inner loop filling columns `1 .. len(b)` **strictly left-to-right** (necessary because `curr_row[x]` reads `curr_row[x - 1]`, which must already be filled!). *(Naming self-awareness note: here `x` is the column index usually named `j`; if asked "Why `x`?", explain you thought of `x` as the horizontal x-coordinate across the row, though `j` paired with `i` is cleaner and avoids confusion with `E04` solution's `for i, x in enumerate(a)` where `x` is a character.)*
  - **The 3-way `min` mapping ([lines 51–55](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py#L51-L55)):**
    - `prev_row[x] + 1` $\equiv D[i - 1][x] + 1$: **Delete** `a[i - 1]` (cell directly above).
    - `curr_row[x - 1] + 1` $\equiv D[i][x - 1] + 1$: **Insert** `b[x - 1]` (cell immediately to the left in the *current* row).
    - `prev_row[x - 1] + cost` $\equiv D[i - 1][x - 1] + \text{cost}$: **Keep** (`cost = 0`) or **Substitute** (`cost = 1`) `a[i - 1] -> b[x - 1]` (diagonal top-left cell).
  - `prev_row = curr_row` (line 56): Rebinds `prev_row` to the finished row. **Why doesn't this cause an aliasing bug without `.copy()`?** Because on the *next* iteration of line 46, `curr_row = [0] * (len(b) + 1)` creates a **brand-new list object** rather than mutating the list `prev_row` points to!
  - `return prev_row[-1]` (line 57): Returns the bottom-right value (`D[len(a)][len(b)]`), and crucially works even when `a == ""` (when the outer loop runs `0` times and `curr_row` was never even defined!).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `a`, `b`: `Sequence[Any]` (`str`, `list`, `tuple` — must support `len()` and indexing `a[i - 1]`).
  - `prev_row`, `curr_row`: `list[int]` of length `len(b) + 1`.
  - `i`, `x`, `cost`: `int`.
  - Return type: `int`.
- **Concrete Step-by-Step Row Trace (`levenshtein_row("cat", "cut")`):**
  - `b = "cut"` (`len(b) = 3`).
  - **Before loop (`i = 0`, `""`):** `prev_row = [0, 1, 2, 3]` (columns for `""`, `"c"`, `"cu"`, `"cut"`).
  - **`i = 1` (`a[0] = 'c'`):** `curr_row` starts `[1, 0, 0, 0]`.
    - `x = 1` (`'c' == 'c'`, `cost = 0`): `min(1+1, 1+1, 0+0) = 0` -> `[1, 0, 0, 0]`
    - `x = 2` (`'c' != 'u'`, `cost = 1`): `min(2+1, 0+1, 1+1) = 1` -> `[1, 0, 1, 0]`
    - `x = 3` (`'c' != 't'`, `cost = 1`): `min(3+1, 1+1, 2+1) = 2` -> `prev_row = [1, 0, 1, 2]`
  - **`i = 2` (`a[1] = 'a'`):** `curr_row` starts `[2, 0, 0, 0]`.
    - `x = 1` (`'a' != 'c'`, `cost = 1`): `min(0+1, 2+1, 1+1) = 1`
    - `x = 2` (`'a' != 'u'`, `cost = 1`): `min(1+1, 1+1, 0+1) = 1` (diagonal substitute `'a'->'u'`)
    - `x = 3` (`'a' != 't'`, `cost = 1`): `min(2+1, 1+1, 1+1) = 2` -> `prev_row = [2, 1, 1, 2]`
  - **`i = 3` (`a[2] = 't'`):** `curr_row` starts `[3, 0, 0, 0]`.
    - `x = 1` (`'t' != 'c'`): `min(1+1, 3+1, 2+1) = 2`
    - `x = 2` (`'t' != 'u'`): `min(1+1, 2+1, 1+1) = 2`
    - `x = 3` (`'t' == 't'`, `cost = 0`): `min(2+1, 2+1, 1+0) = 1` -> `prev_row = [3, 2, 2, 1]`
  - Returns `prev_row[-1]` = **`1`**.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **`a = ""`, `b = "abc"`:** `prev_row = [0, 1, 2, 3]`. `range(1, 1)` is empty -> outer loop skipped completely! If line 57 had returned `curr_row[-1]`, it would crash with **`UnboundLocalError: cannot access local variable 'curr_row'`**! Returning `prev_row[-1]` cleanly returns **`3`**.
  2. **`a = "abc"`, `b = ""`:** `prev_row = [0]`. Outer loop runs `i = 1, 2, 3`: `curr_row = [i]`, inner loop `range(1, 1)` skipped, `prev_row = [i]`. Returns `prev_row[-1]` = **`3`**.
  3. **`a = ""`, `b = ""`:** `prev_row = [0]`, outer loop skipped, returns `prev_row[-1]` = **`0`**.
  4. **Generator / `set` input (`levenshtein_row(set("ab"), "ab")`):** `len()` works on `set`, **but** `a[i - 1]` on line 50 raises `TypeError: 'set' object is not subscriptable`. (Official solution using `enumerate` avoids indexing `a` and `b` directly, though `len(b)` still requires `b` to be `Sized`.)

### Pillar 3 — Analyse (Complexity & Space-Time Trade-offs)

- **Time Complexity:** **`O(n * m)`** — identical number of inner-loop iterations ($n \times m$) and `O(1)` work per cell as `E01`'s full `edit_table` (actually slightly *faster* in wall-clock time due to better CPU L1 cache locality on two tiny arrays!).
- **Space Complexity:** **`O(m)`** (`O(len(b))`) — at peak inside the outer loop, only `prev_row` (`m + 1` ints) and `curr_row` (`m + 1` ints) exist simultaneously; when `prev_row = curr_row` executes, the old `prev_row` drops to reference count `0` and is immediately freed by CPython.
  - **Can you make it `O(min(n, m))`?** **YES!** Because Levenshtein distance is symmetric ($d(a, b) = d(b, a)$: every insertion in $a \to b$ is a deletion in $b \to a$), adding `if len(a) < len(b): a, b = b, a` at the top ensures `len(b)` is always the shorter length! Comparing a 5-letter word against a 1,000,000-character string then uses **6 integers** of memory instead of 1,000,001!
  - **Can you use literally ONE list instead of two?** Yes—maintain a single `row` plus one scalar `diag` saving `row[x - 1]`'s old value before `row[x - 1]` is overwritten (same `O(m)` asymptotic space, half the memory).
- **What Do We LOSE With Two Rows? (The Classic Interview Question!):**
  - You lose [`edits(a, b)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L96-L121) **traceback**! `edits` walks backwards from `D[n][m]` through interior rows `n - 1, n - 2, ..., 0` to reconstruct *which* substitutions/insertions/deletions achieved the minimum distance. Discarding rows `0 .. n - 2` destroys the predecessor trail. *(Bonus flex: Hirschberg's divide-and-conquer algorithm recovers the full edit script in `O(n * m)` time and `O(min(n, m))` space by running forward and reverse one-row DP to find the midpoint split!)*

### Likely Interview Q&A

1. **Q: Suppose I tried to optimize memory allocations by moving `curr_row = [0] * (len(b) + 1)` BEFORE `for i in range(1, len(a) + 1):` and leaving everything else unchanged. What breaks?**
   - **A:** After iteration `i = 1`, `prev_row = curr_row` makes **both names point to the exact same list**! On iteration `i = 2`, `curr_row[0] = 2` overwrites `prev_row[0]` (`D[1][0]`), so when `x = 1` reads `prev_row[x - 1] + cost`, it reads the *newly overwritten* `curr_row[0]` instead of the old diagonal `D[1][0]`, corrupting the distances! To reuse two pre-allocated lists safely without allocating per row, you must **swap** them: `prev_row, curr_row = curr_row, prev_row`!
2. **Q: Could `for x in range(len(b), 0, -1):` fill `curr_row` right-to-left instead of left-to-right?**
   - **A:** **No!** Computing `curr_row[x]` requires `curr_row[x - 1] + 1` (insertion in the current row). Filling right-to-left means `curr_row[x - 1]` is still `0` when `curr_row[x]` reads it! Data dependencies (`(i-1, x)`, `(i-1, x-1)`, and `(i, x-1)`) force left-to-right order within each row.
3. **Q: What would happen on line 57 if `a` were `""` and you wrote `return curr_row[-1]` instead of `return prev_row[-1]`?**
   - **A:** `range(1, 1)` wouldn't execute a single iteration, so `curr_row` would never be assigned and Python would raise `UnboundLocalError`! Returning `prev_row[-1]` handles `a == ""` seamlessly because `prev_row` already holds row `0` (`[0, 1, ..., len(b)]`).

---

## 6. `E05_spell.py` — Dictionary Spellchecking & Deterministic Tie-Breaking

- **File:** [E05_spell.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py)
- **Function:** [`suggest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L26-L42)
- **Difficulty Tier:** Moderate / Hard (**High-Priority `# ANSWER` Watchlist Item!**)

### Your Code

```python
from E01_editdist import levenshtein
from E04_one_row import levenshtein_row
# Given: a small word list, so the doctests need no real dictionary.
WORDS = ["cat", "cart", "car", "cast", "case", "bat", "dog"]


def suggest(word, words, n=3):
    pairs = [(levenshtein_row(word, w), w) for w in words]

    pairs.sort()

    return [w for dist, w in pairs[:n]]


# ANSWER: If it is sorted based on distance only then words with a the same distance
# are not sorted alphabetically and may not match the order of the doctests.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `suggest` implements a spellchecker using the classic **Decorate-Sort-Undecorate** (Schwartzian transform) pattern: it pairs every candidate word `w` in `words` with its `levenshtein_row` distance `(dist, w)`, sorts the tuples lexicographically so ties break alphabetically, and unpacks the top `n` words. Using `E04`'s `levenshtein_row` avoids allocating 100,000 full 2D DP tables across a real dictionary.
- **Line-by-Line & Variable Breakdown:**
  - Imports (lines 20–21): Notice `levenshtein` on line 20 is left over from the starter stub and unused because you upgraded to `levenshtein_row` on line 21!
  - `pairs = [(levenshtein_row(word, w), w) for w in words]` (line 38): **Decorate step**—computes edit distance **exactly once** per dictionary word `w` and builds `list[tuple[int, str]]`.
  - `pairs.sort()` (line 40): **Sort step**—sorts `pairs` in-place via Python's Timsort. Tuples compare element-by-element: first `pair[0]` (`int` edit distance, ascending), and **only when distances are equal**, `pair[1]` (`str` word, ascending ASCII/Unicode alphabetical order).
  - `return [w for dist, w in pairs[:n]]` (line 42): **Undecorate step**—slices the first `n` `(dist, w)` tuples and extracts `w`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `word`: `str`; `words`: `Iterable[str]`; `n`: `int` (default `3`).
  - `pairs`: `list[tuple[int, str]]`.
  - Return type: `list[str]`.
- **Concrete Step-by-Step Trace (`suggest("cet", WORDS, n=3)`):**
  1. `WORDS = ["cat", "cart", "car", "cast", "case", "bat", "dog"]`.
  2. Line 38 builds `pairs`:
     `[(1, 'cat'), (2, 'cart'), (2, 'car'), (2, 'cast'), (3, 'case'), (2, 'bat'), (3, 'dog')]`.
     *(Notice **four** words tie at distance `2`: `'cart'`, `'car'`, `'cast'`, `'bat'`!)*
  3. Line 40 `pairs.sort()` orders by `dist`, breaking the 4-way tie at `dist = 2` alphabetically (`'bat' < 'car' < 'cart' < 'cast'`):
     `[(1, 'cat'), (2, 'bat'), (2, 'car'), (2, 'cart'), (2, 'cast'), (3, 'case'), (3, 'dog')]`.
  4. `pairs[:3]` -> `[(1, 'cat'), (2, 'bat'), (2, 'car')]` -> returns **`['cat', 'bat', 'car']`**.
  - *What if we had sorted on `distance` alone (`pairs.sort(key=lambda p: p[0])`)?* Because Python's Timsort is **stable**, the 4 tied words at `dist = 2` would stay in `WORDS`'s original input order (`'cart'`, `'car'`, `'cast'`, `'bat'`), returning **`['cat', 'cart', 'car']`** instead of `['cat', 'bat', 'car']`!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty dictionary (`suggest("cat", [])`):** `pairs = []`, `pairs.sort()` is a no-op, `pairs[:3]` is `[]`, returns `[]`.
  2. **`n` larger than dictionary (`suggest("cat", WORDS, n=100)`):** Python list slicing never raises `IndexError` when stop exceeds length; returns all 7 words sorted by distance.
  3. **`n = 0` vs. `n = -1`:** `n = 0` -> `pairs[:0]` returns `[]`. **Tricky quirk if `n = -1`:** `pairs[:-1]` slices everything *except the worst match*, returning `6` words! (If negative `n` shouldn't be allowed, `max(0, n)` guards it.)
  4. **`words` passed as a `set` (`suggest("cet", set(WORDS))`):** Because your code sorts `(dist, w)`, **`suggest("cet", set(WORDS))` is 100% deterministic** even though `set` iteration order is arbitrary across Python hash seeds! If you sorted on `distance` alone, passing a `set` would return **different suggestions on different runs of Python**!

### Pillar 3 — Analyse (Complexity & CRITICAL `# ANSWER` Upgrade!)

- **Time Complexity:** Let `W = len(words)`, `L = len(word)`, and `M` be the average/max word length in `words`:
  - Computing `W` distances via `levenshtein_row`: **`O(W * L * M)`**.
  - Sorting `W` tuples in `pairs.sort()`: **`O(W log W)`** tuple comparisons (up to `O(M)` on distance ties).
  - Slicing and unpacking `pairs[:n]`: **`O(n)`**.
  - **Total:** **`O(W * L * M + W log W)`**.
  - **10/10 Optimization Follow-Up (`heapq.nsmallest`):** For `W = 100,000` and `n = 3`, sorting all 100,000 entries wastes `O(W log W)` work when we only want the top `3`! Using `heapq.nsmallest(n, words, key=lambda w: (levenshtein_row(word, w), w))` maintains a size-`n` max-heap and lowers the selection step from `O(W log W)` to **`O(W log n)`** (i.e., `O(W)` when `n = 3` is constant)! (Even deeper at scale: **BK-trees** or **SymSpell** prune words without computing all `W` DP tables, e.g., immediately skipping any `w` where `abs(len(word) - len(w)) > best_threshold`, since `levenshtein(a, b) >= abs(len(a) - len(b))`!)
- **Space Complexity:** **`O(W + M)`** — `O(M)` transient row space inside each `levenshtein_row` call, plus `O(W)` to hold the `pairs` list. (Compare with `O(W + L * M)` peak or `O(W * L * M)` if tables weren't freed.)
- **CRITICAL WATCHLIST — Embedded `# ANSWER` Review ([lines 45–46](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L45-L46)):**
  - *The Question ([lines 14–17](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L14-L17)):* *"What would change if it sorted on `distance` alone, and **is that a problem with the function or only with the test?**"*
  - *What you wrote in `# ANSWER`:* You wrote that tied words wouldn't be alphabetical *"and may not match the order of the doctests."* **Careful!** That sounds like you're saying it's *only a problem with the test*, whereas the lecturer's intended point is the exact opposite: **it is a genuine problem with the function itself, NOT only with the test!**
  - **What to say in the interview if asked about this:**
    1. **Why ties dominate:** Integer edit distances are tiny (`0, 1, 2, 3`), so in a 100,000-word dictionary, dozens or hundreds of words tie at distance `1` or `2`. Ties are the *normal case*, not a corner case.
    2. **Why `sorted` / `.sort()` stability leaks accidental state:** Python's Timsort is **stable**, so sorting on `distance` alone leaves tied words in whatever order `words` happened to arrive in. Reordering lines in a dictionary file—or passing `words` as a `set` whose hash order varies per Python process (`PYTHONHASHSEED`)—causes the exact same function call on the exact same vocabulary to return **different top-3 answers**!
    3. **Verdict:** A function whose output silently depends on accidental storage order rather than a defined rule is **a flaw in the function's specification/determinism**, and doctests failing is merely the *symptom* that exposes it. (In a production spellchecker, you'd still break ties deterministically, ideally by **corpus word frequency** `(distance, -freq[w], w)` so common words beat obscure ones!)

### Likely Interview Q&A

1. **Q: If you wrote `sorted(words, key=lambda w: (levenshtein_row(word, w), w))` instead of building `pairs`, how many times would `levenshtein_row` be called—`W` times or `W log W` times?**
   - **A:** Still **exactly `W` times**! Python's `sorted(..., key=...)` internally performs the exact same Decorate-Sort-Undecorate pattern in C—calling `key(w)` once per element before running Timsort.
2. **Q: Give me a fast `O(1)` lower bound on `levenshtein(word, w)` that could skip most of a 100,000-word dictionary without running DP at all.**
   - **A:** `abs(len(word) - len(w)) <= levenshtein(word, w)` always holds, because every length difference requires at least one insertion or deletion! Once we have `n = 3` candidates with distance $\le 2$, any dictionary word whose length differs from `len(word)` by `3` or more (e.g., `"encyclopedia"` vs `"cet"`) cannot possibly make the top 3 and can be skipped in `O(1)`!

---

## 7. `E06_wrong_tool.py` — Levenshtein on Floats vs. DTW on Symbols

- **File:** [E06_wrong_tool.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py)
- **Functions:** [`levenshtein_tol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L29-L59), [`dtw_symbols`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L62-L85)
- **Difficulty Tier:** **Hard (8–10 Mark Target)**

### Your Code

```python
INF = float("inf")
INF = float("inf")


def levenshtein_tol(a, b, tol):
    D = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        D[i][0] = i
    for j in range(len(b) + 1):
        D[0][j] = j

    for i in range(1, len(a) + 1):
        for x in range(1, len(b) + 1):
            cost = 0 if abs(a[i - 1] - b[x - 1]) <= tol else 1
            D[i][x] = min(
               D[i - 1][x] + 1,
               D[i][x - 1] + 1,
               D[i - 1][x - 1] + cost 
            )
         
    return D[-1][-1]


def dtw_symbols(a, b):
    D = [[INF] * (len(b) + 1) for _ in range(len(a) + 1)]
    D[0][0] = 0.0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = cost + min(
                D[i - 1][j],
                D[i][j - 1],
                D[i - 1][j - 1]
            )
    return D[-1][-1]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)

- **2-Sentence Elevator Pitch:** `levenshtein_tol` adapts discrete Levenshtein distance to numerical series by replacing exact `==` with a thresholded `abs(a[i-1] - b[x-1]) <= tol` check, while `dtw_symbols` adapts continuous Dynamic Time Warping to strings by replacing `abs(x - y)` with a binary `0`/`1` symbol mismatch cost. Together they expose the hidden modelling assumptions baked into each DP recurrence: Levenshtein assumes **discrete 0/1 identity and penalized insertions/deletions**, whereas DTW assumes **graded numerical magnitude and free elastic repetition (stretching)**.
- **Line-by-Line & Variable Breakdown:**
  - `INF = float("inf")` (lines 25–26): IEEE-754 positive infinity (`INF + 1 == INF`, `min(INF, 0.0) == 0.0`), acting as an impassable wall along row `0` and col `0` of `dtw_symbols`. *(Tiny quirk in your file: `INF = float("inf")` is accidentally duplicated on lines 25 and 26—completely harmless at runtime, just good not to be surprised if the interviewer points at it!)*
  - **In [`levenshtein_tol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L29-L59):**
    - Identical border setup (`D[i][0] = i`, `D[0][j] = j`) and `+ 1` insertion/deletion recurrence to `E01`'s `edit_table`, except line 52 replaces `a[i - 1] == b[x - 1]` with `abs(a[i - 1] - b[x - 1]) <= tol`. *(Notice inner column variable is `x` here and `j` in `dtw_symbols`.)*
  - **In [`dtw_symbols`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L62-L85):**
    - Identical `INF` border (`D[0][0] = 0.0` only) and stretching recurrence (`cost + min(up, left, diag)`) to `E01`'s `dtw`, except line 79 replaces `abs(a[i - 1] - b[j - 1])` with `0 if a[i - 1] == b[j - 1] else 1`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)

- **Types:**
  - `levenshtein_tol(a: Sequence[float], b: Sequence[float], tol: float) -> int` (notice `D` holds `int`s and returns **`int`**!).
  - `dtw_symbols(a: Sequence[Any], b: Sequence[Any]) -> float` (notice `D[0][0] = 0.0` is a `float` and border cells are `float("inf")`, so `float + int -> float` makes `dtw_symbols` return **`float`**, e.g., `0.0` or `3.0` or `inf`!).
- **Concrete Step-by-Step Trace (`dtw_symbols("aab", "ab")` -> `0.0`):**
  - Initial `3 + 1` by `2 + 1` table `D`:
    - Row 0 (`""`): `[0.0, inf, inf]`
  - **`i = 1` (`'a'`):**
    - `j = 1` (`'a' == 'a'`, `cost = 0`): `0 + min(inf, inf, 0.0) = 0.0`
    - `j = 2` (`'a' != 'b'`, `cost = 1`): `1 + min(inf, 0.0, inf) = 1.0` -> Row 1: `[inf, 0.0, 1.0]`
  - **`i = 2` (`'a'` — repeated letter!):**
    - `j = 1` (`'a' == 'a'`, `cost = 0`): `0 + min(0.0 [up!], inf, inf) = 0.0` **(Vertical step reuses `b[0] = 'a'` for `0.0` cost!)**
    - `j = 2` (`'a' != 'b'`, `cost = 1`): `1 + min(1.0, 0.0, 0.0) = 1.0` -> Row 2: `[inf, 0.0, 1.0]`
  - **`i = 3` (`'b'`):**
    - `j = 1` (`'b' != 'a'`, `cost = 1`): `1 + min(0.0, inf, inf) = 1.0`
    - `j = 2` (`'b' == 'b'`, `cost = 0`): `0 + min(1.0, 1.0, 0.0) = 0.0` -> Row 3: `[inf, 1.0, 0.0]`
  - Returns `D[3][2]` = **`0.0`**! In general, `dtw_symbols(a, b) == 0.0` whenever `a` and `b` collapse to the exact same sequence after **run-length deduplicating consecutive identical characters** (`"bookkeeper"` $\to$ `"bokeper"`, `"baaaaanana"` $\to$ `"banana"`)!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty string in `dtw_symbols` (`dtw_symbols("", "abc")` vs. `dtw_symbols("", "")`):**
     - `dtw_symbols("", "abc")`: `D` has 1 row `[0.0, inf, inf, inf]`, outer loop `range(1, 1)` runs 0 times, returns `D[-1][-1]` = **`inf`** (`float("inf")`)! Compare with `levenshtein("", "abc") == 3`: DTW has no insertions/deletions from nothing, so an empty signal cannot warp to a non-empty signal!
     - `dtw_symbols("", "")`: `D = [[0.0]]`, outer loop runs 0 times, returns **`0.0`**.
  2. **Extreme tolerances in `levenshtein_tol`:**
     - **`tol = 0.0` on noisy floats** (every pair differs): Every `cost == 1`, so `levenshtein_tol(a, b, 0.0)` degenerates to the closed form **`max(len(a), len(b))`**! ($\min(n, m)$ diagonal substitutions of cost $1$ + $|n - m|$ insertions/deletions of cost $1$ = $\max(n, m)$.)
     - **`tol = float("inf")` (huge `tol`):** Every `cost == 0`, so every overlapping pair matches for free and `levenshtein_tol` degenerates to **`abs(len(a) - len(b))`** (pure length difference)!
     - **`tol < 0` (e.g., `tol = -0.1`):** Since `abs(...) >= 0` always, `abs(...) <= -0.1` is **always `False`**—even for identical sequences! So `levenshtein_tol([1.0, 2.0], [1.0, 2.0], -0.1)` returns **`2`** (`max(len(a), len(b))`), violating $d(a, a) = 0$!
  3. **Time-stretched series in `levenshtein_tol` (`[1.0, 2.0, 3.0]` vs. `[1.0, 1.0, 2.0, 3.0]`, `tol = 0.1`):** Returns **`1`** (must pay `+1` to insert the extra `1.0`), whereas `dtw` returns **`0.0`**!

### Pillar 3 — Analyse (Complexity & Deep Dive Into Both `# ANSWER`s)

- **Time & Space Complexity:** Both `levenshtein_tol` and `dtw_symbols` build an `(n + 1) x (m + 1)` matrix with `O(1)` work per cell: **`O(n * m)` time** and **`O(n * m)` space**. *(And yes—both could also be space-optimized to two rows in **`O(min(n, m))` space** using `E04`'s technique, since neither returns a traceback!)*
- **Embedded Question 1 (`# ANSWER 1`, [lines 88–94](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L88-L94)) — Explain in Your Own Words:**
  1. **What `levenshtein` degenerates to on measured floats:** Real sensor measurements contain continuous noise (`1.00001 != 0.99998`), so `==` is almost universally `False`, forcing `cost = 1` everywhere. When `cost = 1` everywhere, `D[n][m]` collapses mathematically to **`max(len(a), len(b))`**—completely blind to the numbers themselves!
  2. **Why `tol` does NOT truly fix it (3 distinct failures):**
     - **Step-function / cliff effect (loss of magnitude):** `tol = 0.1` scores `1.0` vs. `1.099` as `0`, and jumps discontinuously at `1.101` to score `1`—the **exact same penalty (`1`) as `1.0` vs. `999.0`**! DTW's `abs(x - y)` preserves magnitude (`0.101` vs. `998.0`).
     - **Non-transitivity:** Within-`tol` matching is not transitive (`1.0 ~ 1.08` and `1.08 ~ 1.16`, yet `1.0 !~ 1.16`), making `tol` arbitrary and brittle to tune.
     - **Wrong time-warping penalty:** Holding a note/pace longer (`[1.0, 1.0, 2.0]`) still incurs `+1` per extra sample in `levenshtein_tol`, whereas DTW charges `0.0`.
- **Embedded Question 2 (`# ANSWER 2`, [lines 96–102](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L96-L102)) — Explain in Your Own Words:**
  1. **Why `dtw_symbols("bookkeeper", "bokeper") == 0.0`:** In DTW, horizontal (`D[i][j-1]`) and vertical (`D[i-1][j]`) moves **repeat/stretch** a character (`many-to-one` alignment) and pay only `cost = (0 if a[i-1] == b[j-1] else 1)`. Matching `'oo'` to `'o'`, `'kk'` to `'k'`, and `'ee'` to `'e'` compares equal letters (`'o' == 'o'`) and therefore adds **`0`**!
  2. **Could DTW ever be used for spellchecking?** **Not for standard orthography**, where doubled vs. single letters (`"desert"` vs. `"dessert"`, `"bookkeeper"` vs. `"bokeper"`) are among the most common spelling errors and change word identity! *(Nuanced AI bonus: DTW/CTC-like alignment IS useful for normalizing expressive social-media text elongations like `"sooooo goooood"` $\to$ `"so good"` or aligning spoken phoneme frames in speech recognition—precisely where duration is continuous rather than lexical!)*

### Likely Interview Q&A

1. **Q: Without tracing a grid, tell me immediately what `levenshtein_tol([10.0, 20.0, 30.0], [10.5, 20.5, 30.5, 40.5, 50.5], 0.1)` returns and why.**
   - **A:** **`5`** (`max(3, 5)`). Every pair differs by at least `0.5 > 0.1`, so `cost == 1` for every cell. We substitute 3 pairs diagonally (`+3`) and insert 2 remaining elements (`+2`) for `3 + 2 = 5`.
2. **Q: Why does `dtw_symbols` initialize borders to `INF` with `D[0][0] = 0.0`, whereas `levenshtein_tol` initializes `D[i][0] = i` and `D[0][j] = j`?**
   - **A:** In Levenshtein, `D[i][0] = i` means you can delete the first `i` symbols before matching anything, paying `1` per deletion. In DTW, deletion does not exist—every element of `a` must align to at least one element of `b` (starting at `(1, 1)` from `(0, 0)`), so states `(i, 0)` for $i > 0$ (consuming `i` items of `a` while matching `0` items of `b`) are illegal and given cost `INF` so `min(...)` never routes through them.
3. **Q: Give an example of two *different* words where `dtw_symbols(a, b)` is NOT `0.0`, and explain why.**
   - **A:** `dtw_symbols("cat", "cut") == 1.0`, or `dtw_symbols("cat", "ct") == 1.0`! When a distinct character `'a'` is missing completely (`"cat"` vs. `"ct"`), `'a'` must align against either `'c'` or `'t'`, neither of which equals `'a'`, paying `cost = 1.0`. DTW is only blind to **consecutive repetitions** of a character that is already present (`"caat"` vs. `"cat"` -> `0.0`), not to missing distinct characters!

---

## 8. Week 7 Master Comparison Cheat Sheets (DP Strategies & Distance Metrics)

### 8.1 Dynamic Programming Implementation Strategies

| Strategy | Week 7 Example | Time | Space | Pros & Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Recursion** | [`fib_slow`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L33-L39) | `O(2^n)` ($\Theta(\varphi^n)$) | `O(n)` stack | Mirrors math definition directly; unusable past $n \approx 35$ due to exponential overlapping calls. |
| **Top-Down Memoization** | [`fib_cached`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L42-L51) (`@cache`) | `O(n)` | `O(n)` cache + stack | 1-line change (`@cache`); solves only needed subproblems; hits Python `RecursionError` at depth $\sim 1000$. |
| **Bottom-Up Full Table** | [`fib_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L13-L26), [`edit_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L54-L78) | `O(n)` / `O(n * m)` | `O(n)` / `O(n * m)` | No recursion limit; **retains full table so [`edits`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py#L96-L121) traceback works**; high memory for long sequences. |
| **Bottom-Up Rolling State** | [`fib_pair`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L29-L42), [`levenshtein_row`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py#L22-L57) | `O(n)` / `O(n * m)` | `O(1)` / `O(min(n, m))` | Minimal memory & best cache speed; **loses straightforward path traceback** (`edits`). |

### 8.2 Sequence Distance Metrics Compared

| Feature | Hamming (`hamming` / `hamming_padded`) | Levenshtein (`levenshtein` / `levenshtein_row`) | Dynamic Time Warping (`dtw`) |
| :--- | :--- | :--- | :--- |
| **Natural Data Type** | Fixed-length discrete symbols | Variable-length discrete symbols (`str`, DNA) | Variable-speed continuous time series (`float`) |
| **Alignment Type** | Rigid `1-to-1` (`a[i]` with `b[i]` only) | `1-to-1` + gaps (`insert` / `delete`, `1-to-0`) | Elastic `many-to-1` / `1-to-many` (no gaps, endpoints pinned) |
| **Element Cost** | `0` if `x == y` else `1` | `0` if `x == y` else `1` (`+1` for gap) | `abs(x - y)` on *every* matched pair |
| **Repeated Item (`"aab"` vs `"ab"`)** | Misaligns everything after (`2` padded) | Costs `1` deletion | Costs **`0.0`** (free time-stretching!) |
| **True Metric? (Triangle Inequality)** | Yes (for equal lengths / padded without `None`) | Yes | **No!** (`d("aab", "ab") = 0` with `"aab" != "ab"`, violating identity of indiscernibles & triangle inequality!) |
| **Time / Optimal Space** | `O(n)` time, `O(1)` space | `O(n * m)` time, `O(min(n, m))` space | `O(n * m)` time, `O(min(n, m))` space |
