# Week 1 Interview Preparation Guide — Sequences, Loops, Slicing & Higher-Order Iteration

⬅️ **Back to:** [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Week 1 Core Topics:** Indexing & slicing (`start:stop:step`), `for`/`while` loops, list & scalar accumulators, Collatz (hailstone) sequences, modular arithmetic & Caesar cipher cryptanalysis, higher-order functions (`iterate`), lexical closures, Newton–Raphson root-finding, and Euclid's GCD algorithm.

---

## Table of Contents

1. [Summary Table of Week 1 Exercises](#summary-table-of-week-1-exercises)
2. [Watchlist Before You Walk In (Your Code's Quirk Audit)](#watchlist-before-you-walk-in-your-codes-quirk-audit)
3. [Reference Context — `E01_newton.py`](#reference-context--e01_newtonpy)
4. [`E02_first_last.py` — `first_last`](#e02_first_lastpy--indexing--returning-a-tuple)
5. [`E03_slices.py` — `middle`, `last_three`](#e03_slicespy--sequence-slicing)
6. [`E04_count_vowels.py` — `count_vowels`](#e04_count_vowelspy--looping-over-a-string)
7. [`E05_squares.py` — `squares`](#e05_squarespy--building-a-list-with-append)
8. [`E06_cumsum.py` — `cumsum`](#e06_cumsumpy--the-accumulator-pattern)
9. [`E07_product.py` — `product`](#e07_productpy--multiplicative-accumulator)
10. [`E08_palindrome.py` — `is_palindrome`](#e08_palindromepy--slicing-with-a-negative-step)
11. [`E09_hailstones.py` — `hailstones`, `longest_hailstone`](#e09_hailstonespy--collatz-sequences--composition)
12. [`E10_hailstones_iterate.py` — `hailstone_step`, `reaches_one`](#e10_hailstones_iteratepy--higher-order-iteration)
13. [`E11_rotate.py` — `rotate`](#e11_rotatepy--modular-rotation-with-slicing)
14. [`E12_caesar_shifts.py` — `all_shifts`](#e12_caesar_shiftspy--brute-force-caesar-decoding)
15. [`E13_caesar_crack.py` — `english_score`, `crack`](#e13_caesar_crackpy--automated-cipher-cracking)
16. [`E14_newton_cbrt.py` — `newton_cbrt`](#e14_newton_cbrtpy--cube-roots-via-iterate--closures)
17. [`E15_gcd.py` — `gcd`](#e15_gcdpy--euclids-algorithm-via-tuple-state-iteration)

---

## Summary Table of Week 1 Exercises

*Input size variables:* `n = len(s)` or `len(L)` (or integer input `n` in `E05`/`E09`/`E10`), $L(n)$ = Collatz stopping length starting at `n`, `m = limit` in `E09`.

| Exercise | Function(s) | Difficulty Tier | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| [E01_newton.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py) | [`newton_sqrt`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py#L16-L45) | Reference *(Modified!)* | `O(min(100, log x + log log(1/tol)))` | `O(1)` |
| [E02_first_last.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E02_first_last.py) | [`first_last`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E02_first_last.py#L11-L26) | `Warm-up` | `O(1)` | `O(1)` |
| [E03_slices.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py) | [`middle`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L11-L21), [`last_three`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L23-L33) | `Warm-up` | `middle`: `O(n)` · `last_three`: `O(1)` | `middle`: `O(n)` · `last_three`: `O(1)` |
| [E04_count_vowels.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E04_count_vowels.py) | [`count_vowels`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E04_count_vowels.py#L11-L28) | `Warm-up` | `O(n)` | `O(1)` |
| [E05_squares.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E05_squares.py) | [`squares`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E05_squares.py#L11-L26) | `Warm-up` | `O(n)` | `O(n)` *(output)* / `O(1)` *(aux)* |
| [E06_cumsum.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E06_cumsum.py) | [`cumsum`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E06_cumsum.py#L11-L31) | `Warm-up` | `O(n)` | `O(n)` *(output)* / `O(1)` *(aux)* |
| [E07_product.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E07_product.py) | [`product`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E07_product.py#L11-L30) | `Warm-up` | `O(n)` | `O(1)` |
| [E08_palindrome.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E08_palindrome.py) | [`is_palindrome`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E08_palindrome.py#L11-L30) | `Warm-up` | `O(n)` | `O(n)` |
| [E09_hailstones.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py) | [`hailstones`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L15-L38), [`longest_hailstone`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L44-L60) | `Moderate` | `O(L(n))` · `O(sum_{i=1}^{m-1} L(i))` | `O(L(n))` · `O(max_{i<m} L(i))` |
| [E10_hailstones_iterate.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py) | [`hailstone_step`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py#L22-L34), [`reaches_one`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py#L37-L49) | `Moderate` | `O(1)` per helper (`O(L(n))` via `iterate`) | `O(1)` |
| [E11_rotate.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E11_rotate.py) | [`rotate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E11_rotate.py#L11-L30) | `Moderate` | `O(n)` | `O(n)` |
| [E12_caesar_shifts.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py) | [`all_shifts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py#L26-L45) | `Moderate` | `O(n)` *(specifically `26 * O(n)`)* | `O(n)` *(26 strings of len `n`)* |
| [E13_caesar_crack.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py) | [`english_score`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L34-L51), [`crack`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L54-L74) | `Hard (8–10 Mark Target)` | `english_score`: `O(n)` · `crack`: `O(n)` | `english_score`: `O(1)` · `crack`: `O(n)` |
| [E14_newton_cbrt.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py) | [`newton_cbrt`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L22-L49) | `Hard (8–10 Mark Target)` | `O(log |x| + log log(1/tol))` | `O(1)` |
| [E15_gcd.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py) | [`gcd`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L22-L49) | `Hard (8–10 Mark Target)` | `O(log(min(a, b)))` | `O(1)` |

---

## Watchlist Before You Walk In (Your Code's Quirk Audit)

Know these specific spots in your submitted Week 1 code so you are **never caught off guard**:

1. **Missing uppercase check in [`english_score`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L49) (`E13_caesar_crack.py`):** The docstring says *"Upper case counts too"*, and in `E04` you used `"AEIOUaeiou"`, **but** in `E13` you wrote `if char in "etaoin":`. Passing `"ATTACK AT DAWN"` returns `0` instead of `8`! Doctests passed only because all three doctest inputs were lowercase.
2. **Implicit `None` return in [`done`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L44-L47) (`E15_gcd.py`):** You wrote `if (b == 0): return True` with no `else` branch. When `b != 0`, `done(x)` returns **`None`** (not `False`!). It works only because `None` is falsy in `if done(x):`.
3. **Shadowing built-in `list` in [`all_shifts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py#L42) (`E12`) and [`crack`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L69) (`E13`):** Naming a local variable `list = []` hides Python's built-in `list()` constructor inside that function scope. Similarly, in `E05` local `squares = []` shadows the function name `squares`.
4. **Rewritten [`newton_sqrt`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py#L33-L45) in `E01_newton.py`:** Unlike the lecture version (`if x < 0: raise ValueError(...)` + `while True:`), your `E01_newton.py` caps at `count < 100` with no negative guard: `newton_sqrt(-1)` raises `ZeroDivisionError`, and `newton_sqrt(-4)` silently returns `-0.9069...`.
5. **Redundant boolean expressions & minor typo:** `palindome = s[::-1]; if palindome == s: return True` in `E08` (typo `palindome`, redundant `if/return True/False`) and `return True if n == 1 else False` in `E10` (`return n == 1`).

---

## Reference Context — `E01_newton.py`

- **File:** [E01_newton.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py)
- **Function:** [`newton_sqrt(x, tol=1e-10)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E01_newton.py#L16-L45)
- **Official Lecture Reference:** [W01_Solutions/E01_newton.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E01_newton.py)

### Your Submitted Code
```python
def newton_sqrt(x, tol=1e-10):
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0
    
    guess = x
    count = 0 # set a limit
    while(count < 100):
        count += 1
        guess = ((guess +(x/guess)) / 2)
        if(abs((guess * guess) - x) < tol):
            return guess
    return guess
```

### Core Concepts (Essential for `E14_newton_cbrt.py`)
1. **Heron's / Newton–Raphson Update Formula:**  
   We want the positive root of $f(g) = g^2 - x = 0$. Applying Newton's step $g_{\text{next}} = g - \frac{f(g)}{f'(g)}$ with $f'(g) = 2g$ gives:
   $$g_{\text{next}} = g - \frac{g^2 - x}{2g} = \frac{g + x / g}{2}$$
   **Intuition:** If $g > \sqrt{x}$, then $x / g < \sqrt{x}$ (and vice versa). The true square root always sits strictly between $g$ and $x/g$, so their arithmetic mean pulls the estimate rapidly toward $\sqrt{x}$ (**quadratic convergence**: the number of correct decimal digits roughly doubles each step near the root).
2. **Stopping Tolerance (`tol=1e-10`):**  
   Floating-point numbers have finite IEEE-754 64-bit precision (~15–17 significant digits), so `guess * guess == x` may *never* hold exactly (e.g. for `x = 2`). Instead we stop when the **residual** $|g^2 - x| < \text{tol}$.
3. **Important Differences Between Your `E01_newton.py` and the Lecture Version:**
   - The original starter/lecture file raised `ValueError` for `x < 0` and ran `while True:`.
   - You rewrote it with `while(count < 100):`. Be aware of three edge behaviors in your version:
     - **`newton_sqrt(-1)`:** Step 1 computes `(-1 + (-1 / -1)) / 2 = 0.0`; Step 2 computes `-1 / 0.0` and raises **`ZeroDivisionError: float division by zero`**.
     - **`newton_sqrt(-4)`:** Since $g^2 \ge 0 > -4$, $|g^2 - (-4)| \ge 4 > 10^{-10}$ forever. It oscillates for 100 steps and **silently returns `-0.9069396510403233`** instead of raising `ValueError`.
     - **Huge inputs (`x = 1e70`):** Far from the root, each step roughly halves `guess`. 100 halvings only divide by $2^{100} \approx 1.26 \times 10^{30}$, exiting the loop unconverged (`~7.9e39` instead of `1e35`).

---

## `E02_first_last.py` — Indexing & Returning a Tuple

- **File:** [E02_first_last.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E02_first_last.py)
- **Function:** [`first_last(L)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E02_first_last.py#L11-L26)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def first_last(L):
    return (L[0], L[-1])
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`first_last` takes any indexable non-empty sequence `L` and returns a 2-element tuple containing its first element at index `0` and its last element at negative index `-1`. Because both `str`, `list`, and `tuple` support integer subscripting in Python, the same one-liner works polymorphically across all sequence types."
- **Line-by-Line & Variable Breakdown:**
  - `L` (parameter): Named `L` by convention for a list/sequence, though duck typing allows any object implementing `__getitem__` with `0` and `-1` (including `str`, `tuple`, `range`).
  - `L[0]`: Fetches the element at offset `0` from the start.
  - `L[-1]`: Python translates negative index `-k` to `len(L) - k`, so `L[-1]` fetches `L[len(L) - 1]` without needing to call `len(L)` explicitly.
  - `(L[0], L[-1])`: Packs both values into an immutable `tuple` of length 2 (parentheses make the tuple literal visually explicit, though the comma `,` is what actually constructs a tuple in Python).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `L`: `Sequence[T]` (`list[T]`, `tuple[T, ...]`, `str`, `range`).
  - Return value: `tuple[T, T]` (specifically `tuple[str, str]` of 1-char strings when `L` is `str`).
- **Concrete Step-by-Step Trace (`first_last("hello")`):**
  1. `L = "hello"` (`str`, length 5).
  2. `L[0]` evaluates to `'h'`.
  3. `L[-1]` resolves index `5 - 1 = 4` and evaluates to `'o'`.
  4. Returns `('h', 'o')` (`tuple`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty list `[]` or empty string `""`:** Raises **`IndexError: list index out of range`** (or `string index out of range`) immediately when evaluating `L[0]`.
  - **Single-element sequence `[7]` or `"x"`:** Both `L[0]` and `L[-1]` resolve to index `0`, returning **`(7, 7)`** or **`('x', 'x')`** — the same element appears twice!
  - **A `set` `{1, 2, 3}` or generator `(x for x in range(3))`:** Sets and iterators are not subscriptable; raises **`TypeError: 'set' object is not subscriptable`**.
  - **A `dict` `{"a": 1, "b": 2}`:** Subscripting a `dict` looks up **keys**, not positions! It looks for key `0`, raising **`KeyError: 0`** (unless keys `0` and `-1` actually exist in the dict!).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(1)`** — Python lists and tuples are backed by contiguous arrays of pointers, and strings use fixed-width Unicode code-point arrays (PEP 393), so indexing `0` and `-1` is direct pointer arithmetic independent of `n = len(L)`.
- **Space Complexity:** **`O(1)`** — Allocates a single 2-tuple holding two object references (it does **not** copy the elements themselves).
- **Alternative Comparison:** Writing `L[len(L) - 1]` instead of `L[-1]` has the same `O(1)` complexity, but `L[-1]` is cleaner, faster (avoids a `len()` call and subtraction in Python bytecode), and idiomatic.

### Likely Interview Q&A
1. **Q: If `L = [[1, 2], [3, 4]]` and I mutate `first_last(L)[0].append(99)`, does `L` change?**  
   **A:** Yes! While the returned `tuple` itself is immutable (you cannot reassign `res[0] = ...`), its first slot holds a reference to the exact same inner list `L[0]`, so `.append(99)` mutates `L` to `[[1, 2, 99], [3, 4]]`.
2. **Q: Does `(L[0], L[-1])` need parentheses to return a tuple?**  
   **A:** Technically no — `return L[0], L[-1]` builds the exact same `tuple` because the comma creates the tuple, though parentheses improve readability.

---

## `E03_slices.py` — Sequence Slicing

- **File:** [E03_slices.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py)
- **Functions:** [`middle(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L11-L21), [`last_three(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L23-L33)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def middle(s):
    return s[1:-1]

def last_three(s):
    return  s[-3:]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`middle` uses half-open slice notation `s[1:-1]` to return a new sequence starting at index `1` up to—but excluding—the last element at index `-1`. `last_three` uses `s[-3:]` to slice from three positions before the end through the end of the sequence, automatically clamping to index `0` if `s` has fewer than three items."
- **Line-by-Line & Variable Breakdown:**
  - `s` (parameter): Named `s` for sequence/string; preserves exact sequence type (`str` returns `str`, `list` returns `list`, `tuple` returns `tuple`).
  - `s[1:-1]` ([`middle`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L21)): Start index `1` skips `s[0]`; stop index `-1` (`len(s) - 1`) is **exclusive**, dropping the last item.
  - `s[-3:]` ([`last_three`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L33)): Omitting `stop` means "slice all the way to `len(s)`" (note that `s[-3:-1]` would wrongly exclude the final element!).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `s`: `Sequence` (`str`, `list`, `tuple`, `range`).
  - Return value: Same concrete type as `s` (a fresh shallow copy).
- **Concrete Step-by-Step Trace:**
  - `middle([1, 2, 3, 4])`: `len(s) = 4`. Start = `1`, Stop = `4 - 1 = 3`. Collects indices `1, 2` -> returns `[2, 3]`.
  - `last_three("hi")`: `len(s) = 2`. Start = `max(0, 2 - 3) = 0`, Stop = `2`. Collects indices `0, 1` -> returns `'hi'`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty sequence `""` or `[]`:** Unlike indexing (`s[0]`), **slicing never raises `IndexError`**! Both `middle("")` and `last_three("")` return `""` (`[]` for `[]`).
  - **Length 1 (`middle("a")`) or Length 2 (`middle("ab")`):** For `"a"`, start `1` > stop `0` -> returns `""`. For `"ab"`, start `1` == stop `1` -> returns `""`.
  - **Why couldn't `last_three` be written `s[-3:0]`?** Because `0` is the very start of the sequence, so `s[-3:0]` with default step `+1` always has `start >= stop` and returns an empty sequence `""`! Omitting `stop` (`s[-3:]`) is the **only** clean way to include the last item without calling `len(s)`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time & Space Complexity (Crucial Contrast!):** Let `n = len(s)`.
  - [`middle(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L11-L21): **`O(n)` time** and **`O(n)` space**. Slicing in Python is **not** a zero-copy view (unlike NumPy arrays or Go slices) — it allocates a new sequence and copies `max(0, n - 2)` references!
  - [`last_three(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E03_slices.py#L23-L33): **`O(1)` time** and **`O(1)` space**! Even if `s` has 10 million elements, `s[-3:]` copies at most `3` elements (`min(3, n) <= 3`).
- **Alternative Comparison:** If you needed a zero-copy view of a huge buffer of bytes, `memoryview(b)[1:-1]` is `O(1)` time and space; for general iterables without slicing, `itertools.islice` streams lazily, though `s[1:-1]` is optimal when a materialized sequence is required.

### Likely Interview Q&A
1. **Q: Why is `middle` `O(n)` while `last_three` is `O(1)`, even though both are a single slice?**  
   **A:** A Python slice takes `O(k)` time and space where `k` is the length of the **output slice**. For `middle`, `k = n - 2` grows linearly with `n`; for `last_three`, `k <= 3` is bounded by a constant.
2. **Q: Why doesn't `last_three("hi")` raise `IndexError` when `-3` goes past the start of `"hi"`?**  
   **A:** Python's slice semantics clamp out-of-range `start` and `stop` indices to `[0, len(s)]` (`slice.indices(len(s))`), whereas single-element indexing enforces strict bounds.

---

## `E04_count_vowels.py` — Looping Over a String

- **File:** [E04_count_vowels.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E04_count_vowels.py)
- **Function:** [`count_vowels(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E04_count_vowels.py#L11-L28)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def count_vowels(s):
    vowels="AEIOUaeiou"
    count = 0
    for char in s:
        if char in vowels:
            count+=1
    return count
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`count_vowels` iterates through every character in `s` once, incrementing an integer counter whenever the character appears in the 10-character lookup string `'AEIOUaeiou'`. Including both uppercase and lowercase vowels in `vowels` handles case-insensitivity directly without allocating a lowercased copy of `s`."
- **Line-by-Line & Variable Breakdown:**
  - `vowels = "AEIOUaeiou"` (line 23): Constant lookup table holding all 10 ASCII vowel characters.
  - `count = 0` (line 24): Scalar accumulator initialized to the additive identity `0` so an empty string returns `0`.
  - `for char in s:` (line 25): Iterates directly over characters of `s` (descriptive name `char`, avoiding unnecessary `range(len(s))` indexing).
  - `if char in vowels:` (line 26): Tests substring/character membership; increments `count` by `1` on a match.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `s`: `str` (or `Iterable[str]`).
  - Locals: `vowels: str`, `count: int`, `char: str` (1-character string).
  - Return value: `int` (`>= 0`).
- **Concrete Step-by-Step Trace (`count_vowels("Hi!")`):**
  | Iteration | `char` | `char in "AEIOUaeiou"` | `count` after step |
  | :--- | :--- | :--- | :--- |
  | Init | — | — | `0` |
  | 1 | `'H'` | `False` | `0` |
  | 2 | `'i'` | `True` | `1` |
  | 3 | `'!'` | `False` | `1` |
  Returns `1`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty string `""`:** Loop body executes 0 times; returns `0`.
  - **Digits/punctuation `"123!@#"` or `"rhythm"`:** Returns `0` (`'y'` is treated as a consonant).
  - **A list of multi-character strings `["AE", "b"]` (Subtle `str` vs `set` quirk!):** Because `vowels` is a **`str`**, `in` checks **contiguous substring** containment! `"AE" in "AEIOUaeiou"` evaluates to **`True`**, returning `1`! If `vowels` were a `set`, `"AE" in set("AEIOUaeiou")` would be `False`.
  - **List of integers `[1, 2]`:** Raises **`TypeError: 'in <string>' requires string as left operand, not int`**.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** where `n = len(s)`. Loop runs `n` times; each `char in vowels` checks at most 10 characters, which is bounded by constant `10 = O(1)`.
- **Space Complexity:** **`O(1)`** auxiliary space!
  - **Why your code beats the official solution on space:** [W01_Solutions/E04_count_vowels.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E04_count_vowels.py#L24) wrote `for c in s.lower():`, which allocates a brand-new `n`-character string in **`O(n)`** auxiliary memory! Checking `"AEIOUaeiou"` avoids copying `s` altogether.
- **Alternative / Data Structure Comparison:**
  - **`set` vs `str` for `vowels`:** Using `VOWELS = set("AEIOUaeiou")` makes membership `O(1)` via hashing instead of linear scan `O(|vowels|)`. For 10 characters, C-level string search (`memchr`) is actually slightly faster than hashing, *but* if the target set grew to `k = 10,000` items, `str`/`list` membership would degrade to `O(n * k)` whereas `set` stays `O(n)`.
  - **Generator expression:** `sum(1 for char in s if char in "AEIOUaeiou")` — concise one-liner, same `O(n)` time and `O(1)` space.

### Likely Interview Q&A
1. **Q: Would changing `vowels` from a string to a `set` change the Big-O time complexity here?**  
   **A:** Not asymptotically for a fixed 10-letter alphabet—both are `O(n)` because `10` is a constant. However, if the alphabet size `m` were an input parameter, `in` on a string/list is `O(n * m)` whereas constructing a `set` once makes it `O(n + m)`.
2. **Q: Compare your `vowels = "AEIOUaeiou"` against calling `s.lower()` first.**  
   **A:** `s.lower()` allocates a second string of length `n` (`O(n)` extra space and an extra pass over `s`), whereas checking a 10-character string uses `O(1)` space in a single pass.

---

## `E05_squares.py` — Building a List with `append`

- **File:** [E05_squares.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E05_squares.py)
- **Function:** [`squares(n)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E05_squares.py#L11-L26)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def squares(n):
    squares = []
    
    for i in range(1, n+1):
        squares.append(i*i)

    return squares
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`squares` builds and returns a list of perfect squares from $1^2$ up to $n^2$ inclusive by iterating `i` over `range(1, n + 1)` and appending `i * i` on each pass. Using `n + 1` as the stop bound compensates for `range` being half-open."
- **Line-by-Line & Variable Breakdown:**
  - `squares = []` (line 21): List accumulator initialized empty. **Naming Watchout:** This local variable has the **exact same name** as the function `squares`! Inside `squares(n)`, local `squares` shadows the outer function object in the local namespace (harmless here since `squares` isn't recursive, but naming it `result` like the official solution avoids shadowing).
  - `range(1, n+1)` (line 23): Lazy sequence object generating integers `1, 2, ..., n`.
  - `squares.append(i*i)` (line 24): Multiplies `i * i` (faster than `i ** 2` in Python) and appends to the end of the list in place.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `n`: `int`.
  - Locals: `squares: list[int]`, `i: int`.
  - Return value: `list[int]`.
- **Concrete Step-by-Step Trace (`squares(3)`):**
  - `squares = []`, `range(1, 4)` yields `1, 2, 3`.
  - `i = 1`: `squares` -> `[1]`.
  - `i = 2`: `squares` -> `[1, 4]`.
  - `i = 3`: `squares` -> `[1, 4, 9]`. Returns `[1, 4, 9]`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`n = 0`:** `range(1, 1)` is empty -> loop doesn't run -> returns `[]`.
  - **Negative `n` (e.g. `squares(-5)`):** `range(1, -4)` with default step `+1` is empty -> returns `[]` without error.
  - **Float `n` (e.g. `squares(3.0)`):** `range(1, 4.0)` raises **`TypeError: 'float' object cannot be interpreted as an integer`**.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** (for `n >= 0`; `O(1)` for `n <= 0`). `list.append` runs in **amortized `O(1)`** time because CPython over-allocates the underlying pointer array geometrically (~1.125x growth factor) when resizing. Note: doing `squares = squares + [i*i]` instead of `.append()` would copy the entire list every step and degrade to **`O(n^2)`**!
- **Space Complexity:** **`O(n)`** for the returned list, and **`O(1)` auxiliary space** because `range(1, n + 1)` in Python 3 stores only `(start, stop, step)` rather than materializing `[1..n]` in memory.
- **Alternative Comparison:** List comprehension `[i * i for i in range(1, n + 1)]` is the idiomatic Python equivalent — same `O(n)` time/space, ~20–30% faster in CPython because it uses the dedicated `LIST_APPEND` bytecode instruction instead of looking up the `.append` method attribute on every iteration.

### Likely Interview Q&A
1. **Q: Why did you name the list `squares` inside `def squares(n)`, and could that ever cause a bug?**  
   **A:** Local `squares` shadows the function `squares` inside the local scope (`LEGB` rule). It works here because the function is iterative, but if I ever needed a recursive call inside the body, calling `squares(n - 1)` would raise `TypeError: 'list' object is not callable`. Naming it `result` is safer.
2. **Q: How much memory does `range(1, 10_000_000)` use by itself?**  
   **A:** `O(1)` (~48 bytes) — `range` is a lazy sequence object that computes values on demand rather than storing 10 million integers up front.

---

## `E06_cumsum.py` — The Accumulator Pattern

- **File:** [E06_cumsum.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E06_cumsum.py)
- **Function:** [`cumsum(L)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E06_cumsum.py#L11-L31)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def cumsum(L):
    result = []
    for i in L:
        if not result:
            result.append(i)
        else:
            result.append(i + result[-1])
    return result
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`cumsum` computes the running prefix sums of any iterable `L` in a single pass by storing the first item directly and adding each subsequent item to `result[-1]`, the previous cumulative sum. Because it always appends into a fresh `result` list, passing a tuple still returns a `list` without mutating the input."
- **Line-by-Line & Variable Breakdown:**
  - `result = []` (line 25): Output list that doubles as our state tracker via its last element `result[-1]`.
  - `for i in L:` (line 26): Iterates over each **element** of `L` (**Naming Watchout:** `i` usually means an *index*; `x` or `num` is clearer when iterating over values directly).
  - `if not result:` (line 27): True **only** on the very first iteration when `result` is empty `[]`, seeding `result` with `[i]` (since `result[-1]` would raise `IndexError` on an empty list).
  - `result.append(i + result[-1])` (line 30): Reads the previous running sum in `O(1)` time (`result[-1]`), adds the new item `i`, and appends the new running sum.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `L`: `Iterable[T]` (typically `list[int | float]` or `tuple[int | float, ...]`).
  - Locals: `result: list[T]`, `i: T`.
  - Return value: `list[T]`.
- **Concrete Step-by-Step Trace (`cumsum([0, 2, -1])` — Tricky Falsy-Zero Trace!):**
  | Step | `i` | `result` before | `not result` | Branch taken | `result` after |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | 1 | `0` | `[]` | `True` | `if` (`append(0)`) | `[0]` |
  | 2 | `2` | `[0]` | **`False`!** | `else` (`2 + 0`) | `[0, 2]` |
  | 3 | `-1` | `[0, 2]` | `False` | `else` (`-1 + 2`) | `[0, 2, 1]` |
  *Crucial observation on Step 2:* Even though `0` is falsy, `[0]` is a **non-empty list** (`len([0]) == 1`), so `bool([0])` is `True` and `not result` is `False`!
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty list `[]` or empty tuple `()`:** Loop runs 0 times; returns `[]`.
  - **Strings `cumsum(["a", "b", "c"])` (Cool bonus vs Official Solution!):** The [official solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E06_cumsum.py#L25-L29) initialized `total = 0; total += x`, which **crashes** with `TypeError: unsupported operand type(s) for +=: 'int' and 'str'` on `["a", "b", "c"]`! Your `if not result:` version avoids hardcoding `0` and cleanly returns `['a', 'ab', 'abc']` (though note string `+` across `n` strings would be `O(n^2)`).
  - **A generator `cumsum(x for x in [1, 2, 3])`:** Works cleanly and returns `[1, 3, 6]`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** where `n = len(L)` (for numbers). Each iteration performs an `O(1)` truthiness check, `O(1)` `result[-1]` lookup, `O(1)` addition, and amortized `O(1)` `.append()`.
  - *Contrast with the naive trap:* Computing `[sum(L[:k+1]) for k in range(len(L))]` recomputes every prefix from scratch: $1 + 2 + \dots + n = \frac{n(n+1)}{2} =$ **`O(n^2)`**! Reusing the previous prefix sum (`result[-1]` or `total`) is dynamic programming in miniature, cutting `O(n^2)` down to `O(n)`.
- **Space Complexity:** **`O(n)`** for `result` (`O(1)` auxiliary memory).
- **Alternative Comparison:**
  - **Scalar accumulator (`total = 0`):** Slightly faster per iteration because it avoids the `if not result:` branch and `result[-1]` subscript, at the minor cost of assuming numeric (`0`-compatible) inputs.
  - **Standard library:** `list(itertools.accumulate(L))` runs in C in `O(n)` time and also handles non-numeric types without an initial `0`!

### Likely Interview Q&A
1. **Q: What happens if the first element of `L` is `0`, i.e., `cumsum([0, 5])`? Doesn't `if not result:` trigger again on the second element?**  
   **A:** No! On iteration 1, `result` becomes `[0]`. A list's truthiness depends strictly on its **length**, not its contents: `len([0]) == 1`, so `bool([0])` is `True` and `not result` is `False`.
2. **Q: What would be the time complexity if someone wrote `[sum(L[:j+1]) for j in range(len(L))]` instead?**  
   **A:** `O(n^2)` time, because slicing `L[:j+1]` and summing it takes `O(j)` work for each `j` from `0` to `n - 1`. By adding onto `result[-1]`, each step takes `O(1)` and total time is `O(n)`.

---

## `E07_product.py` — Multiplicative Accumulator

- **File:** [E07_product.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E07_product.py)
- **Function:** [`product(L)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E07_product.py#L11-L30)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def product(L):
    result = 1
    for i in L:
        result *= i

    return result
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`product` multiplies every number in `L` into an accumulator `result` initialized to `1`, the multiplicative identity. Starting at `1` ensures both that the first element isn't wiped out to zero and that the empty list `[]` mathematically returns the empty product `1`."
- **Line-by-Line & Variable Breakdown:**
  - `result = 1` (line 26): Multiplicative identity ($1 \times x = x$). Just as `sum([]) == 0` so `sum(A + B) == sum(A) + sum(B)`, `product([]) == 1` preserves `product(A + B) == product(A) * product(B)`.
  - `for i in L:` (line 27): Walks every item in `L` (`x` would be a slightly clearer name than `i`).
  - `result *= i` (line 28): Updates `result = result * i` on each element.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `L`: `Iterable[int | float]`.
  - Local / Return value `result`: `int` if all elements of `L` are `int` (or `L` is empty); promotes to `float` as soon as any `float` is multiplied in!
- **Concrete Step-by-Step Trace (`product([2, 3.0, 4])`):**
  - Init: `result = 1` (`int`).
  - `i = 2`: `result = 2` (`int`).
  - `i = 3.0`: `result = 6.0` (**promotes to `float`!**).
  - `i = 4`: `result = 24.0` (`float`). Returns `24.0`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`product([])`:** Returns `1` (`int`).
  - **`product([0, 2.5])` (Why NOT short-circuiting on `0` is subtle!):** If you wrote `if i == 0: return 0`, then `product([0, 2.5])` would return `0` (`int`) instead of `0.0` (`float`), and `product([0, float('nan')])` would return `0` instead of `nan`, and `product([0, "abc"])` wouldn't raise `TypeError` if another invalid element followed!
  - **`product(["ab", 3])`:** In Python, `1 * "ab"` is `"ab"` and `"ab" * 3` is `"ababab"`, so it actually returns `'ababab'`! Whereas `product(["a", "b"])` raises `TypeError: can't multiply sequence by non-int of type 'str'`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** arithmetic operations where `n = len(L)` (for bounded-size numbers / floats). *Bonus nuance:* Python `int` has arbitrary precision, so if you multiply `n` integers > `1` (like computing $n!$), the bit-length of `result` grows as $O(n \log n)$ bits, making big-int multiplication super-linear in bit operations.
- **Space Complexity:** **`O(1)`** auxiliary space (for bounded-size numbers / floats).
- **Alternative Comparison:** Python 3.8+ actually *did* add `math.prod(L)` in the `math` module (implemented in C, `math.prod([]) == 1`), or functionally `functools.reduce(operator.mul, L, 1)`.

### Likely Interview Q&A
1. **Q: Why is the product of an empty list `1` instead of `0`?**  
   **A:** `1` is the multiplicative identity, just as `0` is the additive identity. If `product([])` were `0`, splitting a list `L = [] + [2, 3]` would violate the law `product(A + B) == product(A) * product(B)` (`6 != 0 * 6`), and initializing `result = 0` would make every product `0`.
2. **Q: Could we optimize `product(L)` by adding `if result == 0: return 0` inside the loop?**  
   **A:** For pure integer lists, yes, that short-circuits to `O(1)` after seeing a `0`. The trade-off is an extra branch every iteration when zeros are rare, plus losing float type promotion (`[0, 1.5]` returning `0` instead of `0.0`) or `nan`/`inf` IEEE-754 semantics (`0 * float('inf')` is `nan`!).

---

## `E08_palindrome.py` — Slicing with a Negative Step

- **File:** [E08_palindrome.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E08_palindrome.py)
- **Function:** [`is_palindrome(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E08_palindrome.py#L11-L30)
- **Difficulty Tier:** `Warm-up`

### Your Submitted Code
```python
def is_palindrome(s):
    palindome = s[::-1]
    if palindome == s:
        return True
    return False
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`is_palindrome` builds a reversed copy of `s` using a negative-step slice `s[::-1]` and checks whether it equals the original sequence `s`. If every element matches forwards and backwards, it returns `True`, otherwise `False`."
- **Line-by-Line & Variable Breakdown:**
  - `palindome = s[::-1]` (line 27): Omitting `start` and `stop` with step `-1` tells Python to traverse from the end (`len(s) - 1`) backwards down to index `0`, producing a reversed copy.
    - **Quirk 1 (Typo & Meaning):** `palindome` is missing an `'r'`, and semantically holds the *reversed* sequence (`reversed_s` or `rev`), whether or not `s` is actually a palindrome.
  - `if palindome == s: return True` / `return False` (lines 28–30):
    - **Quirk 2 (Boolean Redundancy):** Since `palindome == s` already evaluates to a `bool` (`True` or `False`), the `if` statement is redundant — `return s == s[::-1]` ([official solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E08_palindrome.py#L27)) does the exact same work in one line.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameter `s`: `Sequence` (`str`, `list`, `tuple`).
  - Local `palindome`: Same sequence type as `s`.
  - Return value: `bool`.
- **Concrete Step-by-Step Trace (`is_palindrome("ab")` vs `is_palindrome("aba")`):**
  - `"ab"`: `palindome = "ba"`. `"ba" == "ab"` -> `False` at index `0` -> returns `False`.
  - `"aba"`: `palindome = "aba"`. `"aba" == "aba"` -> `True` -> returns `True`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty string `""` or single char `"a"`:** `""[::-1]` is `""` (`True`); `"a"[::-1]` is `"a"` (`True`).
  - **Mixed case `"Racecar"`:** Case-sensitive! `"Racecar"[::-1]` is `"racecaR"`, and `'r' != 'R'`, so it returns **`False`**.
  - **Phrases with spaces `"nurses run"`:** Spaces are treated as ordinary characters (`"nur sesrun" != "nurses run"`), returning **`False`**.
  - **A list `[1, 2, 1]`:** Works seamlessly and returns **`True`**.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** where `n = len(s)`. `s[::-1]` copies all `n` characters (`O(n)`), and `==` compares up to `n` characters (`O(n)`). Notice that even if the very first and last characters differ (`"a...10M chars...z"`), `s[::-1]` **still copies all `n` characters** before `==` immediately fails at index `0`!
- **Space Complexity:** **`O(n)`** auxiliary space for the reversed copy `palindome = s[::-1]`.
- **Alternative Comparison — Slicing vs Two-Pointer Scan (Classic 8–10 Mark Trade-off!):**
  ```python
  left, right = 0, len(s) - 1
  while left < right:
      if s[left] != s[right]:
          return False
      left += 1
      right -= 1
  return True
  ```
  | Approach | Worst-Case Time | Best-Case Time (first/last mismatch) | Auxiliary Space | Practical Speed in CPython |
  | :--- | :--- | :--- | :--- | :--- |
  | `s == s[::-1]` *(Yours)* | `O(n)` | **`O(n)`** *(must finish copying slice first)* | **`O(n)`** | Very fast for short/medium strings (runs entirely in C) |
  | Two-Pointer `while` | `O(n)` *(at most `n // 2` checks)* | **`O(1)`** *(stops on step 1!)* | **`O(1)`** | Uses zero extra memory; wins on huge strings or early mismatches |

### Likely Interview Q&A
1. **Q: What is the space complexity of `is_palindrome`, and how would you reduce it to `O(1)`?**  
   **A:** Currently `O(n)` because `s[::-1]` allocates a full reversed string of length `n`. Using two integer indices `left = 0` and `right = len(s) - 1` walking inward while `s[left] == s[right]` reduces auxiliary space to `O(1)` and also gives `O(1)` best-case early exit on non-palindromes.
2. **Q: How could you simplify lines 27–30 without changing the algorithm?**  
   **A:** Replace the temporary variable and `if/return True/return False` with `return s == s[::-1]`, since `==` already evaluates to a boolean.

---

## `E09_hailstones.py` — Collatz Sequences & Composition

- **File:** [E09_hailstones.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py)
- **Functions:** [`hailstones(n)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L15-L38), [`longest_hailstone(limit)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L44-L60)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def hailstones(n):
    result = []
    result.append(n)
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = (3 * n) + 1
        result.append(n)

    return result


def longest_hailstone(limit):
    result = (0, 0)
    for i in range(1, limit):
        ret = len(hailstones(i))
        if ret > result[1]:
            result = (i, ret)
    
    return  result
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`hailstones` generates the Collatz trajectory from `n` down to `1` by repeatedly halving even numbers with integer division `//` and mapping odd numbers to `3 * n + 1`, appending each term to `result`. `longest_hailstone` composes `hailstones` across every starting integer `1 <= i < limit`, tracking the best `(starting_n, sequence_length)` pair seen so far."
- **Line-by-Line & Variable Breakdown:**
  - **In [`hailstones`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L15-L38):**
    - `result = []; result.append(n)` (lines 29–30): Seeds the list with the starting value `n` *before* the loop so `hailstones(1)` returns `[1]`. (Equivalent to `result = [n]`.)
    - `while n > 1:` (line 31): Continues stepping until `n` reaches `1` (an indefinite `while` loop is required because we cannot predict how many steps `n` will take ahead of time!).
    - `n = n // 2` (line 33): **Crucial operator:** `//` performs **integer floor division**, keeping `n` an `int`. Using `/` would turn `n` into a `float` (`5.0`), breaking exact integer output and losing precision for integers $> 2^{53}$!
  - **In [`longest_hailstone`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E09_hailstones.py#L44-L60):**
    - `result = (0, 0)` (line 54): Best-so-far tuple `(best_n, best_length)` initialized to sentinel `(0, 0)` so any real length `>= 1` beats `0`.
    - `for i in range(1, limit):` (line 55): Tests all positive integers strictly less than `limit` (`1` through `limit - 1`).
    - `ret = len(hailstones(i))` (line 56): Computes the length of `i`'s trajectory (`seq_len` would be a slightly more descriptive name than `ret`).
    - `if ret > result[1]: result = (i, ret)` (lines 57–58): Updates the champion tuple whenever a strictly longer sequence is found.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `hailstones(n: int) -> list[int]`.
  - `longest_hailstone(limit: int) -> tuple[int, int]`, with locals `result: tuple[int, int]`, `i: int`, `ret: int`.
- **Concrete Step-by-Step Trace (`longest_hailstone(5)`):**
  | `i` | `hailstones(i)` | `ret` | `ret > result[1]`? | `result` after |
  | :--- | :--- | :--- | :--- | :--- |
  | Init | — | — | — | `(0, 0)` |
  | `1` | `[1]` | `1` | `1 > 0` (`True`) | `(1, 1)` |
  | `2` | `[2, 1]` | `2` | `2 > 1` (`True`) | `(2, 2)` |
  | `3` | `[3, 10, 5, 16, 8, 4, 2, 1]` | `8` | `8 > 2` (`True`) | `(3, 8)` |
  | `4` | `[4, 2, 1]` | `3` | `3 > 8` (`False`) | `(3, 8)` |
  Returns `(3, 8)`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`hailstones(0)` or `hailstones(-5)` (Your `while n > 1:` SAVES YOU from an infinite loop!):** Look at [W01_Solutions/E09_hailstones.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E09_hailstones.py#L26): the official solution wrote `while n != 1:`, which **hangs in an infinite loop** on `0` (`0 -> 0 -> 0...`) and negative numbers! Your `while n > 1:` immediately skips the loop and returns `[0]` or `[-5]`.
  - **`longest_hailstone(1)` or `longest_hailstone(0)`:** `range(1, 1)` is empty, returning `(0, 0)` (whereas the official solution initialized `(1, 1)` and wrongly returned `(1, 1)` even though `1` is not `< 1`!).
  - **Ties in sequence length (e.g. `12` and `13` both have length `10`):** Because you used strict `>` (`if ret > result[1]:`), a tie does **not** overwrite `result`, so the **smallest** `i` achieving the maximum length wins (`>=` would pick the largest `i`).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - `hailstones(n)`: **`O(L(n))`**, where $L(n)$ is the Collatz stopping length of `n`. *(Bonus flex: Whether $L(n)$ is finite for every positive integer is the famous unsolved **Collatz Conjecture**, though empirically $L(n)$ averages $O(\log n)$ with irregular spikes like $L(27) = 112$.)*
  - `longest_hailstone(limit)`: **`O(sum_{i=1}^{limit-1} L(i))`** (empirically roughly `O(limit * log(limit))`).
- **Space Complexity:**
  - `hailstones(n)`: **`O(L(n))`** for the returned list.
  - `longest_hailstone(limit)`: **`O(max_{i < limit} L(i))`** peak memory (each temporary list `hailstones(i)` is garbage-collected right after `len(...)` finishes).
- **Two Major Optimizations for `longest_hailstone` (8–10 Mark Analysis Gold!):**
  1. **Eliminate list allocation (`O(1)` space):** `longest_hailstone` only calls `len(hailstones(i))` and throws away the list! Writing a helper `hailstone_length(n)` that just increments `count += 1` without `result.append(n)` cuts auxiliary space from `O(L(n))` to **`O(1)`** and removes list-allocation overhead.
  2. **Memoization / Dynamic Programming (`dict` cache):** Notice that `hailstones(10)` (`10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1`) recomputes the entire trajectory of `5`, which was *already computed* when `i = 5`! Caching known lengths in a dictionary `cache = {1: 1}` lets any trajectory stop the instant it hits a previously visited integer, cutting total runtime down to **amortized `O(limit)`** time at the cost of `O(limit)` cache space!

### Likely Interview Q&A
1. **Q: Why did you use `//` on line 33 instead of `/`?**  
   **A:** `/` in Python 3 always produces a `float` (`10 / 2 == 5.0`), whereas `//` is integer division (`10 // 2 == 5`). Beyond keeping list elements as `int`, IEEE-754 floats only have 53 bits of significand precision, so large hailstone excursions above $2^{53}$ would silently round and corrupt parity checks (`n % 2`) if stored as floats!
2. **Q: How would you speed up `longest_hailstone(1_000_000)` by 10x+?**  
   **A:** Two ways: first, don't build the list when we only need the count of steps (`O(1)` space); second, memoize lengths in a dictionary `memo[n]` so whenever a sequence hits a number whose length is already known, we return `steps_so_far + memo[n]` immediately instead of walking all the way to `1` again.

---

## `E10_hailstones_iterate.py` — Higher-Order Iteration

- **File:** [E10_hailstones_iterate.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py)
- **Functions:** [`iterate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py#L13-L19) *(Given)*, [`hailstone_step(n)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py#L22-L34), [`reaches_one(n)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E10_hailstones_iterate.py#L37-L49)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def iterate(x, transform, done, max_steps=10000):
    """Apply transform to x over and over, until done(x) is true."""
    for _ in range(max_steps):
        if done(x):
            return x
        x = transform(x)
    raise RuntimeError("iterate: gave up after too many steps")


def hailstone_step(n):
    if n % 2 == 0:
        return n // 2
    return (3 * n) + 1


def reaches_one(n):
    return True if n == 1 else False
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "Instead of writing a custom `while` loop, we separate *how one step changes the state* (`hailstone_step`) from *when to stop* (`reaches_one`) and pass both functions into the higher-order `iterate` driver. `iterate` repeatedly checks `done(x)` and updates `x = transform(x)` up to `max_steps` times, preventing infinite hangs if a sequence never terminates."
- **Line-by-Line & Variable Breakdown:**
  - `iterate(x, transform, done, max_steps=10000)` (lines 13–19): Higher-order function — `transform` and `done` are **function objects** passed without parentheses (`iterate(27, hailstone_step, reaches_one)`), called inside `iterate` as `done(x)` and `transform(x)`. Note `_` is Python's throwaway loop variable convention when the step index itself isn't used.
  - `hailstone_step(n)` (lines 22–34): Pure single-step state transition $n \mapsto n // 2$ (even) or $3n + 1$ (odd). Note it has **no stopping logic**: `hailstone_step(1)` returns `4` (`1 -> 4 -> 2 -> 1` is the trivial Collatz cycle!).
  - `reaches_one(n)` (line 49): Stopping predicate. **Style Watchout:** `return True if n == 1 else False` is a redundant conditional expression — `return n == 1` already returns `True` or `False` directly.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `hailstone_step(n: int) -> int`.
  - `reaches_one(n: int) -> bool`.
  - `iterate(x: T, transform: Callable[[T], T], done: Callable[[T], bool], max_steps: int = 10000) -> T`.
- **Concrete Step-by-Step Trace (`iterate(4, hailstone_step, reaches_one)`):**
  - `_ = 0`: `x = 4`. `reaches_one(4)` -> `False`. `x = hailstone_step(4)` -> `2`.
  - `_ = 1`: `x = 2`. `reaches_one(2)` -> `False`. `x = hailstone_step(2)` -> `1`.
  - `_ = 2`: `x = 1`. `reaches_one(1)` -> `True` -> **returns `1`**.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`iterate(1, hailstone_step, reaches_one)`:** Because `if done(x):` runs **before** `x = transform(x)`, `reaches_one(1)` is `True` on `_ = 0`, returning `1` immediately with 0 calls to `hailstone_step`! (If `iterate` transformed *before* checking `done`, `1` would go `1 -> 4 -> 2 -> 1` in 3 wasted steps.)
  - **`iterate(0, hailstone_step, reaches_one)`:** `0 % 2 == 0`, so `hailstone_step(0)` is `0` forever. After 10,000 iterations, raises **`RuntimeError: iterate: gave up after too many steps`**.
  - **What if `x` reaches `1` on the exact 10,000th `transform` (`_ = 9999`)?** Look closely at lines 15–19 of `iterate`: on `_ = 9999`, `done(x)` was `False`, then `x = transform(x)` makes `x == 1`, and then the `for` loop ends and **raises `RuntimeError`** without checking `done(x)` one last time! So `iterate` actually allows at most `max_steps - 1` (`9999`) transformations to succeed!
  - **Calling `iterate(27, hailstone_step(), reaches_one)` with parentheses by mistake:** Immediately raises `TypeError: hailstone_step() missing 1 required positional argument: 'n'` *before* `iterate` is even entered.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** `hailstone_step` is **`O(1)`**; `reaches_one` is **`O(1)`**; `iterate(n, hailstone_step, reaches_one)` runs in **`O(min(L(n), max_steps))`** time.
- **Space Complexity:** **`O(1)`** auxiliary space! Compare this with `E09`'s `hailstones(n)` which used `O(L(n))` space to store every intermediate value — `iterate` overwrites `x` in place and only keeps the current state.
- **Design Comparison:** What is the limitation of `iterate(27, hailstone_step, reaches_one)` always returning `1`? You only verify *that* it reached `1`, losing the path length! (Preview of `E15`: if you wanted `iterate` to also count steps, you could pass a tuple `(n, 0)` where `transform` maps `(n, steps) -> (hailstone_step(n), steps + 1)`!)

### Likely Interview Q&A
1. **Q: Why does `iterate(27, hailstone_step, reaches_one)` always return `1`? Is that even useful?**  
   **A:** Because `reaches_one(x)` is only true when `x == 1`, any successful return value must be `1`—the real test is whether it returns `1` *instead of raising `RuntimeError`*. If we wanted the step count too, we could make the state a tuple `(n, count)` just like we do in `E15_gcd.py`.
2. **Q: Why do we pass `hailstone_step` without `()` into `iterate`?**  
   **A:** Functions are first-class objects in Python. Writing `hailstone_step` passes a reference to the function itself so `iterate` can call it repeatedly inside its loop; writing `hailstone_step()` would try to execute it immediately at the call site.

---

## `E11_rotate.py` — Modular Rotation with Slicing

- **File:** [E11_rotate.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E11_rotate.py)
- **Function:** [`rotate(s, k)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E11_rotate.py#L11-L30)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
def rotate(s, k):
    return s[k % len(s):] + s[:k % len(s)] if s else s
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`rotate` shifts the first `k` items of `s` to the back by wrapping `k` into `[0, len(s))` with modulo `k % len(s)` and concatenating the suffix `s[idx:]` in front of the prefix `s[:idx]`. The trailing `if s else s` guard short-circuits empty sequences so `k % 0` never triggers a `ZeroDivisionError`."
- **Line-by-Line & Variable Breakdown:**
  - `if s else s` (line 30): Python evaluates the condition `s` **first**! Empty sequences (`""`, `[]`, `()`) are falsy, so Python skips the left expression entirely and returns `s` (preserving the exact input type: `"" -> ""`, `[] -> []`).
  - `k % len(s)`: Wraps shifts larger than `len(s)` (or negative shifts!) into a valid split point in `0 .. len(s) - 1`. (Minor note: `k % len(s)` is computed twice on line 30; both are `O(1)`, though storing `k %= len(s)` as in the official solution avoids repeating the expression.)
  - `s[idx:] + s[:idx]`: Splits `s` at `idx` and swaps the two halves via `+` concatenation.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameters: `s: Sequence` (`str`, `list`, `tuple`), `k: int`.
  - Return value: Same type as `s`.
- **Concrete Step-by-Step Trace (`rotate("abc", 4)`):**
  1. `bool("abc")` is `True` -> evaluates true-branch.
  2. `len("abc") = 3`; `4 % 3 = 1`.
  3. `"abc"[1:]` -> `"bc"`; `"abc"[:1]` -> `"a"`.
  4. `"bc" + "a"` -> returns `'bca'`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty string/list `rotate("", 2)` or `rotate([], 5)`:** `bool(s)` is `False` -> immediately returns `''` or `[]` without evaluating `2 % 0`.
  - **Negative `k`, e.g., `rotate("abcdef", -2)` (Classic Python `%` question!):** In Python, `%` always matches the sign of the divisor (`6 > 0`), so **`-2 % 6 == 4`** (unlike C/Java remainder where `-2 % 6 == -2`). Then `s[4:] + s[:4]` gives `"ef" + "abcd" = 'efabcd'`, which cleanly **rotates right by 2 places**!
  - **`k = 0` on a mutable list `L = [1, 2]; out = rotate(L, 0)` (Subtle aliasing detail!):** For non-empty `L`, `L[0:] + L[:0]` returns a **new shallow copy** (`out is L` is `False`), *whereas* for an empty list `E = []`, the `else s` branch returns **the exact same list object** (`rotate(E, 0) is E` is `True`!).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** where `n = len(s)` (`O(1)` when `n == 0`). Modulo is `O(1)`, `s[idx:]` copies `n - idx` items, `s[:idx]` copies `idx` items, and `+` allocates and copies all `n` items into the final result (`2n` element copies total).
- **Space Complexity:** **`O(n)`** — allocates two intermediate slices (`O(n)`) plus the concatenated output sequence (`O(n)`).
- **Alternative Comparison:**
  - **`collections.deque.rotate(-k)`:** If you are rotating a queue repeatedly in a loop, `deque.rotate(m)` performs rotation in **`O(k)`** time and **`O(1)` extra space** without copying all `n` elements.
  - **In-place list reversal trick:** For a mutable `list`, reversing `[0:k]`, reversing `[k:n]`, and reversing `[0:n]` rotates in `O(n)` time with **`O(1)` auxiliary space** (impossible for `str`/`tuple` since they are immutable).

### Likely Interview Q&A
1. **Q: Why doesn't `s[k % len(s):] ... if s else s` crash with `ZeroDivisionError` when `s = ""`? `k % len(s)` is written to the left of `if s`!**  
   **A:** Python's ternary expression `X if C else Y` is **short-circuiting**: it evaluates condition `C` (`s`) *first*, and only evaluates `X` if `C` is truthy. When `s == ""`, `X` is never executed.
2. **Q: What happens if we didn't use `% len(s)` and just wrote `s[k:] + s[:k]`? Would `rotate("abc", 4)` crash?**  
   **A:** It wouldn't crash (slicing clamps out-of-bounds indices), *but* it would return the **wrong answer**: `"abc"[4:] + "abc"[:4]` evaluates to `"" + "abc" == "abc"` instead of wrapping around to `"bca"`! That's why `% len(s)` is essential.

---

## `E12_caesar_shifts.py` — Brute-Force Caesar Decoding

- **File:** [E12_caesar_shifts.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py)
- **Functions:** [`caesar(s, k)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py#L14-L23) *(Given)*, [`all_shifts(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E12_caesar_shifts.py#L26-L45)
- **Difficulty Tier:** `Moderate`

### Your Submitted Code
```python
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def caesar(s, k):
    """Shift every letter of s forward by k places. Leave other characters alone."""
    shifted = ALPHABET[k % 26:] + ALPHABET[:k % 26]
    out = []
    for c in s:
        if c in ALPHABET:
            out.append(shifted[ALPHABET.index(c)])
        else:
            out.append(c)
    return "".join(out)

def all_shifts(s):
    list = []
    for i in range(26):
        list.append((i, caesar(s, (26-i)))) # mod is handled by caesar function
    return list
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`all_shifts` brute-forces all 26 possible Caesar cipher keys `i` from `0` to `25`, returning a list of `(i, decoded_plaintext)` tuples. Because encoding with key `i` shifted letters forward by `+i`, decoding reverses that shift by shifting forward `26 - i` places modulo 26."
- **Line-by-Line & Variable Breakdown:**
  - **`caesar(s, k)` (Given, lines 14–23):** Uses `E11`'s rotation trick on `ALPHABET` (`shifted = ALPHABET[k % 26:] + ALPHABET[:k % 26]`), maps each lowercase letter `c` via `shifted[ALPHABET.index(c)]`, leaves spaces/punctuation/uppercase untouched, and joins characters once at the end with `"".join(out)` (`O(n)` instead of `O(n^2)` string `+=`).
  - `list = []` (line 42): **Naming Watchout!** Shadows Python's built-in `list` type inside `all_shifts`. Be ready to point this out proactively ("I'd rename this `shifts` or `result` so I don't shadow the built-in `list` constructor").
  - `caesar(s, (26-i))` (line 44): Shifts forward by `26 - i`. Since $i + (26 - i) = 26 \equiv 0 \pmod{26}$, shifting by `26 - i` is congruent to shifting by `-i`! When `i = 0`, `26 - 0 = 26`, and `26 % 26 == 0` inside `caesar` leaves `s` unchanged.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `s: str` -> `all_shifts(s)` returns `list[tuple[int, str]]` of exact length `26`.
- **Concrete Step-by-Step Trace (`all_shifts("khoor")` at `i = 0` and `i = 3`):**
  - `i = 0`: `26 - 0 = 26`, `26 % 26 = 0` -> `caesar("khoor", 26)` -> `'khoor'` -> appends `(0, 'khoor')`.
  - `i = 3`: `26 - 3 = 23`, `23 % 26 = 23` -> `'k'` (index 10) maps to `shifted[10] = ALPHABET[(10 + 23) % 26] = ALPHABET[7] = 'h'`, decoding `'khoor'` -> `'hello'` -> appends `(3, 'hello')`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Empty string `all_shifts("")`:** Still returns a **26-element list**: `[(0, ''), (1, ''), ..., (25, '')]`.
  - **Uppercase letters `all_shifts("KHOOR")`:** Because `ALPHABET` is strictly lowercase `"a..z"`, `c in ALPHABET` is `False` for `'K'..'R'`, so **all 26 entries are `(i, 'KHOOR')` unchanged**!
  - **Digits & punctuation `all_shifts("khoor, 123!")`:** Entry `3` is `(3, 'hello, 123!')` — non-letters pass through the `else` branch intact.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** where `n = len(s)` (or more generally **`O(|Sigma|^2 * n)`** for an alphabet of size $|\Sigma|$, where here $|\Sigma| = 26$ is a constant).
  - *Hidden cost inside `caesar`:* For each of the `n` characters, `c in ALPHABET` and `ALPHABET.index(c)` linearly scan up to 26 characters (`O(|Sigma|)`), and `all_shifts` calls `caesar` $|\Sigma| = 26$ times (`26 * 26 * n = 676n` operations).
- **Space Complexity:** **`O(n)`** (stores 26 decoded strings of length `n`, i.e., `26 * n = O(n)` characters).
- **Alternative / Data Structure Comparison:**
  - **List comprehension:** `[(k, caesar(s, -k)) for k in range(26)]` (used in `E13`).
  - **Speeding up `caesar` from `O(|Sigma| * n)` to `O(|Sigma| + n)`:** Replace `ALPHABET.index(c)` with either:
    1. Ordinal arithmetic: `chr((ord(c) - ord('a') + k) % 26 + ord('a'))` (`O(1)` math per char, zero lookup scan!), or
    2. Hash table / C translation table: `s.translate(str.maketrans(ALPHABET, shifted))` (runs completely in C in `O(n)`).

### Likely Interview Q&A
1. **Q: Why does `caesar(s, 26 - i)` give the exact same result as `caesar(s, -i)`?**  
   **A:** Because `caesar` reduces the shift modulo 26 (`k % 26`), and $(26 - i) \equiv -i \pmod{26}$ for every integer `i` (including `i = 0`, where `26 % 26 == 0 == -0 % 26`).
2. **Q: Why did `caesar` collect characters in `out = []` and call `"".join(out)` instead of doing `out += c` on a string?**  
   **A:** Strings in Python are immutable, so repeated `out += c` conceptually allocates a new string every iteration (`O(n^2)` total copies), whereas appending to a list and calling `"".join(out)` once allocates the exact target buffer size in a single `O(n)` pass.

---

## `E13_caesar_crack.py` — Automated Cipher Cracking

- **File:** [E13_caesar_crack.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py)
- **Functions:** [`caesar`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L17-L26) *(Given)*, [`all_shifts`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L29-L31) *(Given)*, [`english_score(text)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L34-L51), [`crack(s)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E13_caesar_crack.py#L54-L74)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def english_score(text):
    count = 0
    for char in text:
        if char in "etaoin":
            count+=1
    return count


def crack(s):
    list = all_shifts(s)

    score = [] 
    for i in range(26):
        score.append((english_score(list[i][1]), list[i][1]))
    return max(score)[1]

# It fails because even though these are the most commonly used letters that does not a word guarantee. 
# An dictionary of english words to compare the result with could be a solution.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`english_score` estimates how much a candidate string looks like English by counting occurrences of the six high-frequency letters `e, t, a, o, i, n`. `crack` generates all 26 Caesar decodings with `all_shifts(s)`, pairs each candidate plaintext with its `english_score` in a `(score, plaintext)` tuple, and picks the highest-scoring plaintext with `max(score)[1]`."
- **Line-by-Line & Variable Breakdown:**
  - **`english_score(text)` (lines 47–51):** Loops over `text` and counts characters in `"etaoin"`.
    - **CRITICAL BUG TO KNOW COLD (line 49):** The docstring on line 38 specifies *"Upper case counts too"*, **but** `"etaoin"` is lowercase only! Unlike `E04` where you wrote `"AEIOUaeiou"`, here uppercase `'E','T','A','O','I','N'` are missed (`english_score("ATTACK AT DAWN")` returns `0` instead of `8`). Own this immediately if asked: changing `"etaoin"` to `"etaoinETAOIN"` fixes it in `O(1)` space!
  - **`list = all_shifts(s)` (line 69):** Stores the 26 `(k, plaintext)` pairs. *(Watchout: shadows built-in `list`.)*
  - **`score = []` & `score.append((english_score(list[i][1]), list[i][1]))` (lines 71–73):** Builds a list of 26 `(int_score, str_plaintext)` tuples. Putting the integer score **first** in the tuple is critical so `max(score)` compares scores before comparing strings!
  - **`return max(score)[1]` (line 74):** Finds the maximum `(score, plaintext)` tuple and extracts index `[1]` (the winning plaintext `str`).

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `english_score(text: str) -> int`.
  - `crack(s: str) -> str`, with locals `list: list[tuple[int, str]]`, `score: list[tuple[int, str]]`.
- **Concrete Step-by-Step Trace (`crack("khoor zruog")` — Why the Short Doctest Fails!):**
  - `all_shifts("khoor zruog")` produces 26 candidates, including:
    - `i = 3`: `'hello world'` -> letters in `"etaoin"` are `'e', 'o', 'o'` -> `english_score` = **`3`** -> tuple `(3, 'hello world')`.
    - `i = 6`: `'ebiil tloia'` -> letters in `"etaoin"` are `'e', 'i', 'i', 't', 'o', 'i', 'a'` -> `english_score` = **`7`** -> tuple `(7, 'ebiil tloia')`.
  - `max(score)` picks `(7, 'ebiil tloia')`, and `[1]` returns `'ebiil tloia'`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Uppercase input `english_score("HELLO")`:** Returns **`0`** (instead of `2`) because `"etaoin"` lacks `"ETAOIN"`. And `crack("KHOOR")` has all 26 shifts identical `(0, 'KHOOR')`, returning `'KHOOR'`.
  - **Tie-breaking quirk on `crack("a")` (Subtle difference from Official Solution!):**
    - `all_shifts("a")` produces all 26 lowercase letters `'a'`, `'z'`, `'y'`, ..., `'b'`.
    - Six candidates (`'e'`, `'t'`, `'a'`, `'o'`, `'i'`, `'n'`) tie with `english_score == 1`!
    - How does `max([(1, 'a'), ..., (1, 't'), ...])` break ties? Python compares tuples **lexicographically**: when element `[0]` (`1 == 1`) ties, it compares element `[1]` (`str`) alphabetically! Since `'t'` > `'o'` > `'n'` > `'i'` > `'e'` > `'a'`, your `max(score)[1]` returns **`'t'`**! (By contrast, the [official solution](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/week_01/W01_Solutions/W01_Solutions/E13_caesar_crack.py#L73) used `if score > best_score:`, keeping the **first** shift `k = 0`, returning `'a'`!)
  - **Empty string `crack("")`:** All 26 entries in `score` are `(0, '')`; `max(score)[1]` returns `''`.

### Pillar 3 — Analyse (Complexity, Trade-offs & `# ANSWER`)
- **Time Complexity:**
  - `english_score(text)`: **`O(n)`** (`n = len(text)`, at most 6 char comparisons per char).
  - `crack(s)`: **`O(n)`** (`all_shifts(s)` takes `26 * O(n) = O(n)`, scoring 26 strings takes `26 * O(n) = O(n)`, and `max(score)` compares 26 tuples in `O(n)` worst-case string tie-break / `O(1)` when integer scores differ).
- **Space Complexity:** `english_score` is **`O(1)`**; `crack` is **`O(n)`** (`all_shifts` + `score` store 26 strings of length `n`).
  - *Single-variable alternative:* Using `max(( plaintext for _, plaintext in all_shifts(s) ), key=english_score)` avoids building the `score` list and breaks ties by first occurrence rather than string alphabetical order!
- **Embedded File Question (`# ANSWER`, lines 9–10 & 76–77):**
  > **QUESTION:** *`crack` fails on the short message below (`"khoor zruog"` -> `'ebiil tloia'`). Why? What would you need in order to fix it?*
  - **Your Comment (`#L76-L77`):** Noted that common letters alone do not guarantee valid English words, and proposed checking decoded words against an English dictionary.
  - **10/10 Model Answer for the Interview (Combine Statistical Variance + Model Richness):**
    1. **Why it fails (Small-Sample Variance / Law of Large Numbers):** `english_score` relies on an asymptotic statistical property of English (`etaoin` makes up ~50% of long English text). On an 11-character sample (`"hello world"`), sample variance is huge — `"hello world"` happens to contain three `'l'`s and only 3 `"etaoin"` letters, whereas Caesar shift 6 (`'ebiil tloia'`) turns `'h'->'e'`, `'l'->'i'`, `'w'->'t'`, `'r'->'o'`, `'d'->'a'`, scoring 7 by sheer coincidence!
    2. **Two ways to fix it:**
       - **More data:** On longer ciphertexts (30+ chars), random shifts revert toward `26`-letter uniform noise (~$6/26 \approx 23\%$ `etaoin`) while true English converges to ~50%.
       - **A richer language model:** (a) Use **weighted full-alphabet log-probabilities** or $\chi^2$ goodness-of-fit (which penalizes rare letters/weird frequencies instead of giving `e` and `n` equal flat weight), (b) score **character bigrams/trigrams** (like `'th'`, `'he'`, `'ll'` vs impossible `'ii'`, `'tl'`), or (c) **dictionary word matching** (splitting on spaces and counting hits in a `set` of English words).

### Likely Interview Q&A
1. **Q: Look at `english_score` — what does `english_score("ETAOIN")` return in your code, and why didn't `doctest` catch it?**  
   **A:** It returns `0` instead of `6` because line 49 checks `if char in "etaoin":` without `"ETAOIN"` or `.lower()`. `doctest` didn't catch it because none of the three doctests in `english_score` contained uppercase letters — a great reminder that passing doctests only proves correctness on the tested cases!
2. **Q: Why did you put `english_score(...)` as the *first* item of the tuple in `score` rather than `(plaintext, english_score)`?**  
   **A:** Because `max()` compares tuples element-by-element from index `0`. If `plaintext` were first, `max()` would simply pick whichever shift starts with the highest ASCII letter (`'z...'`) and completely ignore the score!

---

## `E14_newton_cbrt.py` — Cube Roots via `iterate` & Closures

- **File:** [E14_newton_cbrt.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py)
- **Functions:** [`iterate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L13-L19) *(Given)*, [`newton_cbrt(x, tol=1e-10)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L22-L49), [`transform(g)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L43-L44), [`done(g)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E14_newton_cbrt.py#L46-L47)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def newton_cbrt(x, tol=1e-10):
    if x == 0:
        return 0.0

    def transform(g):
        return (2*g + x / (g*g)) / 3 # When defining a function within another function you can access the variables of the outer function, so x is available here. This is called Closure.

    def done(g):
        return abs(g*g*g - x) < tol

    return iterate(x, transform, done)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`newton_cbrt` computes the real cube root of any positive, negative, or zero number `x` by passing nested `transform` and `done` closures into `iterate`. Because `iterate` expects one-argument functions `transform(g)` and `done(g)`, defining them inside `newton_cbrt` lets them capture `x` and `tol` from the enclosing scope."
- **Line-by-Line & Variable Breakdown:**
  - `if x == 0: return 0.0` (lines 40–41): Guards against `0.0` division in `x / (g * g)` inside `transform` and guarantees a `float` `0.0` return.
  - `def transform(g): return (2*g + x / (g*g)) / 3` (lines 43–44): Newton–Raphson step for $f(g) = g^3 - x = 0$ ($f'(g) = 3g^2$):
    $$g_{\text{next}} = g - \frac{g^3 - x}{3g^2} = \frac{2g + x / g^2}{3}$$
    *(Geometric average intuition: $g \cdot g \cdot (x/g^2) = x$, so taking the arithmetic average of two copies of $g$ and one copy of $x/g^2$ bracket-averages toward $\sqrt[3]{x}$!)*
  - **Closure (your comment on line 44!):** By Python's **LEGB** scoping rule (*Local → Enclosing → Global → Built-in*), `x` is a free variable in `transform` and `x`, `tol` are free variables in `done`, resolved in the **Enclosing** frame of `newton_cbrt`.
  - `def done(g): return abs(g*g*g - x) < tol` (lines 46–47): Stops when $g^3$ is within `tol` of `x`.
  - `return iterate(x, transform, done)` (line 49): Starts from initial guess `g_0 = x` and runs up to `10000` steps.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - Parameters: `x: int | float`, `tol: float = 1e-10`.
  - Inner functions: `transform: Callable[[float], float]`, `done: Callable[[int | float], bool]`.
  - Return value: Usually `float` — **EXCEPT** see the `x = 1` / `x = -1` trace below!
- **Concrete Step-by-Step Trace (`newton_cbrt(-8)` — Why Negative Numbers Work!):**
  - `x = -8` (`!= 0`). Enters `iterate(-8, transform, done)`:
  - Step 0: `g = -8`. `done(-8)`: `abs(-512 - (-8)) = 504 < 1e-10` (`False`).  
    `transform(-8) = (2*(-8) + (-8)/64) / 3 = (-16 - 0.125) / 3 = -5.375`.
  - Step 1: `g = -5.375` -> `transform` -> `-3.67569...`
  - Steps 2–7: `-2.5795... -> -2.0970... -> -2.00436... -> -2.0000094... -> -2.000000000044...`
  - Step 8: `abs(g**3 - (-8)) < 1e-10` is `True` -> returns `-2.000000000044699`.
  - *Why can `g` NEVER hit `0` for `x != 0`?* Because $g_0 = x$ and $g^2 > 0$, both terms $2g$ and $x/g^2$ have the **exact same sign as `x`** on every single step! Their sum can never cross zero!
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`newton_cbrt(1)` or `newton_cbrt(-1)` (Awesome Return-Type Quirk!):** On step 0 of `iterate`, `done(1)` checks `abs(1*1*1 - 1) < 1e-10` (`0 < 1e-10 == True`) **before `transform` ever runs**! So `newton_cbrt(1)` returns **`1` (`int`, NOT `float`!)**, and `newton_cbrt(-1)` returns **`-1` (`int`)**!
  - **Tiny input `newton_cbrt(1e-11)` (Absolute Residual Trap!):** On step 0, `done(1e-11)` checks `abs((1e-11)**3 - 1e-11) ≈ 1e-11 < 1e-10` -> **`True` immediately!** It returns **`1e-11`** without a single step, even though the true cube root is $\approx 2.154 \times 10^{-4}$ (20,000x larger)! Why? Because `abs(g**3 - x) < tol` measures absolute error in $g^3$, not relative error in $g$.
  - **`tol = 0` or `tol = -1`:** `abs(...) < -1` is never `True` (and for `tol = 0`, floating-point rounding may oscillate around the last bit), hitting `10000` steps and raising **`RuntimeError: iterate: gave up after too many steps`**.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(log |x| + log log(1 / tol))`** iterations.
  - **Phase 1 (Linear damping far from root):** When $|g| \gg |x|^{1/3}$, $g_{\text{next}} \approx \frac{2}{3} g$, reducing $|g|$ by a constant factor $2/3$ per step -> takes $O(\log |x|)$ steps to reach the ballpark of $x^{1/3}$ (e.g., even for `x = 1e100`, $\log_{1.5}(10^{67}) \approx 380 \ll 10000$ steps).
  - **Phase 2 (Quadratic convergence near root):** Once close to $x^{1/3}$, relative error squares each step ($e_{k+1} \approx e_k^2$), taking $O(\log \log(1/\text{tol}))$ (~5–6 steps) to reach `1e-10`.
- **Space Complexity:** **`O(1)`** auxiliary space (two small closure objects created once + scalar `g` updated in place inside `iterate`).
- **Alternative Comparison:** Why not compute `x ** (1/3)` in Python? Two huge reasons!
  1. In Python, **`(-8) ** (1/3)` returns a `complex` number** `(1.0000000000000002+1.7320508075688772j)` (the principal complex root), NOT `-2.0`!
  2. `1 / 3` is not exactly representable in binary floating-point (`0.3333333333333333`), so `8 ** (1/3)` or `64 ** (1/3)` (`3.9999999999999996`) suffers rounding inaccuracies! (Python 3.11+ added `math.cbrt(x)` specifically to solve both issues.)

### Likely Interview Q&A
1. **Q: Why couldn't `transform` be defined at the top level of the module as `def transform(g, x): ...`?**  
   **A:** Because `iterate` calls `transform(x)` with **only one argument** (`g`). By nesting `def transform(g):` inside `newton_cbrt(x, tol)`, `transform` forms a **closure** that captures `x` from the enclosing scope while matching `iterate`'s 1-argument interface.
2. **Q: Why does `newton_cbrt(-8)` work cleanly while `newton_sqrt(-8)` fails?**  
   **A:** Mathematically, odd powers preserve sign ($f(g) = g^3 + 8$ crosses zero cleanly at $g = -2$ with positive slope $3g^2 > 0$ everywhere except $0$), and starting at $g_0 = -8$, both $2g$ and $x/g^2$ are negative so the iterates stay strictly negative and converge monotonically to $-2$. For square roots, $g^2 + 8 = 0$ has no real root!

---

## `E15_gcd.py` — Euclid's Algorithm via Tuple-State Iteration

- **File:** [E15_gcd.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py)
- **Functions:** [`iterate`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L13-L19) *(Given)*, [`gcd(a, b)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L22-L49), [`transform(x)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L40-L42), [`done(x)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/assignment_01/W01/E15_gcd.py#L44-L47)
- **Difficulty Tier:** `Hard (8–10 Mark Target)`

### Your Submitted Code
```python
def gcd(a, b):
    def transform(x):
        a, b = x
        return (b, a % b)

    def done(x):
        a, b = x
        if (b == 0):
            return True
        
    return  iterate((a, b), transform, done)[0]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** "`gcd` implements Euclid's algorithm ($\gcd(a, b) = \gcd(b, a \bmod b)$) on top of `iterate` by packing the two numbers into a single state tuple `(a, b)`. Once `done` detects that the remainder slot `b` has reached `0`, `iterate` returns the final pair `(d, 0)` and `[0]` extracts the greatest common divisor `d`."
- **Line-by-Line & Variable Breakdown:**
  - `transform(x)` (lines 40–42): Unpacks `a, b = x` and returns the next Euclid state `(b, a % b)`.
  - `done(x)` (lines 44–47): Unpacks `a, b = x` and checks `if (b == 0): return True`.
    - **MAJOR QUIRK TO KNOW COLD (lines 46–47):** What does `done((48, 18))` return? **`None`** (`NoneType`), **NOT `False`**! Because there is no `else: return False` (or `return b == 0`), Python implicitly returns `None` whenever `b != 0`. `iterate` still works because `if done(x):` evaluates truthiness and `bool(None)` is `False`, *but* `return b == 0` is much cleaner!
  - **Scoping note (`a, b = x`):** Unlike `E14`, `transform` and `done` here unpack *local* variables `a, b = x` that shadow `gcd`'s parameters `a, b` — they don't actually close over any outer variables (they could even be module-level helpers!).
  - `iterate((a, b), transform, done)[0]` (line 49): Passes initial tuple `(a, b)` as `x`, gets back `(ans, 0)`, and indexes `[0]` to return `ans`.

### Pillar 2 — Trace (Types, Step-by-Step Execution & Caller Edge Cases)
- **Types:**
  - `gcd(a: int, b: int) -> int`.
  - State `x` inside `iterate`: `tuple[int, int]`.
  - `done(x)` return type in your code: **`Literal[True] | None`** (`bool | None`)!
- **Concrete Step-by-Step Trace (`gcd(18, 48)` — When `a < b`!):**
  | Step `_` | State `x = (a, b)` | `done(x)` | `transform(x) = (b, a % b)` |
  | :--- | :--- | :--- | :--- |
  | 0 | `(18, 48)` | `None` *(falsy)* | `(48, 18 % 48) = (48, 18)` *(auto-swaps!)* |
  | 1 | `(48, 18)` | `None` | `(18, 48 % 18) = (18, 12)` |
  | 2 | `(18, 12)` | `None` | `(12, 18 % 12) = (12, 6)` |
  | 3 | `(12, 6)` | `None` | `(6, 12 % 6) = (6, 0)` |
  | 4 | `(6, 0)` | `True` | — (`iterate` returns `(6, 0)`) |
  `[0]` extracts and returns `6`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`gcd(7, 0)` and `gcd(0, 7)`:** `gcd(7, 0)` hits `done((7, 0)) == True` on step 0 (never divides `7 % 0`!) and returns `7`. `gcd(0, 7)` transforms `(0, 7) -> (7, 0)` on step 0 and returns `7` on step 1!
  - **`gcd(0, 0)`:** `done((0, 0))` is `True` on step 0 -> returns **`0`** (matching `math.gcd(0, 0) == 0`).
  - **Negative inputs `gcd(-48, 18)` vs `gcd(48, -18)` (Sharp Python `%` Edge Case!):**
    - `gcd(-48, 18)`: `-48 % 18 == 6` -> `(18, 6)` -> `(6, 0)` -> returns **`6`**.
    - `gcd(48, -18)`: Because Python's `%` takes the sign of the divisor (`-18`), `48 % -18 == -6` -> `(-18, -6)` -> `(-6, 0)` -> returns **`-6`**! (By contrast, standard `math.gcd(48, -18)` always returns non-negative `+6`; wrapping `abs(...)` would normalize signs.)

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(log(min(a, b)))`** steps (Euclid's / Lamé's Theorem).
  - **Why logarithmic? (10/10 Explanation):** Whenever $a \ge b > 0$, $a \bmod b < b$ AND in fact $a \bmod b < a / 2$ (if $b \le a/2$, then $a \bmod b < b \le a/2$; if $b > a/2$, then $a \bmod b = a - b < a/2$). Thus **every two steps at least halve the numbers**!
  - **Worst-case inputs:** Consecutive **Fibonacci numbers** `(F_{k+1}, F_k)` (like `gcd(89, 55)`), where every quotient is `1` and each step shrinks by the golden ratio $\phi \approx 1.618$. Even then, `max_steps = 10000` handles integers with over **2,000 decimal digits**!
  - *Contrast with naive brute force:* Checking every divisor from `1` up to `min(a, b)` takes **`O(min(a, b))`** (exponential in the number of digits!), which is completely intractable on 100-digit RSA integers where Euclid finishes in milliseconds.
- **Space Complexity:** **`O(1)`** auxiliary space (for fixed-width integers). Only one 2-tuple is active at a time — whereas recursive `def gcd(a, b): return a if b == 0 else gcd(b, a % b)` uses **`O(log(min(a, b)))`** call-stack frames (and hits Python's `RecursionError` around 1,000 steps!).

### Likely Interview Q&A
1. **Q: In your `done(x)` function, what is the exact value and type returned when `x = (48, 18)`?**  
   **A:** It returns `None` (`NoneType`), not `False`, because execution falls off the end of `done` when `b == 0` is false. `if done(x):` inside `iterate` still treats `None` as falsy, though writing `return b == 0` is much cleaner because it always returns a `bool`.
2. **Q: Why did we pack `(a, b)` into a tuple instead of just modifying two variables?**  
   **A:** Because `iterate(x, transform, done)` is designed around a single state value `x = transform(x)`. Representing multi-variable state as a tuple `(a, b)` lets us reuse `iterate` unchanged without modifying its signature.
3. **Q: What inputs make `gcd(a, b)` take the maximum number of steps for a given size?**  
   **A:** Consecutive Fibonacci numbers, such as `gcd(89, 55)`, because `a % b` is `a - b` at every single step—the slowest possible decay—giving `O(log(min(a, b)))` steps by Lamé's Theorem.
