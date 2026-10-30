# Week 04 Interview Prep — Hash Tables, Collisions & Python's Data Model (Dunder Methods)

← Back to [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Source Directory:** [`assignment_01/W04/`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04)  
**Core Week 04 Themes:** Linear-scan association lists (`PairListDict`) vs separate-chaining hash tables (`SimpleDict`), `hash(key) % capacity`, mutability & the hash invariant, Pigeonhole Principle & SipHash string randomization, dynamic resizing (`_grow` at load factor `0.75`), Python's special/dunder methods (`__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__iter__`, `__len__`, `__repr__`), Python's `in` fallback protocol, and rigorous micro-benchmarking.

> **Why Week 04 Matters for 8–10 Marks:** Week 04 combines **data structures & complexity analysis** (`O(1)` average vs `O(n)` worst-case, amortized resizing, separate chaining vs open addressing tombstones) with **Python's object data model** (how syntax like `d[k]`, `del d[k]`, and `k in d` dispatches to `__dunder__` methods). `E04`, `E05`, and especially `E06` are prime 8–10 mark interview targets!

---

## Table of Contents

1. [Summary Complexity & Difficulty Matrix](#summary-complexity--difficulty-matrix)
2. [Reference Context — `E01_SimpleDict.py` (Given Code)](#reference-context--e01_simpledictpy-given-code)
3. [`E02_bucket_index.py` — `bucket_index`](#e02_bucket_indexpy--bucket_index)
4. [`E03_is_hashable.py` — `is_hashable`](#e03_is_hashablepy--is_hashable)
5. [`E04_string_collision.py` — `find_collision`](#e04_string_collisionpy--find_collision)
6. [`E05_delitem.py` — `SimpleDict.__delitem__`](#e05_delitempy--simpledict__delitem__)
7. [`E06_fast_contains.py` — `SimpleDict.__contains__` & The 3 Benchmark Questions](#e06_fast_containspy--simpledict__contains__--the-3-benchmark-questions)
8. [Week 04 Watchlist — Subtle Quirks in Your Submitted Code](#week-04-watchlist--subtle-quirks-in-your-submitted-code)

---

## Summary Complexity & Difficulty Matrix

*(Let `n` = number of key-value pairs stored, `C` = `capacity` (number of buckets, where `C = Theta(n)` once populated), `m` = `len(words)` in `E04`, and assume `hash(key)` & `==` on keys take `O(1)` time.)*

| Exercise File | Functions / Methods | Difficulty Tier | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| [E01_SimpleDict.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py) | [`PairListDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L24-L76) (`[k]`, `[k]=v`, `in`) | Reference (Given) | `O(n)` (`__len__` is `O(1)`) | `O(n)` total (`0` wasted slots) |
| [E01_SimpleDict.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py) | [`SimpleDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L79-L268) (`[k]`, `[k]=v`) | Reference (Given) | `O(1)` avg/amortized, `O(n)` worst; `k in d` is **`O(C + n)`** without `__contains__`! | `O(C + n)` (`O(n)` once filled) |
| [E02_bucket_index.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E02_bucket_index.py) | [`bucket_index`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E02_bucket_index.py#L11-L39) | Warm-up | `O(1)` (or `O(len(key))` first hash) | `O(1)` |
| [E03_is_hashable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py) | [`is_hashable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L15-L52) | Warm-up / Moderate | `O(1)` primitive / `O(size)` tuple | `O(1)` (or `O(depth)` C stack on nested tuple) |
| [E04_string_collision.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py) | [`find_collision`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py#L25-L66) | Hard (8–10 Mark Target) | `O(min(m, C))` avg (Pigeonhole cap!), `O(m)` worst | `O(min(m, C))` (`bucket` dict) |
| [E05_delitem.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py) | [`SimpleDict.__delitem__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L75-L125) | Hard (8–10 Mark Target) | `O(1)` average, `O(n)` worst-case | `O(1)` auxiliary |
| [E06_fast_contains.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py) | [`SimpleDict.__contains__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L100-L150) | Hard (8–10 Mark Target) | `O(1)` average, `O(n)` worst-case | `O(1)` auxiliary |

---

## Reference Context — `E01_SimpleDict.py` (Given Code)

**File:** [E01_SimpleDict.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py)

Every exercise in Week 04 builds on or benchmarks [`PairListDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L24-L76) and [`SimpleDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L79-L268). Make sure you can explain these 5 foundational mechanisms without hesitation:

### 1. Python's Data Model (Dunder Method Dispatch Table)
| Python Syntax | Method Python Calls | Return / Error Contract |
| :--- | :--- | :--- |
| `d = SimpleDict()` | [`__init__(self, capacity=8)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L134-L137) | Initializes `self.capacity`, `self.n = 0`, `self.buckets` (`None`) |
| `d[k] = v` | [`__setitem__(self, key, value)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L168-L177) | Overwrites existing key or appends & increments `self.n` (`None`) |
| `d[k]` | [`__getitem__(self, key)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L179-L183) | Returns `v`, or raises `KeyError(key)` |
| `del d[k]` *(E05)* | [`__delitem__(self, key)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L75-L125) | Removes pair & decrements `self.n`, or raises `KeyError(key)` |
| `k in d` *(E06)* | [`__contains__(self, key)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L100-L150) *(fallback: `__iter__`!)* | Returns `bool` (`True` / `False`) |
| `len(d)` | [`__len__(self)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L190-L200) | Returns `int` (`self.n` in `O(1)`) |
| `for k in d:` | [`__iter__(self)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L202-L215) | Returns iterator/generator yielding keys |
| `repr(d)` / REPL | [`__repr__(self)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L229-L240) | Returns `str`, using `{k!r}: {v!r}` so strings show quotes |

### 2. `PairListDict` vs `SimpleDict` Architecture
- **[`PairListDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L24-L76):** Stores a single flat list `self.pairs = [(k1, v1), (k2, v2), ...]`. Zero wasted empty slots, preserves insertion order, and doesn't even require keys to be hashable — **but** `__getitem__`, `__setitem__` (must check for existing key before appending!), and `in` all scan linearly in **`O(n)`** time.
- **[`SimpleDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L79-L268) (Separate Chaining):** Allocates `self.buckets = [[] for _ in range(capacity)]` — a list of `capacity` independent bucket lists.
  - **Classic Python Trap:** Why `[[] for _ in range(capacity)]` on [Line 137](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L137) instead of `[[]] * capacity`? Because `[[]] * capacity` creates `capacity` references to the **exact same inner list**, so appending to bucket `0` would appear in **every** bucket!

### 3. Load Factor (`0.75`) & Why [`_grow()`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L242-L267) Must Re-hash Everything
- Whenever `self.n > 0.75 * self.capacity` (e.g., inserting the 7th item when `capacity = 8`, since `7 > 6.0`), [`_grow()`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L242-L267) doubles `self.capacity *= 2` (dropping load factor $\alpha = \frac{n}{\text{capacity}}$ to $\approx 0.375$), allocates fresh empty buckets, resets `self.n = 0`, and re-inserts every `(k, v)` pair via `self[k] = v`.
- **Why can't `_grow()` just copy the old buckets across?** Because a key's bucket is `hash(key) % self.capacity`! When `capacity` doubles from `8` to `16`, `11 % 8 == 3` moves to `11 % 16 == 11`.
- **Why is `__setitem__` still `O(1)` *amortized* if `_grow()` takes `O(n)`?** Because capacity doubles geometrically (`8, 16, 32, 64, ...`), so across `n` insertions total re-insertion work is $8 + 16 + 32 + \dots + n < 2n = O(n)$, which averages out to **`O(1)` per insertion**!

### 4. The Missing `__contains__` Trap ([Lines 185–188](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L185-L188))
When you evaluate `key in d` and a class does **not** define `__contains__`, Python does **not** raise `TypeError` — instead, Python falls back to [`__iter__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L202-L215), pulling keys out one by one and testing `k == key`! That turns `SimpleDict`'s `in` operator back into an **`O(capacity + n)`** linear scan until you implement `__contains__` in `E06`.

### 5. Benchmarking Rules in [`time_lookups`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L281-L320)
1. **Warm up first & discard** ([L331–332](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L331-L332)): Eliminates cold CPU frequency scaling, cold caches, and CPython 3.11+ adaptive bytecode specialization artifacts.
2. **Spread probes evenly** (`keys[i * n // PROBE]`): Taking the first 200 keys would let `PairListDict` find all of them in indices `0..199`, falsely making `PairListDict` look `O(1)`!
3. **Keep the minimum (`best`), not the average** ([L315–316](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E01_SimpleDict.py#L315-L316)): OS interrupts and background processes can only **add** delay (one-sided positive noise), never make code run faster than hardware allows — so `min` is the least noisy estimate.

---

## `E02_bucket_index.py` — `bucket_index`

- **File:** [E02_bucket_index.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E02_bucket_index.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E02_bucket_index.py))
- **Symbol:** [`bucket_index`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E02_bucket_index.py#L11-L39)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def bucket_index(key, capacity):
    return hash(key) % capacity
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"It maps any hashable `key` onto a valid bucket list index between `0` and `capacity - 1` in two steps: `hash(key)` converts the key into an arbitrary signed integer, and `% capacity` folds that integer into the table's index range."*
- **Line-by-Line & Variable Breakdown:**
  - `hash(key)`: Calls `key.__hash__()`, returning a signed platform-word integer (which may be huge or negative).
  - `% capacity`: Python's **floored modulo** operator. Unlike C or Java (where `-3 % 8` is `-3`), Python defines `a % b = a - b * floor(a / b)`, so whenever `capacity > 0`, the result is **guaranteed** to satisfy `0 <= idx < capacity`! *(Note: in Python, a negative index like `-3` wouldn't crash `self.buckets[-3]` — it would silently index the 3rd bucket from the end, which makes floored modulo very neat, though keeping indices strictly in `0 .. capacity - 1` avoids confusion!)*

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `key`: `Hashable` (any immutable hashable object: `int`, `str`, `float`, `bool`, `None`, `tuple` of hashables)
  - `capacity`: `int` (`> 0`)
  - Return type: `int` in `range(0, capacity)`
- **Concrete Step-by-Step Trace:**
  - `bucket_index(3, 8)`: `hash(3)` is `3` → `3 % 8` → `3`.
  - `bucket_index(11, 8)`: `hash(11)` is `11` → `11 % 8` → `3` (**collision** with `3`!).
  - `bucket_index(11, 16)`: `hash(11)` is `11` → `11 % 16` → `11` (no longer collides with `3`!).
  - `bucket_index(-3, 8)`: `hash(-3)` is `-3` → `-3 % 8` (`-3 = 8 * (-1) + 5`) → `5`.
  - **CPython quirk (`key = -1`):** `hash(-1)` is **`-2`** (not `-1`, because CPython's C API reserves `-1` as the error return code!) → `bucket_index(-1, 8)` returns `-2 % 8 == 6`!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Unhashable key `bucket_index([1, 2], 8)`:** Raises **`TypeError: unhashable type: 'list'`**.
  2. **`capacity = 0`:** Raises **`ZeroDivisionError: integer modulo by zero`**.
  3. **Negative capacity `bucket_index(3, -8)`:** Does NOT raise an error — Python floored modulo gives `-5` (takes the sign of the negative divisor `-8`!).
  4. **Equal keys of different types: `3`, `3.0`, and `True` (`1`):**
     - Because `3 == 3.0` and `1 == True` in Python, Python's hash law (`a == b` $\implies$ `hash(a) == hash(b)`) forces `hash(3) == hash(3.0) == 3` and `hash(1) == hash(True) == 1`. Thus `bucket_index(3, 8)` and `bucket_index(3.0, 8)` **always** land in the exact same bucket (`3`)!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:** **Time `O(1)`** for `int`, `float`, `bool`, and already-cached `str` (or `O(len(key))` the very first time a new string or tuple is hashed); **Space `O(1)`**.
- **Design Trade-off (`% capacity` vs `& (capacity - 1)`):** Because CPython's built-in `dict` forces `capacity` to always be a **power of 2** ($2^k$), CPython replaces slow integer division `% capacity` with a single-cycle bitwise AND `hash(key) & (capacity - 1)`. Using `% capacity` in `SimpleDict` works for *any* positive integer `capacity` (like `capacity = 5` in the doctest!).

### Likely Interview Q&A
1. **Q: Two keys land in the same bucket. Does that mean `hash(k1) == hash(k2)`?**  
   **A:** Almost never! Usually `hash(k1) != hash(k2)` (for example `hash(3) == 3` and `hash(11) == 11`), and the collision happens at the **modulo step** because both hashes leave the same remainder mod `capacity` (`3 % 8 == 11 % 8 == 3`).
2. **Q: Why does `1 == True` and `hash(1) == hash(True)` matter for `SimpleDict`?**  
   **A:** If you execute `d[1] = "one"` and then `d[True] = "true"`, `True` lands in bucket `1`, matches `k == key` (`1 == True` is `True`!), and overwrites the value so `d` still has length `1`! If `hash(1)` and `hash(True)` differed while `1 == True`, `1` and `True` could end up in different buckets, breaking dictionary uniqueness.

---

## `E03_is_hashable.py` — `is_hashable`

- **File:** [E03_is_hashable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E03_is_hashable.py))
- **Symbol:** [`is_hashable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L15-L52)
- **Difficulty Tier:** `Warm-up / Moderate`

### Your Submitted Code
```python
def is_hashable(x):
    try:
        hash(x)
        return True
    except:
        return False


# ANSWER: The reason is it holds an object that is mutable and so the values of the list can change and are mutable.
#  We cannot hash mutable objects as they may change next time and we would have an invalid hash unless we update the hash everytime the mutable object changes.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"It uses Python's EAFP ('Easier to Ask Forgiveness than Permission') pattern to test whether an object `x` can be used as a dictionary key by calling `hash(x)` inside a `try` block and returning `True` if it succeeds or `False` if hashing raises an error."*
- **Line-by-Line & Variable Breakdown:**
  - `try: hash(x)` (Lines 48–49): Actually invokes `x.__hash__()` (which for container types like `tuple` or `frozenset` recursively hashes every element inside `x`!).
  - `return True` (Line 50): Reached only if `hash(x)` returned an `int` without raising.
  - **`except:` (Line 51 — Self-Critique Ready!):** Look closely! Your submitted code used a **bare `except:`**, whereas the docstring and [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E03_is_hashable.py#L51) specify **`except TypeError:`**. Be ready to proactively say: *"In production I should write `except TypeError:` rather than a bare `except:`, because bare `except:` catches `BaseException` — including `KeyboardInterrupt`, `SystemExit`, or unrelated bugs inside a custom `__hash__` method!"*

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `x`: `Any`
  - Return type: `bool` (`True` or `False`)
- **Concrete Step-by-Step Trace on `is_hashable((1, [2, 3]))`:**
  1. Enters `try:` and calls `hash((1, [2, 3]))`.
  2. `tuple.__hash__` begins combining element hashes:
     - Element `0`: calls `hash(1)` → returns `1`.
     - Element `1`: calls `hash([2, 3])` → `list.__hash__` is `None` → CPython raises `TypeError: unhashable type: 'list'`.
  3. Jumps immediately to `except:` (skipping `return True`) and returns `False`.
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Nested immutable vs mutable containers:**
     - `(1, (2, 3))` → `True`; `frozenset({1, 2})` → `True`; `(1, {2, 3})` (`set` inside `tuple`) → `False`.
  2. **Empty tuple `()` vs empty list `[]`:**
     - `is_hashable(())` → `True`! What about `is_hashable(([],))`? `False`!
  3. **Why NOT use `isinstance(x, collections.abc.Hashable)` instead of `try: hash(x)`? (10/10 Interview Insight!)**
     - Try it in Python: `isinstance((1, [2, 3]), collections.abc.Hashable)` returns **`True`**!! Why? Because `isinstance(..., Hashable)` only checks whether the **class** `tuple` defines a `__hash__` method — it does **not** inspect the elements inside the tuple! Only actually calling `hash(x)` inside `try / except TypeError` gives the right answer `False` for `(1, [2, 3])`!
  4. **Custom user-defined class `class Foo: pass`:**
     - By default in Python, custom class instances ARE hashable (`is_hashable(Foo())` is `True`, hashing by object identity/address) *unless* you override `__eq__` without defining `__hash__`, in which case Python automatically sets `Foo.__hash__ = None` (`is_hashable(Foo())` becomes `False`)!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - For flat primitives (`int`, `float`, `None`, cached `str`): **Time `O(1)`**, **Space `O(1)`**.
  - For a nested `tuple` or `frozenset` containing `m` total items at nesting depth `d`: **Time `O(m)`** (must verify/combine every inner element's hash!), **Space `O(d)`** on the C call stack.
- **Embedded File Question (`# ANSWER` on [Lines 55–56](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L55-L56)):**
  - *Question:* Why is a tuple hashable when it holds numbers, but not when it holds a list?
  - *Your written answer:* *"The reason is it holds an object that is mutable and so the values of the list can change and are mutable. We cannot hash mutable objects as they may change next time and we would have an invalid hash unless we update the hash everytime the mutable object changes."*
  - **CRITICAL INTERVIEW SHARPENING:** Notice the end of your comment said *"unless we update the hash everytime the mutable object changes"*. **Even if Python updated the hash whenever the list changed, dictionary lookup would STILL break!** Explain why using buckets:
    1. Suppose `k = (1, [2, 3])` hashed to bucket `5` when you inserted `d[k] = "hello"`, so `SimpleDict` placed `(k, "hello")` in `self.buckets[5]`.
    2. Later you mutate `k[1].append(4)`. If `k`'s hash updated to reflect `[2, 3, 4]`, `hash(k) % 8` might now be bucket `2`!
    3. When you look up `d[k]`, `SimpleDict` checks `self.buckets[2]` and raises `KeyError` — while `k` is stranded forever inside `self.buckets[5]`!
    - **Golden Rule to State Aloud:** *"A dictionary key's hash must remain **constant** for its entire lifetime in the dictionary, and a tuple computes its hash from its elements' hashes — so a tuple is only hashable if every element inside it is recursively hashable."*

### Likely Interview Q&A
1. **Q: Look at line 51 of your `is_hashable`: why is `except TypeError:` better than `except:`?**  
   **A:** Unhashable objects specifically raise `TypeError`. A bare `except:` catches `BaseException`, which would swallow `KeyboardInterrupt`, `SystemExit`, or unexpected bugs inside a custom `__hash__` implementation and falsely report `False`.
2. **Q: Why is `frozenset` hashable while `set` is not, and why can't you have a `set` of `list`s?**  
   **A:** A `set` is implemented under the hood as a hash table (just like a `dict` with keys and no values)! So elements of a `set` must be hashable (ruling out `list`s), and a `set` itself is mutable (`.add()` / `.remove()`), so `set` sets `__hash__ = None`, whereas immutable `frozenset` can safely hash its elements.

---

## `E04_string_collision.py` — `find_collision`

- **File:** [E04_string_collision.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E04_string_collision.py))
- **Symbols:** [`bucket_index`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py#L21-L22) *(given)*, [`find_collision`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py#L25-L66)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def find_collision(words, capacity):
    bucket = {}

    for word in words:
        try:
            idx = bucket_index(word, capacity)
            if idx not in bucket:
                bucket[idx] = word
            else:
                return (bucket[idx], word)
        except:
            return None
    return None
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"It walks through `words` one by one, using a dictionary `bucket` to record the first word that landed at each bucket index `idx = bucket_index(word, capacity)`. As soon as a word computes an `idx` already present in `bucket`, we have found two words sharing a bucket and immediately return `(bucket[idx], word)`; if the loop finishes without a repeat, it returns `None`."*
- **Line-by-Line & Variable Breakdown:**
  - `bucket = {}` (Line 55): Lookup dictionary mapping **`int` (bucket index `0 .. capacity-1`) → `str` (first word seen at that index)**. *(Note: the official solution names this variable `seen = {}`; if asked about the name `bucket`, clarify immediately: "Its keys are integer bucket indices and its values are the first word that landed in each bucket!")*
  - `idx = bucket_index(word, capacity)` (Line 59): Computes `hash(word) % capacity`.
  - `if idx not in bucket: bucket[idx] = word` (Lines 60–61): `O(1)` hash-table check in Python's `dict` — records `word` as the occupant of bucket `idx`.
  - `else: return (bucket[idx], word)` (Lines 62–63): Second hit on `idx`! Returns `(first_word, second_word)` in the exact order encountered, short-circuiting the rest of `words`.
  - `try ... except: return None` (Lines 58–65): Defensive wrapper (not in the official solution) — know its exact side effects below!

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `words`: `Iterable[str]`, `capacity`: `int`
  - `bucket`: `dict[int, str]`, `idx`: `int`
  - Return type: `tuple[str, str] | None`
- **Concrete Step-by-Step Trace (Suppose in this Python process run: `"cat" -> 5`, `"dog" -> 2`, `"emu" -> 5` for `capacity = 8`):**
  1. Start: `bucket = {}`.
  2. `word = "cat"`: `idx = 5`. `5 not in bucket` → `bucket = {5: "cat"}`.
  3. `word = "dog"`: `idx = 2`. `2 not in bucket` → `bucket = {5: "cat", 2: "dog"}`.
  4. `word = "emu"`: `idx = 5`. `5 not in bucket` is `False` → enters `else:` → immediately returns `('cat', 'emu')` without ever inspecting the remaining 9 words!
- **"What If the Caller Passed...?" (Edge Cases — KNOW #1 & #2 COLD!):**
  1. **Duplicate identical words, e.g. `find_collision(["cat", "cat"], 8)` (SUBTLE BUG IN BOTH YOUR CODE AND THE OFFICIAL SOLUTION!):**
     - Iteration 1: `"cat"` → `bucket[idx] = "cat"`.
     - Iteration 2: `"cat"` → `idx` is already in `bucket` → **returns `('cat', 'cat')`**!
     - Wait: the docstring says *"Return two **different** words from `words` sharing a bucket"* (`first != second`)! Both your code and `W04_Solutions` assumed `words` contained distinct strings.
     - *Instant fix if asked:* Change `else:` to `elif bucket[idx] != word: return (bucket[idx], word)`! Mentioning this shows razor-sharp code reading.
  2. **`capacity = 0` or `words = [[1, 2], "cat"]` (Effect of your `try / except`):**
     - Because of `except: return None` on lines 64–65, `find_collision(["cat", "dog"], 0)` catches `ZeroDivisionError` and **returns `None`** instead of crashing, and `find_collision([[1, 2], "cat", "dog"], 1)` catches `TypeError` on `[1, 2]` and **immediately returns `None`** (aborting the loop!). Without `try / except`, those invalid inputs would raise `ZeroDivisionError` / `TypeError`.
  3. **`capacity = 1` with `["cat", "dog"]`:**
     - Every integer `% 1` equals `0`! `"cat"` sets `bucket[0] = "cat"`, `"dog"` gets `idx = 0` and immediately returns `('cat', 'dog')`.
  4. **`words = []` or `words = ["cat"]`:**
     - Returns `None` cleanly (`0` or `1` word can never produce a pair).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity (Pigeonhole Principle Bound — 10/10 Answer!):**
  - Let `m = len(words)` (distinct words of `O(1)` length) and `C = capacity`.
  - **How many loop iterations can possibly run when `C = 8` and `m = 1,000,000`?** At most **`9` (`C + 1`)**! By the **Pigeonhole Principle**, once `8` words occupy all `8` buckets `0..7`, the **9th** distinct word *must* hit an already-occupied bucket and return!
  - Therefore:
    - **Time Complexity:** **`O(min(m, C))`** average case (assuming distinct words and `O(1)` dict ops)! *(Even if `words` has millions of duplicates of `"cat"` with the duplicate-fix applied, worst-case scan is `O(m)`.)*
    - **Space Complexity:** **`O(min(m, C))`**, because `bucket` holds at most `1` entry per bucket index, so `len(bucket) <= C` always!
- **Why Naive Pairwise Search Would Be Worse:**
  - Checking all pairs with nested loops `for i ... for j ...` without a `seen`/`bucket` dict would take `O(min(m, C)^2)` (`O(m^2)` when no collision exists, e.g. `C = 10_000_000`) instead of `O(m)`! Using a hash table (`bucket = {}`) to find a hash-table collision reduces `O(m^2)` to `O(m)`!
- **Birthday Paradox & Python String Hash Randomization:**
  - **Birthday Paradox:** You don't even need `C + 1` random words to likely see a collision — collisions reach >50% probability at around $\sqrt{C}$ words ($\approx 1.18\sqrt{C}$; e.g., ~`3,700` words for `10,000,000` buckets, or ~`3–4` words for `8` buckets!). With `12` words in `10,000,000` buckets (`66` pairs), collision probability is only $\frac{66}{10^7} \approx 0.00066\%$.
  - **Why does `find_collision` return a different pair every time you re-run Python?** CPython uses **SipHash** seeded with random OS bytes at startup (`PYTHONHASHSEED`) so external attackers cannot pre-compute thousands of colliding string keys to launch a **Hash-Flooding Denial-of-Service (`O(n^2)`) attack** against web servers!

### Likely Interview Q&A
1. **Q: With `12` distinct words and `capacity = 8`, could `find_collision` ever return `None`? What is the maximum number of words it inspects?**  
   **A:** Never — by the **Pigeonhole Principle**, `8` buckets can hold at most `8` non-colliding words, so by the **9th** word at the very latest a bucket index must repeat! It inspects between `2` (best case) and `9` (worst case) words.
2. **Q: What are the keys and values in your `bucket = {}` dictionary on line 55?**  
   **A:** Each key is an `int` bucket index (`0` through `capacity - 1`), and its value is the `str` — the first word from `words` that hashed into that bucket.
3. **Q: Why can we hardcode `3` and `11` colliding in a doctest, yet we couldn't hardcode two colliding strings in `E04`'s doctest?**  
   **A:** In CPython, small integers hash deterministically to themselves (`hash(3) == 3`, `hash(11) == 11`) in every run, whereas strings are salted with a fresh random seed per Python process (`PYTHONHASHSEED`) to prevent hash-flooding DoS attacks.

---

## `E05_delitem.py` — `SimpleDict.__delitem__`

- **File:** [E05_delitem.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py) (Compare: [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E05_delitem.py))
- **Class / Symbol:** [`SimpleDict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L23-L125), [`SimpleDict.__delitem__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L75-L125)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
    def __delitem__(self, key):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.n -= 1
                return
        raise KeyError(key)
```
*(Matches the [Official Solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_04/W04_Solutions/E05_delitem.py#L119-L125) line-for-line!)*

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"This implements Python's `del d[key]` operator by hashing `key` to jump straight to its single candidate bucket, scanning that bucket with `enumerate` to find the `(k, v)` pair where `k == key`, deleting index `i` from the bucket list, decrementing `self.n`, and returning — or raising `KeyError(key)` if the bucket doesn't contain `key`."*
- **Line-by-Line & Variable Breakdown:**
  - `bucket = self._bucket(key)` (Line 119): Evaluates `self.buckets[hash(key) % self.capacity]`, giving a direct reference to the inner Python `list` where `key` must live if present.
  - `for i, (k, v) in enumerate(bucket):` (Line 120): Unpacks both the list index `i` (needed for `del bucket[i]`) and the stored tuple `(k, v)`.
  - `if k == key:` (Line 121): Must still test equality `==`, because colliding keys share the same `bucket`!
  - `del bucket[i]` (Line 122): Mutates the bucket `list` in-place (which in turn mutates `self.buckets[idx]` because `bucket` is a reference to that list, not a copy!).
  - `self.n -= 1` (Line 123): Keeps the cached size invariant accurate so `len(d)` and the load-factor check `self.n > 0.75 * self.capacity` stay truthful!
  - `return` (Line 124): Exits immediately (returning `None`, as required by `__delitem__`). **Crucial:** mutating `bucket` with `del bucket[i]` while iterating `bucket` is *only* safe because we `return` on the very next line and never continue the loop!
  - `raise KeyError(key)` (Line 125): Reached if `bucket` was empty or held only colliding keys != `key`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `self`: `SimpleDict`, `key`: `Hashable`
  - `bucket`: `list[tuple[Hashable, Any]]`, `i`: `int`, `k`: `Hashable`, `v`: `Any`
  - Return type: `None` (or raises `KeyError` / `TypeError`)
- **Concrete Step-by-Step Trace on Colliding Keys (`capacity = 8`, `d[3] = "three"`, `d[11] = "eleven"`, then `del d[3]`):**
  1. Before `del d[3]`: `d.n == 2`, `d.buckets[3] == [(3, 'three'), (11, 'eleven')]`, all other 7 buckets are `[]`.
  2. `del d[3]` invokes `SimpleDict.__delitem__(d, 3)`.
  3. `bucket = d._bucket(3)` → `d.buckets[3]` → `[(3, 'three'), (11, 'eleven')]`.
  4. Loop `i = 0, (k, v) = (3, 'three')`: `3 == 3` is `True`!
  5. `del bucket[0]` shifts `(11, 'eleven')` left into index `0` → `d.buckets[3]` is now `[(11, 'eleven')]`.
  6. `d.n -= 1` → `d.n` becomes `1`.
  7. `return` → exits cleanly; subsequent `d[11]` checks `d.buckets[3][0]` and still finds `'eleven'`!
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Deleting a missing key `del d["emu"]` or deleting the same key twice (`del d["cat"]; del d["cat"]`):**
     - Scans 1 bucket (0 or ~1 items), falls out of `for` loop, raises **`KeyError: 'emu'`** / **`KeyError: 'cat'`**.
  2. **Deleting a key that collides with a present key, e.g. `d[3] = "three"; del d[11]` (`capacity = 8`):**
     - `d._bucket(11)` returns `[(3, 'three')]` (non-empty bucket!). Loop checks `3 == 11` (`False`), finishes loop, raises **`KeyError: 11`** without touching `(3, 'three')`!
  3. **Deleting an unhashable key `del d[[1, 2]]`:**
     - `self._bucket([1, 2])` calls `hash([1, 2])` and raises **`TypeError: unhashable type: 'list'`** (matching built-in `dict`!).
  4. **Inserting 10,000 items then deleting all 10,000 items:**
     - `len(d)` correctly drops to `0`, **but `d.capacity` stays at `16384`** because `SimpleDict` has no `_shrink()` method!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Complexity:**
  - **Average case:** `self._bucket(key)` is `O(1)`, and because `_grow()` caps the load factor $\alpha \le 0.75$, the expected bucket length is $< 1$, so scanning `bucket` and shifting elements in `del bucket[i]` takes **`O(1)`** time!
  - **Worst case:** If all `n` keys hash/collide into the **same** bucket, `bucket` has length `n`, so scanning and shifting `del bucket[i]` takes **`O(n)`** time.
  - **Auxiliary Space:** **`O(1)`**.
- **Separate Chaining vs Open Addressing Deletion ([Lines 128–135](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L128-L135) — PRIME 10/10 QUESTION!):**
  - *Why is `del` so easy in `SimpleDict` (`del bucket[i]`), yet notoriously tricky in CPython's real `dict`?*
  - **`SimpleDict` uses Separate Chaining:** Each bucket is an isolated list. Deleting `(3, 'three')` from `buckets[3]` shifts `(11, 'eleven')` forward inside `buckets[3]`, so `11` is still right there in `buckets[3]`!
  - **Real CPython `dict` uses Open Addressing:** All pairs live directly in one flat table array; when `11` collides with `3` at slot `3`, `11` probes forward into e.g. slot `4`. If `del d[3]` simply reset slot `3` to `EMPTY`, a future lookup `d[11]` would hit `EMPTY` at slot `3` and **stop probing early**, falsely claiming `11` isn't in the dict! Therefore, open-addressed hash tables must overwrite deleted slots with a **tombstone / dummy sentinel** ("keep probing past me, an item used to live here"), and periodically rebuild the table to clear accumulated tombstones!
- **Bonus Trade-off (Why not shrink `capacity` at `< 0.375`?):**
  - If you grew at `> 0.75` (doubling capacity so load factor becomes `0.375`) and immediately shrunk whenever `< 0.375`, alternating `d[k] = 1` and `del d[k]` right on the threshold would trigger an `O(n)` resize on *every single operation* (**thrashing**)! Dynamic tables that support shrinking wait until load factor drops below **`0.25`** (hysteresis) to preserve `O(1)` amortized cost.

### Likely Interview Q&A
1. **Q: Why is it usually dangerous to do `del L[i]` inside `for i, x in enumerate(L):`, and why doesn't your `__delitem__` have that bug?**  
   **A:** Deleting index `i` shifts `L[i+1]` into `L[i]`, while `enumerate` advances to `i+1` on the next iteration — skipping an element! My `__delitem__` is completely safe **only because** dictionary keys are unique and line 124 executes `return` immediately after `del bucket[i]`, never taking another step of the loop.
2. **Q: What would break if you forgot `self.n -= 1` on line 123?**  
   **A:** Two things: `len(d)` would stay artificially high (counting deleted items), and `__setitem__`'s `if self.n > 0.75 * self.capacity: self._grow()` would keep doubling `self.buckets` indefinitely during repeated insert-then-delete cycles even when the dictionary only held 1 real item!
3. **Q: Why couldn't you write `bucket.remove((key, value))` instead of `enumerate` + `del bucket[i]`?**  
   **A:** Because `__delitem__(self, key)` is only passed `key` — we don't know `value` until we scan `bucket` to find the tuple whose first element equals `key`!

---

## `E06_fast_contains.py` — `SimpleDict.__contains__` & The 3 Benchmark Questions

- **File:** [E06_fast_contains.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py) *(Capstone Extension Exercise — no official solution file released)*
- **Class / Symbols:** [`SimpleDict.__contains__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L100-L150), [`time_in`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L156-L168), [`row`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L184-L201), [`# ANSWER`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L218-L235)
- **Difficulty Tier:** `Hard (8–10 Mark Target)` (**Highest-probability 8–10 mark discussion in Week 04!**)

### Your Submitted Code
```python
    def __contains__(self, key):
        bucket = self._bucket(key)
        for k, v in bucket:
            if k == key:
                return True
        return False
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** *"This hooks Python's `key in d` operator directly into `SimpleDict`'s hash table by computing `self._bucket(key)` in `O(1)` time and scanning only that single short bucket list for `k == key`, returning `True` on a match or `False` otherwise instead of letting Python fall back to an `O(n)` full-table iteration via `__iter__`."*
- **Line-by-Line & Variable Breakdown:**
  - `def __contains__(self, key):` (Line 100): Special dunder method invoked automatically whenever Python evaluates `key in d` or `key not in d` (`not (key in d)`).
  - `bucket = self._bucket(key)` (Line 146): Hashes `key` and indexes `self.buckets[hash(key) % self.capacity]` — ruling out the other `capacity - 1` buckets in one `O(1)` step!
  - `for k, v in bucket:` (Line 147): Loops over the `(key, value)` pairs inside that single bucket (typically `0` or `1` pair when load factor $\le 0.75$).
  - `if k == key: return True` (Lines 148–149) / `return False` (Line 150): Short-circuits `True` on match, or returns `False` once the tiny bucket is exhausted.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `self`: `SimpleDict`, `key`: `Hashable`
  - `bucket`: `list[tuple[Hashable, Any]]`
  - Return type: `bool` *(note: even if a custom `__contains__` returned a truthy/falsy value, Python's `in` operator coerces the result to strict `bool`!)*
- **Concrete Step-by-Step Trace (`n = 8000` keys, where `capacity = 16384`):**
  - **Without `__contains__` (`SimpleDictNoContains` from `E01`):** `"xyz!" in d` (absent key) sees no `__contains__`, calls `d.__iter__()`, steps through **all `16,384` bucket lists** and compares `"xyz!" == k` against **all `8,000` stored keys** → takes **`689.2` µs**!
  - **With `__contains__` (`E06`):** `"xyz!" in d` calls `d.__contains__("xyz!")`, computes `hash("xyz!") % 16384` (say `9412`), inspects `d.buckets[9412]` (which has ~`0` or `1` item since $\alpha = 8000 / 16384 \approx 0.49$), sees no match, returns `False` → takes **`0.28` µs** (~**2,460x faster** at `n = 8000`!).
- **"What If the Caller Passed...?" (Edge Cases):**
  1. **Empty dictionary `"cat" in SimpleDict()`:**
     - `capacity = 8`, `self._bucket("cat")` is `[]`, `for` loop runs `0` times, returns `False` cleanly.
  2. **Unhashable key `[1, 2] in d` (FASCINATING BEHAVIOR CHANGE BETWEEN E01 AND E06!):**
     - In `PairListDict` AND in `SimpleDictNoContains` (`E01`): `[1, 2] in d` **returns `False`** without raising an error, because `__iter__` fallback only tests `k == [1, 2]` and never calls `hash([1, 2])`!
     - In `SimpleDict` (`E06`, with `__contains__`) AND in Python's real `dict`: `[1, 2] in d` calls `self._bucket([1, 2])` → `hash([1, 2])` → **raises `TypeError: unhashable type: 'list'`**!
  3. **Value `None` stored under key (`d["cat"] = None`):**
     - `"cat" in d` returns **`True`**! *(Notice why a naive implementation like `return d.get("cat") is not None` would be buggy when `None` is a legitimate value!)*
  4. **Colliding keys after `del` (`d[3] = "three"; d[11] = "eleven"; del d[3]`):**
     - `3 in d` checks `buckets[3]` (`[(11, 'eleven')]`), sees `11 != 3`, returns `False`; `11 in d` sees `11 == 11`, returns `True`.

### Pillar 3 — Analyse (Complexity, Alternative Implementation & The 3 Benchmark Questions)
- **Complexity:**
  - **Time:** **`O(1)` average** (expected bucket length $\alpha \le 0.75$), **`O(n)` worst-case** (pathological all-keys-collide scenario).
  - **Space:** **`O(1)`** auxiliary memory.
- **Alternative Comparison (`for k, v in bucket` vs `try: self[key]`):**
  - You could write `__contains__` by reusing `__getitem__`:
    ```python
    try:
        self[key]
        return True
    except KeyError:
        return False
    ```
  - **Why your direct bucket loop is BETTER:** In Python, `try` is nearly free when no exception occurs, **but raising, instantiating, and catching `KeyError` when a key is absent is relatively expensive**! With your loop, an absent key simply finishes a 0–1 item loop and executes `return False` (`0.28` µs — actually *faster* than a present key at `0.29` µs!). With `try / except KeyError`, absent keys would be noticeably slower than present keys due to exception-handling overhead.

### Deep Dive on Your Embedded Benchmark Table & 3 Questions ([Lines 218–235](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L218-L235))

Here is the exact table from your file:
```text
       |    PairListDict |SimpleDict (E01) |  + __contains__
     n | present  absent | present  absent | present  absent
   500 |     7.6    14.3 |    22.4    45.6 |    0.29    0.28
  2000 |    31.6    60.3 |    91.5   173.7 |    0.29    0.28
  8000 |   125.3   234.1 |   375.0   689.2 |    0.29    0.28
```
Notice the scaling down each column when `n` **quadruples** (`500 -> 2000 -> 8000`):
- `PairListDict` quadruples (`7.6 -> 31.6 -> 125.3` µs) → **`O(n)`**.
- `SimpleDict (E01)` quadruples (`22.4 -> 91.5 -> 375.0` µs) → **`O(n)`**.
- `+ __contains__` stays completely flat (`0.29 -> 0.29 -> 0.29` µs) → **`O(1)`**.

Now review the 3 questions — **especially Question 2, where your written comment missed the `n / 2` math!**

1. **Question 1:** *Why does `SimpleDict (E01)` come out ~3x SLOWER than `PairListDict` (`375 µs` vs `125 µs`), when `E01` showed it hundreds of times faster at `d[k]`?*
   - **Your comment:** Correctly noted `SimpleDict` goes through every bucket while `PairListDict` goes through a flat list.
   - **10/10 Verbal Answer:** Because `E01`'s `SimpleDict` lacks `__contains__`, `k in d` ignores hashing completely and falls back to `__iter__`! Both classes do an `O(n)` generator scan, **but** `PairListDict.__iter__` iterates one contiguous flat list of `8,000` tuples (`O(n)`), whereas `SimpleDict.__iter__` runs a nested loop over **`16,384` separate heap-allocated bucket lists** (`O(capacity + n)`), more than half of which are empty, paying extra loop, pointer-chasing, and cache-miss overhead!

2. **Question 2 (CRITICAL — SHARPEN YOUR WRITTEN ANSWER!):** *Why does an absent key cost about **twice** what a present one costs for the first two columns (`14.3` vs `7.6`, `234.1` vs `125.3`), but the **same** (`0.28` vs `0.29`) for the third?*
   - **Watch out in your comment ([L229–230](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L229-L230)):** You wrote *"For the first two it must look through every item to conclude if the item is present or absent."* Wait — if it looked through *every* item when **present** too, present and absent would take the **same** time, not a `1 : 2` ratio!
   - **10/10 Verbal Answer (Give the `n / 2` vs `n` math!):**
     - **First two columns (`__iter__` linear scan):** When a key is **present** (and our `100` probes are spread uniformly from start to end of the dictionary), Python's `in` operator **stops early (short-circuits)** as soon as it hits `k == key` — so on average it checks **`n / 2`** keys (half the dictionary)! When a key is **absent**, it can *never* stop early — it must scan **all `n` keys** (`100%` of the dictionary) to be sure it isn't there. Scanning `n` items takes **twice as long (`2x`)** as scanning `n / 2` items!
     - **Third column (`+ __contains__`):** Both present and absent compute `hash(key) % capacity` once and check **only one bucket**. At `n = 8000` and `capacity = 16384`, average bucket length is $\frac{8000}{16384} \approx 0.49$ items — so whether the key is present or absent, Python hashes once and inspects at most ~`0–1` tuple (`O(1)`), costing `~0.28–0.29` µs either way!

3. **Question 3:** *Which change made `in` fast — hashing, or writing `__contains__`?*
   - **10/10 Verbal Answer:** **Both together — neither works alone!** `SimpleDict (E01)` *already* had hashing, buckets, and `_grow()`, yet `in` took `689 µs` because Python didn't know `in` could use `_bucket(key)` and fell back to `__iter__`. Conversely, adding `__contains__` to `PairListDict` without hash buckets would still be `O(n)`. Hashing built the `O(1)` data structure; `__contains__` wired Python's `in` operator to use it.

### Likely Interview Q&A
1. **Q: Look at `row(n)` on line 191: why did the benchmark pick `present = [keys[i * n // 100] for i in range(100)]` instead of `keys[:100]`?**  
   **A:** `PairListDict` appends keys in insertion order and searches from index `0`! If we probed `keys[:100]`, every lookup in `PairListDict` would finish within the first 100 slots regardless of whether `n` was `500` or `8,000` — making `PairListDict` falsely appear `O(1)`! Spreading probes across all indices measures true average-case `n / 2` work.
2. **Q: Why is `absent` (`0.28` µs) actually a tiny bit faster than `present` (`0.29` µs) in the `+ __contains__` column?**  
   **A:** At `n = 8000` and `capacity = 16384`, the load factor is `8000 / 16384 ≈ 0.49`, meaning **over half the buckets are completely empty (`[]`)**! An absent key landing in an empty bucket executes `0` loop iterations and `0` string equality comparisons `k == key`, whereas a present key *always* lands in a non-empty bucket and does at least `1` tuple unpack and `k == key` check!
3. **Q: Could you implement `__getitem__` using `__contains__`, or `__contains__` using `__getitem__`?**  
   **A:** Implementing `__getitem__` by calling `if key in self:` first would hash and scan the bucket *twice*. Implementing `__contains__` via `try: self[key]; return True except KeyError: return False` only hashes once, so it's `O(1)`, but raising/catching `KeyError` on every absent key has much higher constant overhead than returning `False` from a 4-line bucket loop.

---

## Week 04 Watchlist — Subtle Quirks in Your Submitted Code

Review these 5 points right before your interview so nothing catches you off guard:

1. **[`E03_is_hashable.py` L51](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L51) (Bare `except:`):** You wrote `except:` instead of `except TypeError:`. Acknowledge immediately if asked that `except TypeError:` is cleaner so `KeyboardInterrupt` / `SystemExit` aren't caught.
2. **[`E03_is_hashable.py` L55–L56](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E03_is_hashable.py#L55-L56) (Why mutable hashes break dicts):** Don't say *"unless we update the hash every time it changes"* — explain that *even if* the hash updated on mutation, the key would now hash to a **different bucket** while sitting stored in its **old bucket**, making it unfindable!
3. **[`E04_string_collision.py` L60–L65](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E04_string_collision.py#L60-L65) (Duplicate words & `try/except`):**
   - Passing duplicate words `["cat", "cat"]` returns `("cat", "cat")` instead of two *different* words (fix: `elif bucket[idx] != word:`).
   - Your `try ... except: return None` swallows `ZeroDivisionError` (`capacity = 0`) and `TypeError` (unhashable element in `words`), returning `None`.
4. **[`E05_delitem.py` L122–L124](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E05_delitem.py#L122-L124) (`del` during loop & Open Addressing):** Remember `del bucket[i]` inside `for i, ... in enumerate(bucket)` is *only* safe because `return` executes immediately, and be ready to contrast separate-chaining list deletion with open-addressing **tombstones**!
5. **[`E06_fast_contains.py` L229–L230](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W04/E06_fast_contains.py#L229-L230) (Benchmark Question 2 — `n / 2` vs `n`):** Your written comment didn't explain *why* absent is **2x** slower than present in columns 1 & 2. In the live interview, state clearly: **present keys short-circuit halfway through on average (`n / 2` checks), whereas absent keys must scan all `n` keys (`2 * (n / 2)` = 2x time)!**
