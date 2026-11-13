# Week 8 Interview Preparation Guide — NumPy, Vectorisation & Broadcasting

← Back to [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Week 8 Core Topics:** NumPy `ndarray` internals (shapes, `dtype`s, strides, views vs copies), C-level `ufunc` vectorisation, right-to-left broadcasting rules, boolean masks & fancy indexing, axis reductions (`axis=0` vs `axis=1`), pairwise distance matrices (`scipy.spatial.distance.cdist`), `np.argsort`, and tensor-vector contraction via `@` (`matmul`).

---

## Table of Contents

1. [Summary Table of All Week 8 Exercises](#1-summary-table-of-all-week-8-exercises)
2. [Pre-Interview Checklist & Key NumPy Mental Models](#2-pre-interview-checklist--key-numpy-mental-models)
3. [Reference Context: `E01_photos.py` & `prep_data.py` (Given Code)](#3-reference-context-e01_photospy--prep_datapy-given-code)
4. [`E02_vectorise.py` — Elementwise `ufunc` Vectorisation (`softplus`)](#4-e02_vectorisepy--elementwise-ufunc-vectorisation-softplus)
5. [`E03_broadcast.py` — Broadcasting & Outer Products (`combine`, `times_table`)](#5-e03_broadcastpy--broadcasting--outer-products-combine-times_table)
6. [`E04_axis_masks.py` — Boolean Masks & Axis Reductions (`count_above`, `values_above`, `column_means`, `row_maxes`)](#6-e04_axis_maskspy--boolean-masks--axis-reductions-count_above-values_above-column_means-row_maxes)
7. [`E05_broadcastable.py` — Implementing NumPy's Broadcasting Rule (`is_broadcastable`)](#7-e05_broadcastablepy--implementing-numpys-broadcasting-rule-is_broadcastable)
8. [`E06_heatmap.py` — All-Pairs Distance Matrix (`distance_matrix`)](#8-e06_heatmappy--all-pairs-distance-matrix-distance_matrix)
9. [`E07_brightness.py` — Image Reductions & Fancy Indexing (`brightness`, `darkest_first`)](#9-e07_brightnesspy--image-reductions--fancy-indexing-brightness-darkest_first)
10. [`E08_grayscale.py` — Luminance Dot Product Along Last Axis (`to_gray`)](#10-e08_grayscalepy--luminance-dot-product-along-last-axis-to_gray)

---

## 1. Summary Table of All Week 8 Exercises

| File | Function(s) | Difficulty Tier | Input → Output Shapes & Dtypes | Time Complexity | Aux Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [E01_photos.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py) | [`load`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L25-L34), [`histogram_numpy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L67-L89), [`as_proportions`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L103-L119), [`distances_to`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L122-L135), [`most_similar`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L138-L149) | Reference (Given) | `(H, W, 3)` `uint8` → `(n, 64)` `float64` → `(k,)` `int64` | `O(B^3 * H * W)` hist; `O(n * d + n log n)` k-NN | `O(H * W)` / `O(n * d)` |
| [E02_vectorise.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py) | [`softplus`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py#L20-L42) | Warm-up | Scalar → `np.float64`; `(...)` → `(...)` `float64` | `O(N)` (`N = x.size`) | `O(N)` |
| [E03_broadcast.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py) | [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43), [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L46-L58) | Moderate | `(n, m), (n,), (m,), scalar` → `(n, m)` `float64`; `int` → `(n, n)` `int64` | `O(n * m)` / `O(n^2)` | `O(n * m)` / `O(n^2)` |
| [E04_axis_masks.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py) | [`count_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L19-L28), [`values_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L31-L40), [`column_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L43-L52), [`row_maxes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L55-L64) | Warm-up / Moderate | `(...)` → `int` / `(k,)`; `(n, m)` → `(m,)` / `(n,)` | `O(N)` (`N` = total elements) | `O(N)` mask; `O(m)` / `O(n)` reductions |
| [E05_broadcastable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py) | [`is_broadcastable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py#L22-L42) | **Hard (8–10 Mark Target)** | `ndarray, ndarray` → `bool` | `O(min(X.ndim, Y.ndim))` (`O(1)` in data size!) | `O(1)` |
| [E06_heatmap.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py) | [`distance_matrix`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L31-L45) | **Hard (8–10 Mark Target)** | `(n, d)` → `(n, n)` `float64` | `O(n^2 * d)` | `O(n^2)` (no `(n, n, d)` tensor!) |
| [E07_brightness.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py) | [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33), [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50) | Moderate | `(H, W, 3)` `uint8` → `float`; `list[str], list[float]` → `(n,)` `<U...` | `O(H * W)` / `O(n log n + n * L)` | `O(1)` / `O(n * L)` |
| [E08_grayscale.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py) | [`to_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L34-L51) | **Hard (8–10 Mark Target)** | `(H, W, 3)` `uint8` `@` `(3,)` `float64` → `(H, W)` `float64` | `O(H * W * C)` (`C = 3`) | `O(H * W)` |

---

## 2. Pre-Interview Checklist & Key NumPy Mental Models

> [!TIP]
> **Portfolio Status for Week 8:** Every exercise file (`E02` through `E08`) passes all doctests, matches the expected return types (`int`, `float`, `bool`, `ndarray`), and both written `# ANSWER` comments ([E03_broadcast.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L60-L66) and [E06_heatmap.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L80)) are filled in. One tiny optional polish point: in [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L58), know why `np.arange(1, n + 1)` is slightly cleaner than `np.array(range(1, n + 1))` if the interviewer asks.

### Four Rules That Answer 90% of Week 8 Trace & Analyse Questions
1. **`axis=k` is the axis that collapses (disappears):** If `X` has shape `(n, m)`, `X.mean(axis=0)` collapses the `n` rows and leaves shape `(m,)`; `X.max(axis=1)` collapses the `m` columns and leaves shape `(n,)`.
2. **Views vs Copies (`O(1)` vs `O(N)` memory):**
   - **Views (`O(1)` time & space, shares data buffer):** `.reshape(...)` (on contiguous arrays), basic slicing (`image[:, :, :3]`), and broadcasting's "virtual stretching" (setting stride `= 0` along a length-1 axis without copying bytes).
   - **Copies (`O(N)` time & space, new buffer):** Arithmetic operations (`A + b`), boolean mask indexing (`x[x > t]`), fancy integer-array indexing (`names_arr[order]`), and `.astype(...)`.
3. **NumPy Scalars vs Python Scalars:** Reductions like `np.sum(...)` or `image.mean()` return `np.int64` / `np.float64` (0-D NumPy scalars), *not* built-in Python `int` or `float`. In NumPy 2.x, `repr(np.int64(3))` prints `'np.int64(3)'`, which is why [`count_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L28) wraps in `int(...)` and [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L33) wraps in `float(...)`.
4. **`uint8` Arithmetic Overflow Trap:** Raw images have `dtype=uint8` (unsigned 8-bit integers in `0..255`). Direct addition like `np.uint8(200) + np.uint8(200)` wraps modulo 256 to `144`! Reductions like `.mean()` and `.sum()` avoid this by automatically upcasting accumulators to `float64` / `uint64`, and `image @ WEIGHTS` promotes `uint8` × `float64` → `float64`.

---

## 3. Reference Context: `E01_photos.py` & `prep_data.py` (Given Code)

**Files:** [E01_photos.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py) and [prep_data.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/prep_data.py)

Even though `E01_photos.py` is given code, exercises `E06`, `E07`, and `E08` import directly from it (`DATA`, [`load`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L25-L34), [`build_matrix`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L92-L100), [`as_proportions`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L103-L119)), and Week 9's k-NN classifier builds directly on [`distances_to`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L122-L135) and [`most_similar`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L138-L149).

### End-to-End Pipeline Walkthrough
1. **Dataset Generation ([`make_sizes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/prep_data.py#L32-L41)):** Downloads 24 Kodak True Color PNGs (`768×512` or `512×768`) and saves each at 3 scales: `full` (`1.0×`), `half` (`0.5×`), and `thumb` (`0.125×`, i.e., `1/8` width × `1/8` height = `1/64` as many pixels), producing `72` PNGs in `data/photos/`.
2. **Image Representation ([`load`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L25-L34)):**
   - `plt.imread(path)` reads a PNG as `float32` in `[0.0, 1.0]` with shape `(H, W, 3)` or `(H, W, 4)` (if RGBA).
   - `[:, :, :3]` slices off any alpha channel (a view), and `np.round(rgb * 255).astype(np.uint8)` converts to `(H, W, 3)` `uint8` in `{0, ..., 255}`.
3. **3-D Colour Histogram Extraction ([`histogram_python`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L37-L64) vs [`histogram_numpy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L67-L89)):**
   - Quantises each RGB channel into `B = 4` bins of width `WIDTH = 256 // 4 = 64` via integer floor division `image // 64` (`0..63 -> 0`, `64..127 -> 1`, `128..191 -> 2`, `192..255 -> 3`).
   - `histogram_python` flattens spatial axes via `image.reshape(-1, 3)` (`(H*W, 3)`) and loops in Python over ~393,216 pixels (`~150–300 ms`).
   - `histogram_numpy` loops in Python only over the `B**3 = 64` bins (`4 × 4 × 4`), while C-level NumPy handles all pixels per bin via `(binned[:, :, 0] == r) & (binned[:, :, 1] == g) & (binned[:, :, 2] == b)` (note bitwise `&` for elementwise boolean AND, because Python's `and` raises `ValueError: The truth value of an array with more than one element is ambiguous`).
4. **Feature Matrix & Scale Normalisation ([`build_matrix`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L92-L100) & [`as_proportions`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L103-L119)):**
   - Reshapes each `(4, 4, 4)` histogram into a 1-D vector of `64` features, stacking all `72` photos into `X` of shape `(72, 64)` (`dtype=float64`).
   - Raw pixel counts fail when comparing `kodim01_thumb` (`6,144` pixels) against `kodim01_full` (`393,216` pixels): `kodim01_thumb` is closer in raw Euclidean count space to *other thumbnails* of totally different scenes than to `kodim01_full`!
   - `as_proportions(X)` computes `X / X.sum(axis=1).reshape(-1, 1)`: `X.sum(axis=1)` has shape `(n,)` (total pixels per photo), `.reshape(-1, 1)` turns it into `(n, 1)`, and broadcasting divides every row by its own pixel count so every row sums to `1.0`.
5. **Nearest-Neighbour Search ([`distances_to`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L122-L135) & [`most_similar`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L138-L149)):**
   - `np.linalg.norm(X - x, axis=1)` subtracts query row `x` `(64,)` from all rows of `X` `(72, 64)` via broadcasting and takes the $L_2$ norm of each row → `(72,)`.
   - `d[i] = np.inf` masks out the query photo itself (whose distance to itself is `0.0`), and `np.argsort(d)[:k]` returns the indices of the `k` closest photos.

---

## 4. `E02_vectorise.py` — Elementwise `ufunc` Vectorisation (`softplus`)

- **File:** [E02_vectorise.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py)
- **Function:** [`softplus`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py#L20-L42) (Helper given: [`plot`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py#L47-L60))
- **Difficulty Tier:** Warm-up

### Your Code
```python
def softplus(x):
    return np.log(1 + np.exp(x))
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`softplus`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py#L20-L42) computes the smooth activation function $\ln(1 + e^x)$, mapping any real number in $(-\infty, \infty)$ strictly into $(0, \infty)$. Because `np.exp`, `+`, and `np.log` are NumPy universal functions (`ufunc`s), the exact same single expression works seamlessly on both a single scalar and an entire `ndarray` of any shape without a Python loop.
- **Line-by-Line & Method Breakdown:**
  - `np.exp(x)`: Applies $e^{x_i}$ elementwise in compiled C.
  - `1 + ...`: Broadcasts the scalar `1` across the shape of `np.exp(x)` and adds elementwise.
  - `np.log(...)`: Computes the natural logarithm ($\ln$, base $e$, *not* $\log_{10}$) elementwise.
  - **Domain Context (Why Softplus over Clipping/ReLU?):** Hard clipping $\max(0, x)$ (ReLU) maps all negative inputs to exact `0` (zero gradient, "dead neurons") and has a non-differentiable corner at $x = 0$. Softplus is strictly positive and infinitely differentiable ($C^\infty$) everywhere; its derivative is the logistic sigmoid $\frac{d}{dx}\ln(1 + e^x) = \frac{e^x}{1 + e^x} = \frac{1}{1 + e^{-x}}$, and for large positive $x$, $e^x \gg 1 \implies \ln(1 + e^x) \approx \ln(e^x) = x$.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - If `x` is a Python `int` or `float` (e.g., `0` or `3.0`): `np.exp(0)` returns `np.float64(1.0)`, `1 + ...` gives `np.float64(2.0)`, and `np.log(...)` returns **`np.float64(0.6931471805599453)`** (a 0-D NumPy scalar, *not* a built-in Python `float` — notice line 30's doctest explicitly casts `float(softplus(0))`).
  - If `x` is an `ndarray` of arbitrary shape `S` (e.g., `(200,)` in [`plot`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E02_vectorise.py#L49-L50) or `(2, 3, 4)`): every intermediate result and the returned array has exact shape **`S`** and `dtype=float64` (or `float32` if `x` was `float32`).
- **Concrete Step-by-Step Trace:**
  - Input: `x = np.array([-2.0, 0.0, 2.0])` → shape `(3,)`, `dtype=float64`.
  - Step 1 (`np.exp(x)`): `array([0.13533528, 1.0, 7.3890561])` → shape `(3,)`, `dtype=float64`.
  - Step 2 (`1 + ...`): `array([1.13533528, 2.0, 8.3890561])` → shape `(3,)`, `dtype=float64`.
  - Step 3 (`np.log(...)`): `array([0.12692801, 0.69314718, 2.12692801])` → shape `(3,)`, `dtype=float64`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Large positive `x` (e.g., `softplus(1000.0)`):** **IEEE-754 Overflow!** The largest finite `float64` is $\approx 1.798 \times 10^{308}$, and $\ln(1.798 \times 10^{308}) \approx 709.78$. For `x = 1000.0`, `np.exp(1000.0)` emits `RuntimeWarning: overflow encountered in exp` and returns `np.inf`, so `np.log(1 + np.inf)` returns `np.inf` — even though mathematically $\ln(1 + e^{1000}) \approx 1000.0$ is completely finite! Numerically stable implementations use `np.logaddexp(0, x)`, which rewrites $\ln(1 + e^x) = \max(0, x) + \ln(1 + e^{-|x|})$ so the exponent argument is always $\le 0$.
  - **Large negative `x` (e.g., `softplus(-50.0)`):** ** Precision Underflow!** $e^{-50} \approx 1.93 \times 10^{-22}$, which is smaller than `float64` machine epsilon ($\epsilon \approx 2.22 \times 10^{-16}$). Adding `1 + 1.93e-22` rounds to exact `1.0`, so `np.log(1.0)` returns `0.0` instead of `1.93e-22`. Using `np.log1p(np.exp(x))` preserves precision near zero because `log1p(u)` computes $\ln(1 + u)$ via Taylor series for tiny $u$.
  - **A plain Python `list` (e.g., `softplus([0, 3])`):** Works! NumPy `ufunc`s automatically coerce array-like sequences via `np.asarray` and return a `float64` `ndarray`.
  - **What if we had used `math.log(1 + math.exp(x))`?** Works for scalars, but crashes immediately on an `ndarray` with `TypeError: only length-1 arrays can be converted to Python scalars`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** `O(N)` where `N = x.size` is the total number of elements. Performs 3 linear C passes over `N` elements (`exp`, `+ 1`, `log`), avoiding per-element Python bytecode dispatch and object boxing (`~50–100×` faster than `[math.log(1 + math.exp(v)) for v in x]`).
- **Space Complexity:** `O(N)` auxiliary space for the `ndarray` case (`np.exp(x)` allocates an `N`-element buffer, `1 + ...` allocates a second, and `np.log(...)` allocates the returned `N`-element array; intermediate temporaries are garbage-collected as soon as the expression finishes, keeping peak overhead `O(N)`). For a scalar input, `O(1)`.

### Likely Interview Q&A
- **Q: Why didn't you have to write an `if isinstance(x, np.ndarray):` branch inside `softplus`?**  
  **A:** Because `np.exp`, `+`, and `np.log` are NumPy universal functions (`ufunc`s). They dispatch at the C level on both 0-D scalars and arbitrary-dimensional `ndarray`s element-by-element.
- **Q: What happens if a neural network outputs `x = 800` into your `softplus(x)`? How would you fix it?**  
  **A:** `np.exp(800)` overflows 64-bit floating-point (`> 709.78`), producing `np.inf`. I would replace `np.log(1 + np.exp(x))` with `np.logaddexp(0, x)` (or `np.maximum(0, x) + np.log1p(np.exp(-np.abs(x)))`), which never exponentiates a positive number.

---

## 5. `E03_broadcast.py` — Broadcasting & Outer Products (`combine`, `times_table`)

- **File:** [E03_broadcast.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py)
- **Functions:** [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43), [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L46-L58), and [`# ANSWER`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L60-L66)
- **Difficulty Tier:** Moderate

### Your Code
```python
def combine(A, b, c, d):
    return A + b.reshape(-1, 1) + c + d


def times_table(n):
    return np.array(range(1, n+1)).reshape(-1, 1) * np.array(range(1, n + 1))

# ANSWER: A has shape (n, m), b has shape (n,), and c has shape (m,).
# When broadcasting, NumPy aligns shapes from right to left and pads missing
# dimensions on the left with 1.
# For c, this becomes (1, m), which aligns with the columns of A and stretches down the rows.
# For b, (n,) aligns with the trailing axis (the columns m), which is the wrong axis
# and causes an error unless n == m.
# Reshaping b to (n, 1) puts n on the rows and lets the 1 stretch across the columns.
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43) builds an `(n, m)` matrix $z_{i,j} = A_{i,j} + b_i + c_j + d$ in one vectorised expression by reshaping the row-offset vector `b` from `(n,)` into a column vector `(n, 1)` so it stretches horizontally across columns, while `c` `(m,)` naturally stretches vertically down rows. [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L46-L58) computes the outer product of `1..n` with itself by multiplying an `(n, 1)` column vector against an `(n,)` row vector to yield an `(n, n)` multiplication grid.
- **Line-by-Line & Shape Breakdown:**
  - `b.reshape(-1, 1)`: `-1` tells NumPy *"infer this dimension automatically from `b.size`"* (`n // 1 = n`), producing a 2-D view of shape `(n, 1)` without copying `b`'s data (`b[:, None]` or `b[:, np.newaxis]` do the exact same thing).
  - `A + b.reshape(-1, 1)`: `(n, m)` + `(n, 1)` → axis 1 of `b` has length `1`, so NumPy sets its column stride to `0` and stretches `b[i]` across all `m` columns → `(n, m)`.
  - `+ c`: `(n, m)` + `(m,)` → NumPy right-aligns `(m,)` and left-pads with `1` to `(1, m)`, stretching `c[j]` down all `n` rows → `(n, m)`.
  - `+ d`: `(n, m)` + `()` (scalar) → left-padded to `(1, 1)` and stretched across both axes → `(n, m)`.
  - `times_table(n)`: Creates `1..n` of shape `(n,)`, reshapes the left copy to `(n, 1)`, and multiplies `(n, 1) * (n,)` (which pads the right copy to `(1, n)`), broadcasting both axes to `(n, n)` where entry `[i, j]` is `(i + 1) * (j + 1)`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43): `A` `(n, m)` `float64`, `b` `(n,)` → `b.reshape(-1, 1)` `(n, 1)`, `c` `(m,)`, `d` `float`/`int` → returns `ndarray` of shape **`(n, m)`** and `dtype=float64`.
  - [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L46-L58): `n` (`int`, `n >= 1`) → `(n, 1)` `int64` × `(n,)` `int64` → returns `ndarray` of shape **`(n, n)`** and `dtype=int64`.
- **Concrete Step-by-Step Trace (`combine` Doctest 2):**
  - `A` = `[[1., 2., 3.], [4., 5., 6.]]` → shape `(2, 3)`.
  - `b` = `[0., 10.]` `(2,)` → `b.reshape(-1, 1)` = `[[0.], [10.]]` `(2, 1)`.
  - `A + b.reshape(-1, 1)` = `[[1., 2., 3.], [14., 15., 16.]]` `(2, 3)`.
  - `+ c` (`[0., 0., 100.]`, shape `(3,)` → `(1, 3)`) = `[[1., 2., 103.], [14., 15., 116.]]` `(2, 3)`.
  - `+ d` (`1.0`, shape `()`) = `[[2., 3., 104.], [15., 16., 117.]]` `(2, 3)`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Silent Bug Trap if `n == m` and you forgot `b.reshape(-1, 1)`:** In Doctest 1, `A` is `(4, 4)` (`n == m == 4`) and `b` is `(4,)`. Without `.reshape(-1, 1)`, `A + b` **would NOT raise an error** — it would silently treat `b` as `(1, 4)` and add `b[j]` along the *columns* instead of `b[i]` down the *rows*, returning wrong numbers (`[[121., 132., 143., 154.], ...]`)! Only when `n != m` (Doctest 2: `(2, 3)` and `(2,)`) does NumPy raise `ValueError: operands could not be broadcast together with shapes (2,3) (2,)`.
  - **`times_table(0)` or `times_table(-3)`:** `range(1, 1)` is empty! `np.array(range(1, 1))` produces an empty 1-D array `array([], dtype=float64)` (note: `np.array([])` defaults to **`float64`**, whereas `np.arange(1, 1)` preserves `int64`!). Reshaping `(0,)` with `.reshape(-1, 1)` yields `(0, 1)`, and `(0, 1) * (0,)` broadcasts `(0, 1)` with `(1, 0)` to return an empty array of shape `(0, 0)` and `dtype=float64`.
  - **`times_table(3.0)` (passing a `float`):** `range(1, 4.0)` raises `TypeError: 'float' object cannot be interpreted as an integer`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - [`combine`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L22-L43): `O(n * m)` (`.reshape(-1, 1)` is `O(1)`; each of the three `+` operations touches `n * m` elements in C).
  - [`times_table`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L46-L58): `O(n^2)` (`O(n)` to create the 1-D vectors, dominated by `O(n^2)` to compute all `n * n` products).
- **Space Complexity:**
  - **Crucial Distinction ("Nothing is copied" vs Output Materialisation):** Broadcasting *itself* copies nothing — `b.reshape(-1, 1)` and the stretched `(n, m)` view of `b` or `c` use **`O(1)`** view metadata (stride `= 0` along the stretched axis). However, the **result** of `A + ...` and `col * row` IS a newly allocated `(n, m)` / `(n, n)` array in memory, so total output space is **`O(n * m)`** for `combine` and **`O(n^2)`** for `times_table`.
- **Comparison with Official Solution (`times_table`) & Embedded `QUESTION`:**
  - The official solution writes `row = np.arange(1, n + 1); return row.reshape(-1, 1) * row`. Compared to `np.array(range(1, n+1))`, `np.arange` builds the `int64` buffer directly in C without iterating a Python `range` object or constructing the `1..n` array twice, and keeps `dtype=int64` even when `n = 0`. Asymptotically both are `O(n^2)` time and `O(n^2)` space.
  - **Embedded `QUESTION` ([lines 60–66](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E03_broadcast.py#L60-L66)):** Your written explanation is spot-on: NumPy aligns shapes at the **trailing (right-hand) end** and left-pads shorter shapes with `1`s. Thus `c` `(m,)` becomes `(1, m)` (matching `A`'s `m` columns and stretching down `n` rows), whereas `b` `(n,)` would become `(1, n)` and collide with `m` on the column axis unless reshaped to `(n, 1)`.

### Likely Interview Q&A
- **Q: The module docstring says *"Nothing is copied: the stretching is a fiction Numpy maintains."* How does NumPy stretch `(n, 1)` to `(n, m)` without copying memory?**  
  **A:** Every `ndarray` stores a `strides` tuple giving the byte step to advance by 1 index along each axis. When broadcasting an axis of length `1` to length `m`, NumPy sets the byte stride for that axis to `0`, so the C loop reads the exact same memory address `m` times across each row without duplicating values.
- **Q: What does `-1` mean in `b.reshape(-1, 1)`? Could you write `b.reshape(-1, -1)`?**  
  **A:** `-1` asks NumPy to infer that axis length by dividing `b.size` by the product of the specified dimensions (`n // 1 = n`). You can only use `-1` on **at most one** axis — `b.reshape(-1, -1)` raises `ValueError: can only specify one unknown dimension` because the factorisation would be ambiguous.

---

## 6. `E04_axis_masks.py` — Boolean Masks & Axis Reductions (`count_above`, `values_above`, `column_means`, `row_maxes`)

- **File:** [E04_axis_masks.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py)
- **Functions:** [`count_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L19-L28), [`values_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L31-L40), [`column_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L43-L52), [`row_maxes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L55-L64)
- **Difficulty Tier:** Warm-up / Moderate

### Your Code
```python
def count_above(x, t):
    return int(np.sum(x > t))


def values_above(x, t):
    return x[x > t]


def column_means(X):
    return X.mean(axis=0)


def row_maxes(X):
    return X.max(axis=1)
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`count_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L19-L28) and [`values_above`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L31-L40) build a boolean mask `x > t` of `True`/`False` entries, then either sum the `True`s (`True == 1, False == 0`) or index `x` with the mask to extract matching values. [`column_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L43-L52) and [`row_maxes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L55-L64) collapse a 2-D matrix along `axis=0` (down the rows, one mean per column) and `axis=1` (across the columns, one maximum per row).
- **Line-by-Line & Method Breakdown:**
  - `x > t`: Broadcasts threshold `t` against `x` to produce an `ndarray` of `dtype=bool` with the exact same shape as `x`.
  - `int(np.sum(x > t))`: `np.sum` treats `True` as `1` and `False` as `0` in an `int64` accumulator; `int(...)` converts the returned `np.int64` scalar into a plain Python `int`. (Alternative: `int(np.count_nonzero(x > t))`.)
  - `x[x > t]`: Boolean mask indexing selects every element where the mask is `True`, preserving row-major (`C`-contiguous) order.
  - `X.mean(axis=0)`: Collapses axis `0` (rows) of `(n, m)` → returns `(m,)` `float64`.
  - `X.max(axis=1)`: Collapses axis `1` (columns) of `(n, m)` → returns `(n,)` with the same `dtype` as `X`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes Summary:**

| Function | Input `X` / `x` Shape & Dtype | Intermediate Shape & Dtype | Return Type, Shape & Dtype |
| :--- | :--- | :--- | :--- |
| [`count_above(x, t)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L19-L28) | Any shape `S`, numeric `dtype` | `x > t`: shape `S`, `bool`; `np.sum`: `()` `int64` | Plain Python `int` |
| [`values_above(x, t)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L31-L40) | Any shape `S`, `dtype=D` | `x > t`: shape `S`, `bool` | `ndarray`, **1-D shape `(k,)`**, `dtype=D` (always a **copy**!) |
| [`column_means(X)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L43-L52) | `(n, m)`, `int64` or `float64` | — | `ndarray`, shape **`(m,)`**, `dtype=float64` |
| [`row_maxes(X)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E04_axis_masks.py#L55-L64) | `(n, m)`, `dtype=D` | — | `ndarray`, shape **`(n,)`**, `dtype=D` |

- **Concrete Step-by-Step Trace (`values_above` & `column_means`):**
  - `x = np.array([1, 5, 3, 9, 2])` (`(5,)`, `int64`), `t = 2`:
    - `mask = x > 2` → `array([False, True, True, True, False])` (`(5,)`, `bool`).
    - `count_above`: `np.sum(mask)` → `np.int64(3)` → `int(...)` → `3`.
    - `values_above`: `x[mask]` → `array([5, 3, 9])` (`(3,)`, `int64`).
  - `X = np.array([[1.0, 2.0, 3.0], [3.0, 4.0, 9.0]])` (`(2, 3)`, `float64`):
    - `X.mean(axis=0)` averages `(1+3)/2, (2+4)/2, (3+9)/2` → `array([2., 3., 6.])` (`(3,)`).
    - `X.max(axis=1)` takes `max(1,2,3), max(3,4,9)` → `array([3., 9.])` (`(2,)`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **2-D array into `values_above` (Classic Trace Trap!):** Suppose `x = np.array([[1, 8], [6, 2]])` (shape `(2, 2)`) and `t = 5`. What shape does `values_above(x, 5)` return? **1-D shape `(2,)`** (`array([8, 6])`), *not* 2-D! Because different rows can have different numbers of `True` values, boolean indexing cannot form a rectangular 2-D grid and **always flattens** to 1-D.
  - **No values qualify (`t = 100`):** `values_above` returns an empty 1-D array `array([], dtype=x.dtype)` of shape `(0,)`; `count_above` returns `0`.
  - **Empty rows/columns in `row_maxes` vs `column_means`:**
    - `row_maxes(np.zeros((2, 0)))` raises **`ValueError: zero-size array to reduction operation maximum which has no identity`**, because `max` over an empty set has no neutral element!
    - `column_means(np.zeros((0, 3)))` emits `RuntimeWarning: Mean of empty slice` (`0.0 / 0`) and returns `array([nan, nan, nan])`.
  - **`np.nan` inside `X`:** Any comparison with `NaN` (`np.nan > t`) is `False`. In `X.mean(axis=0)` and `X.max(axis=1)`, NumPy **propagates `nan`** into any column/row containing a `nan` (unlike `np.nanmean`/`np.nanmax` or pandas `.mean()`, which skip `NaN` by default).
  - **1-D array passed to `row_maxes(np.array([1.0, 2.0]))`:** Raises `np.exceptions.AxisError: axis 1 is out of bounds for array of dimension 1`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** All four functions run in **`O(N)`** where `N` is the total number of elements (`x.size` or `n * m`), visiting each element a constant number of times in C.
- **Space Complexity:**
  - `count_above(x, t)`: **`O(N)`** temporary memory because `x > t` materialises an `N`-byte boolean array before `np.sum` reduces it.
  - `values_above(x, t)`: **`O(N)`** (`N` bytes for the boolean mask + `k` elements for the newly allocated output copy, where `0 <= k <= N`). Note: unlike slicing `x[1:4]`, **`x[x > t]` is ALWAYS a copy**, so mutating the returned array never mutates `x`.
  - `column_means(X)` / `row_maxes(X)`: **`O(m)`** and **`O(n)`** respectively for the reduced output vector (`O(1)` extra working space).

### Likely Interview Q&A
- **Q: Why is `axis=0` the *column* means when axis `0` is the *rows*?**  
  **A:** In NumPy, `axis` specifies the dimension you **collapse** (sum over), not the dimension that survives. Collapsing axis `0` (stepping down the `n` rows) reduces shape `(n, m)` to `(m,)`, leaving one average for each of the `m` columns.
- **Q: If I modify the array returned by `values_above(x, 2)`, does `x` change?**  
  **A:** No. Boolean mask indexing (`x[mask]`) must gather non-contiguous elements scattered across memory, so NumPy always allocates and returns a fresh **copy**, unlike basic slice indexing (`x[1:4]`), which returns a stride-based **view**.

---

## 7. `E05_broadcastable.py` — Implementing NumPy's Broadcasting Rule (`is_broadcastable`)

- **File:** [E05_broadcastable.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py)
- **Function:** [`is_broadcastable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py#L22-L42)
- **Difficulty Tier:** **Hard (8–10 Mark Target)**

### Your Code
```python
def is_broadcastable(X, Y):
    # need to check from right to left. If the values don't match and either value isn't 1 then it's false.

    for n, m in zip(reversed(X.shape), reversed(Y.shape)):
        if n != m and n != 1 and m != 1:
            return False
    return True
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`is_broadcastable`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E05_broadcastable.py#L22-L42) checks whether two NumPy arrays `X` and `Y` have compatible shapes for elementwise broadcasting without ever touching their data values. It pairs their dimension lengths from right to left using `zip(reversed(X.shape), reversed(Y.shape))` and returns `False` the moment it finds an aligned pair `(n, m)` that are unequal and neither is `1`; otherwise it returns `True`.
- **Line-by-Line & Mathematical Equivalence Breakdown:**
  - `X.shape`, `Y.shape`: Tuples of non-negative `int`s (e.g., `(2, 3, 4)` and `(3, 1)`), stored in the `ndarray` C header.
  - `reversed(X.shape)`: Returns a lazy `tuple_reverseiterator` yielding dimensions from the trailing (rightmost) axis backwards (e.g., `4, 3, 2`).
  - `zip(..., ...)`: Pairs trailing dimensions `(n, m)` one by one and **stops automatically when the shorter shape runs out**.
  - **KEY INSIGHT — Why `zip` (stopping early) is 100% equivalent to left-padding with `1`s:**  
    NumPy's specification states: *"pad the shorter shape on the left with `1`s."* Suppose `X.shape` is `(2, 3, 4)` and `Y.shape` is `(3, 1)`. Padded, `Y.shape` becomes `(1, 3, 1)`, so the leftmost pair is `(2, 1)`. In general, *every* extra leading dimension `d` of the longer shape would be paired against a padded `1` (`m = 1`). Since two axes are ALWAYS compatible when either one is `1` (`m == 1` makes `n != m and n != 1 and m != 1` guaranteed `False` for *every* integer `n`, even `n = 0`!), those leading dimensions can **never** cause a failure. Stopping when the shorter tuple ends via `zip` is therefore mathematically identical to `itertools.zip_longest(..., fillvalue=1)`!
  - `if n != m and n != 1 and m != 1:`: De Morgan's negation of compatibility `not (n == m or n == 1 or m == 1)`. Early-returns `False` on the first clash.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - Inputs: `X: np.ndarray`, `Y: np.ndarray` (any shapes, any dtypes).
  - Intermediates: `X.shape`, `Y.shape` are `tuple[int, ...]`; `n` and `m` are plain Python `int`s.
  - Return Type: Plain Python `bool` (`True` or `False`).
- **Concrete Step-by-Step Traces:**
  1. `X` shape `(2, 3, 4)`, `Y` shape `(3, 1)`:
     - `reversed(X.shape)` → `4, 3, 2`; `reversed(Y.shape)` → `1, 3`.
     - Iteration 1: `n = 4, m = 1` → `m == 1`, `if` condition is `False` (compatible, result axis = `4`).
     - Iteration 2: `n = 3, m = 3` → `n == m`, `if` condition is `False` (compatible, result axis = `3`).
     - `zip` exhausts `Y.shape` (leading `2` is implicitly compatible with `1`). Loop ends → returns **`True`**.
  2. `X` shape `(3, 5)`, `Y` shape `(3,)`:
     - Iteration 1: `n = 5, m = 3` → `5 != 3 and 5 != 1 and 3 != 1` is `True` → immediately returns **`False`**.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **0-D Scalar Arrays (`X = np.array(42)`, `X.shape == ()`):** `reversed(())` is empty, so `zip` yields zero pairs, the loop executes `0` times, and the function returns **`True`**! That matches NumPy: a 0-D scalar broadcasts with *any* array shape.
  - **Zero-Length (Empty) Axes (`(0, 3)` vs `(1, 3)` and `(0, 3)` vs `(4, 3)`):**
    - `(0, 3)` and `(1, 3)`: `3 == 3`, then `n = 0, m = 1`. Because `m == 1`, the `if` condition is `False` → returns **`True`**! Verify in NumPy: `(np.zeros((0, 3)) + np.zeros((1, 3))).shape == (0, 3)` (a length-`1` axis can validly stretch `0` times to length `0`!).
    - `(0, 3)` and `(4, 3)`: `3 == 3`, then `n = 0, m = 4`. Neither is `1` and `0 != 4` → returns **`False`**! Verify in NumPy: raises `ValueError: operands could not be broadcast together with shapes (0,3) (4,3)`.
  - **Plain Python `list` or `int` (e.g., `is_broadcastable([1, 2], 5)`):** Raises `AttributeError: 'list' object has no attribute 'shape'`. (If we wanted to support array-likes, we'd read `np.shape(X)` instead of `X.shape`, though `np.shape([1, 2])` would traverse the list.)

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(min(d_X, d_Y))`** where `d_X = X.ndim` and `d_Y = Y.ndim`. Crucially, with respect to the **number of array elements** $N$, this function is **`O(1)`**! Whether `X` holds `6` elements or `6,000,000,000` elements, `X.shape` is already cached in the array header and no array data is ever read.
- **Space Complexity:** **`O(1)`** auxiliary space! Both `reversed(tuple)` and `zip(...)` return lazy C iterators rather than slicing or copying tuples like `X.shape[::-1]` (which would allocate reversed tuple copies of size `O(d_X + d_Y)`).
- **Comparison with Built-in `np.broadcast_shapes(X.shape, Y.shape)`:** NumPy 1.20+ provides `np.broadcast_shapes`, which throws `ValueError` on mismatch and returns the resulting broadcast shape tuple (e.g., `(2, 3, 4)`), whereas writing the loop directly in `O(1)` space avoids exception-handling control flow and cleanly exposes the right-to-left rule.

### Likely Interview Q&A
- **Q: Your function doesn't pad the shorter shape with `1`s on the left, yet the docstring states padding with `1`s is part of NumPy's rule. Why doesn't a missing leading dimension ever break your `zip` loop?**  
  **A:** Because any leading dimension `d` of the longer shape would only ever be paired against a padded `1`. Under the compatibility rule, `1` is compatible with *every* dimension length (`m == 1`), so those pairs can never trigger `return False`. Stopping early when `zip` exhausts the shorter shape is therefore completely equivalent.
- **Q: What would you change if the interviewer asked you to return the *resulting broadcast shape* tuple instead of `True`/`False` (or `None` if incompatible)?**  
  **A:** Then I *would* need the leading dimensions! I would use `itertools.zip_longest(reversed(X.shape), reversed(Y.shape), fillvalue=1)`, collect `max(n, m)` at each compatible step (except when one is `0` and the other is `1`, where the broadcast length is **`0`**, so `n if m == 1 else m`!), and reverse the collected list at the end! *(Mentioning the `(0, 1) -> 0` trap vs `max(0, 1) -> 1` is a guaranteed 10/10 insight!)*

---

## 8. `E06_heatmap.py` — All-Pairs Distance Matrix (`distance_matrix`)

- **File:** [E06_heatmap.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py)
- **Function:** [`distance_matrix`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L31-L45) (Helpers given: [`plot_heatmap`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L50-L59), [`main`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L62-L73)) and [`# ANSWER`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L80)
- **Difficulty Tier:** **Hard (8–10 Mark Target — Complexity & Memory Trade-off)**

### Your Code
```python
def distance_matrix(X):
    return cdist(X, X)

# ... (plot_heatmap and main given) ...

# ANSWER: The diagonal from top left to bottom right is different as this is the image being compared against itself for each row and column. 
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`distance_matrix`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L31-L45) computes the all-pairs Euclidean distance table `D` where `D[i, j]` is the $L_2$ distance between row `i` and row `j` of feature matrix `X`. Passing `(X, X)` to `scipy.spatial.distance.cdist` delegates the doubly nested pair loop to compiled C, returning a square, symmetric `(n, n)` matrix with `0.0` down the main diagonal.
- **Line-by-Line & Pipeline Breakdown:**
  - `cdist(XA, XB, metric='euclidean')`: Computes $D_{i,j} = \sqrt{\sum_{k=0}^{d-1} (XA_{i,k} - XB_{j,k})^2}$ for every row $i \in \{0, \dots, n_A - 1\}$ and row $j \in \{0, \dots, n_B - 1\}$.
  - When `XA` and `XB` are both `X` of shape `(n, d)` (`(72, 64)` in [`main`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L67-L68), where `72` = 24 Kodak photos × 3 sizes and `64` = $4^3$ colour-bin proportions), `cdist(X, X)` produces shape `(72, 72)`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - Input `X`: 2-D `ndarray` of shape `(n, d)` (`n` observations/photos, `d` features).
  - Output `D`: 2-D `ndarray` of shape **`(n, n)`** and **`dtype=float64`** (even if `X` has `int64` or `uint8` dtype, `cdist` converts inputs to C `double` and returns `float64`).
- **Concrete Step-by-Step Trace (Doctest 1):**
  - `X = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])` → shape `(3, 2)` (`n = 3` points in `d = 2` dimensions).
  - `D[0, 0] = ||[0,0] - [0,0]|| = 0.0`; `D[0, 1] = sqrt(3^2 + 4^2) = 5.0`; `D[0, 2] = sqrt(6^2 + 8^2) = 10.0`.
  - Returns `array([[0., 5., 10.], [5., 0., 5.], [10., 5., 0.]])` → shape `(3, 3)`, symmetric (`D == D.T`), zero diagonal (`np.diag(D) == [0., 0., 0.]`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **1-D Array (e.g., `distance_matrix(np.array([1.0, 4.0]))`):** **Crashes!** `cdist` strictly enforces 2-D inputs and raises `ValueError: XA must be a 2-dimensional array.` Notice Doctest 2 passes `np.array([[1.0], [4.0]])` (shape `(2, 1)`, 2 rows of 1 feature).
  - **Single Row (`X` shape `(1, 64)`):** Returns `array([[0.]])` of shape `(1, 1)`.
  - **Empty Rows (`X` shape `(0, 64)`):** Returns an empty matrix of shape `(0, 0)` and `dtype=float64`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n^2 * d)`** — there are $n^2$ pairs `(i, j)`, and each Euclidean distance sums $d$ squared feature differences. (Note: because `D` is symmetric with a zero diagonal, `scipy.spatial.distance.squareform(pdist(X))` computes only the $\frac{n(n-1)}{2}$ upper-triangle pairs, cutting the constant factor in half while keeping asymptotic `O(n^2 * d)`.)
- **Space Complexity (THE Star Analyse Comparison — `cdist` vs 3-D Broadcasting!):**
  - **`cdist(X, X)`:** **`O(n^2)`** space — allocates only the `(n, n)` output matrix (`72 × 72 × 8` bytes ≈ `41 KB`), accumulating each `d`-dimensional dot/difference inside CPU registers in C!
  - **Pure-NumPy 3-D Broadcasting (`np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)`):** Broadcasts `(n, 1, d) - (1, n, d)` into a full **`(n, n, d)`** intermediate tensor in RAM, costing **`O(n^2 * d)`** memory! If `n = 10,000` photos and `d = 64` bins, `cdist` needs `800 MB`, whereas 3-D broadcasting tries to allocate `51.2 GB` and crashes with `MemoryError`!
- **Embedded `QUESTION` Deep Dive ([line 80](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E06_heatmap.py#L80)):**
  - Your `# ANSWER` rightly notes that entry `(i, i)` along the top-left to bottom-right diagonal compares each photo against itself.
  - **Two Extra Details to Mention Verbally in the Interview for Full Marks:**
    1. **Why it gets an extreme colour:** A photo's distance to itself is **exact `0.0`**, and since Euclidean distance is non-negative ($D_{i,j} \ge 0$, with $D_{i,j} > 0$ for distinct histograms), `0.0` sits at the absolute minimum end of `imshow`'s `viridis` colour scale (deep purple).
    2. **The faint `3 × 3` squares along the diagonal:** Because `paths` is sorted alphabetically (`kodim01_full`, `kodim01_half`, `kodim01_thumb`, `kodim02_full`, ...), every block of 3 consecutive rows/columns is the *same* photograph at three resolutions (`full`, `half`, `thumb`). After [`as_proportions`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E01_photos.py#L103-L119) normalises pixel counts, those 3 versions have nearly identical colour distributions ($D_{i,j} \approx 0$), forming `24` tiny `3 × 3` dark blocks down the diagonal!

### Likely Interview Q&A
- **Q: Could you write `distance_matrix(X)` in pure NumPy using broadcasting without `cdist`? Why is `cdist` better?**  
  **A:** Yes: `np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)`. Both take `O(n^2 * d)` time, but 3-D broadcasting materialises an `(n, n, d)` intermediate array (`O(n^2 * d)` RAM), whereas `cdist` computes each distance in a C loop and stores only the `(n, n)` result (`O(n^2)` RAM).
- **Q: Looking at `distances.png`, why is the heatmap symmetric across the diagonal, and what are the tiny `3×3` squares along the diagonal?**  
  **A:** Symmetry comes from $\|x_i - x_j\|_2 = \|x_j - x_i\|_2$ (`D[i, j] == D[j, i]`). The `3×3` squares appear because each Kodak image is stored at `full`, `half`, and `thumb` sizes adjacent in alphabetical order, and `as_proportions` makes their normalised histograms nearly identical.

---

## 9. `E07_brightness.py` — Image Reductions & Fancy Indexing (`brightness`, `darkest_first`)

- **File:** [E07_brightness.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py)
- **Functions:** [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33), [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50) (Helper given: [`main`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L53-L64))
- **Difficulty Tier:** Moderate

### Your Code
```python
def brightness(image):
    return float(image.mean())


def darkest_first(names, values):
    # sort = np.argsort(values)
    # names_arr = np.array(names)
    # return names_arr[sort]
    return np.array(names)[np.argsort(values)]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33) collapses an entire `(H, W, 3)` `uint8` image across height, width, and all three RGB channels simultaneously via `image.mean()` (`axis=None`) and converts the NumPy scalar into a plain Python `float`. [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50) finds the index permutation that sorts `values` ascending via `np.argsort(values)` and uses **fancy indexing** on `np.array(names)` to reorder the photo names from darkest to brightest.
- **Line-by-Line & Method Breakdown:**
  - `image.mean()`: With no `axis` argument (`axis=None`), NumPy sums all $H \times W \times 3$ bytes into a `float64` accumulator (preventing `uint8` 0–255 wrap-around!) and divides by `image.size`, returning `np.float64`.
  - `float(...)`: Unboxes `np.float64` into a native Python `float` as required by the docstring (*"as an ordinary float"*).
  - `np.argsort(values)`: Accepts a list or array of `n` numbers and returns an `int64` `ndarray` of shape `(n,)` holding the **original indices** in the order that sorts `values` from smallest to largest.
  - `np.array(names)[...]`: Converts Python `list[str]` into a fixed-width Unicode NumPy array (`dtype='<U...'`) **because plain Python `list`s do not support indexing with an array/list of integers** (`names[order]` on a `list` raises `TypeError: only integer scalar arrays can be converted to a scalar index`). Indexing an `ndarray` with an integer `ndarray` is **fancy indexing**.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - [`brightness(image)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33): `image` `(H, W, 3)` `uint8` → `image.mean()` `()` `np.float64` → `float(...)` → plain Python **`float`**.
  - [`darkest_first(names, values)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50):
    - `names`: `list[str]` of length `n` → `np.array(names)`: shape `(n,)`, `dtype='<Uk'` (where `k` is the length of the longest string in `names`, e.g., `'<U1'` for `["a", "b", "c"]` or `'<U12'` for `'kodim01_full'`).
    - `values`: `list[float]` or `ndarray` of length `n` → `np.argsort(values)`: shape `(n,)`, `dtype=int64`.
    - Return value: `ndarray` of shape **`(n,)`** and `dtype='<Uk'` (a **copy**).
- **Concrete Step-by-Step Trace (Doctest 1):**
  - `names = ["a", "b", "c"]`, `values = [5.0, 1.0, 3.0]`.
  - `np.argsort([5.0, 1.0, 3.0])`: Smallest is `1.0` at index `1`, next is `3.0` at index `2`, largest is `5.0` at index `0` → `array([1, 2, 0])` (`(3,)`, `int64`).
  - `np.array(["a", "b", "c"])` → `array(['a', 'b', 'c'], dtype='<U1')`.
  - Fancy index `[1, 2, 0]` picks index `1` (`'b'`), index `2` (`'c'`), index `0` (`'a'`) → `array(['b', 'c', 'a'], dtype='<U1')`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Tied brightness values (e.g., `values = [3.0, 1.0, 3.0]`):** Default `np.argsort` uses introsort (`kind='quicksort'`), which is not guaranteed stable across all types/versions unless `np.argsort(values, kind='stable')` is passed (with `'stable'`, tied indices `0` and `2` are guaranteed to stay `[1, 0, 2]`).
  - **Mismatched lengths:**
    - If `len(values) > len(names)` (e.g., `names` has 2 items, `values` has 3): `np.argsort` produces index `2`, which raises **`IndexError: index 2 is out of bounds for axis 0 with size 2`**.
    - If `len(values) < len(names)` (e.g., `names` has 5 items, `values` has 3): `np.argsort` only contains indices `0, 1, 2`, so it **silently drops** `names[3:]` without raising an error!
  - **Brightest first (descending order):** How would you reverse it? `np.array(names)[np.argsort(values)[::-1]]` (or `np.argsort(-np.asarray(values))` for numeric values).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33): **`O(H * W)`** (specifically `3 * H * W` pixel-channel values summed in C).
  - [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50): **`O(n log n + n * L)`** where `n = len(values)` and `L` is the max string length (`O(n log n)` comparisons in `np.argsort` + `O(n * L)` to build and fancy-index the `<UL` string array).
- **Space Complexity:**
  - [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33): **`O(1)`** auxiliary memory! `image.mean()` streams through the buffer without copying the image.
  - [`darkest_first`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L36-L50): **`O(n * L)`** (allocates `np.array(names)` of `n * L * 4` bytes for UTF-32 `<U`, the `(n,)` `int64` index array from `argsort`, and the reordered `(n,)` `<U` copy).

### Likely Interview Q&A
- **Q: Why couldn't you just write `return names[np.argsort(values)]` without `np.array(names)`?**  
  **A:** `names` is a Python `list`, and Python lists only accept a single `int` or a `slice` inside `[]`. Converting `names` to a NumPy `ndarray` unlocks **fancy indexing**, where passing an integer array `idx` of shape `(n,)` gathers `[names_arr[i] for i in idx]` in C.
- **Q: `image` has `dtype=uint8` (max 255). Why doesn't `image.mean()` overflow when summing hundreds of thousands of pixels?**  
  **A:** Because `ndarray.mean()` automatically upcasts integer inputs to a `float64` accumulator internally before summing and dividing, unlike manual elementwise addition `img_a + img_b` which stays in `uint8` and wraps modulo 256.

---

## 10. `E08_grayscale.py` — Luminance Dot Product Along Last Axis (`to_gray`)

- **File:** [E08_grayscale.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py)
- **Function:** [`to_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L34-L51) (Constant: [`WEIGHTS`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L31); Helpers given: [`plot_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L56-L63), [`main`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L66-L77))
- **Difficulty Tier:** **Hard (8–10 Mark Target — N-D `@` Contraction & Dtype Promotion)**

### Your Code
```python
WEIGHTS = np.array([0.2126, 0.7152, 0.0722])


def to_gray(image):
    return image @ WEIGHTS
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`to_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L34-L51) converts an `(H, W, 3)` RGB colour image into a 2-D `(H, W)` greyscale luminance array by taking the dot product of every pixel's `[R, G, B]` triple with the ITU-R BT.709 perceptual weights `[0.2126, 0.7152, 0.0722]` in one vectorised `@` (`matmul`) operation. Because human vision is far more sensitive to green than red or blue, green carries `71.52%` of the weight, red `21.26%`, and blue `7.22%` (summing to `1.0`).
- **How `@` (`np.matmul`) Works on a 3-D Tensor and a 1-D Vector:**
  - For a single pixel `p = [r, g, b]` of shape `(3,)`, `p @ WEIGHTS` computes the inner product:
    $$\text{grey} = 0.2126\,r + 0.7152\,g + 0.0722\,b$$
  - When the left operand is **3-D** `(H, W, 3)` and the right operand is **1-D** `(3,)`, `np.matmul` (`@`) applies its general `gufunc` signature `(..., k), (k) -> (...)`: it treats the leading dimensions `(H, W)` as batch dimensions, contracts the **last axis** of `image` (size `3`) against the **only axis** of `WEIGHTS` (size `3`), and **drops the contracted axis**, returning shape `(H, W)`!
  - Notice how [`brightness`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E07_brightness.py#L24-L33) (`E07`) weighted R, G, and B equally (`1/3` each) and collapsed *all* axes to a single scalar, whereas [`to_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L34-L51) uses perceptual weights and collapses *only* the channel axis (`axis=-1`), preserving spatial `(H, W)`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - `image`: `ndarray` of shape `(H, W, 3)`, `dtype=uint8` (values `0..255`).
  - `WEIGHTS`: `ndarray` of shape `(3,)`, `dtype=float64` (`[0.2126, 0.7152, 0.0722]`).
  - Return value `image @ WEIGHTS`: `ndarray` of shape **`(H, W)`** (one axis fewer: `ndim` drops from `3` to `2`!) and **`dtype=float64`** (via NumPy type promotion `np.result_type(np.uint8, np.float64) == np.float64`, with values in `[0.0, 255.0]`).
- **Concrete Step-by-Step Trace (Doctests):**
  - `image = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)` → shape `(1, 2, 3)`.
    - Pixel `[0, 0]`: `0*0.2126 + 0*0.7152 + 0*0.0722 = 0.0`.
    - Pixel `[0, 1]`: `255*0.2126 + 255*0.7152 + 255*0.0722 = 255 * 1.0 = 255.0`.
    - Output: `array([[0., 255.]])`, shape `(1, 2)`, `dtype=float64`.
  - Pure red `[[[255, 0, 0]]]` `(1, 1, 3)` → `255 * 0.2126 = 54.213` (`54.21`, dark grey).
  - Pure green `[[[0, 255, 0]]]` `(1, 1, 3)` → `255 * 0.7152 = 182.376` (`182.38`, bright grey).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **An RGBA image with 4 channels `(H, W, 4)` (e.g., forgetting `[:, :, :3]` in `load`):** Raises **`ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0 ... (size 3 is different from 4)`**, because the last axis of `image` (`4`) must match `WEIGHTS.shape[0]` (`3`).
  - **What if `WEIGHTS` had shape `(3, 1)` instead of `(3,)`?** Then `(H, W, 3) @ (3, 1)` would return **3-D shape `(H, W, 1)`** instead of 2-D `(H, W)`! Because `WEIGHTS` is 1-D `(3,)`, `matmul` squeezes away the contracted dimension automatically.
  - **A single 1-D pixel `np.array([255, 0, 0], dtype=np.uint8)` (shape `(3,)`):** Still works! `(3,) @ (3,)` computes the vector inner product and returns 0-D scalar `np.float64(54.213)`.
  - **Why `vmin=0, vmax=255` in [`plot_gray`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W08/W08/E08_grayscale.py#L59)?** Without `vmin=0, vmax=255`, `plt.imshow(..., cmap="gray")` auto-scales the darkest pixel in the photo to pure black (`0`) and the brightest pixel to pure white (`255`), so a uniform mid-grey image of all `128.0`s would be rendered completely black!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(H * W * C)`** where `C = 3` (i.e., **`O(H * W)`** — 3 multiplications and 2 additions per pixel, executed in BLAS / compiled C).
- **Space Complexity (`@` vs Broadcasting `(image * WEIGHTS).sum(axis=-1)` — Great 9–10 Mark Point!):**
  - **`image @ WEIGHTS`:** Allocates `(H, W)` `float64` output (`8 * H * W` bytes, `O(H * W)` space; NumPy casts small chunks to `float64` internally during the `matmul` ufunc loop without materialising the whole 3-channel float image at once).
  - **`(image * WEIGHTS).sum(axis=2)`:** Broadcasting `(H, W, 3)` `uint8` × `(3,)` `float64` first materialises an entire **`(H, W, 3)` `float64`** intermediate array (`24 * H * W` bytes — **3× more float RAM** than the `(H, W)` output!) before `.sum(axis=2)` collapses it to `(H, W)`. Thus `image @ WEIGHTS` is simultaneously shorter, faster, and `3×` more memory-efficient!

### Likely Interview Q&A
- **Q: Usually `@` multiplies two 2-D matrices. Why does `image @ WEIGHTS` work when `image` is 3-D `(H, W, 3)` and `WEIGHTS` is 1-D `(3,)`, and why is the output 2-D `(H, W)`?**  
  **A:** NumPy's `matmul` (`@`) generalises to N-D arrays: when the right operand is 1-D of length `k`, `@` takes the dot product along the **last axis** of the left operand (which also has length `k = 3`) for every `(row, col)` position independently, collapsing that trailing axis so `(H, W, 3) @ (3,)` becomes `(H, W)`.
- **Q: Why is the output `dtype` `float64` instead of `uint8`, and why do `WEIGHTS` add up to `1.0`?**  
  **A:** Multiplying `uint8` by `float64` promotes to `float64` so fractional luminance values aren't truncated. Having positive weights that sum to `1.0` (`0.2126 + 0.7152 + 0.0722 = 1.0`) guarantees a convex combination: any RGB pixel with channels in `[0, 255]` maps cleanly into `[0.0, 255.0]`, with pure black `[0,0,0] -> 0.0` and pure white `[255,255,255] -> 255.0`.
