# CT5148 Programming & Tools for AI — Master Interview Playbook

**Student:** Jack Hickey (`26257770`)  
**Module:** CT5148 (University of Galway, 2026/2027)  
**Assessment Formula:** `Python CA Grade = (Proportion of Exercises Passing Tests) × (Interview Score / 10)`

This folder contains **complete, exercise-by-exercise interview preparation guides** covering all 8 active Python weeks (`W01`–`W04` from your submitted [`assignment_01/`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01) portfolio, and `W06`–`W09` from [`W06/`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06)–[`W09/`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09)). *(Week 0 is environment setup only and Week 5 was catch-up / Assignment 1 submission.)*

---

## 1. Weekly Study Guides (Click to Open)

| Week | Study Guide | Core Topics | High-Probability "8–10 Mark" Targets |
| :--- | :--- | :--- | :--- |
| **Week 1** | **[W01_Interview_Prep.md](./W01_Interview_Prep.md)** | Loops, Slicing, Accumulators, Collatz, Caesar Cipher, Closures & `iterate`, Newton's Method, GCD | [`crack`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L54-L75), [`newton_cbrt`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L25-L49), [`gcd`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L23-L49) |
| **Week 2** | **[W02_Interview_Prep.md](./W02_Interview_Prep.md)** | Dictionaries, Tallying, Grouping, Run-Length Stats, File/JSON I/O, N-Gram Language Models | [`invert_dict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py#L14-L37), [`longest_run`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L18-L51), [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L46-L86) & [`sweep`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L89-L105) |
| **Week 3** | **[W03_Interview_Prep.md](./W03_Interview_Prep.md)** | Recursive Trees, Bill of Materials (BOM), Lazy Generators (`yield`/`yield from`), Non-Mutating JSON Updates | [`flatten`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py#L11-L36), [`apply_fn_to_list_gen`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py#L50-L74), [`part_paths`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L25-L63) & [`find_part`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py#L66-L94), [`repriced`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L44-L70) |
| **Week 4** | **[W04_Interview_Prep.md](./W04_Interview_Prep.md)** | Hash Tables (`SimpleDict` vs `PairListDict`), Collisions, Hashability, Dunder Dispatch (`__delitem__`, `__contains__`) | [`is_hashable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L15-L52), [`find_collision`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py#L25-L66), [`__delitem__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L75-L125), [`__contains__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L116-L163) |
| **Week 6** | **[W06_Interview_Prep.md](./W06_Interview_Prep.md)** | Explicit & Implicit State-Space Graphs, BFS, DFS, Priority Queues (`heapq`), Dijkstra's Shortest Path | [`hops_from`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L20-L43), [`fewest_presses`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py#L49-L68), [`time_lost`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L19-L41) & [`quickest_times`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L44-L60) |
| **Week 7** | **[W07_Interview_Prep.md](./W07_Interview_Prep.md)** | Memoization vs Tabulation vs Rolling-Row DP, Hamming, Levenshtein Edit Distance, Spellcheck, DTW | [`fib_pair`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py#L30-L47), [`levenshtein_row`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py#L22-L57), [`suggest`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L23-L42), [`levenshtein_tol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L29-L60) & [`dtw_symbols`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py#L63-L85) |
| **Week 8** | **[W08_Interview_Prep.md](./W08_Interview_Prep.md)** | NumPy Vectorisation, Broadcasting Rules, Boolean Masks, Axis Reductions, `cdist`, `argsort` Fancy Indexing, `@` Dot Product | [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43), [`is_broadcastable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py#L22-L42), [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50), [`to_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L33-L50) |
| **Week 9** | **[W09_Interview_Prep.md](./W09_Interview_Prep.md)** | `pandas` Filtering, `ddof=1` Summary Stats, `groupby`, `NaN` Imputation, `pivot_table`, One-Hot Encoding, `KNN` Estimator & Paper | [`fill_with_median`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72), [`wide`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L25-L39) & [`best_by`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L42-L50), [`encode`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L26-L52), [`label_for`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L49-L69), [`E09_paper.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py) |

---

## 2. How to Score 8–10 / 10 in the 15-Minute Interview

According to `assignments.pdf`, the interviewer starts with a **moderately easy** exercise. If you answer cleanly and concisely, they **immediately jump to harder exercises** (`W03`, `W04`, `W06`, `W07`, `W08`, `W09`) so you have the opportunity to prove **8–10 mark** mastery.

### The Rubric's Three Pillars & Exact Question Archetypes

| Pillar | What the Examiner Checks | Exact Questions from `assignments.pdf` | How to Answer for Full Marks |
| :--- | :--- | :--- | :--- |
| **1. Explain** | Do you genuinely understand every line and design choice in *your* code? | • *"What does this line do?"*<br>• *"Can you walk me through this algorithm?"*<br>• *"Why do we need this variable?"*<br>• *"Why did you give the variable that name?"* | Start with a **1-sentence goal** (*"This computes shortest unweighted hop counts from `start` using BFS"*), then explain **invariant/mechanism** (*"A FIFO `deque` visits nodes in non-decreasing distance layers, and `dist` both records hop count and prevents revisiting nodes"*). |
| **2. Trace** | Can you mentally execute your code and track types, shapes, and edge inputs? | • *"What type is this value?"*<br>• *"What does this function return?"*<br>• *"What would happen if the caller passed-in such-and-such a value?"* | Be **exact about types/shapes** (`list[str]`, `dict[str, int]`, `generator`, `1-D ndarray` of shape `(m,)` with `dtype float64`, `pd.Series`, `None` vs `0` vs `KeyError`). Trace 1–2 concrete iterations aloud when asked about a caller input. |
| **3. Analyse** | Can you derive Big-O time/space and compare data structures or algorithms? | • *"What is the time complexity of this function?"*<br>• *"Compare data structures or algorithms."* | Always **define your variables** first (*"Let `n` be `len(a)` and `m` be `len(b)`"* or *"Let `V` be vertices and `E` be edges"*), state **both Time and Auxiliary Space**, and proactively note **why** (`dict`/`set` `O(1)` average hash lookup vs `list` `O(n)` scan; `deque.popleft()` `O(1)` vs `list.pop(0)` `O(n)`). |

> [!TIP]
> **What separates a `6–7` from a `9–10`?**  
> A `6–7` candidate explains what their lines do and traces normal inputs. A `9–10` candidate **volunteers trade-offs without prompting**—for example, pointing out when their own code uses `O(V * (V + E) log V)` instead of a single-pass `O((V + E) log V)`, or explaining why throwing away the 2-D DP table in `levenshtein_row` saves `O(n * m)` memory down to `O(m)` at the cost of losing traceback (`edits`).

---

## 3. Code Audit & Watchlist (Read Before Submitting W06–W09 & Before Your Interview!)

While auditing every single `.py` file across your repository, we found several **critical hidden-test traps in Weeks 6–9** (which you can still fix before building your Week 10/12 submission zip!) plus **subtle quirks in your already-submitted Weeks 1–4 code** that you should know cold in case the interviewer asks *"What would happen if...?"* or *"What type does this return?"*

### Part A — Actionable Pre-Submission Fixes for Weeks 6–9

> [!WARNING]
> **Fix these in `W06`–`W09` before running `python selfcheck.py --zip` for your second submission!** Several pass `doctest` only by accident (e.g. `print("4.57")` looks identical to `print(4.57)`), so hidden autograder unit tests checking return types or extra decimal places would fail.

1. **[`E03_summary.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) (Week 9 — 3 issues in one file!):**
   - **[`spread`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L45-L57) (Line 57 — Return Type Bug):** Currently `return (f"{df[name].std():.2f}")`, which returns a **`str`** (`'4.57'`) instead of a **`float`** (`4.57`)! It only passes doctests because `print(...)` strips quotes. Change to `return round(df[name].std(), 2)` (or `round(float(df[name].std()), 2)`).
   - **[`column_mean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L34-L42) (Line 42 — Missing `round`):** Currently `return df[name].mean()` without rounding to 2 decimal places (`4140.0` and `44.4` happened to terminate at 1 decimal place). Change to `return round(df[name].mean(), 2)`.
   - **[`column_range`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L21-L31) (Lines 29–30 — Redundant `.max().max()`):** `df[name]` is a 1-D `Series`, so `df[name].max()` already returns a scalar (`np.float64`). Calling `.max()` a second time only avoids crashing because NumPy scalars implement a no-op `.max()` method (on string or Python-float columns it raises `AttributeError`). Change to `return df[name].min(), df[name].max()`.
2. **[`E08_estimator.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py) (Week 9 — [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86), Line 86):**
   - Docstring specifies *"as a plain float"* and line 89 notes `# accuracy is model.score with a float() round it`, but line 86 returns `model.score(X, y)` (`np.float64`). In NumPy 2.x, `repr(np.float64(1.0))` is `'np.float64(1.0)'`, which **fails the doctest** `1.0`! Wrap it as `return float(model.score(X, y))`.
3. **[`E05_missing.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L75) & [`E09_paper.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py#L79) (Week 9 — Unfilled `# ANSWER:` Placeholders):**
   - Both files still read `# ANSWER: (the QUESTION is at the top of this file)`. Complete model answers (including your exact `SEED = 26257770` numbers vs lecture `SEED = 0`) are written out in **[W09_Interview_Prep.md](./W09_Interview_Prep.md)**.
   - Also check your exported paper [`PTAI_Penguins_Jack_Hickey.pdf`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/PTAI_Penguins_Jack_Hickey.pdf): `E09_paper.py` Step 7 asks to save a copy named `paper.pdf` beside `E09_paper.py`, and note that the Overleaf template prose says *"repeated five times, giving 25 train/test splits"* whereas `E01_penguins.py` (`SPLITS, REPEATS = 5, 6`) actually ran **6 repeats = 30 splits**.
4. **[`E05_spell.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py#L45-L46) (Week 7 — `# ANSWER` Trap):**
   - The prompt asks whether sorting on `distance` alone is *"a problem with the function or only with the test?"* Your comment currently mentions *"may not match the order of the doctests"*. Be sure to clarify (both in the comment and verbally) that **it is a flaw in the function itself**: because Python's Timsort is stable and edit-distance ties are ubiquitous, omitting the secondary key `word` makes the function's output depend on the arbitrary ordering of the input vocabulary (and non-deterministic if passed a `set`!).
5. **[`E03_reachable.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py#L1) & [`E04_hops.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py#L1) (Week 6 — Docstring Header & Single-Source Optimization):**
   - Line 1 of both files currently ends with `SOLUTION.` — clean that up and make sure you can explain every line of both files fluently from scratch.
   - In [`E06_route.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L60), [`quickest_times(start)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py#L44-L60) calls `dijkstra(roads_from, start, town)` inside a dict comprehension for every `town in ROADS` (`V` full runs = `O(V * (V + E) log V)`). Know immediately if asked: removing `if node == goal:` from `dijkstra` computes *all* shortest times from `start` in **one single pass** of `O((V + E) log V)`!

---

### Part B — Interview Watchlist for Already-Submitted Weeks 1–4 (`assignment_01/`)

Because `assignment_01` is already submitted, **do not panic** about any of these—every single doctest passed (`19/19`, `20/20`, `18/18`, `8/8`), and knowing these edge cases cold turns potential "gotcha" questions into **instant 10/10 answers**:

| File & Function | Quirk in Your Submitted Code | How to Handle It Smoothly in the Interview |
| :--- | :--- | :--- |
| [`E01_newton.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py#L33-L45) (`newton_sqrt`) | Replaced the given `if x < 0: raise ValueError` + `while True:` with `while(count < 100):` | Note that `x = -1` sets `guess = 0.0` then hits `ZeroDivisionError`, `x = -4` oscillates for 100 steps and returns `-0.907`, and huge `x` (`1e70`) stops before converging after 100 halvings. |
| [`E13_caesar_crack.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L49) (`english_score`) | Checks `if char in "etaoin":` (lowercase only), though docstring says uppercase counts too | Point out immediately if asked: *"For uppercase ciphertext, I'd either write `'etaoinETAOIN'` like I did in `E04_count_vowels` (`'AEIOUaeiou'`) or check `char.lower() in 'etaoin'`."* Also note `max(score)[1]` breaks score ties alphabetically by plaintext (`(score, plaintext)` tuple comparison). |
| [`E15_gcd.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L44-L47) (`done`) | `if (b == 0): return True` has no `else: return False` | State clearly: when `b != 0`, `done` returns `None` (`NoneType`), which still works inside `while not done(x):` because `None` is falsy in Python (`not None` is `True`), though `return b == 0` is cleaner. |
| `E05`, `E12`, `E13` (W01) & `E09` (W02) | Local variables named `list = []`, `dict = {}`, and `squares = []` | If asked *"Why did you give the variable that name?"*, proactively say: *"It holds the output list/dict, though in hindsight naming it `shifts` or `results` avoids shadowing Python's built-in `list`/`dict` constructor inside the function scope."* |
| [`E09_ngram_sweep.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L72-L86) (`accuracy`) | Accumulates `tmp_his += char` each step; slices `history[-k:]` when `k = 0` | Explain two things: (1) growing an immutable `str` in a loop is theoretically `O(n^2)` (mitigated in CPython by in-place refcount-1 resizing), whereas indexing `history[:i]` avoids `tmp_his` altogether; (2) for `k = 0`, `-0 == 0` makes `history[-0:]` equal the **entire** string `history[0:]` instead of `""`! |
| [`E08_bom_json.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py#L95) (`save_bom`) | Opens `(DATA / path)` instead of `path` | Explain why the doctest passed: in `pathlib`, joining `DATA / Path("/abs/temp/file.json")` discards the left-hand path when the right-hand side is **absolute**, whereas a relative filename `"out.json"` would write inside `W03/data/out.json`. |
| [`E03_is_hashable.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L50-L56) (`is_hashable`) | Uses bare `except:` and `# ANSWER` says *"unless we update the hash everytime..."* | State two key upgrades: (1) catch `except TypeError:` specifically (note `isinstance((1, [2]), Hashable)` falsely returns `True`, so `try: hash(x)` is genuinely needed!); (2) **even if a mutable key updated its hash on mutation, `dict` would still break** because the key is still sitting physically inside its *old* bucket index! |
| [`E06_fast_contains.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L218-L234) (`# ANSWER` Q1–Q3) | `# ANSWER` Q2 didn't explain the **2x** ratio between `absent` and `present` | Nail all 3 points aloud: (1) Without `__contains__`, Python's `in` falls back to `__iter__`; `SimpleDict.__iter__` loops over all empty + non-empty buckets (`16,384` buckets at `n = 8,000`), adding bucket-iteration overhead on top of `n` key checks, making it ~3x slower than `PairListDict`'s flat list; (2) **Present keys match halfway through on average (`n / 2` checks), whereas absent keys must check all `n` items (`2x` slower)**; (3) `__contains__` hashes once (`O(1)`, `~0.29 µs`) for *both* present and absent! |

---

## 4. Master Complexity & Comparison Cheat-Sheet

Keep these complexities at your fingertips—nearly every `Analyse` question draws from one of these tables.

### A. Core Python Operations
| Data Structure / Operation | Average Time | Worst-Case Time | Notes for the Interview |
| :--- | :--- | :--- | :--- |
| `list` index `xs[i]` / `xs.append(x)` / `xs.pop()` | `O(1)` | `O(1)` (amortized) | Dynamic array over-allocates so `.append()` is amortized `O(1)`. |
| `list.pop(0)` / `list.insert(0, x)` / `x in list` | `O(n)` | `O(n)` | Shifts or scans up to `n` elements—use `collections.deque` (`popleft()` is `O(1)`) for queues and `set`/`dict` (`O(1)`) for membership! |
| Slice `xs[a:b]` / reverse `s[::-1]` | `O(b - a)` / `O(n)` | `O(n)` | Allocates a **shallow copy** of the sliced elements (`O(k)` time and space). |
| `sorted(xs)` / `xs.sort()` (Timsort) | `O(n log n)` | `O(n log n)` | `O(n)` best-case on nearly sorted data; **stable** (preserves relative order of ties); `O(n)` aux space. |
| `dict` / `set` lookup `k in d`, `d[k]`, `d[k] = v`, `del d[k]` | `O(1)` | `O(n)` | `O(n)` worst case only if all `n` keys collide into one bucket; load factor cap (`0.75` in `SimpleDict`, `2/3` in CPython) keeps buckets `O(1)`. |
| `str` membership `c in "aeiou"` | `O(1)` (fixed 5/10 chars) | `O(m)` for pattern of len `m` | Note: on `str`, `in` tests **substring** (`"ae" in "aeiou"` is `True`), whereas on `set`/`tuple` it tests **element** membership! |

### B. Algorithms Across Weeks 3–9
| Algorithm / Technique | Time Complexity | Space Complexity | Key Trade-off / When to Use |
| :--- | :--- | :--- | :--- |
| **Tree DFS Recursion** (`W03` BOM) | `O(N)` nodes visited | `O(d)` call stack (`d` = depth) | Watch out for copying sublists at every level (`flatten` is `O(N + L*d)`). Generators (`yield from`) keep working memory `O(d)` instead of `O(N)`. |
| **Breadth-First Search (BFS)** (`W06`) | `O(V + E)` (or `O(b^d)`) | `O(V)` (`seen` / `came_from` + `deque`) | Guarantees **shortest path by edge/hop count** (unweighted graphs). Fails to find fastest *weighted* route (`E04` vs `E06`). |
| **Depth-First Search (DFS)** (`W06`) | `O(V + E)` | `O(V)` | Uses LIFO stack; does **not** guarantee shortest path; can get trapped down infinite branches. |
| **Dijkstra's Algorithm** (`W06`) | `O((V + E) log V)` | `O(V + E)` (lazy heap entries) | Guarantees **minimum-weight path** when all edge weights are **`>= 0`**. Fails on negative edge weights (once popped, a node's best cost is assumed final). |
| **Fibonacci**: Naive vs `@cache` vs Table vs Pair (`W07`) | `O(2^n)` -> `O(n)` | `O(n)` stack/table -> **`O(1)`** (`fib_pair`) | `fib_slow` recomputes overlapping subproblems exponentially; `fib_pair` keeps only `(a, b)` since step `i` only depends on `i-1` and `i-2`. |
| **Levenshtein**: Full Table (`E01`) vs 1-Row (`E04`) (`W07`) | `O(n * m)` | `O(n * m)` -> **`O(m)`** (or `O(min(n, m))`) | 1-Row DP gives the exact edit distance in linear memory, **but loses the ability to traceback** the edit script (`edits(a, b)`). |
| **Hamming vs Levenshtein vs DTW** (`W07`) | `O(n)` vs `O(n * m)` vs `O(n * m)` | `O(1)` vs `O(m)`/`O(n*m)` vs `O(n*m)` | **Hamming**: 1-to-1 same-position substitutions only. **Levenshtein**: discrete symbols with insert/delete/substitute (`+1` per unmatched step). **DTW**: continuous time-series with elastic many-to-one stretching (`"bookkeeper"` vs `"bokeper"` has DTW cost `0`!). |
| **NumPy Vectorisation & Broadcasting** (`W08`) | `O(size of output)` in C | `O(1)` view for `reshape`/broadcast; `O(output)` on arithmetic | Eliminates Python bytecode & dynamic-type dispatch per element (~50–100x faster). Broadcasting stretches size-`1` axes via `stride = 0` without copying input memory. |
| **Pairwise Distances (`cdist(X, X)`)** (`W08`) | `O(n^2 * d)` | `O(n^2)` | Avoids materializing a `3-D` `(n, n, d)` difference tensor (`O(n^2 * d)` RAM) that naive broadcasting `X[:, None, :] - X[None, :, :]` would allocate! |
| **k-Nearest Neighbours (`KNN`)** (`W09`) | `fit`: `O(1)`<br>`predict`: `O(n_test * n_train * d)` | `O(n_train * d)` stored training set | "Lazy learner": memorizes `X_`, `y_` at `fit` time and computes all distances at `predict` time. Requires **feature scaling (`StandardScaler`) fit on `X_train` only** so large-unit features (`mass_g ~ 4000`) don't drown out small-unit features (`bill_mm ~ 45`). |

---

## 5. Complete Exercise Directory (All 67 Files)

### Week 1 — [Open `W01_Interview_Prep.md`](./W01_Interview_Prep.md)
* [`E01_newton.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py) — `newton_sqrt` *(Reference / Modified Given Code)*
* [`E02_first_last.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E02_first_last.py) — `first_last`
* [`E03_slices.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py) — `middle`, `last_three`
* [`E04_count_vowels.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E04_count_vowels.py) — `count_vowels`
* [`E05_squares.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E05_squares.py) — `squares`
* [`E06_cumsum.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E06_cumsum.py) — `cumsum`
* [`E07_product.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E07_product.py) — `product`
* [`E08_palindrome.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E08_palindrome.py) — `is_palindrome`
* [`E09_hailstones.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py) — `hailstones`, `longest_hailstone`
* [`E10_hailstones_iterate.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py) — `hailstone_step`, `reaches_one`
* [`E11_rotate.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E11_rotate.py) — `rotate`
* [`E12_caesar_shifts.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py) — `all_shifts`
* [`E13_caesar_crack.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py) — `english_score`, `crack`
* [`E14_newton_cbrt.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py) — `newton_cbrt`
* [`E15_gcd.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py) — `gcd`

### Week 2 — [Open `W02_Interview_Prep.md`](./W02_Interview_Prep.md)
* [`E01_oracle.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py) & [`oracle_keys.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/oracle_keys.py) — `predict_ngram`, `update`, `load`, `save` *(Given Code)*
* [`E02_get_or.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E02_get_or.py) — `get_or`
* [`E03_invert_dict.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py) — `invert_dict`
* [`E04_merge.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E04_merge.py) — `merge`
* [`E05_tally.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py) — `tally`, `tally_counter`
* [`E06_group_by.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py) — `group_by_first_letter`
* [`E07_key_stats.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py) — `longest_run`, `switch_rate`
* [`E08_save_history.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py) — `history_path`, `save_history`, `load_histories`, `total_keys`
* [`E09_ngram_sweep.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py) — `accuracy`, `sweep`

### Week 3 — [Open `W03_Interview_Prep.md`](./W03_Interview_Prep.md)
* [`E01_bom.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E01_bom.py) — `load_bom`, `everything`, `is_steel`, `unit_mass`, `parts` *(Given Code)*
* [`E02_sort_by_key.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E02_sort_by_key.py) — `sort_by_mass`, `heaviest`
* [`E03_nested_sum.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E03_nested_sum.py) — `nested_sum`
* [`E04_flatten.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E04_flatten.py) — `flatten`
* [`E05_count_parts.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E05_count_parts.py) — `count_parts`, `deepest`
* [`E06_apply_fn.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E06_apply_fn.py) — `apply_fn_to_list`, `apply_fn_to_list_gen`
* [`E07_part_paths.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E07_part_paths.py) — `part_paths`, `find_part`
* [`E08_bom_json.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W03/E08_bom_json.py) — `load_bom`, `repriced`, `save_bom`

### Week 4 — [Open `W04_Interview_Prep.md`](./W04_Interview_Prep.md)
* [`E01_SimpleDict.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py) — `PairListDict`, `SimpleDict` *(Given Code)*
* [`E02_bucket_index.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E02_bucket_index.py) — `bucket_index`
* [`E03_is_hashable.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py) — `is_hashable`
* [`E04_string_collision.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py) — `find_collision`
* [`E05_delitem.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py) — `SimpleDict.__delitem__`
* [`E06_fast_contains.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py) — `SimpleDict.__contains__`

### Week 6 — [Open `W06_Interview_Prep.md`](./W06_Interview_Prep.md)
* [`E01_river.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E01_river.py) — `bfs`, `dfs`, `PriorityQueue`, `dijkstra`, `roads_from`, `road_time` *(Given Code)*
* [`E02_neighbours.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E02_neighbours.py) — `neighbours`, `is_edge`, `degree`
* [`E03_reachable.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E03_reachable.py) — `reachable`, `connected`
* [`E04_hops.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E04_hops.py) — `hops_from`, `farthest_hops`
* [`E05_calculator.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E05_calculator.py) — `calc_successors`, `presses`, `fewest_presses`
* [`E06_route.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W06/W06/E06_route.py) — `time_lost`, `quickest_times`

### Week 7 — [Open `W07_Interview_Prep.md`](./W07_Interview_Prep.md)
* [`E01_editdist.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E01_editdist.py) — `fib_slow`, `fib_cached`, `edit_table`, `levenshtein`, `edits`, `dtw` *(Given Code)*
* [`E02_hamming.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E02_hamming.py) — `hamming`, `hamming_padded`
* [`E03_fib_table.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E03_fib_table.py) — `fib_table`, `fib_pair`
* [`E04_one_row.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E04_one_row.py) — `levenshtein_row`
* [`E05_spell.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E05_spell.py) — `suggest`
* [`E06_wrong_tool.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W07/W07/E06_wrong_tool.py) — `levenshtein_tol`, `dtw_symbols`

### Week 8 — [Open `W08_Interview_Prep.md`](./W08_Interview_Prep.md)
* [`E01_photos.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py) & [`prep_data.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/prep_data.py) — `load`, `build_matrix`, `as_proportions`, `nearest` *(Given Code)*
* [`E02_vectorise.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py) — `softplus`
* [`E03_broadcast.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py) — `combine`, `times_table`
* [`E04_axis_masks.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py) — `count_above`, `values_above`, `column_means`, `row_maxes`
* [`E05_broadcastable.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py) — `is_broadcastable`
* [`E06_heatmap.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py) — `distance_matrix`
* [`E07_brightness.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py) — `brightness`, `darkest_first`
* [`E08_grayscale.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py) — `to_gray`

### Week 9 — [Open `W09_Interview_Prep.md`](./W09_Interview_Prep.md)
* [`E01_penguins.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py) — `KNN`, `clean`, `protocol`, `score_cell` *(Given Code with `SEED = 26257770`)*
* [`E02_select.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py) — `column_list`, `heavier_than`
* [`E03_summary.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) — `column_range`, `column_mean`, `spread`
* [`E04_groups.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py) — `group_sizes`, `group_means`
* [`E05_missing.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py) — `count_missing`, `drop_missing`, `fill_with_median`
* [`E06_pivot.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py) — `wide`, `best_by`
* [`E07_dummies.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py) — `encode`, `n_new_columns`
* [`E08_estimator.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py) — `train`, `label_for`, `accuracy`
* [`E09_paper.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py) — Reproducible Penguins Paper (`SEED = 26257770`)

