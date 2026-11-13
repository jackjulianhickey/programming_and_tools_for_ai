# Week 9 Interview Preparation Guide — pandas, Experimental Design & k-NN Classifiers

← Back to [Master Interview Playbook](./README.md)

**Module:** CT5148 — Programming and Tools for AI  
**Week 9 Core Topics:** `pandas` `DataFrame` & `Series` operations, boolean filtering, summary statistics (`ddof=1` vs `ddof=0`), `groupby` split–apply–combine, IEEE-754 `NaN` semantics & missing-data strategies (`dropna` vs median imputation), tidy ("long") vs wide tables (`pivot_table` & `idxmax`), one-hot encoding (`pd.get_dummies`), the `scikit-learn` estimator API (`fit`/`predict`/`score`, `Pipeline`, data-leakage prevention), custom `KNN` internals, and reproducible factorial experiments (`SEED = 26257770`).

---

## Table of Contents

1. [Summary Table of All Week 9 Exercises](#1-summary-table-of-all-week-9-exercises)
2. [Pre-Submission & Pre-Interview Action List (Critical Gotchas Spotted!)](#2-pre-submission--pre-interview-action-list-critical-gotchas-spotted)
3. [Reference Context: `E01_penguins.py` (Given Code — Full Experiment & `KNN` Class)](#3-reference-context-e01_penguinspy-given-code--full-experiment--knn-class)
4. [`E02_select.py` — Column Extraction & Row Filtering (`column_list`, `heavier_than`)](#4-e02_selectpy--column-extraction--row-filtering-column_list-heavier_than)
5. [`E03_summary.py` — Column Reductions & Bessel's Correction (`column_range`, `column_mean`, `spread`)](#5-e03_summarypy--column-reductions--bessels-correction-column_range-column_mean-spread)
6. [`E04_groups.py` — Split–Apply–Combine with `groupby` (`group_sizes`, `group_means`)](#6-e04_groupspy--splitapplycombine-with-groupby-group_sizes-group_means)
7. [`E05_missing.py` — Missing Values: `NaN`, Dropping vs Imputing (`count_missing`, `drop_missing`, `fill_with_median`)](#7-e05_missingpy--missing-values-nan-dropping-vs-imputing-count_missing-drop_missing-fill_with_median)
8. [`E06_pivot.py` — Long-to-Wide Reshaping & Group Argmax (`wide`, `best_by`)](#8-e06_pivotpy--long-to-wide-reshaping--group-argmax-wide-best_by)
9. [`E07_dummies.py` — One-Hot Encoding Categorical Features (`encode`, `n_new_columns`)](#9-e07_dummiespy--one-hot-encoding-categorical-features-encode-n_new_columns)
10. [`E08_estimator.py` — The scikit-learn Estimator Contract (`train`, `label_for`, `accuracy`)](#10-e08_estimatorpy--the-scikit-learn-estimator-contract-train-label_for-accuracy)
11. [`E09_paper.py` — Reproducible Research & Your `SEED = 26257770` Findings](#11-e09_paperpy--reproducible-research--your-seed--26257770-findings)

---

## 1. Summary Table of All Week 9 Exercises

| File | Function(s) | Difficulty Tier | Input → Return Type & Shape | Time Complexity | Aux Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [E01_penguins.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py) | [`clean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L153-L193), [`KNN`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L214-L269), [`build`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L272-L287), [`protocol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L292-L328), [`best_cell`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L665-L677) | Reference (Given) | `(344, 7)` CSV → `96` cells × `30` CV splits = `2880` rows | `fit`: `O(n log n)`; `predict`: `O(q * n * d + q * n log n)` | `O(q * n)` |
| [E02_select.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py) | [`column_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L25-L33), [`heavier_than`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L35-L50) | Warm-up | `DataFrame` `(n, c)` → `list` `(n,)` / `DataFrame` `(m, c)` | `O(n)` / `O(n + m * c)` | `O(n)` / `O(n + m * c)` |
| [E03_summary.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) | [`column_range`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L21-L31), [`column_mean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L34-L42), [`spread`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L45-L57) | Warm-up ⚠️ *(See Gotchas!)* | `DataFrame` `(n, c)` → `tuple` / `np.float64` / **`str` (!)** | `O(n)` | `O(1)` |
| [E04_groups.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py) | [`group_sizes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L24-L33), [`group_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L36-L46) | Moderate | `DataFrame` `(n, c)` → `dict[key, int]` / `dict[key, float]` | `O(n + g log g)` (`g` groups) | `O(n)` |
| [E05_missing.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py) | [`count_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L29-L38), [`drop_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L41-L49), [`fill_with_median`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72) | **Moderate / Hard** ⚠️ *(`# ANSWER`)* | `DataFrame` `(n, c)` → `dict[str, int]` / `DataFrame` `(m, c)` / `DataFrame` `(n, c)` | `O(n * c)` / `O(n + m * c)` / `O(n * c + n log n)` | `O(n * c)` |
| [E06_pivot.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py) | [`wide`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L25-L39), [`best_by`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L42-L50) | Moderate | `DataFrame` `(n, c)` → `DataFrame` `(r, k)` / group key (`str`) | `O(n + r * k)` / `O(n + g log g)` | `O(n + r * k)` / `O(g)` |
| [E07_dummies.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py) | [`encode`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L26-L52), [`n_new_columns`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L55-L65) | Moderate | `DataFrame` `(n, c)` → `DataFrame` `(n, c - 1 + u)` / `int` | `O(n * (c + u))` / `O(n)` | `O(n * (c + u))` / `O(u)` |
| [E08_estimator.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py) | [`train`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L33-L46), [`label_for`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L49-L69), [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86) | **Hard (8–10 Mark Target)** ⚠️ | `(n, d), (n,), int` → `KNN` / `str` / `float` (`np.float64`) | `O(n log n)` / `O(n * d + n log n)` / `O(q * n * d + q * n log n)` | `O(n * d)` / `O(n)` / `O(q * n)` |
| [E09_paper.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py) | Research Workflow & [`# ANSWER`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py#L79) | **Hard (8–10 Mark Target)** ⚠️ | `SEED = 26257770` → LaTeX Tables, Figure & PDF | — | — |

---

## 2. Pre-Submission & Pre-Interview Action List (Critical Gotchas Spotted!)

> [!CAUTION]
> **Review These Items Before Building Your Final `submission_26257770.zip` (and Know Them Cold for the Interview!):**
>
> 1. **[`spread`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L45-L57) in [E03_summary.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) returns a `str` (`"4.57"`), NOT a `float` (`4.57`)!**  
>    Line 57 writes `return (f"{df[name].std():.2f}")`. It *only* passes the doctest because the doctest calls `print(spread(...))`, where `print("4.57")` and `print(4.57)` print identical characters! Any hidden grading test checking `spread(df, col) == 4.57` or `isinstance(..., float)` will fail (`'4.57' == 4.57` is `False`). Fix: `return round(float(df[name].std()), 2)` (or `round(df[name].std(), 2)`).
> 2. **[`column_mean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L34-L42) in [E03_summary.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) omits `round(..., 2)`!**  
>    Line 42 writes `return df[name].mean()`. It passes the 5-row doctest only because `20700 / 5 = 4140.0` and `222.0 / 5 = 44.4` terminate in 1 decimal place. On a 3-row hidden test (`[1.0, 1.0, 2.0]`), it returns `1.3333333333333333` instead of `1.33`! Fix: `return round(float(df[name].mean()), 2)`.
> 3. **[`column_range`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L21-L31) in [E03_summary.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py) calls `.max().max()` and `.min().min()` twice on a 1-D `Series`!**  
>    `df[name].max()` is *already* a scalar (`np.float64`). The second `.max()` only avoids crashing because `np.float64` inherits a no-op `.max()` method — if passed a string column (`"species"`), `'Gentoo'.max()` crashes with `AttributeError`! Fix: `return df[name].min(), df[name].max()`.
> 4. **[`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86) in [E08_estimator.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py) omits `float(...)` around `model.score(X, y)`!**  
>    Line 89's hint explicitly notes: `# accuracy is model.score with a float() round it.` Depending on the `scikit-learn` + `numpy` 2.x version, `model.score(X, y)` can return `np.float64(1.0)`, which prints as `np.float64(1.0)` in doctests instead of `1.0` and fails `type(res) is float`. Fix: `return float(model.score(X, y))`.
> 5. **Unfilled `# ANSWER:` placeholders in [E05_missing.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L75) and [E09_paper.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py#L79):**  
>    Both files still end with `# ANSWER: (the QUESTION is at the top of this file)`. Ready-to-use answers grounded in your code and your `SEED = 26257770` results are in Sections 7 and 11 below.
> 6. **Paper PDF Filename, Prose `"25 splits"` Typo & `selfcheck.py` `SEED` Interaction:**
>    - In `W09/W09/`, your exported PDF is named [PTAI_Penguins_Jack_Hickey.pdf](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/PTAI_Penguins_Jack_Hickey.pdf), whereas [E09_paper.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py#L48-L49) Step 7 asks to save it as `paper.pdf` (though [selfcheck.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/selfcheck.py#L364-L377) `--zip` only zips `.py` files, check if Blackboard/Canvas asks for `paper.pdf` separately!).
>    - In [PTAI_Penguins_Jack_Hickey.pdf](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/PTAI_Penguins_Jack_Hickey.pdf), the template prose still says *"repeated **five** times, giving **25** train/test splits"* (Section 2, Table 1/2 captions, Figure 1 caption), whereas [`SPLITS, REPEATS = 5, 6`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L113) (and Figure 1's y-axis!) actually ran **6 repeats = 30 splits**!
>    - In [E01_penguins.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L110), `SEED = 26257770` is rightly set to your student ID, which causes `selfcheck.py` to report 2 doctest failures on `E01_penguins.py` (`score_cell` expects `0.919` from `SEED = 0`, and `load_checkpoint` expects `seed was 1, now 0`). That is completely normal because `E01_penguins.py`'s doctests hardcoded `SEED = 0`!

---

## 3. Reference Context: `E01_penguins.py` (Given Code — Full Experiment & `KNN` Class)

**File:** [E01_penguins.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py)

Every exercise in Week 9 (`E02`–`E09`) is one isolated building block of `E01_penguins.py`. Understanding how `E01_penguins.py` fits together gives you superpowers in the interview.

### Five Pillars of the Experiment Architecture
1. **Data Cleaning ([`load_raw`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L134-L150) & [`clean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L153-L193)):**
   - Reads `344` Palmer penguins across `7` columns (`species`, `island`, `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`).
   - `11` penguins have `sex = NaN` (including the `2` penguins missing physical measurements). [`clean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L187) drops unlabelled rows (`raw.dropna(subset=[TARGET])`), leaving **`333` complete penguins** (`0` missing values remaining!).
   - When `use_categoricals=False`: `X` has `4` columns (the physical measurements). When `use_categoricals=True`: `pd.get_dummies(..., dtype=float)` expands `species` (3 values) and `island` (3 values) into `6` binary `0.0/1.0` columns, giving `X` **`10` columns**.
2. **Preventing Data Leakage ([`protocol`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L292-L328) & [`build`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L272-L287)):**
   - **Row-index split:** `protocol(y)` splits integer row indices `np.arange(333)` (`test_size=0.2, stratify=y, random_state=SEED`) into **`266` development rows** and **`67` held-out test rows** (touched *once* at line 779!). Splitting row indices guarantees both `cats=False` and `cats=True` tables are evaluated on the **exact same penguins**.
   - **Why `StandardScaler()` lives inside `make_pipeline(StandardScaler(), model)`:** Standardisation ($z = \frac{x - \mu}{\sigma}$) must learn $\mu$ and $\sigma$ from the **training fold only** (`~213` rows) and apply those training parameters to transform the validation fold (`~53` rows). Scaling the entire `333`-row table beforehand would leak validation/test means and standard deviations into training!
3. **Custom `KNN` Estimator ([`KNN`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L214-L269)):**
   - Follows all 4 scikit-learn conventions: (1) [`__init__`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L247-L249) stores `self.k = k` and `self.metric = metric` verbatim without mutating/validating them (required by `sklearn.base.clone()` inside `cross_val_score`!); (2) learned attributes [`X_`, `y_`, `classes_`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L253-L255) end with a trailing underscore `_`; (3) [`fit`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L251-L256) returns `self`; (4) inherits `get_params`/`set_params` from `BaseEstimator` and `score` (mean accuracy) from `ClassifierMixin`.
   - [`predict`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L258-L269) computes `distances = cdist(X, self.X_, metric=self.metric)` (`(n_query, n_train)`), takes `nearest = np.argsort(distances, axis=1)[:, :self.k]` (`(n_query, k)`), and takes a majority vote per row via `Counter(self.y_[row]).most_common(1)[0][0]`.
4. **Full Factorial Design ([`planned_cells`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L379-L397)):**
   - `2` feature sets (`cats`: off/on) × `2` normalisations (`norm`: off/on) × `3` metrics (`euclidean`, `manhattan`/`cityblock`, `chebyshev`) × `7` odd neighbour counts (`KS = [1, 3, 5, 9, 15, 25, 45]`) = **`84` KNN cells** + `3` reference models (`Dummy`, `DecisionTree`, `RandomForest`) × `4` `(cats, norm)` settings (`12` cells) = **`96` cells** × `30` splits (`5` folds × `6` repeats) = **`2,880` rows** in `results.csv`.
5. **Baselines & Sanity Checks ([`reference_models`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L356-L376)):**
   - `DummyClassifier(strategy="most_frequent")` scores **`0.504`** (since sex is roughly 50/50 Male/Female).
   - `DecisionTreeClassifier` and `RandomForestClassifier` split one feature at a time against a threshold, which is invariant to monotonic linear rescaling ($x > \theta \iff \frac{x - \mu}{\sigma} > \frac{\theta - \mu}{\sigma}$ for $\sigma > 0$), confirming in Table 1 that normalisation barely changes tree accuracy (differing only in the 3rd decimal place due to floating-point tie-breaking on midpoint thresholds).

---

## 4. `E02_select.py` — Column Extraction & Row Filtering (`column_list`, `heavier_than`)

- **File:** [E02_select.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py)
- **Functions:** [`column_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L25-L33), [`heavier_than`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L35-L50)
- **Difficulty Tier:** Warm-up

### Your Code
```python
def column_list(df, name):
    return df[name].tolist()

def heavier_than(df, grams):
    return df[df["mass_g"] > grams]
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`column_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L25-L33) selects a single named column from `df` as a 1-D `pd.Series` and converts its values into a native Python `list` via `.tolist()`. [`heavier_than`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L35-L50) builds a boolean `pd.Series` mask `df["mass_g"] > grams` and uses boolean row indexing `df[...]` to return a filtered `DataFrame` containing only matching penguins with all columns intact.
- **Line-by-Line & Method Breakdown:**
  - `df[name]`: Indexing a `DataFrame` with a single string key returns a 1-D `pd.Series` sharing `df`'s row index. (Contrast: `df[[name]]` with a list of strings returns a 1-column 2-D `DataFrame`!)
  - `.tolist()`: Converts the underlying NumPy/Extension array directly to a Python `list` of native Python objects (`str`, `float`, `int`), unboxing `np.float64` into Python `float`.
  - `df["mass_g"] > grams`: Vectorised comparison returning a `pd.Series` of `dtype=bool` aligned to `df.index`.
  - `df[mask]`: When passed a boolean `Series` of length `len(df)`, `DataFrame.__getitem__` filters **rows** (unlike `df["mass_g"]`, where a string selects a **column**!).

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes:**
  - [`column_list(df, name)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L25-L33): `df` `(n, c)` `DataFrame` → `df[name]` `(n,)` `Series` → returns Python `list` of length `n` (`list[str]` or `list[float]`).
  - [`heavier_than(df, grams)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L35-L50): `df` `(n, c)` `DataFrame` → `df["mass_g"] > grams` `(n,)` `Series[bool]` → returns `pd.DataFrame` of shape `(m, c)` (`0 <= m <= n`), preserving original column names, column `dtype`s, and **original row index labels** (e.g., index `[2, 3]` for `grams = 4000`, *not* `[0, 1]`).
- **Concrete Step-by-Step Trace (`heavier_than(PENGUINS, 4000)`):**
  - `PENGUINS["mass_g"]`: `[3750.0, 3250.0, 4500.0, 5700.0, 3500.0]` (index `0..4`).
  - `PENGUINS["mass_g"] > 4000`: `Series([False, False, True, True, False])`.
  - `PENGUINS[mask]`: `DataFrame` of shape `(2, 4)` with row indices `[2, 3]` (`Gentoo` on `Biscoe`, `4500.0` and `5700.0`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`grams = 10000` (nothing matches):** Returns an empty `DataFrame` with shape `(0, 4)` (`len(...) == 0`), keeping all 4 column names and `dtype`s rather than raising an error.
  - **Missing column name (`column_list(PENGUINS, "age")`):** Raises `KeyError: 'age'`.
  - **`NaN` entries in `mass_g`:** By IEEE-754 rules, `NaN > grams` evaluates to `False`, so penguins with missing `mass_g` are cleanly excluded without crashing.
  - **Difference between `list(df["mass_g"])` and `df["mass_g"].tolist()`:** `.tolist()` unboxes to built-in Python `float` in C, whereas iterating `list(s)` goes through Python iterator overhead (and on raw NumPy arrays `list(arr)` yields `np.float64` scalars rather than plain Python `float`s!).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - [`column_list`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L25-L33): `O(n)` (`O(1)` dictionary column lookup + `O(n)` list allocation/unboxing).
  - [`heavier_than`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E02_select.py#L35-L50): `O(n + m * c)` where `n` is row count, `m` is matching rows, and `c` is column count (`O(n)` C comparison + `O(m * c)` copying matching rows across `c` columns).
- **Space Complexity:** `O(n)` for `column_list`; `O(n + m * c)` for `heavier_than` (`n`-byte boolean mask + new `(m, c)` `DataFrame`).

### Likely Interview Q&A
- **Q: Why does `df["mass_g"]` select a *column*, whereas `df[df["mass_g"] > 4000]` selects *rows*?**  
  **A:** `DataFrame.__getitem__` (`[]`) overloads its behaviour by key type: a string (or list of strings) indexes the column axis, whereas a 1-D boolean `Series` or `ndarray` of length `len(df)` acts as a row filter (equivalent to `df.loc[df["mass_g"] > 4000]`).
- **Q: What are the row index numbers of `heavier_than(PENGUINS, 4000)`? What happens if you try `result[0]` or `result.loc[0]`?**  
  **A:** Its row index is `[2, 3]`, preserved from `PENGUINS`. `result.loc[0]` looks up label `0` and raises `KeyError: 0`, whereas `result.iloc[0]` looks up positional row `0` and returns the first matching Gentoo row (label `2`).

---

## 5. `E03_summary.py` — Column Reductions & Bessel's Correction (`column_range`, `column_mean`, `spread`)

- **File:** [E03_summary.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py)
- **Functions:** [`column_range`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L21-L31), [`column_mean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L34-L42), [`spread`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L45-L57)
- **Difficulty Tier:** Warm-up (Conceptually) / **High-Priority Interview & Grading Watchlist!**

### Your Code (Current vs Recommended Clean Version)
```python
# Current code in W09/W09/E03_summary.py:
def column_range(df, name):
    largest = df[name].max().max()
    smallest = df[name].min().min()
    return (smallest, largest)


def column_mean(df, name):
    return df[name].mean()


def spread(df, name):
    return (f"{df[name].std():.2f}")
```

> [!WARNING]
> **Three Specific Bugs / Quirks in Your Current `E03_summary.py` (Know Exactly Why They Happen!):**
> 1. **`spread` returns `str`, NOT `float`:** `f"{df[name].std():.2f}"` formats the float into a **string** (`'4.57'`). Because the doctest writes `>>> print(spread(PENGUINS, "bill_mm"))`, `print` strips quotes from strings so `'4.57'` looks identical to `4.57`! Also, if a column had `std = 4.5`, `f"{4.5:.2f}"` prints `4.50` whereas `round(4.5, 2)` prints `4.5`. Official solution: `return round(df[name].std(), 2)`.
> 2. **`column_mean` omits `round(..., 2)`:** Passes `PENGUINS` only because `4140.0` and `44.4` happen to be exact tenths. Official solution: `return round(df[name].mean(), 2)`.
> 3. **`column_range` chains `.max().max()` on a 1-D `Series`:** `df[name]` is a 1-D `Series`, so the *first* `.max()` already returns a scalar `np.float64(5700.0)`! Calling `.max()` a *second* time only succeeds because NumPy scalar objects (`np.generic`) define a 0-D `.max()` method returning `self`. If `df[name].max()` returns a plain Python `float` or `str` (e.g., `column_range(PENGUINS, "species")` → `'Gentoo'`), the second `.max()` crashes with **`AttributeError: 'str' object has no attribute 'max'`**! (Two `.sum().sum()` calls are only needed on a 2-D `DataFrame`, as in `df.isna().sum().sum()` in `E01_penguins.py` line 704.)

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** These three functions reduce a single numeric `DataFrame` column (`df[name]`) down to summary scalars: its `(min, max)` range tuple, its arithmetic mean, and its sample standard deviation. All three pandas reductions (`min`, `max`, `mean`, `std`) skip `NaN` values automatically (`skipna=True` by default) and run in vectorised C over the underlying column array.
- **Bessel's Correction (`ddof=1` in pandas vs `ddof=0` in NumPy — Core Lecture Concept!):**
  - **pandas `Series.std()` defaults to `ddof=1`** (Delta Degrees of Freedom = 1), computing the **sample standard deviation**:
    $$s = \sqrt{\frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2}$$
    Why divide by $n - 1$? Because the sample mean $\bar{x}$ was estimated from the *same* $n$ points, which minimises squared deviations relative to the true population mean $\mu$, making $\frac{1}{n}\sum (x_i - \bar{x})^2$ downward-biased; dividing by $n - 1$ makes $s^2$ an unbiased estimator of population variance $\sigma^2$.
  - **NumPy `np.std()` defaults to `ddof=0`**, computing the **population standard deviation** (dividing by $n$).
  - On `PENGUINS["bill_mm"]` ($n = 5$): pandas `df["bill_mm"].std()` gives **`4.57`** (`4.57165...`), whereas `np.std(PENGUINS["bill_mm"].to_numpy())` gives $4.57165 \times \sqrt{4/5} =$ **`4.09`** (`4.0890...`)! To make them agree, pass `ddof=1` to NumPy or `ddof=0` to pandas.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Values on `PENGUINS` (Tracing Your Exact Current Code vs Official):**
  - [`column_range(PENGUINS, "mass_g")`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L21-L31):
    - `df["mass_g"]` → `Series` `(5,)`, `float64`.
    - `df["mass_g"].max()` → `np.float64(5700.0)` → `.max()` → `np.float64(5700.0)`.
    - Returns **`tuple[np.float64, np.float64]`**: `(np.float64(3250.0), np.float64(5700.0))`.
  - [`column_mean(PENGUINS, "bill_mm")`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L34-L42):
    - `(39.1 + 40.3 + 46.1 + 50.0 + 46.5) / 5 = 222.0 / 5` → returns **`np.float64(44.4)`**.
  - [`spread(PENGUINS, "bill_mm")`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E03_summary.py#L45-L57):
    - `df["bill_mm"].std()` → `np.float64(4.571651780264984)`.
    - Current code returns **`'4.57'`** (type **`str`**!). With `round(df[name].std(), 2)`, returns `np.float64(4.57)` (or Python `float` `4.57` if `round(float(...), 2)`).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **A 1-row `DataFrame` into `spread` (`n = 1`):** Because pandas uses `ddof=1`, the denominator is $n - 1 = 0$! `df[name].std()` returns **`np.nan`** (no crash; your current f-string returns `'nan'`, and `round(np.nan, 2)` returns `nan`). By contrast, `np.std` (`ddof=0`) on 1 element returns `0.0`!
  - **Column with `NaN`s:** `skipna=True` ignores `NaN`s and sets $n$ to the count of *non-missing* values. If *every* value in the column is `NaN` (or `df` has `0` rows), `min`, `max`, `mean`, and `std` all return `np.nan`.
  - **String column into `column_range(PENGUINS, "species")`:** Your current `.max().max()` raises `AttributeError` because `'Gentoo'` is a `str` with no `.max()` method; with a single `.min(), .max()`, it lexicographically compares strings and returns `('Adelie', 'Gentoo')`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n)`** for all three functions (`column_range` makes 2 linear scans over `n` rows; `column_mean` makes 1 scan; `spread` computes mean and squared deviations in C in `O(n)`).
- **Space Complexity:** **`O(1)`** auxiliary memory — reductions stream over the contiguous `float64` column buffer without allocating intermediate arrays.

### Likely Interview Q&A
- **Q: Look at line 57 of your `E03_summary.py`: `return (f"{df[name].std():.2f}")`. What type does `spread` return, and why did the doctest still pass?**  
  **A:** An f-string always evaluates to a `str` (`'4.57'`), not a `float`! The doctest passed only because it wrapped the call in `print(spread(...))`, which prints `'4.57'` without quotes identically to `4.57`. To return an actual rounded number, it should be `round(float(df[name].std()), 2)`.
- **Q: Why do `df["bill_mm"].std()` and `np.std(df["bill_mm"].to_numpy())` give different numbers (`4.57` vs `4.09`), and what happens to both if `df` has only 1 row?**  
  **A:** Pandas defaults to sample standard deviation (`ddof=1`, dividing variance by $n - 1$), whereas NumPy defaults to population standard deviation (`ddof=0`, dividing by $n$). On a 1-row table ($n = 1$), pandas divides by $1 - 1 = 0$ and returns `NaN`, whereas NumPy divides by `1` and returns `0.0`.

---

## 6. `E04_groups.py` — Split–Apply–Combine with `groupby` (`group_sizes`, `group_means`)

- **File:** [E04_groups.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py)
- **Functions:** [`group_sizes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L24-L33), [`group_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L36-L46)
- **Difficulty Tier:** Moderate

### Your Code
```python
def group_sizes(df, by):
    return df.groupby(by).size().to_dict()


def group_means(df, by, column):
    return df.groupby(by)[column].mean().round(1).to_dict()
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** Both functions apply pandas' **split–apply–combine** pattern: `df.groupby(by)` partitions rows by unique values of `by`, `.size()` or `[column].mean().round(1)` summarises each group into a `pd.Series` indexed by group name, and `.to_dict()` converts that `Series` into an ordinary Python `dict`.
- **Line-by-Line & Method Breakdown:**
  - `df.groupby(by)`: Lazily constructs a `DataFrameGroupBy` object (no numbers computed yet!). By default, `sort=True` (sorts group keys alphabetically) and `dropna=True` (ignores rows where `df[by]` itself is `NaN`).
  - `.size()` (in [`group_sizes`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L33)): Counts total rows in each group (including rows that have `NaN`s in other columns!), returning a `pd.Series` of `int64` indexed by unique `by` values.
  - `[column].mean()` (in [`group_means`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E04_groups.py#L46)): Selecting `[column]` **before** `.mean()` creates a `SeriesGroupBy` so pandas *only* averages that single numeric column! (If you wrote `df.groupby(by).mean()[column]` instead, pandas 2.0+ would try to average `"island"` too and crash with **`TypeError: agg function failed [how->mean,dtype->object]`** because `numeric_only=False` is now default!)
  - `.round(1).to_dict()`: Rounds each group mean to 1 decimal place and returns `{group_label: value}`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes (`PENGUINS`, `by="species"`, `column="mass_g"`):**
  - `PENGUINS.groupby("species")` → `DataFrameGroupBy` (3 groups: `'Adelie'` rows `[0, 1]`, `'Chinstrap'` row `[4]`, `'Gentoo'` rows `[2, 3]`).
  - `.size()` → `pd.Series({'Adelie': 2, 'Chinstrap': 1, 'Gentoo': 2}, dtype=int64)` → `.to_dict()` → Python `dict[str, int]`: `{'Adelie': 2, 'Chinstrap': 1, 'Gentoo': 2}`.
  - `["mass_g"].mean()` → `pd.Series({'Adelie': 3500.0, 'Chinstrap': 3500.0, 'Gentoo': 5100.0}, dtype=float64)` → `.round(1).to_dict()` → Python `dict[str, float]`.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`NaN` inside `df[by]` (the grouping column):** Because `groupby(..., dropna=True)` is the default, rows whose `species` is `NaN` are silently omitted from the dict! (Notice [`resume`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L529) in `E01_penguins.py` explicitly passes `dropna=False` so no checkpoint rows can hide!)
  - **`NaN` inside `df[column]` (the value column):** `group_sizes` still counts that row (because `.size()` counts rows), whereas `group_means` skips the `NaN` when averaging (`skipna=True`), or puts `nan` in the dict if *all* rows in that group have `NaN` in `column`.
  - **Grouping by a list of columns (`by=["species", "island"]`):** Works out of the box! `Series` gets a `MultiIndex`, and `.to_dict()` produces tuple keys like `{('Adelie', 'Biscoe'): 1, ('Adelie', 'Dream'): 1, ...}` (just like [`resume`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L530) does!).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:** **`O(n + g log g)`** where `n` is the number of rows and `g <= n` is the number of distinct groups (`O(n)` hash-based factorisation of `df[by]` + `O(g log g)` sorting the `g` group keys because `sort=True` by default + `O(n)` single pass summing/counting per group). Passing `sort=False` makes `groupby` pure expected `O(n)`, since a Python `dict` doesn't care about key order for `==`!
- **Space Complexity:** **`O(n)`** (`O(n)` integer group-code array built during factorisation + `O(g)` output `Series` and `dict`).
- **Classic Interview Comparison — `.size()` vs `.count()` on `GroupBy`:**
  - `df.groupby(by).size()` → returns a **`Series`** of **total row counts** per group (including `NaN`s).
  - `df.groupby(by).count()` → returns a **`DataFrame`** with one column per remaining column, counting **only non-`NaN` entries**!

### Likely Interview Q&A
- **Q: What is the difference between `df.groupby("species").size()` and `df.groupby("species").count()`?**  
  **A:** `.size()` returns a 1-D `Series` counting how many rows belong to each group regardless of missing values. `.count()` returns a 2-D `DataFrame` counting non-`NaN` values separately in every other column (and even `df.groupby("species")["mass_g"].count()` would undercount groups where `mass_g` has `NaN`s).
- **Q: Why is `df.groupby(by)[column].mean()` better than `df.groupby(by).mean()[column]`?**  
  **A:** Two reasons: (1) efficiency — indexing `[column]` first avoids computing means for every other column in a wide table; and (2) correctness — in pandas 2.0+, `.mean()` defaults to `numeric_only=False`, so calling `.mean()` on the whole `DataFrame` crashes with `TypeError` whenever `df` has another string column like `"island"`.

---

## 7. `E05_missing.py` — Missing Values: `NaN`, Dropping vs Imputing (`count_missing`, `drop_missing`, `fill_with_median`)

- **File:** [E05_missing.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py)
- **Functions:** [`count_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L29-L38), [`drop_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L41-L49), [`fill_with_median`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72), and [`# ANSWER`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L75)
- **Difficulty Tier:** **Moderate / Hard (Core ML Methodology + Copy Semantics)**

### Your Code
```python
def count_missing(df):
    return df.isna().sum().to_dict()


def drop_missing(df, column):
    return df.dropna(subset=[column])


def fill_with_median(df, column):
    df_copy = df.copy()
    median = df_copy[column].median()
    df_copy[column] = df_copy[column].fillna(median)
    return df_copy


# ANSWER: (the QUESTION is at the top of this file)
```

> [!IMPORTANT]
> **Unfilled `# ANSWER:` on Line 75 of `E05_missing.py`!**  
> Before running `selfcheck.py --zip`, replace line 75 with your answer to the module `QUESTION` (*"Why is filling in a missing measurement reasonable, while filling in a missing label is not?"*):
> ```python
> # ANSWER: A missing measurement is an input feature (X): imputing it with the
> # median is an imperfect guess that at worst adds noise and makes prediction
> # harder, while we still evaluate against real ground-truth labels. A missing
> # label (y) is the ground-truth answer itself: inventing a label and scoring
> # the model against our own invention creates circular evaluation, measuring
> # whether the model agrees with our guess rather than with reality.
> ```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`count_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L29-L38) maps every cell to `True`/`False` via `df.isna()`, sums down each column (`axis=0` default), and returns a `{col: missing_count}` dict. [`drop_missing`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L41-L49) removes rows missing a specific column using `df.dropna(subset=[column])` (ideal for missing labels), while [`fill_with_median`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72) clones `df` via `.copy()` and replaces `NaN`s in `column` with the median of its observed values (ideal for missing numeric features without mutating the caller's `DataFrame`).
- **Line-by-Line & Concept Breakdown:**
  - **Why `df == np.nan` NEVER works (IEEE-754):** `NaN` ("Not a Number") represents indeterminate operations (`0.0 / 0.0`, `inf - inf`). Under IEEE-754, **`NaN == NaN` is `False`** (in fact, `x != x` is `True` if and only if `x` is `NaN`!). Therefore `df[col] == np.nan` yields all `False`; you *must* use `.isna()` (or its exact alias `.isnull()`).
  - **Why `subset=[column]` in `dropna`:** Plain `df.dropna()` drops any row with a `NaN` in *any* column! In `PENGUINS`, row `1` has `bill_mm = NaN` but a valid `mass_g = 3250.0`. `drop_missing(PENGUINS, "mass_g")` keeps row `1` (returning 3 rows), whereas `df.dropna()` would drop row `1` too (returning only 2 rows).
  - **Why `df_copy = df.copy()`:** In Python, `df` is passed by object-reference. Assigning `df[column] = ...` directly mutates the caller's `PENGUINS` table in place, breaking any subsequent call (`count_missing(PENGUINS)["mass_g"]` in Doctest 3 would become `0` instead of `2`!). `df.copy()` (`deep=True` by default) duplicates the column buffers and index so `df` stays untouched.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Step-by-Step Trace on [`PENGUINS`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L22-L26) (shape `(5, 3)`):**
  - Note how Python `None` in `"bill_mm": [39.1, None, 46.1, 50.0, 46.5]` is automatically coerced to IEEE-754 `np.nan` (`float64`) when pandas builds a numeric column! (And if an integer column has `None`, classic pandas upcasts the whole column from `int64` to `float64` because standard `int64` has no `NaN` bit pattern!)
  - [`count_missing(PENGUINS)`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L29-L38):
    1. `df.isna()` → `(5, 3)` `DataFrame` of `bool`.
    2. `.sum()` (`axis=0` default) → `(3,)` `Series` of `int64`: `species: 0, bill_mm: 1, mass_g: 2`.
    3. `.to_dict()` → `{'species': 0, 'bill_mm': 1, 'mass_g': 2}` (`dict[str, int]`).
  - [`fill_with_median(PENGUINS, "bill_mm")`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72):
    1. Non-missing values of `bill_mm` ($k = 4$, even count): sorted `[39.1, 46.1, 46.5, 50.0]`.
    2. `median`: average of the two middle values $(46.1 + 46.5) / 2 = \mathbf{46.3}$.
    3. `.fillna(46.3)` replaces index `1`'s `NaN` → `[39.1, 46.3, 46.1, 50.0, 46.5]`.
  - [`fill_with_median(PENGUINS, "mass_g")`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E05_missing.py#L52-L72):
    1. Non-missing values of `mass_g` ($k = 3$, odd count): sorted `[3250.0, 3750.0, 5700.0]`.
    2. `median`: middle value = **`3750.0`** (notice how the mean would be pulled up by `5700.0` to `4233.33`, whereas the median resists the heavy Gentoo outlier!).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Entire column is `NaN`:** `df_copy[column].median()` returns `np.nan`, and `fillna(np.nan)` leaves all entries as `NaN` without raising an error.
  - **String column into `fill_with_median(PENGUINS, "species")`:** `df_copy["species"].median()` raises `TypeError: Cannot convert [...] to numeric` (categorical columns must be imputed with `.mode()[0]` or a `"Missing"` category instead).
  - **Data Leakage Warning in ML (High-Mark Interview Connection!):** If you used `fill_with_median` on an entire dataset *before* `train_test_split` or cross-validation, the test set values would influence `median` (data leakage!). Just like `StandardScaler()` in [`build`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L272-L287), median imputation in an ML experiment belongs inside a `Pipeline` (`SimpleImputer(strategy="median")`) so the median is learned solely on each training fold.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - `count_missing`: `O(n * c)` across `n` rows and `c` columns.
  - `drop_missing`: `O(n + m * c)` where `m <= n` is the number of retained rows.
  - `fill_with_median`: `O(n * c + k)` (pandas computes medians using `np.partition` / quickselect in **`O(k)`** average time over the `k <= n` non-null entries, plus `O(n * c)` for `df.copy()`).
- **Space Complexity:** `O(n * c)` for `count_missing` (the `(n, c)` boolean `DataFrame` from `df.isna()`) and `fill_with_median` (the deep copy of `df`); `O(m * c)` for `drop_missing`.

### Likely Interview Q&A
- **Q: Why can't we write `(df == np.nan).sum()` in `count_missing`?**  
  **A:** Under IEEE-754 floating-point arithmetic, `NaN == NaN` evaluates to `False`, so `df == np.nan` produces a table of all `False`s and sums to `0` for every column. `.isna()` explicitly checks the IEEE-754 `NaN` bit pattern (and Python `None`).
- **Q: Why did you choose the *median* rather than the *mean* here, and why did you call `df.copy()` first?**  
  **A:** The median is robust to skewed distributions and outliers (like one `5700 g` Gentoo pulling the mean above `4200 g`). Calling `df.copy()` creates an independent deep copy so assigning `df_copy[column] = ...` does not mutate the caller's original `DataFrame` in place.

---

## 8. `E06_pivot.py` — Long-to-Wide Reshaping & Group Argmax (`wide`, `best_by`)

- **File:** [E06_pivot.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py)
- **Functions:** [`wide`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L25-L39), [`best_by`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L42-L50)
- **Difficulty Tier:** Moderate

### Your Code
```python
def wide(df, index, columns, values):
    return df.pivot_table(index=index, columns=columns, values=values)


def best_by(df, group, column):
    return df.groupby(group)[column].mean().idxmax()
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`wide`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L25-L39) reshapes a "long" (tidy) experimental log into a human-readable 2-D summary table using `df.pivot_table`, placing `index` labels down the rows, `columns` labels across the top, and mean `values` inside the cells. [`best_by`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L42-L50) groups `df` by `group`, averages `column`, and calls `.idxmax()` to return the **group label** (not the numerical score!) that achieved the highest mean.
- **Line-by-Line & Lecture Connection:**
  - `wide` mirrors [`table_references`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L582) and [`table_factorial`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L595) in `E01_penguins.py`.
  - `best_by` mirrors [`best_cell`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L665-L677) in `E01_penguins.py` (`knn.groupby(["cats", "norm", "metric", "k"])["accuracy"].mean().idxmax()`).
  - **`.max()` vs `.argmax()` vs `.idxmax()` on a `Series`:**
    - `.max()` → returns the maximum **value** (`0.825`).
    - `.argmax()` → returns the integer **0-based position** (`0`).
    - `.idxmax()` → returns the **index label** (`'euclidean'`), which is the winning group's name!

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Step-by-Step Trace on [`RUNS`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E06_pivot.py#L18-L22) (shape `(4, 3)`):**
  - `wide(RUNS, "setting", "metric", "accuracy")`:
    - Unique `"setting"` values (sorted): `['norm off', 'norm on']` → `index` (2 rows).
    - Unique `"metric"` values (sorted): `['euclidean', 'manhattan']` → `columns` (2 columns).
    - Returns a `(2, 2)` `pd.DataFrame` (`float64`). Notice swapping `index` and `columns` (`wide(RUNS, "metric", "setting", "accuracy")`) returns the exact transpose `.T`!
  - `best_by(RUNS, "metric", "accuracy")`:
    - `RUNS.groupby("metric")["accuracy"].mean()` → `Series({'euclidean': 0.825, 'manhattan': 0.780})`.
    - `.idxmax()` → `'euclidean'` (type `str`, or a `tuple` if `group` is a list of column names as in [`best_cell`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L676)!).
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Duplicate `(index, columns)` pairs (e.g., 30 CV splits per setting in `results.csv`!):** **`pivot_table` vs `pivot`!** `df.pivot(...)` crashes with `ValueError: Index contains duplicate entries, cannot reshape`, whereas `df.pivot_table(...)` uses `aggfunc="mean"` by default and cleanly averages all 30 splits per cell!
  - **Missing `(index, columns)` combination (sparse grid):** `pivot_table` fills unobserved cells with `NaN` (unless `fill_value=...` is passed).
  - **Tie in `best_by`:** If two groups tie for the exact highest mean, `.idxmax()` returns the **first** occurrence in the `Series` index (which is alphabetically first because `groupby` defaults to `sort=True`).
  - **All-`NaN` or empty `Series` in `best_by`:** `.idxmax()` raises `ValueError: attempt to get argmax of an empty sequence` (or `FutureWarning` / `ValueError` on all-`NaN`).

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time Complexity:**
  - `wide`: `O(n + r * k + r log r + k log k)` where `n` is input rows, `r` is unique `index` levels, and `k` is unique `columns` levels.
  - `best_by`: `O(n + g log g)` for `n` rows and `g` groups (`O(g)` scan for `idxmax`).
- **Space Complexity:** `O(n + r * k)` for `wide` (output table is `r × k`); `O(n)` grouping codes + `O(g)` reduced `Series` for `best_by`.
- **Why Store Experiment Logs Long (`results.csv`) Instead of Wide?** Long ("tidy") format lets you append 30 rows per cell incrementally (`mode="a"`) for crash recovery ([`run_cells`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L434)), store arbitrary metadata (`seed`, `splits`, `repeats`, `split`), and compute *both* means (`pivot_table`) and error bars (`std` over splits) on demand — once collapsed into a wide table of means, the per-split variance is lost forever!

### Likely Interview Q&A
- **Q: Why did `wide` use `df.pivot_table(...)` instead of `df.pivot(...)`?**  
  **A:** `df.pivot` requires every `(index, columns)` pair to appear at most once and throws `ValueError` on duplicates. In real experiments like `E01_penguins.py`, each cell has 30 cross-validation scores; `pivot_table` aggregates duplicate `(index, columns)` entries using `aggfunc='mean'` automatically.
- **Q: What is the difference between `.max()`, `.argmax()`, and `.idxmax()` on the `Series` in `best_by`?**  
  **A:** `.max()` returns the winning accuracy float (`0.825`), `.argmax()` returns the integer positional index (`0`), and `.idxmax()` returns the Series index label (`'euclidean'`), which is the group name we want.

---

## 9. `E07_dummies.py` — One-Hot Encoding Categorical Features (`encode`, `n_new_columns`)

- **File:** [E07_dummies.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py)
- **Functions:** [`encode`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L26-L52), [`n_new_columns`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L55-L65)
- **Difficulty Tier:** Moderate

### Your Code
```python
def encode(df, column):
    return pd.get_dummies(df, columns=[column], dtype=int)


def n_new_columns(df, column):
    return df[column].nunique() - 1
```

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`encode`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L26-L52) performs **one-hot encoding** on a single text column using `pd.get_dummies(df, columns=[column], dtype=int)`, removing `column` and appending one `0`/`1` integer indicator column (`"{column}_{value}"`) per distinct category while leaving all other columns untouched. [`n_new_columns`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E07_dummies.py#L55-L65) computes the net change in table width: `u` distinct categories arrive and `1` original column leaves, so width changes by `df[column].nunique() - 1`.
- **Line-by-Line & Method Breakdown:**
  - `columns=[column]`: Crucial! Without `columns=[column]`, `pd.get_dummies(df)` encodes **every** `object`/`string`/`category` column in `df` (so calling `pd.get_dummies(PENGUINS)` would encode *both* `"species"` and `"island"` at once!).
  - `dtype=int`: Since pandas 2.0, `pd.get_dummies` defaults to `dtype=bool` (`True`/`False`). Passing `dtype=int` produces clean `0`/`1` `int64` columns (and `E01_penguins.py` passes `dtype=float` so `X` is uniformly `float64` for `cdist`).
  - `df[column].nunique()`: Counts unique non-`NaN` values (`dropna=True` by default) and returns a plain Python `int`.

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Types & Shapes (`encode(PENGUINS, "species")`):**
  - Input `PENGUINS`: shape `(5, 4)` (`['species', 'island', 'bill_mm', 'mass_g']`).
  - Unique `"species"` values (sorted alphabetically by `get_dummies`): `'Adelie'`, `'Chinstrap'`, `'Gentoo'` (`u = 3`).
  - Output `out`: new `pd.DataFrame` of shape **`(5, 6)`** (`4 - 1 + 3 = 6`, matching `n_new_columns == 3 - 1 = 2`), with columns `['island', 'bill_mm', 'mass_g', 'species_Adelie', 'species_Chinstrap', 'species_Gentoo']`, where the 3 new columns have `dtype=int64` and each row has a single `1` and two `0`s.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **`NaN` in `df[column]`:** Both `pd.get_dummies` (`dummy_na=False` default) and `df[column].nunique()` (`dropna=True` default) ignore `NaN`! A row with `species = NaN` receives `[0, 0, 0]` across all dummy columns, and no `species_nan` column is added — so `encode(df, col).shape[1] - df.shape[1] == n_new_columns(df, col)` **still holds**!
  - **Column with only 1 unique value (`u = 1`):** `n_new_columns` returns `1 - 1 = 0` (1 column removed, 1 column added → net change `0`). If `df` is empty (`0` rows, `u = 0`), `pd.get_dummies` drops `column` and adds `0` columns → net change `-1`, and `0 - 1 = -1` still matches!
  - **Train/Test Column Mismatch Trap in Production ML (9–10 Mark Insight!):** Suppose the training fold has `'Adelie'`, `'Chinstrap'`, `'Gentoo'`, while a small test batch only contains `'Adelie'` and `'Gentoo'` (or contains an unseen species `'Emperor'`). Calling `pd.get_dummies` separately on `X_test` would produce **fewer (or different) columns** than `X_train`, crashing `model.predict(X_test)`! In `E01_penguins.py`, [`clean`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L191) avoids this because one-hot encoding is purely deterministic per row (no statistics leaked across rows, since the 3 penguin species and 3 islands in the study are fixed ahead of time); in general production pipelines, `sklearn.preprocessing.OneHotEncoder(handle_unknown="ignore")` remembers the exact training categories during `fit`.

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time & Space Complexity:**
  - `encode`: **`O(n * (c + u))`** time and space (`n` rows, `c` original columns, `u` unique categories in `column` — note that for high-cardinality columns like postcodes where `u = 10,000`, dense one-hot encoding explodes memory by `n * u`, unless `sparse=True` is used!).
  - `n_new_columns`: **`O(n)`** expected time (hash table over `n` items in C) and **`O(u)`** auxiliary space to store the `u` distinct values.
- **Why One-Hot Encoding Beats Integer Label Encoding (`0, 1, 2`) — AND Why `cats=True` Hurt Normalised k-NN in `E01_penguins.py`!**
  1. **One-Hot vs Ordinal (`0, 1, 2`):** Mapping `Adelie=0, Chinstrap=1, Gentoo=2` invents a fake ordering where $|0 - 2| = 2 > |0 - 1| = 1$, telling k-NN that Adelie is twice as far from Gentoo as from Chinstrap! One-hot encoding puts `[1,0,0]`, `[0,1,0]`, `[0,0,1]` at orthogonal corners of a simplex so every pair of distinct species has identical Euclidean distance $\sqrt{(1-0)^2 + (0-1)^2} = \sqrt{2}$.
  2. **Why `cats on, norm on` degraded accuracy in Figure 1 / Table 2:** Without normalisation (`norm off`), a `0/1` dummy column contributes at most $1^2 = 1$ to squared distance while `body_mass_g` contributes $\sim 1000^2 = 10^6$, so categorical columns are ignored (`0.761` vs `0.761`). Once `StandardScaler` is turned on (`norm on`), **every one of the 6 dummy columns (`3` species + `3` islands) is scaled to unit variance (`1.0`)**, giving 6 categorical columns `60%` of the total feature variance against only 4 body-measurement columns (`40%`) — and since males and females live on the *same* islands in ~50/50 ratios, `island` adds pure grouping noise that swamps body measurements at large `k` (collapsing `chebyshev, k=45` to `0.712`)!

### Likely Interview Q&A
- **Q: Why couldn't we just map `"Adelie" -> 0`, `"Chinstrap" -> 1`, `"Gentoo" -> 2` in a single column instead of adding extra columns with `get_dummies`?**  
  **A:** Because k-NN computes geometric distances: `0, 1, 2` would falsely force `"Chinstrap"` to lie halfway between `"Adelie"` and `"Gentoo"` (distance `1` vs `2`). One-hot vectors `[1,0,0]`, `[0,1,0]`, `[0,0,1]` make all pairs of distinct categories equidistant ($\sqrt{2}$ in Euclidean distance, `2` in Manhattan distance).
- **Q: In `E01_penguins.py`'s Figure 1, why did turning categorical variables `on` change almost nothing when normalisation was `off`, yet hurt accuracy when normalisation was `on`?**  
  **A:** Unnormalised distances are completely dominated by `body_mass_g` (hundreds/thousands of grams vs `0` or `1` in a dummy column). When normalised, `StandardScaler` gives each of the 6 binary species/island columns unit variance equal to `bill_length_mm` or `body_mass_g`, diluting the 4 sexually dimorphic physical measurements with 6 sex-neutral indicator columns (especially `island`).

---

## 10. `E08_estimator.py` — The scikit-learn Estimator Contract (`train`, `label_for`, `accuracy`)

- **File:** [E08_estimator.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py) (imports [`KNN`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L214-L269) from [E01_penguins.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py))
- **Functions:** [`train`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L33-L46), [`label_for`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L49-L69), [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86)
- **Difficulty Tier:** **Hard (8–10 Mark Target — Estimator API, 2-D Shapes & Lazy Learning Complexity)**

### Your Code
```python
def train(X, y, k):
    model = KNN(k=k)
    model.fit(X, y)
    return model


def label_for(model, row):
    prediction = model.predict([row])
    return str(prediction[0])


def accuracy(model, X, y):
    return model.score(X, y)
```

> [!WARNING]
> **Return-Type Watch on [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86) (Line 86):**  
> The docstring specifies *"as a plain float"* and line 89's hint says `# accuracy is model.score with a float() round it.` Depending on the `scikit-learn` / `numpy` 2.x version, `ClassifierMixin.score(X, y)` can return a `np.float64` scalar (whose `repr` in NumPy 2.x is `'np.float64(1.0)'` rather than `'1.0'`). Wrapping `return float(model.score(X, y))` guarantees a plain Python `float` in every environment! (Also note in [`train`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L44-L46): since `KNN.fit(X, y)` returns `self`, `return KNN(k=k).fit(X, y)` does the exact same thing in one line.)

### Pillar 1 — Explain (Walkthrough & Variable Roles)
- **2-Sentence Elevator Pitch:** [`train`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L33-L46) instantiates `KNN(k=k)` and fits it on training table `X` and labels `y` (which for lazy-learning k-NN simply stores `X_`, `y_`, and `classes_`). [`label_for`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L49-L69) wraps a single 1-D feature vector `row` into a 1-row 2-D batch `[row]` for `model.predict`, unpacking and casting the single predicted label to a Python `str`, while [`accuracy`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E08_estimator.py#L73-L86) delegates to `ClassifierMixin.score(X, y)` to compute the fraction of rows where `model.predict(X) == y`.
- **Deep Walkthrough of What Happens Inside `KNN` (`E01_penguins.py` lines 247–269):**
  1. `KNN(k=k)` sets hyperparameter `self.k = k` and `self.metric = "euclidean"`. Before `.fit(...)`, `hasattr(model, "X_")` is `False`.
  2. `model.fit(X, y)` stores `self.X_ = np.asarray(X, dtype=float)` (`(n_train, d)`), `self.y_ = np.asarray(y)` (`(n_train,)`), `self.classes_ = np.unique(y)`, and `return self`.
  3. `model.predict([row])`:
     - Converts `[row]` to `(1, d)` `float64` array and runs `cdist(..., self.X_)` → `(1, n_train)` distance matrix.
     - `np.argsort(distances, axis=1)[:, :self.k]` → `(1, k)` indices of the `k` closest training birds.
     - `Counter(self.y_[row_idx]).most_common(1)[0][0]` counts votes among those `k` training labels and picks the winner!

### Pillar 2 — Trace (Shapes, Dtypes, Return Types & Caller Edge Cases)
- **Step-by-Step Trace (`label_for(train(X, Y, 3), [6.0])`):**
  - Training set: `X = [[3.0], [3.5], [10.0], [11.0]]` (`(4, 1)`), `Y = ['stork', 'stork', 'swan', 'swan']` (`(4,)`).
  - Query `row = [6.0]` (length `1`) → `[row] = [[6.0]]` → `np.asarray([[6.0]], dtype=float)` has shape **`(1, 1)`**.
  - `distances = cdist([[6.0]], X)` → `array([[3.0, 2.5, 4.0, 5.0]])`, shape **`(1, 4)`**, `dtype=float64`.
  - `np.argsort(distances, axis=1)` → `array([[1, 0, 2, 3]])` (`3.5` is closest at dist `2.5`, then `3.0` at `3.0`, then `10.0` at `4.0`, then `11.0` at `5.0`).
  - `[:, :3]` (`k = 3`) → `nearest = array([[1, 0, 2]])`, shape **`(1, 3)`**.
  - Voter labels `self.y_[[1, 0, 2]]` → `array(['stork', 'stork', 'swan'])`.
  - `Counter(...).most_common(1)` → `[('stork', 2)]` → `[0][0]` → `'stork'`.
  - `prediction` = `array(['stork'], dtype='<U5')` (`(1,)`). `str(prediction[0])` unboxes `np.str_('stork')` → plain Python **`'stork'`**.
- **"What If the Caller Passed...?" (Edge Cases):**
  - **Passing `row` directly without `[row]` (`model.predict([6.0])` instead of `model.predict([[6.0]])`):** `np.asarray([6.0])` is 1-D `(1,)`, so `cdist` immediately crashes with **`ValueError: XA must be a 2-dimensional array.`**! Why? Because scikit-learn's `predict` is ambiguous on 1-D `[6.0, 7.0]` (is that *1 bird with 2 features* `(1, 2)`, or *2 birds with 1 feature* `(2, 1)`?), so `predict` strictly requires a 2-D `(n_samples, n_features)` table!
  - **Calling `label_for` or `accuracy` on an *unfitted* `KNN(k=3)`:** Raises `AttributeError: 'KNN' object has no attribute 'X_'`.
  - **Passing `k > len(X_train)` (e.g., `k = 10` on 4 birds):** In NumPy slicing, `[:, :10]` on a `(1, 4)` array does **not** raise `IndexError` — it clamps cleanly to all `4` training birds (`[:, :4]`)! (By contrast, `sklearn`'s `KNeighborsClassifier(n_neighbors=10)` explicitly validates and raises `ValueError: Expected n_neighbors <= n_samples_fit`!)
  - **Even `k` Tie-Breaking (`k = 2` on query `[[6.75]]`):** Distances to `[3.5]` and `[10.0]` are both `3.25` (1 `'stork'`, 1 `'swan'`). In Python 3.7+, `Counter.most_common(1)` preserves first-seen insertion order, so **whichever neighbour came first in `argsort`** (the closer neighbour, or lower training index on exact distance tie) wins! By contrast, `sklearn`'s `KNeighborsClassifier` breaks ties by **alphabetical class order** (`classes_` index `0`, always `'stork'`). That is also why `E01_penguins.py` chose strictly **odd** `KS = [1, 3, 5, 9, 15, 25, 45]` for binary Male/Female classification: an odd vote between two classes can never tie!

### Pillar 3 — Analyse (Complexity & Design Trade-offs)
- **Time & Space Complexity (Lazy Learner vs Eager Learner — Classic 10/10 Question!):**
  - **`KNN.fit(X, y)` (`n` training rows, `d` features):**
    - Time: `O(n * d + n log n)` (`O(1)` if `X` is already a `float64` `ndarray`, or `O(n * d)` to copy/cast to `float64`, plus `O(n log n)` for `np.unique(y)`). **Zero model-parameter optimisation!**
    - Space: **`O(n * d)`** — must retain the *entire* training dataset `self.X_` in memory forever!
  - **`KNN.predict(X_query)` (`q` query rows):**
    - Time: **`O(q * n * d + q * n log n)`** (`O(q * n * d)` for `cdist`, `O(q * n log n)` for full `np.argsort` along each row, and `O(q * k)` for `Counter` voting). Note: for `label_for`, `q = 1`, so `O(n * d + n log n)`. *(Bonus optimisation insight: replacing `np.argsort(distances, axis=1)[:, :self.k]` with `np.argpartition(distances, self.k - 1, axis=1)[:, :self.k]` lowers the selection step from `O(q * n log n)` to **`O(q * n)`**!)*
    - Space: **`O(q * n)`** for the `distances` matrix (`O(n)` when `q = 1` in `label_for`).

### Likely Interview Q&A
- **Q: Why does `label_for` have to wrap `row` in `[row]` before calling `model.predict`, and why wrap `[0]` in `str(...)` afterwards?**  
  **A:** Scikit-learn estimators always operate on batches of rows of 2-D shape `(n_samples, n_features)` — passing a 1-D `row` of shape `(d,)` causes `cdist` inside `KNN.predict` to raise `ValueError: XA must be a 2-dimensional array`. `[row]` gives shape `(1, d)`, `predict` returns a 1-element NumPy `<U` array, `[0]` extracts `np.str_`, and `str(...)` unboxes it into a built-in Python `str`.
- **Q: Why is k-NN called a "lazy learner", and what is the trade-off between `fit` and `predict` compared to a logistic regression or neural network?**  
  **A:** k-NN does almost no work in `fit` (just memorising `self.X_` and `self.y_`), deferring 100% of the computation to `predict`, which must compare every query against all `n` training points in `O(n * d)` time and keep all `O(n * d)` training features in RAM. A parametric model spends heavy compute in `fit` compressing the data into `O(d)` weights, after which `predict` takes only `O(d)` time and `O(d)` memory independent of `n`!

---

## 11. `E09_paper.py` — Reproducible Research & Your `SEED = 26257770` Findings

- **File:** [E09_paper.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py) (Data & Paper: [E01_penguins.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L110), [table1.csv](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/table1.csv), [table2.csv](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/table2.csv), [PTAI_Penguins_Jack_Hickey.pdf](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/PTAI_Penguins_Jack_Hickey.pdf))
- **Difficulty Tier:** **Hard (8–10 Mark Target — Experimental Methodology, Variance & Model Selection)**

### Exact Quantitative Comparison: Lecture (`SEED = 0`) vs Your Run (`SEED = 26257770`)

You updated [`SEED = 26257770`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L110) in `E01_penguins.py` and ran the full 96-cell × 30-split grid (`2,880` evaluations in `results.csv`). Here is the exact side-by-side comparison between the lecture (`W09_Solutions/`, `SEED = 0`) and your run (`W09/W09/`, `SEED = 26257770`):

| Quantity | Lecture (`SEED = 0`) | Your Run (`SEED = 26257770`) | Why It Moved (or Stayed Fixed) |
| :--- | :--- | :--- | :--- |
| **Winning `best_cell(df)` on Dev Set** | `cats off, norm on, euclidean, k=5` (**`0.919`**) | **`cats off, norm on, chebyshev, k=5`** (**`0.910`**) | **Changed!** Euclidean `k=5` moved to `0.906` and Manhattan `k=9` to `0.909`; all three are well inside one within-cell SD (`~0.036`)! |
| **Dummy Classifier (Table 1)** | `0.504` | `0.504` | **Unchanged!** `stratify=y` preserves the exact Male/Female ratio (`168/333 ≈ 50.45%`) in the 266-bird dev set and every CV fold! |
| **Decision Tree (`cats off`, `norm off`/`on`)** | `0.847` / `0.849` | **`0.881` / `0.883`** | High-variance single tree + different 266-bird dev split and `random_state=SEED`. |
| **Random Forest (`cats on`, `norm off`/`on`)** | `0.901` / `0.902` | **`0.910` / `0.912`** | Different 266-bird dev split + bootstrap `random_state=SEED`. |
| **Pooled `norm` Effect (`False` → `True`)** | `0.7462` → `0.8802` (**`+13.4` pts**) | `0.7596` → `0.8795` (**`+12.0` pts**) | You updated Table 2's caption to *"worth roughly twelve points"*. |
| **Pooled `cats` Effect (`False` → `True`)** | `0.8189` → `0.8076` (`-1.1` pts) | `0.8266` → `0.8124` (`-1.4` pts) | Consistent negative effect from uninformative `island` dummies. |
| **Pooled `k` Peak (across all settings)** | `k = 9` (`0.8252`) / `k = 5` (`0.8249`) | `k = 9` (`0.8341`) | Within `cats off, norm on`, Chebyshev peaks at `k = 5` (`0.910`). |

> [!IMPORTANT]
> **Unfilled `# ANSWER:` on Line 79 of [E09_paper.py](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E09_paper.py#L79) + Two Final Paper Checks!**
> 1. **Ready-to-use `# ANSWER:` for `W09/W09/E09_paper.py` line 79:**
>    ```python
>    # ANSWER: Yes -- with SEED = 26257770, the best cross-validated cell changed
>    # from (cats off, norm on, euclidean, k=5) at 0.919 to (cats off, norm on,
>    # chebyshev, k=5) at 0.910 (with manhattan, k=9 at 0.909 and euclidean, k=5
>    # at 0.906). In the prose/captions, the pooled gain from normalisation moved
>    # from ~13.4 points to ~12.0 points (0.760 to 0.880), Decision Tree accuracy
>    # moved from 0.847-0.852 to 0.878-0.883, and 5 folds x 6 repeats gives 30
>    # splits rather than 25. Changing SEED reshuffles which 67 of the 333 sexed
>    # penguins are held out in train_test_split and reshuffles the 30 stratified
>    # CV splits on the 266 development penguins; on so few birds, random fold
>    # composition shifts cell means by ~0.01, easily swapping tied metrics.
>    ```
> 2. **Overleaf Prose `"25 splits"` Check:** In [PTAI_Penguins_Jack_Hickey.pdf](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/PTAI_Penguins_Jack_Hickey.pdf), Section 2 and the captions of Table 1, Table 2, and Figure 1 still say *"repeated **five** times, giving **25** train/test splits"*, whereas `SPLITS, REPEATS = 5, 6` in `E01_penguins.py` (and Figure 1's y-axis label `5-fold CV, 6 repeats`!) actually ran **six repeats = 30 splits**. Also check Table 2's caption (*"accuracy peaks around $k = 5$"* — still true for `cats off, norm on` Chebyshev `0.910` and Euclidean `0.906`, while Manhattan peaks at $k = 9$ with `0.909`).
> 3. **PDF Filename Check:** `E09_paper.py` Step 7 says *"save it beside this file as `paper.pdf`"*, whereas your file is currently named `PTAI_Penguins_Jack_Hickey.pdf`. Saving a copy as `W09/W09/paper.pdf` ensures both names exist!

### Pillar 1 & 3 — Deep Methodological Analysis (High-Scoring Interview Topics)
- **Why Checkpoint Invalidation (`load_checkpoint` & `resume`) Exists:**
  - [`load_checkpoint`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L442-L483) checks that `results.csv`'s recorded `seed`, `splits`, and `repeats` match the current module constants; when you changed `SEED` from `0` to `26257770`, it printed `results.csv: seed was 0, now 26257770. Starting again.`, deleted the stale CSV, and re-ran all 96 cells cleanly so two seeds could never be mixed in one table.
  - [`resume`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L486-L548) checks that every completed cell has all `SPLITS * REPEATS = 30` rows, dropping any partially written cell from a mid-run crash so `mode="a"` never duplicates rows.
- **Why the Held-Out Test Score Is Usually Slightly *Lower* Than the Best CV Score ("Winner's Curse" / Selection Bias):**
  - Look at [`main`](file:///Users/jackhickey/Documents/university/Semester1/programming_and_tools_for_ai/W09/W09/E01_penguins.py#L767-L780): we picked the maximum of **84** noisy cross-validation averages (`best_cell(df)`). Whenever several cells have nearly identical true accuracy (e.g., Euclidean, Manhattan, and Chebyshev around `k = 5..9`), choosing the `max` picks whichever cell got **luckiest** on the development splits! Evaluating that single chosen winner once on the untouched `67`-penguin test set gives an unbiased estimate free of selection optimism.

### Likely Interview Q&A
- **Q: Why did changing `SEED` from `0` to `26257770` change the winning metric from Euclidean to Chebyshev, yet leave the Dummy Classifier at `0.504`?**  
  **A:** `SEED` controls `train_test_split` (which `266` of the `333` penguins enter the development set) and `RepeatedStratifiedKFold` (how those `266` penguins are partitioned across the 30 splits). Because Euclidean, Manhattan, and Chebyshev on normalised features have nearly identical true performance (within `~0.004`, far smaller than the `~0.036` fold-to-fold standard deviation), sampling variation swaps which metric lands slightly higher. Meanwhile, `stratify=y` forces every split to preserve the exact Male/Female class proportion (`~50.4%` Male), so `DummyClassifier(strategy="most_frequent")` always predicts Male and scores `0.504`!
- **Q: Why does `E01_penguins.py` lock away 67 penguins at the start if it is already doing 30-split cross-validation on the 266 development penguins?**  
  **A:** Because we use the cross-validation scores to **make decisions** — selecting the best `(cats, norm, metric, k)` out of 84 candidates. Taking the maximum of 84 noisy estimates introduces optimistic selection bias ("winner's curse"). The held-out 67-penguin test set is never seen during model selection, so scoring the single winning configuration on it once at the very end gives an honest, unbiased generalisation estimate.
