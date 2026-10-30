# Week 2 Interview Preparation Guide — Dictionaries, `Counter`, `defaultdict`, File I/O & N-Gram Models

⬅️ **Back to:** [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Week 2 Core Topics:** Hash-table lookups (`dict`), key membership vs falsy values, dictionary comprehensions & bijective inversion, aliasing vs shallow copying, frequency counting (`collections.Counter`), grouping (`collections.defaultdict`), sequence randomness statistics, `pathlib.Path` & persistent file I/O (`with open`), and online N-gram language-model evaluation & hyperparameter sweeps (Aaronson's Oracle).

---

## Table of Contents

1. [Summary Table of Week 2 Exercises](#summary-table-of-week-2-exercises)
2. [Watchlist Before You Walk In (Your Code's Quirk Audit)](#watchlist-before-you-walk-in-your-codes-quirk-audit)
3. [Reference Context — `E01_oracle.py` & `oracle_keys.py`](#reference-context--e01_oraclepy--oracle_keyspy)
4. [`E02_get_or.py` — `get_or`](#e02_get_orpy--safe-dictionary-lookup)
5. [`E03_invert_dict.py` — `invert_dict`](#e03_invert_dictpy--dict-comprehensions--key-uniqueness)
6. [`E04_merge.py` — `merge`](#e04_mergepy--non-mutating-dictionary-merge)
7. [`E05_tally.py` — `tally`, `tally_counter`](#e05_tallypy--counting-by-hand-vs-counter)
8. [`E06_group_by.py` — `group_by_first_letter`](#e06_group_bypy--grouping-with-defaultdict)
9. [`E07_key_stats.py` — `longest_run`, `switch_rate`](#e07_key_statspy--measuring-non-randomness)
10. [`E08_save_history.py` — `history_path`, `save_history`, `load_histories`, `total_keys`](#e08_save_historypy--persistent-session-storage-with-pathlib)
11. [`E09_ngram_sweep.py` — `accuracy`, `sweep`](#e09_ngram_sweeppy--offline-n-gram-hyperparameter-sweep)

---

## Summary Table of Week 2 Exercises

*Input size variables:* `n = len(d)` / `len(xs)` / `len(history)`, `m = len(d2)` (or session length), `u` = number of unique keys (`u <= n`), `S` = number of saved sessions, `N` = total characters across all sessions, `k` = context length ($N_{\text{ngram}} = k + 1$).

| Exercise | Function(s) | Difficulty Tier | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| [E01_oracle.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py) & [oracle_keys.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/oracle_keys.py) | [`predict_ngram`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L73-L97), [`update`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L100-L112), [`save`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L117-L121), [`load`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L124-L140), [`play`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L149-L163) | Reference *(Given)* | `O(K)` per keypress (`O(u log u)` `save`) | `O(K * min(n, 2^K))` |
| [E02_get_or.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E02_get_or.py) | [`get_or`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E02_get_or.py#L11-L35) | `Warm-up` | `O(1)` average | `O(1)` |
| [E03_invert_dict.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py) | [`invert_dict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py#L14-L35) | `Warm-up` | `O(n)` average | `O(n)` |
| [E04_merge.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E04_merge.py) | [`merge`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E04_merge.py#L11-L38) | `Warm-up` | `O(n + m)` average | `O(n + m)` |
| [E05_tally.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py) | [`tally`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py#L13-L28), [`tally_counter`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py#L31-L51) | `Warm-up` | `O(n)` average | `O(u)` |
| [E06_group_by.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py) | [`group_by_first_letter`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py#L13-L30) | `Moderate` | `O(n)` average *(assuming short words)* | `O(n)` |
| [E07_key_stats.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py) | [`longest_run`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L17-L51), [`switch_rate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L54-L85) | `Moderate` | `O(n)` | `O(1)` |
| [E08_save_history.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py) | [`history_path`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L26-L37), [`save_history`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L40-L54), [`load_histories`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L57-L81), [`total_keys`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L84-L96) | `Moderate` | `O(1)` · `O(m)` · `O(N + S)` · `O(N + S)` | `O(1)` · `O(m)` · `O(N + S)` · `O(N + S)` |
| [E09_ngram_sweep.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py) | [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L40-L83), [`sweep`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L86-L95) | `Hard (8–10 Mark Target)` | `O(n^2 + n * k)` *(conceptual `+=`)* / `O(n * k)` *(CPython)* | `O(n + k * min(n, 2^k))` |

---

## Watchlist Before You Walk In (Your Code's Quirk Audit)

1. **`tmp_his += char` inside the loop in [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L82) (`E09_ngram_sweep.py`):** Strings in Python are immutable! Appending to `tmp_his` `n` times conceptually costs `O(n^2)` time and `O(n)` space (even though CPython often optimizes refcount-1 `+=` in place). Know how to eliminate `tmp_his` completely using `enumerate(history)` and slicing `history[max(0, i - k):i]`! *(Note: your scratch file [short_prog.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/short_prog.py) is still in `assignment_01/W02/`, where you tested `his += str(i); s += his`!)*
2. **Shadowing built-in `dict` in [`sweep`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L92) (`E09_ngram_sweep.py`):** `dict = {}` shadows Python's built-in `dict` type inside `sweep`. Mention proactively that you'd rename it `results` or write `{k: accuracy(history, k) for k in ks}`.
3. **The `k = 0` Slicing Trap (`history[-0:]`) in [`E09_ngram_sweep.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L30):** In Python, `-0 == 0`, so `history[-0:]` is `history[0:]` (the **entire** string, NOT `""`!). Calling `accuracy("dddd", 0)` returns `0.0` because every step has a unique full-history context!
4. **Unbound class call `Path.exists(p)` in [`load_histories`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L76) (`E08_save_history.py`):** Works because `p` is passed as `self` to `Path.exists`, though idiomatic Python writes `p.exists()`. Also in [`total_keys`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L96), loop variable `sessions` represents a *single* session string.
5. **Empty-word `IndexError` in [`group_by_first_letter`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py#L29) (`E06_group_by.py`):** Passing `[""]` triggers `IndexError` at `word[0]`.
6. **Float vs Percentage in [`E07_key_stats.py`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L88) `# ANSWER`:** You wrote `50%`; in the interview say **`0.5`** (since `switch_rate` returns a float in `[0.0, 1.0]`, i.e. 50%).

---

## Reference Context — `E01_oracle.py` & `oracle_keys.py`

- **Files:** [E01_oracle.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py) & [oracle_keys.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/oracle_keys.py) *(plus scratch file [short_prog.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/short_prog.py))*

### Architecture You Must Understand (Powers `E07`, `E08`, and `E09`)
1. **Aaronson's Oracle & N-gram Structure ([`predict_ngram`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L73-L97), [`update`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L100-L112)):**
   - The player types `"f"` or `"d"` trying to be unpredictable.
   - An **N-gram** of length $N = K + 1$ consists of a **context** of length $K$ (`context = history[-K:]`, default `K = 4` for 5-grams) concatenated with the **next key** (`"f"` or `"d"`).
   - `counts` is a `collections.Counter` mapping strings like `"fdfdf"` $\to 7$ and `"fdfdd"` $\to 2$. Because `Counter` returns `0` for unseen keys without raising `KeyError`, `predict_ngram` simply compares `counts[context + "f"]` vs `counts[context + "d"]` (breaking ties with `random.choice("fd")`).
   - *Warm-up detail:* When `len(history) < K` (the first `K` keypresses), `history[-K:]` clamps cleanly to all of `history`, so `counts` temporarily records shorter 1-grams through `K`-grams (`"f"`, `"fd"`, `"fdf"`, `"fdfd"`)!
2. **Uniform Model Interface & Polymorphic [`play`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L149-L163):**
   - [`predict_no_information`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L43-L49), [`predict_no_3_repeats`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L52-L70), and [`predict_ngram`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L73-L97) all accept `(counts, history)`, stored in the dispatch dictionary [`MODELS`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L211-L213) so `play(predict, counts)` can call any strategy without `if/elif` branching.
   - **Honest Online Loop Order:** `guess = predict(...)` $\to$ `key = read_key()` $\to$ score `guess == key` $\to$ `update(counts, history, key)` $\to$ `history = history + key`. Predicting *before* updating prevents data leakage!
3. **Model Persistence ([`save`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L117-L121) / [`load`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E01_oracle.py#L124-L140)) vs Raw Data Persistence (`E08`):**
   - `E01` serializes `counts` as plain-text space-separated lines `"{ngram} {count}\n"` (sorted alphabetically).
   - **Key insight for `E08` & `E09`:** From saved `counts` (a 5-gram model), you **cannot** reconstruct the original keypress sequence or test 3-grams or 8-grams! Saving the **raw data** (`history` in `E08`) is strictly more informative because any model for any `k` can be re-trained from it (`E09`).
4. **How [`read_key`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/oracle_keys.py#L13-L40) Works (`oracle_keys.py`):**
   - Switches Unix terminals into `cbreak` mode (`tty.setcbreak`) inside a `try ... finally` block so a single keypress is read immediately (`sys.stdin.read(1)`) without waiting for Enter, while guaranteeing `termios.tcsetattr` restores normal terminal mode even on `Ctrl-C`.
   - *Note on [short_prog.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/short_prog.py):* If the interviewer asks what `short_prog.py` is, it's your 10-line scratch test printing `"112123123412345123456"` while experimenting with `his += ...` for `E09`.

---

## `E02_get_or.py` — Safe Dictionary Lookup

- **File:** [E02_get_or.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E02_get_or.py)
- **Function:** [`get_or(d, key, default)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E02_get_or.py#L11-L35)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def get_or(d, key, default):
    if key in d:
        return d[key]
    return default
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`get_or` implements Python's built-in `d.get(key, default)` from scratch by testing whether `key` is a key in dictionary `d` using the `in` operator. If found, it returns the associated value `d[key]`; otherwise it returns `default` instead of letting `d[key]` raise a `KeyError`."
- **Line-by-Line & Variable Breakdown:**
  - `if key in d:` (line 33): Checks hash-table **key** membership (never values!).
  - `return d[key]` (line 34): Safe subscript because line 33 just confirmed `key` is present; returns `d[key]` *even if `d[key]` is falsy* (`0`, `""`, `False`, `None`, `[]`).
  - `return default` (line 35): Fallback value returned when `key` is absent.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameters: `d: Mapping[K, V]`, `key: Hashable`, `default: D`.
  - Return value: `V | D`.
- **Concrete Step-by-Step Trace (`get_or({"ann": 0}, "ann", 99)` — The Falsy-Value Doctest!):**
  1. Evaluates `"ann" in {"ann": 0}` -> `True` (`"ann"` is a present key).
  2. Evaluates `d["ann"]` -> returns **`0`** (`int`), ignoring `default = 99`.
  - *Why `d.get(key) or default` would FAIL here:* `0 or 99` evaluates truthiness of `0` (`False`) and wrongly returns `99`!
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Key matches a *value* instead of a key (`get_or({"ann": 7}, 7, -1)`):** `7 in d` checks keys only -> `False` -> returns `-1`.
  - **Unhashable key (`get_or({"a": 1}, [1, 2], 0)`):** Lists cannot be hashed! `if key in d:` immediately raises **`TypeError: unhashable type: 'list'`**.
  - **Empty dict (`get_or({}, "ann", None)`):** Returns `None`.
  - **Equivalent keys with equal hashes (`get_or({1: "one"}, True, "missing")`):** In Python `True == 1` and `hash(True) == hash(1)`, so `True in {1: "one"}` is **`True`** and returns `'one'`!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(1)` average** (`O(n)` worst-case only under adversarial hash collisions, which Python mitigates via SipHash randomization).
  - *Anti-pattern warning:* Writing `if key in list(d.keys()):` converts an `O(1)` hash lookup into an **`O(n)`** linear list copy and scan! (`key in d` and `key in d.keys()` are both `O(1)`, with `key in d` faster by avoiding method lookup.)
- **Space Complexity:** **`O(1)`**.
- **Alternative Comparison — LBYL vs EAFP:**
  - **LBYL (*Look Before You Leap*, yours):** `if key in d: return d[key]` — hashes `key` **twice** when `key` is present (once for `in`, once for `d[key]`), and **once** when missing.
  - **EAFP (*Easier to Ask Forgiveness than Permission*):** `try: return d[key] except KeyError: return default` — hashes `key` **only once** on hits (faster when hits are >95% of calls), but much slower on misses due to exception-stack unwinding overhead.
  - **Built-in `d.get(key, default)`:** Implemented in C, hashes `key` **only once** in both hit and miss cases with zero exception overhead!

### Likely Interview Q&A
1. **Q: Why does the docstring specifically test `get_or({"ann": 0}, "ann", 99)`?**  
   **A:** To catch a classic bug where someone writes `val = d.get(key); return val if val else default` (or `d.get(key) or default`). Because `0`, `""`, `[]`, and `False` are falsy, truthiness checks confuse a legitimate falsy value with a missing key!
2. **Q: Why is `key in d` `O(1)` on a dictionary when `x in L` is `O(n)` on a list?**  
   **A:** A Python `dict` is a hash table: it computes `hash(key)` to jump directly to a bucket index in constant expected time, whereas a `list` has no hash index and must scan element-by-element from index `0`.

---

## `E03_invert_dict.py` — Dict Comprehensions & Key Uniqueness

- **File:** [E03_invert_dict.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py)
- **Function:** [`invert_dict(d)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E03_invert_dict.py#L14-L35)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def invert_dict(d):
    dict_inverted = {value: key for key, value in d.items()}
    return dict_inverted


# The last doctest loses a pair because dictionaries cannot have duplicate keys. 
# In the example `{"a": 1, "b": 1}` both "a" and "b" have the same value of 1. 
# When inverting the dictionary the key 1 can only map to one value so it ends up mapping to 'b', which is the last key processed.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`invert_dict` uses a dictionary comprehension over `d.items()` to build a new dictionary where every `(key, value)` pair becomes `(value, key)`. When multiple keys share the same value, later entries overwrite earlier ones in insertion order because dictionary keys must be unique."
- **Line-by-Line & Variable Breakdown:**
  - `d.items()` (line 34): Returns a dynamic dictionary view yielding `(key, value)` 2-tuples in insertion order (`O(1)` memory view, not a materialized list!).
  - `{value: key for key, value in d.items()}` (line 34): Unpacks each tuple into `key, value` and inserts `dict_inverted[value] = key` into a brand-new dictionary, leaving `d` untouched.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `d`: `dict[K, V]` *(requires `V` to be `Hashable`!)*.
  - Return value: `dict[V, K]`.
- **Concrete Step-by-Step Trace (`invert_dict({"a": 1, "b": 1})`):**
  1. Comprehension starts with `{}`.
  2. First pair `("a", 1)`: sets `res[1] = 'a'` -> `{1: 'a'}`.
  3. Second pair `("b", 1)`: key `1` already exists! Overwrites `res[1] = 'b'` -> `{1: 'b'}`.
  4. Returns `{1: 'b'}` (`len` dropped from `2` to `1`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Mutable / Unhashable values (`invert_dict({"a": [1, 2]})`):** Dictionary *values* can be anything, **but dictionary *keys* must be hashable (immutable)**! Swapping `[1, 2]` into key position raises **`TypeError: unhashable type: 'list'`**.
  - **Equal-but-distinct values (`invert_dict({"a": 1, "b": True})` — 10/10 Python Trivia!):** Because `1 == True` and `hash(1) == hash(True)`, Python treats `True` as colliding with existing key `1`! Python **keeps the original key `1`** and **updates its value to `'b'`**, returning **`{1: 'b'}`**!
  - **Empty dictionary `invert_dict({})`:** Returns `{}`.

### Pillar 3 — Analyse (Complexity, Trade-offs & `# ANSWER`)
- **Time Complexity:** **`O(n)` average** where `n = len(d)` (`n` hash insertions into the new dict).
- **Space Complexity:** **`O(u)`** (bounded by **`O(n)`**), where `u <= n` is the number of distinct values in `d`.
- **Embedded File Question (`# ANSWER`, lines 9–10 & 38–40):**
  > **QUESTION:** *the last doctest below (`invert_dict({"a": 1, "b": 1})` -> `{1: 'b'}`) loses a pair. Why?*
  - **Your Comment (`#L38-L40`):** Spot-on! Dicts cannot have duplicate keys; since Python 3.7+ guarantees insertion-order iteration, `"b"` is processed last and overwrites `'a'`.
  - **Follow-up Upgrade (How to Invert *Without* Losing Data!):** Ask yourself what the lecturer will ask next: *"How would you write `invert_dict` so no keys are lost when values collide?"*
    - **Answer:** Map each value to a **list of keys** using `defaultdict(list)` (connecting directly to `E06_group_by.py`!):
      ```python
      inv = defaultdict(list)
      for k, v in d.items():
          inv[v].append(k)
      return dict(inv)  # {1: ['a', 'b']}
      ```
    - Mathematically, `{v: k ...}` is lossless if and only if `d` represents an **injective (one-to-one)** function (`len(set(d.values())) == len(d)`).

### Likely Interview Q&A
1. **Q: Can *every* Python dictionary be passed to `invert_dict` without raising an exception?**  
   **A:** No! If any **value** in `d` is unhashable—such as a `list`, `set`, or nested `dict`—making it a key in `dict_inverted` immediately raises `TypeError: unhashable type`. A tuple of immutables `(1, 2)` works, whereas a tuple containing a list `([1], 2)` also raises `TypeError`.
2. **Q: How could you check in one line whether `invert_dict(d)` lost any pairs?**  
   **A:** Check `len(invert_dict(d)) == len(d)`! Since every collision reduces the output key count by 1, equal lengths prove all original values were unique.

---

## `E04_merge.py` — Non-Mutating Dictionary Merge

- **File:** [E04_merge.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E04_merge.py)
- **Function:** [`merge(d1, d2)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E04_merge.py#L11-L38)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def merge(d1, d2):
    merged_dict = {}
    for k in d1:
        merged_dict[k] = d1[k]
    for k in d2:
        merged_dict[k] = d2[k]
    return merged_dict
#     merged_dict = {**d1, **d2} 
#     return merged_dict
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`merge` allocates a brand-new empty dictionary `merged_dict`, copies every key-value pair from `d1`, and then copies every key-value pair from `d2` on top of it. Writing `d2` second ensures `d2` wins on any clashing keys while leaving both input dictionaries `d1` and `d2` completely unmutated."
- **Line-by-Line & Variable Breakdown:**
  - `merged_dict = {}` (line 33): Allocates a fresh dictionary object in memory. **Why NOT `merged_dict = d1`?** Because `merged_dict = d1` only creates an **alias** (a second reference pointing to the *same* dictionary), so writing `d2`'s keys into `merged_dict` would mutate `d1` in place and fail the doctest `first == {'a': 1, 'b': 2}`!
  - `for k in d1: merged_dict[k] = d1[k]` (lines 34–35): Iterating `for k in d1` yields keys in insertion order; copies all pairs from `d1`.
  - `for k in d2: merged_dict[k] = d2[k]` (lines 36–37): Inserts new keys from `d2` and overwrites any key already copied from `d1`.
  - `# merged_dict = {**d1, **d2}` (line 39): Your commented-out unpacking one-liner — completely valid and equivalent!

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameters: `d1: dict[K1, V1]`, `d2: dict[K2, V2]`.
  - Return value: `dict[K1 | K2, V1 | V2]`.
- **Concrete Step-by-Step Trace (`merge({"a": 1, "b": 2}, {"a": 17, "c": 3})`):**
  1. `merged_dict = {}`.
  2. Loop 1 (`d1`): sets `'a': 1`, then `'b': 2` -> `{'a': 1, 'b': 2}`.
  3. Loop 2 (`d2`): overwrites `'a': 17`, adds `'c': 3` -> `{'a': 17, 'b': 2, 'c': 3}` *(note `'a'` keeps its original insertion slot from `d1` at the front!)*.
  4. `d1` is still `{'a': 1, 'b': 2}`; `d2` is still `{'a': 17, 'c': 3}`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Both empty `merge({}, {})`:** Returns a new `{}` (`is not d1` and `is not d2`).
  - **Same dict passed twice `merge(d1, d1)`:** Returns a shallow copy of `d1` (`merge(d1, d1) == d1` is `True`, `merge(d1, d1) is d1` is `False`).
  - **Nested mutable values (`d1 = {"x": [1, 2]}; m = merge(d1, {}); m["x"].append(99)`):** **Shallow-copy trap!** `merged_dict["x"]` points to the *same inner list* `[1, 2]` as `d1["x"]`! Rebinding `m["x"] = [5]` doesn't affect `d1`, *but* mutating `m["x"].append(99)` **does** mutate `d1["x"]` unless `copy.deepcopy` is used.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n + m)` average** where `n = len(d1)` and `m = len(d2)` (`n` hash lookups/writes + `m` hash lookups/writes). *(Minor improvement: `for k, v in d1.items(): merged_dict[k] = v` avoids the extra `d1[k]` lookup!)*
- **Space Complexity:** **`O(n + m)`** (specifically `O(u)` where `u <= n + m` is the number of distinct keys across `d1` and `d2`).
- **Alternative Idioms Comparison (Great 8–10 Mark Fluency!):**
  1. **`d1 | d2`** (Python 3.9+ dict union operator, PEP 584): Cleanest modern syntax (`d1 |= d2` is the in-place version).
  2. **`{**d1, **d2}`** (Python 3.5+ dict unpacking, your line 39 comment!): Runs in C, works with **any** hashable key type (`int`, `tuple`, `str`). *(Watchout: `dict(d1, **d2)` is a trap because `**kwargs` in a function call requires `d2`'s keys to be `str`, crashing with `TypeError` on `{1: 'a'}`!)*
  3. **`out = d1.copy(); out.update(d2)`**: Classic two-liner.

### Likely Interview Q&A
1. **Q: Why did the doctest assign `first` and `second` to variables and print them *after* calling `merge(first, second)`?**  
   **A:** To test for **unintended side effects (in-place mutation)**! If `merge` had written `d1.update(d2); return d1`, `merge(first, second)` would return the right output, *but* `first` would be corrupted to `{'a': 17, 'b': 2, 'c': 3}`.
2. **Q: Is there any difference between `{**d1, **d2}` (your comment on line 39) and `dict(d1, **d2)`?**  
   **A:** Yes! `{**d1, **d2}` unpacks inside a dict literal and accepts any hashable keys (like integers or tuples), whereas `dict(d1, **d2)` passes `d2` as keyword arguments, raising `TypeError: keywords must be strings` if `d2` has integer keys!

---

## `E05_tally.py` — Counting by Hand vs `Counter`

- **File:** [E05_tally.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py)
- **Functions:** [`tally(xs)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py#L13-L28), [`tally_counter(xs)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E05_tally.py#L31-L51)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
from collections import Counter

def tally(xs):
    counts = {}
    for item in xs:
        counts[item] = counts.get(item, 0) + 1
    return counts

def tally_counter(xs):
    return Counter(xs)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`tally` counts item frequencies in a single pass over `xs` using a plain dictionary and `counts.get(item, 0) + 1` to safely initialize unseen items from `0` to `1`. `tally_counter` delegates the exact same job to `collections.Counter(xs)`, returning a specialized `dict` subclass tailored for multiset counting."
- **Line-by-Line & Variable Breakdown:**
  - `counts = {}` (line 25): Plain `dict` accumulator mapping `item -> frequency`.
  - `counts[item] = counts.get(item, 0) + 1` (line 27): Directly applies the `get_or` pattern from `E02`! Avoids the 4-line `if item in counts: ... else: ...` boilerplate in the [official solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_02/W02_Solutions/E05_tally.py#L27-L30).
  - `return Counter(xs)` (line 51): `Counter` iterates `xs` in C (`_count_elements`) and populates counts automatically.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `xs: Iterable[T]` (where `T` is `Hashable`).
  - `tally(xs) -> dict[T, int]`; `tally_counter(xs) -> Counter[T]` *(note: `isinstance(Counter(xs), dict)` is **`True`** because `Counter` subclasses `dict`!)*.
- **Concrete Step-by-Step Trace (`tally("aba")`):**
  - Init: `counts = {}`.
  - `item = 'a'`: `counts.get('a', 0)` is `0` -> `counts['a'] = 1` -> `{'a': 1}`.
  - `item = 'b'`: `counts.get('b', 0)` is `0` -> `counts['b'] = 1` -> `{'a': 1, 'b': 1}`.
  - `item = 'a'`: `counts.get('a', 0)` is `1` -> `counts['a'] = 2` -> `{'a': 2, 'b': 1}`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Missing-key lookup after return (`c["z"]`):** `tally("banana")["z"]` raises **`KeyError: 'z'`**, whereas `tally_counter("banana")["z"]` returns **`0`** (via `Counter.__missing__`) **without** inserting `'z'` into the `Counter`!
  - **Unhashable item `tally([[1], [2]])`:** Both `tally` and `tally_counter` raise **`TypeError: unhashable type: 'list'`**.
  - **Generator / single-pass iterator `tally(x * x for x in range(3))`:** Works cleanly because `xs` is walked **only once**!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)` average** where `n` is the number of items in `xs`. Each step does an `O(1)` hash lookup and `O(1)` hash write.
  - **Contrast with the `O(n^2)` Trap:** Writing `{x: xs.count(x) for x in xs}` calls `xs.count(x)` (`O(n)` full scan!) for *each* of the `n` elements = **`O(n^2)`** time (e.g., 100,000 items takes 10 billion comparisons instead of 100,000, and crashes on generators since generators have no `.count()`!).
- **Space Complexity:** **`O(u)`** where `u <= n` is the number of **unique** items in `xs` (e.g., for `E01_oracle`'s 1,000,000 `"f"`/`"d"` keypresses, `tally(history)` uses `u = 2` entries = **`O(1)`** space!).
- **Comparison — Plain `dict` vs `defaultdict(int)` vs `Counter`:**
  | Feature | Plain `dict` (`tally`) | `defaultdict(int)` | `collections.Counter` |
  | :--- | :--- | :--- | :--- |
  | Missing key `d["z"]` | Raises `KeyError` | Returns `0` **AND mutates `d`** (`'z': 0` added!) | Returns `0` **without mutating `d`**! |
  | Print (`repr`) order | Insertion order | Insertion order | Descending frequency order |
  | Top-$k$ helper | Manual `sorted(..., key=...)` | Manual `sorted(...)` | Built-in `c.most_common(k)` (`O(u log k)` heap!) |

### Likely Interview Q&A
1. **Q: Wait — when `tally_counter("banana")["z"]` returns `0`, does `"z"` become a key inside the `Counter`?**  
   **A:** No! Unlike `defaultdict(int)`, whose `__missing__` inserts `d["z"] = 0` on a read, `Counter.__missing__` simply returns `0` without modifying the dictionary (`"z" in c` remains `False`). That's why `E01_oracle.py` can check `counts[context + "f"]` safely without polluting `counts` with zero-count n-grams!
2. **Q: Why does `Counter("banana")` print `Counter({'a': 3, 'n': 2, 'b': 1})` while `tally("banana")` prints `{'b': 1, 'a': 3, 'n': 2}`?**  
   **A:** Internally both store keys in insertion order (`'b', 'a', 'n'`), so `list(Counter("banana"))` is still `['b', 'a', 'n']`; however, `Counter.__repr__` sorts items by `most_common()` specifically when formatting itself as a string.

---

## `E06_group_by.py` — Grouping with `defaultdict`

- **File:** [E06_group_by.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py)
- **Function:** [`group_by_first_letter(words)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E06_group_by.py#L13-L30)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
from collections import defaultdict

def group_by_first_letter(words):
    d = defaultdict(list)
    for word in words:
        d[word[0]].append(word)
    return dict(d)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`group_by_first_letter` buckets words by their initial character `word[0]` in a single pass using `defaultdict(list)`, which automatically creates a fresh empty list the first time each letter is seen. Converting `d` back with `dict(d)` at the end returns a clean standard dictionary while preserving both letter-discovery order and within-bucket word order."
- **Line-by-Line & Variable Breakdown:**
  - `d = defaultdict(list)` (line 27): Passes the `list` **type/factory callable** (NOT `list()`, which would pass `[]` and raise `TypeError: first argument must be callable or None`!). Whenever `d[k]` misses, `defaultdict` calls `list()` to create a brand-new `[]` for key `k`.
  - `d[word[0]].append(word)` (line 29): Extracts the first character `word[0]`, retrieves (or auto-creates) that bucket's list, and appends `word` in amortized `O(1)` time.
  - `return dict(d)` (line 30): Converts the `defaultdict` into an ordinary `dict` (shallow-copying the top-level key-to-list mapping).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `words`: `Iterable[str]` *(non-empty strings)*.
  - Local `d`: `defaultdict[str, list[str]]`.
  - Return value: `dict[str, list[str]]`.
- **Concrete Step-by-Step Trace (`group_by_first_letter(["apple", "avocado", "banana"])`):**
  1. `d = defaultdict(list)` (`{}`).
  2. `word = "apple"`: `'a'` missing -> `list()` creates `[]` at `d['a']` -> `.append("apple")` -> `{'a': ['apple']}`.
  3. `word = "avocado"`: `'a'` present -> `.append("avocado")` -> `{'a': ['apple', 'avocado']}`.
  4. `word = "banana"`: `'b'` missing -> `list()` creates `[]` at `d['b']` -> `.append("banana")` -> `{'a': ['apple', 'avocado'], 'b': ['banana']}`.
  5. `dict(d)` returns plain `{'a': ['apple', 'avocado'], 'b': ['banana']}`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **List containing an empty string `group_by_first_letter(["apple", ""])` (CRITICAL EDGE CASE!):** Evaluating `word[0]` on `""` raises **`IndexError: string index out of range`**! *(If you wanted to support empty strings under key `""`, `word[:1]` slices safely without crashing, or you could guard `if word:`.)*
  - **Mixed uppercase/lowercase `["Apple", "apple"]`:** `'A' != 'a'`, so they land in **two separate keys**: `{'A': ['Apple'], 'a': ['apple']}`.
  - **Duplicate words `["cat", "cat"]`:** Since buckets are `list`s (not `set`s), duplicates are preserved: `{'c': ['cat', 'cat']}`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)` average** where `n = len(words)` (each iteration does `O(1)` `word[0]` indexing, `O(1)` hash lookup, amortized `O(1)` `list.append`, and `dict(d)` copies `u <= n` bucket references at the end in `O(u)`).
- **Space Complexity:** **`O(n)`** — across all `u` lists, the total number of stored string references is `n` (note strings themselves aren't copied, only references!).
- **Why `return dict(d)` Matters Beyond Pretty Printing (10/10 Design Insight!):**
  - If you returned the raw `defaultdict(list)` `d`, and the caller later checked `if res["z"]:` on a missing letter `'z'`, simply *reading* `res["z"]` would **silently mutate `res`** by inserting `'z': []` (`len(res)` increases by 1!), and `res["z"]` wouldn't raise `KeyError` as callers expect from a plain `dict`!
- **Plain `dict` Alternative Comparison:**
  - `d.setdefault(word[0], []).append(word)`: Works without importing `defaultdict`, *but* allocates and discards a brand-new empty list `[]` on **every single word** even when `word[0]` already exists! `defaultdict(list)` only calls `list()` on cache misses.

### Likely Interview Q&A
1. **Q: What happens if someone writes `defaultdict([])` instead of `defaultdict(list)`? Why can't `defaultdict` just take an empty list value?**  
   **A:** First, Python raises `TypeError: first argument must be callable or None`. Second, *design-wise*, if `defaultdict` reused a single `[]` instance across keys instead of calling a factory function `list()` each time, **every letter key would alias the exact same list** (`d['a'] is d['b']`), just like Python's mutable-default-argument trap!
2. **Q: What happens if `words` is `[""]`?**  
   **A:** `word[0]` raises `IndexError: string index out of range` because an empty string has no index `0`.

---

## `E07_key_stats.py` — Measuring Non-Randomness

- **File:** [E07_key_stats.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py)
- **Functions:** [`longest_run(history)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L17-L51), [`switch_rate(history)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L54-L85)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def longest_run(history):
    if not history:
        return 0
    
    longest = 1
    current = 1
    for i in range(1, len(history)):
        if history[i] == history[i - 1]:
            current += 1
        else:
            current = 1
        if current > longest:
            longest = current

    return longest


def switch_rate(history):
    if not history or (len(history) == 1):
        return 0.0

    switches = 0
    for i in range(1, len(history)):
        if history[i] != history[i-1]:
            switches += 1
    
    return switches / (len(history)-1)


# ANSWER: 50% as then the ability of predicting the next keystroke can go either way.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`longest_run` scans adjacent pairs `(history[i - 1], history[i])` in a single pass, extending a `current` streak counter when consecutive characters match, resetting to `1` when they differ, and tracking the maximum streak `longest`. `switch_rate` scans those same `len(history) - 1` adjacent transitions, counting how often consecutive keys differ and dividing by `len(history) - 1`."
- **Line-by-Line & Variable Breakdown:**
  - **In [`longest_run`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L17-L51):**
    - `if not history: return 0` (lines 38–39): Handles `""` up front so we can safely initialize `longest = 1` and `current = 1` (since `history[0]` by itself already forms a run of length `1`).
    - `for i in range(1, len(history)):` (line 43): Starts at index `1` so `history[i - 1]` is always `>= 0` (never wraps around to `history[-1]`!).
    - `if current > longest: longest = current` (lines 48–49): **Crucial placement!** Checked on *every* iteration (outside the `else`), NOT just when a run ends — otherwise a run extending to the end of the string (like `"fdffff"` or `"fffff"`) would never update `longest`!
  - **In [`switch_rate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E07_key_stats.py#L54-L85):**
    - `if not history or (len(history) == 1): return 0.0` (lines 77–78): Equivalent to `if len(history) < 2: return 0.0`. Prevents both `ZeroDivisionError` when `len == 1` (`0 / 0`) and negative `-0.0` (`0 / -1`) when `len == 0`!
    - `switches / (len(history) - 1)` (line 85): Fencepost principle — `n` characters have `n - 1` adjacent pairs/transitions. `/` produces a `float` in `[0.0, 1.0]`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `longest_run(history: Sequence) -> int` (locals `longest: int`, `current: int`, `i: int`).
  - `switch_rate(history: Sequence) -> float` (locals `switches: int`, `i: int`).
- **Concrete Step-by-Step Trace (`longest_run("ffdff")` & `switch_rate("ffdd")`):**
  - `longest_run("ffdff")`: Init `current = 1, longest = 1`.
    - `i = 1` (`'f' == 'f'`): `current = 2`, `longest = 2`.
    - `i = 2` (`'d' != 'f'`): `current = 1`, `longest = 2`.
    - `i = 3` (`'f' != 'd'`): `current = 1`, `longest = 2`.
    - `i = 4` (`'f' == 'f'`): `current = 2`, `2 > 2` False, `longest = 2`. Returns `2`.
  - `switch_rate("ffdd")`: Transitions `(0,1): f==f`, `(1,2): f!=d` (`switches = 1`), `(2,3): d==d`. Returns `1 / 3 = 0.3333333333333333`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Why starting `range` at `0` instead of `1` would be a sneaky Python bug!** If someone wrote `for i in range(len(history)): if history[i] == history[i - 1]:`, Python wouldn't raise `IndexError` at `i = 0` — instead `history[-1]` would compare the **first character against the last character**! Starting at `1` avoids that wrap-around bug completely.
  - **Single character `"f"`:** `longest_run("f")` skips `range(1, 1)` and returns `1`; `switch_rate("f")` hits line 77 guard and returns `0.0` (`float`, NOT `int` `0`!).
  - **More than 2 distinct characters (`longest_run("aaabbc")`):** Both functions are alphabet-agnostic and work on any string or list!

### Pillar 3 — Analyse (Complexity, Trade-offs & `# ANSWER`)
- **Time Complexity:** **`O(n)`** for both `longest_run` and `switch_rate` (`n = len(history)`), making a single pass of `n - 1` `O(1)` comparisons.
- **Space Complexity:** **`O(1)`** auxiliary space for both!
  - *Contrast with `zip(history, history[1:])`:* Writing `sum(a != b for a, b in zip(history, history[1:]))` is concise, *but* `history[1:]` allocates an `n - 1` copy (**`O(n)` space**!), whereas your index loop (or Python 3.10+'s `itertools.pairwise(history)`) uses **`O(1)` space**!
- **Alternative for `longest_run`:** `max((sum(1 for _ in group) for _, group in itertools.groupby(history)), default=0)` — functional `O(n)` time, `O(1)` space one-liner.
- **Embedded File Question (`# ANSWER`, lines 12–13 & 88):**
  > **QUESTION:** *for a genuinely random sequence, what would you expect `switch_rate` to be?*
  - **Your Comment (`#L88`):** `50% as then the ability of predicting the next keystroke can go either way.`
  - **10/10 Model Answer for the Interview:**
    1. **Exact return value:** Around **`0.5`** (50%). For an independent, identically distributed (i.i.d.) uniform sequence over 2 keys (`P('f') = P('d') = 0.5`), whatever key was typed at step $i - 1$, step $i$ has probability $0.5$ of matching it and $0.5$ of switching. Across $n - 1$ transitions, linearity of expectation gives $\mathbb{E}[\text{switch\_rate}] = 0.5$. *(Bonus flex: if there were $m$ equally likely keys instead of 2, the expected switch rate would be $\frac{m - 1}{m}$!)*
    2. **Why humans fail (Connecting to `E01_oracle.py`):** Humans trying to look "random" suffer from the **gambler's fallacy** — we feel runs like `"fff"` or `"dddd"` look non-random, so we deliberately alternate too often, pushing human `switch_rate` up to **`0.60–0.75`** (and keeping `longest_run` artificially tiny compared to $\approx \log_2 n$ expected in true coin flips!). That excess switching is exactly what `predict_no_3_repeats` and `predict_ngram` exploit to beat 50%!

### Likely Interview Q&A
1. **Q: In `longest_run`, what bug would happen if you moved `if current > longest: longest = current` *inside* the `else:` block?**  
   **A:** Whenever the longest run occurred at the very end of `history`—such as `"fffff"` (returns `1` instead of `5`!) or `"fdfff"` (returns `1` instead of `3`!)—the `else:` branch would never run after the final streak, missing it completely unless you checked again after the loop.
2. **Q: Why do we divide by `len(history) - 1` instead of `len(history)` in `switch_rate`?**  
   **A:** Because the very first keypress has no predecessor to differ from — in `n` keypresses there are only `n - 1` transitions where a switch *could* happen, so `fdfdfd` (`5` switches in `5` chances) rightly scores `1.0` instead of `5/6`.

---

## `E08_save_history.py` — Persistent Session Storage with `pathlib`

- **File:** [E08_save_history.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py)
- **Functions:** [`history_path(student_id)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L26-L37), [`save_history(history, student_id)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L40-L54), [`load_histories(student_id)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L57-L81), [`total_keys(student_id)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E08_save_history.py#L84-L96)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
from pathlib import Path

DATA = Path(__file__).parent / "data"

def history_path(student_id):
    return DATA / f"history_{student_id}.txt"

def save_history(history, student_id):
    p = history_path(student_id)
    with open(p, "a") as f:
        f.write(f"{history}\n")

def load_histories(student_id):
    p = history_path(student_id)
    hist = []
    if Path.exists(p):
        with open(p, "r") as f:
            for line in f:
                hist.append((line.rstrip('\n')))

    return  hist

def total_keys(student_id):
    return sum(len(sessions) for sessions in load_histories(student_id))
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "This module persists each game session's raw keypress string as one newline-terminated line in `data/history_<student_id>.txt` anchored next to the Python file via `Path(__file__).parent`. Opening with mode `'a'` appends new sessions without erasing old ones, `load_histories` reads them back stripped of trailing `'\n'` (returning `[]` if no file exists yet), and `total_keys` sums session lengths across `load_histories`."
- **Line-by-Line & Variable Breakdown:**
  - `DATA = Path(__file__).parent / "data"` (line 23): `__file__` is the path to `E08_save_history.py`. Anchoring to `.parent` ensures the file always lands in `W02/data/` regardless of which directory `python` was launched from! `Path` overloads `/` (`__truediv__`) for cross-platform path joining.
  - `with open(p, "a") as f:` (line 53): Context manager (`__enter__`/`__exit__`) guarantees the file descriptor is flushed and closed even if an exception occurs; mode `"a"` appends at EOF (creating the file if absent, unlike `"w"` which wipes existing sessions!).
  - `if Path.exists(p):` (line 76): **Style Quirk Watchout!** Usually written `if p.exists():` (calling the bound method on instance `p`). Writing `Path.exists(p)` calls the unbound method on class `Path` and explicitly passes `p` as `self` — totally valid Python, and great to explain if asked!
  - `for line in f: hist.append((line.rstrip('\n')))` (lines 78–79): Iterates lazily line-by-line over file `f` and strips only the trailing newline `'\n'` (note extra outer parentheses `((...))` are harmless).
  - `sum(len(sessions) for sessions in load_histories(student_id))` (line 96): Uses a **generator expression** inside `sum(...)`. *(Naming Watchout: `sessions` is plural even though each loop item is a **single** session string — `session` is clearer.)*

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `history_path(student_id: str | int) -> pathlib.Path`.
  - `save_history(history: str, student_id: str) -> None`.
  - `load_histories(student_id: str) -> list[str]`.
  - `total_keys(student_id: str) -> int`.
- **Concrete Step-by-Step Trace:**
  1. `save_history("fdfd", "42")` -> opens `.../W02/data/history_42.txt` in append mode, writes `"fdfd\n"`, closes file, returns `None`.
  2. `save_history("dd", "42")` -> appends `"dd\n"` -> file bytes are `"fdfd\ndd\n"`.
  3. `load_histories("42")` -> `Path.exists(p)` is `True` -> reads `"fdfd\n"` -> `'fdfd'`, reads `"dd\n"` -> `'dd'` -> returns `['fdfd', 'dd']`.
  4. `total_keys("42")` -> `sum` over generator yielding `4`, `2` -> returns `6`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Unknown student `load_histories("nobody")` / `total_keys("nobody")`:** `Path.exists(p)` is `False` -> `load_histories` returns `[]` -> `total_keys` computes `sum([]) == 0` without raising `FileNotFoundError`!
  - **Saving an empty session `save_history("", "test")`:** Writes `"\n"` (1 byte). `load_histories("test")` strips `'\n'` and returns **`['']`** (a 1-element list containing an empty string, `len == 1` session!), while `total_keys("test")` computes `len('') == 0` keypresses! *(Contrast: if someone used `p.read_text().split()` instead of line iteration, `""` sessions would vanish!)*
  - **Missing `data/` directory:** `open(p, "a")` creates a missing *file*, **not** a missing parent *directory* — if `W02/data/` were deleted, `save_history` would raise `FileNotFoundError` unless `DATA.mkdir(exist_ok=True)` were called first.
  - **`history` containing an embedded `'\n'` (`save_history("fd\ndf", "id")`):** Because newline is the record delimiter, reloading splits one session into two `['fd', 'df']`!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time & Space Complexity:** Let $S$ be the number of sessions for `student_id` and $N = \sum_{i=1}^S |s_i|$ be the total keypresses across all sessions (`m = len(history)` for a single session):
  - `history_path`: **`O(1)`** time and **`O(1)`** space (for bounded `student_id` length).
  - `save_history`: **`O(m)`** time and **`O(m)`** space (`f"{history}\n"` builds an `(m + 1)`-char string; calling `f.write(history)` then `f.write("\n")` would use `O(1)` auxiliary RAM!).
  - `load_histories`: **`O(N + S)`** time and **`O(N + S)`** space (must return all $S$ strings totaling $N$ chars).
  - `total_keys`: **`O(N + S)`** time and **`O(N + S)`** space!
    - **Sharp Space Trade-off Question:** Even though `sum(len(s) for s in ...)` is a generator expression (`O(1)` extra space for `sum`), it iterates over `load_histories(student_id)`, which **already loaded the entire file into a `list[str]` in memory**! If the file were 10 GB, composing `load_histories` would use 10 GB of RAM, whereas streaming directly over `with open(p) as f: return sum(len(line.rstrip('\n')) for line in f)` would use **`O(max_line_len)`** memory — classical **code reuse vs streaming memory** trade-off!
- **LBYL (`if p.exists():`) vs EAFP (`try: open(p) except FileNotFoundError:`):** EAFP avoids a double filesystem stat/open syscall and eliminates the TOCTOU (*time-of-check to time-of-use*) race if another process deletes `p` between `.exists()` and `open(p)`.

### Likely Interview Q&A
1. **Q: Why did the module docstring warn that doctests run in alphabetical order by function name?**  
   **A:** `doctest` runs `history_path`, then `load_histories`, then `save_history`, then `total_keys` alphabetically — NOT top-to-bottom! If `load_histories`'s doctest relied on a file left behind by `save_history`'s doctest above it, `load_histories` would actually run *first* and fail! That's why every doctest uses its own isolated ID (`testA`, `testB`, `testC`) and cleans up with `.unlink()`.
2. **Q: Why is saving the raw `history` here more useful than `E01_oracle.py`'s `save(counts, path)`?**  
   **A:** `save(counts, path)` stores aggregated 5-gram counts, which is a **lossy compression**: it discards chronological order and locks in `K = 4`. From raw `history` strings, we can replay the exact sequence and evaluate *any* model (`k = 1` through `8` in `E09`, or `longest_run`/`switch_rate` in `E07`)!
3. **Q: Why did you write `Path.exists(p)` on line 76 instead of `p.exists()`?**  
   **A:** In Python, `p.exists()` is syntactic sugar for `Path.exists(p)` — calling the method on the `Path` class and passing the `Path` instance `p` explicitly as `self`. Both execute the exact same check, though `p.exists()` is more idiomatic OOP style.

---

## `E09_ngram_sweep.py` — Offline N-Gram Hyperparameter Sweep

- **File:** [E09_ngram_sweep.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py)
- **Functions:** [`predict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L29-L33) *(Given)*, [`update`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L36-L37) *(Given)*, [`accuracy(history, k)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L40-L83), [`sweep(history, ks=range(1, 9))`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L86-L95)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def predict(counts, history, k):
    context = history[-k:]
    if counts[context + "d"] > counts[context + "f"]:
        return "d"
    return "f"


def update(counts, history, key, k):
    counts[history[-k:] + key] += 1


def accuracy(history, k):
    if not history:
        return 0.0
    
    counts = Counter()
    tmp_his = ""
    correct = 0
    for char in history:
        key = predict(counts, tmp_his, k)
        update(counts, tmp_his, char, k)
        if key == char:
            correct += 1
        tmp_his += char
    return correct / len(history)


def sweep(history, ks=range(1, 9)):
    dict = {}
    for i in ks:
        dict[i] = accuracy(history, i)
    return dict


# ANSWER: 
#   1) n = 2 achieved 87.5%
#   2) It takes a lot more information for these to make meaningful predictions
#       and there is so many combinations it may be creating very niche decisions.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`accuracy` performs an honest online (prequential) evaluation of a `(k + 1)`-gram oracle by replaying `history` one keypress at a time: on each step it predicts using only past keypresses `tmp_his`, scores the prediction, updates `counts`, and appends the true keypress. `sweep` runs `accuracy` across a range of context lengths `ks` (defaulting to `1..8`, i.e. `2`-grams through `9`-grams) and returns a `{k: score}` dictionary so we can compare model capacities fairly on identical data."
- **Line-by-Line & Variable Breakdown:**
  - **`predict` & `update` (Given, lines 29–37):** Two critical changes from `E01_oracle.py`:
    1. `k` is passed explicitly as a parameter instead of reading a module global `K`, allowing multiple `k` values in one run.
    2. Ties (`counts[... + "d"] == counts[... + "f"]`) deterministically return `"f"` instead of `random.choice("fd")` so experiments are **100% reproducible** (same `history` + `k` always yields the exact same float).
  - **In [`accuracy(history, k)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L40-L83):**
    - `if not history: return 0.0` (lines 71–72): Prevents `0 / 0` `ZeroDivisionError` on `""`.
    - `counts = Counter()` (line 74): Fresh, empty model so every `k` starts from zero prior knowledge.
    - `tmp_his = ""` (line 75): Prefix of `history` seen *so far* before the current keypress `char`.
    - **Order of lines 78–82 (CRITICAL — Be Ready to Defend Every Line's Position!):**
      1. `key = predict(counts, tmp_his, k)` (line 78 — *Note: `predicted_key` or `guess` would be clearer than `key`!*): Predicts **before** `counts` or `tmp_his` sees `char` (zero data leakage!).
      2. `update(counts, tmp_his, char, k)` (line 79): Safe before `if key == char:` ONLY because `key` was already computed on line 78, AND safe because `tmp_his` has **not yet** had `char` appended!
      3. `if key == char: correct += 1` (lines 80–81): Tallies hits.
      4. `tmp_his += char` (line 82): Advances the visible history *after* both `predict` and `update` used the old `tmp_his`.
  - **In [`sweep(history, ks=range(1, 9))`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W02/E09_ngram_sweep.py#L86-L95):**
    - `ks=range(1, 9)`: Note `range` is **immutable**, so using `range(1, 9)` as a default argument is completely safe (unlike mutable `ks=[1, 2, ...]`)!
    - `dict = {}` (line 92): **Naming Watchout!** Shadows built-in `dict` (`results = {}` or `{k: accuracy(history, k) for k in ks}` is cleaner).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `accuracy(history: str, k: int) -> float` (locals `counts: Counter[str]`, `tmp_his: str`, `correct: int`, `char: str`, `key: str`).
  - `sweep(history: str, ks: Iterable[int] = range(1, 9)) -> dict[int, float]`.
- **Concrete Step-by-Step Trace (`accuracy("fdfd", 1)`):**
  | Step | `char` | `tmp_his` (before) | Context `tmp_his[-1:]` | `counts` (before) | `key` (`predict`) | Hit? | `counts` after `update` |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | 1 | `'f'` | `""` | `""` | `{}` | `'f'` *(0 vs 0 tie -> `'f'`)* | ✅ (`1`) | `{'f': 1}` |
  | 2 | `'d'` | `"f"` | `"f"` | `{'f': 1}` | `'f'` *(`"fd":0, "ff":0` tie -> `'f'`)* | ❌ (`1`) | `{'f': 1, 'fd': 1}` |
  | 3 | `'f'` | `"fd"` | `"d"` | `{'f': 1, 'fd': 1}` | `'f'` *(`"dd":0, "df":0` tie -> `'f'`)* | ✅ (`2`) | `{..., 'df': 1}` |
  | 4 | `'d'` | `"fdf"` | `"f"` | `{..., 'fd': 1, 'ff': 0}` | `'d'` *(`"fd":1 > "ff":0`!)* | ✅ (`3`) | `{..., 'fd': 2}` |
  Returns `3 / 4 = 0.75`. *(And continuing on `"fdfdfdfdfd"` gets all remaining 6 right -> `9 / 10 = 0.9`!)*
- **"What If the Caller Passed...?" (Edge Cases):**
  - **THE `k = 0` SLICING TRAP (`accuracy("dddd", 0)`) — 10/10 Trace Insight!**
    - What happens if someone passes `k = 0` hoping to test a 1-gram (zero-context) model?
    - In Python, **`-0 == 0`**, so inside `predict` and `update`, `history[-0:]` evaluates to **`history[0:]` — the ENTIRE `tmp_his` string**, NOT `""`!
    - Because `tmp_his` grows by 1 character every step (`""`, `"d"`, `"dd"`, `"ddd"`), `tmp_his[-0:]` is a brand-new unseen context on *every single keypress*! `counts` never gets a repeat match, `predict` guesses `'f'` every time, and `accuracy("dddd", 0)` returns **`0.0`** instead of `0.75`! *(Fixing `k = 0` would require `context = history[-k:] if k > 0 else ""`.)*
  - **`k > len(history)` (e.g., `accuracy("fdfd", 100)`):** Slicing clamps `tmp_his[-100:]` to all of `tmp_his`, behaving identically to `k = len(history)` (every step has a unique prefix length `0, 1, 2, 3`, so nothing ever repeats and every step tie-breaks to `'f'`).
  - **Empty `ks` in `sweep(history, [])`:** Returns `{}`.

### Pillar 3 — Analyse (Complexity, Optimization & `# ANSWER`)
- **Time Complexity of `accuracy(history, k)` (Nail Both Sides of `tmp_his += char`!):**  
  Let `n = len(history)` and `k` be the context length:
  1. **Inside `predict` and `update` (per step):** Slicing `tmp_his[-k:]`, concatenating `+ "d"` / `+ "f"` / `+ char`, and hashing `(k + 1)`-char strings in `Counter` each take **`O(k)`** time (`O(n * k)` across `n` steps).
  2. **Hidden cost of `tmp_his += char` (line 82):**
     - **Standard algorithmic model (immutable strings):** Copying a string of length $1, 2, \dots, n$ takes $1 + 2 + \dots + n = \frac{n(n+1)}{2} =$ **`O(n^2)`**, giving **`O(n^2 + n * k)`** total time!
     - **CPython runtime nuance:** Because no other variable holds a reference to `tmp_his` when `tmp_his += char` executes (`predict` and `update` only sliced `tmp_his[-k:]` and already returned), CPython's `PyUnicode_Append` resizing optimization often mutates the buffer in amortized `O(1)` -> **`O(n * k)`** in CPython, **but** relying on interpreter-specific refcount optimizations is fragile!
  3. **How to make `accuracy` strictly `O(n * k)` time AND eliminate `tmp_his` (`O(1)` history space):**
     - We already have `history`! Using `for i, char in enumerate(history):`, the context before index `i` is simply `history[max(0, i - k):i]` — zero `tmp_his` string building! (Or keep only the rolling tail `tmp_his = (tmp_his + char)[-k:]` of max length `k`.)
  - **Time Complexity of `sweep(history, ks)`:** $\sum_{k \in ks} T(\text{accuracy}(n, k)) =$ **`O(|ks| * n^2 + n * sum(ks))`** conceptually, or **`O(n * sum(ks))`** with index slicing (for default `ks = range(1, 9)`, `|ks| = 8` and `sum(ks) = 36`, which is `O(n)`!).
- **Space Complexity of `accuracy(history, k)`:**
  - `tmp_his` grows to length `n`: **`O(n)`**.
  - `counts` (`Counter`) stores at most $\min(n, 2^{k+1})$ full n-grams (plus up to $k$ warm-up prefixes), each of length $\le k + 1$: **`O(k * min(n, 2^k))`**.
  - Total space: **`O(n + k * min(n, 2^k))`** (which shrinks to **`O(k * min(n, 2^k))`** if `tmp_his` is replaced by slicing `history`!).
- **Embedded File Question (`# ANSWER`, lines 13–14 & 107–110):**
  > **QUESTION:** *run the sweep on your own history and write the numbers into the comment at the bottom. Which `n` was best, and why do the big ones fall away?*
  - **Context on Your `# ANSWER` (`n = 2 achieved 87.5%`):** That exact number came from running `python3 W02/E09_ngram_sweep.py` on the shipped `data/history_sample.txt` (600 keypresses: `n=2: 87.5%`, `n=3: 87.2%`, `n=4: 86.8%`, `n=5: 86.3%`, ..., `n=9: 83.0%`), which is heavily alternating `fdfdfd...` so 1-char context (`k = 1`, `n = 2`) immediately captures it!
  - **10/10 Model Answer on Why Large `n` Falls Away (The Bias–Variance / Sparsity Trade-off):**
    1. **Exponential State-Space Explosion ($2^k$ contexts):** Over a 2-key alphabet (`f`, `d`), a context of length `k` (`n = k + 1`) has $2^k$ distinct possible histories:
       - `n = 2` (`k = 1`): only $2^1 = 2$ contexts (`"f"`, `"d"`). In 600 keys, each is seen ~300 times — learns almost instantly!
       - `n = 5` (`k = 4`): $2^4 = 16$ contexts (~37 observations per context) — rich enough to catch multi-key human habits like avoiding 3 repeats without starving for data.
       - `n = 9` (`k = 8`): $2^8 = 256$ contexts! In 600 keys, each context appears only $600 / 256 \approx 2.3$ times on average (and for `k = 12`, $2^{12} = 4096 > 600$!).
    2. **Cold-Start Penalty & Overfitting (Variance):** Every time a context is encountered for the **first** time (or tied `1–1`), `counts` has no evidence and defaults to `"f"` (~50% coin-flip accuracy). Even worse, seeing an 8-key pattern once due to noise causes the model to memorize a fluke (**overfitting / high variance**) rather than a real habit. Small `k` has **high bias** (can't see long patterns) but **low variance**; large `k` has **low bias** but **high variance / data sparsity**!

### Likely Interview Q&A
1. **Q: In `accuracy`, what would happen if you swapped lines 78 and 79 so `update` ran *before* `predict`?**  
   **A:** That would introduce **data leakage (training on the test label)**! Updating `counts` with the current keypress `char` *before* predicting `char` lets the model peek at the answer—on every unseen context its very first count would be `1` for the true `char` vs `0` for the other, artificially inflating accuracy toward 100%!
2. **Q: Why did `E09`'s `predict` break ties by always returning `"f"` instead of `random.choice("fd")` like `E01_oracle.py`?**  
   **A:** In an interactive game (`E01`), deterministic tie-breaking could be exploited by a clever player; in a scientific benchmark (`E09`), randomness adds lucky/unlucky coin-flip noise across different `k` values and makes doctests non-deterministic. Fixing tie-breaks makes every `accuracy(history, k)` call a pure, reproducible function.
3. **Q: Look at line 82 (`tmp_his += char`). What is its complexity risk on a 1,000,000-character history, and how would you remove `tmp_his` completely?**  
   **A:** Because Python strings are immutable, repeated `+=` is conceptually `O(n^2)` time and stores a redundant `O(n)` copy of `history`. Since `history` is already passed in unchanged, we can loop with `for i, char in enumerate(history):` and pass `history[max(0, i - k):i]` (or slice inside `predict`/`update`), guaranteeing strict `O(n * k)` time and eliminating `tmp_his` completely!
