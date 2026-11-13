"""Can you sex a penguin from four measurements? The lecture program, complete.

Run it, run its doctests, read it. Nothing here is left for you to write.

    python E01_penguins.py              # the whole experiment
    python E01_penguins.py --fresh      # ignore the checkpoint and redo it
    python -m doctest E01_penguins.py

It writes five files next to this one:

    results.csv      one row per run: the raw data, and the settings it
                     came from. Written as the experiment goes, so a run
                     that is interrupted picks up where it left off
    table1.tex       the reference rows: what we have to beat
    table2.tex       the factorial: every setting of our own classifier
    accuracy.png     the figure in png format for slides/web
    accuracy.pdf     the figure in pdf format for publication

The question is a real one. Gorman and colleagues measured 344 penguins of
three species at Palmer Station, Antarctica, to study sexual dimorphism --
whether males and females differ in body shape. See:
https://journal.r-project.org/articles/RJ-2022-020/
Their data is in data/, and we are asking their question: given a bill, a 
flipper and a body mass, can you tell a male penguin from a female one?

Nothing here is about penguins, though. It is about how you answer a question
like that without fooling yourself: hold data back, vary one thing at a time
and everything at once, repeat it enough to get an error bar, and compare
against something stupid so you know whether the answer means anything.

Four factors, crossed:

    features        two          the four measurements, or those plus the
                                 species and island columns?
    normalisation   off / on     do we put the measurements on a common scale?
    metric          three        what does "nearest" mean?
    k               seven        how many neighbours vote?

The response is accuracy. The doctests below use small hand-made arrays,
except where they are explicitly about the data file.

After running this code, we can go to Overleaf to create a pdf document.
Here is my document, which you can view.
If you generate new figures or tables, or you want to change the text,
you can fork to your own Overleaf account. This is then a complete 
practice / demo for your research project later in the programme (ie,
not part of Programming and Tools for AI).

Go there, fork it to your own account, put your own name on it in place of
mine, and export the pdf. If you change the experiment, run this program
again and upload the three files it writes that the paper uses --- table1.tex,
table2.tex and accuracy.pdf --- over the ones already there.

https://www.overleaf.com/project/6ab11100f078f79356e41ce6/share#8bf10abbbec8e47045e27ab54789fe163c2ec0756f485f63

"""

import argparse
import itertools
from collections import Counter
from pathlib import Path
from time import perf_counter

import matplotlib
matplotlib.use("Agg")           # write a file; never open a window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (RepeatedStratifiedKFold, cross_val_score,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
DATA = HERE / "data"

MEASUREMENTS = ["bill_length_mm", "bill_depth_mm",
                "flipper_length_mm", "body_mass_g"]
TARGET = "sex"

# The design. Every combination of these is run. That is what "full
# factorial" means: no combination is skipped because we think we already
# know what it would do.
NORMS = [False, True]
KS = [1, 3, 5, 9, 15, 25, 45]

# Whether the classifier may see the species and island columns as well as
# the four measurements. Note where this factor lives: in the experiment, not
# in the estimator. "How many neighbours vote" is a setting of the model and
# belongs in its __init__; "which columns did we record" is a decision about
# the data, taken before any model exists. Putting the second kind inside an
# estimator is a common and confusing mistake -- and the reason it is
# tempting is that both of them change the accuracy, which is all the results
# table can see.
CATEGORICALS = [False, True]

# scipy and scikit-learn disagree about one name: what everyone calls the
# Manhattan distance, scipy calls "cityblock". We use the everyday names in
# the table and translate here, in one place.
METRICS = {"euclidean": "euclidean",
           "manhattan": "cityblock",
           "chebyshev": "chebyshev"}

SEED = 0
# Deliberately not equal. 5 and 5 would give "5 folds, 5 repeats, 25
# scores", and every one of those numbers could be mistaken for another.
SPLITS, REPEATS = 5, 6          # 30 scores per cell: see protocol() below


def label(cats, norm):
    """A heading for one combination of the two on/off factors.

    True and False are correct but unreadable across the top of a table. We
    put this in the results as an ordinary column, so that making the table
    later is a single pivot_table call with nothing to tidy up afterwards.

    >>> label(False, True)
    'cats off, norm on'
    >>> label(True, False)
    'cats on, norm off'
    """
    return (f"cats {'on' if cats else 'off'}, "
            f"norm {'on' if norm else 'off'}")


# ------------------------------------------------------------------ data ---

def load_raw():
    """The data exactly as it was published: 344 penguins, missing values and all.

    >>> raw = load_raw()
    >>> raw.shape
    (344, 7)
    >>> list(raw.columns)[:2]
    ['species', 'island']

    Three columns are worth knowing about before we touch anything:

    >>> int(raw["sex"].isna().sum())         # penguins never sexed
    11
    >>> int(raw["body_mass_g"].isna().sum()) # penguins never weighed
    2
    """
    return pd.read_csv(DATA / "penguins.csv")


def clean(raw, use_categoricals=True):
    """Return (X, y): a numeric table of features, and the labels to predict.

    Two kinds of missing value turn up here and they are not the same kind of
    problem. A missing *feature* can be filled in -- with the column's median,
    say -- because we are only guessing at an input. A missing *label* cannot
    be, because filling it in would mean inventing the answer and then
    marking ourselves against it. So rows with no recorded sex are dropped.

    Species and island are words, not numbers. get_dummies turns each into
    one column per value holding 0 or 1, which is the only form a distance
    can be computed on.

    >>> raw = pd.DataFrame({"species": ["Adelie", "Gentoo", "Adelie"],
    ...                     "island": ["Dream", "Biscoe", "Dream"],
    ...                     "bill_length_mm": [39.1, 46.1, 40.3],
    ...                     "bill_depth_mm": [18.7, 13.2, 18.0],
    ...                     "flipper_length_mm": [181.0, 211.0, 195.0],
    ...                     "body_mass_g": [3750.0, 4500.0, 3250.0],
    ...                     "sex": ["Male", "Female", None]})
    >>> X, y = clean(raw)
    >>> y                                    # the unlabelled penguin is gone
    array(['Male', 'Female'], dtype=object)
    >>> list(X.columns)
    ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'species_Adelie', 'species_Gentoo', 'island_Biscoe', 'island_Dream']
    >>> X["species_Adelie"].tolist()
    [1.0, 0.0]

    Without the categorical columns it is the four measurements alone:

    >>> X, y = clean(raw, use_categoricals=False)
    >>> list(X.columns)
    ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    """
    labelled = raw.dropna(subset=[TARGET])
    columns = MEASUREMENTS + (["species", "island"] if use_categoricals else [])
    # get_dummies expands the str columns and leaves the numbers alone.
    # dtype=float because its default is True/False, and distances need numbers.
    X = pd.get_dummies(labelled[columns], dtype=float)
    y = labelled[TARGET].to_numpy()
    return X, y


# ------------------------------------------------------------- our classifier ---
#
# The scikit-learn conventions, all four of them visible below:
#
#   1. __init__ stores its arguments under their own names and does nothing
#      else -- no validation, no computation. clone() and GridSearchCV work by
#      reading the __init__ signature and expecting to find self.k and
#      self.metric, so a rename or a tidy-up here breaks them.
#   2. Anything learned from data gets a trailing underscore: X_, not X. That
#      is how you tell at a glance what fit() created.
#   3. fit() returns self, so est.fit(X, y).predict(X) reads as one thought.
#   4. Inheriting from BaseEstimator gets get_params and set_params for free,
#      and from ClassifierMixin gets score (accuracy). We write neither.
#
# Week 8 already wrote most of this. distances_to and most_similar in
# E01_photos.py found the rows nearest a query row using np.argsort. All that
# is new here is that the rows have labels, and the neighbours vote.

class KNN(BaseEstimator, ClassifierMixin):
    """Predict the label held by most of the k nearest training rows.

    "Fitting" is nothing but remembering the training set. All of the work
    happens in predict, which is unusual and worth noticing.

    >>> X = np.array([[0.0], [1.0], [10.0], [11.0]])
    >>> y = np.array(["low", "low", "high", "high"])
    >>> model = KNN(k=1).fit(X, y)
    >>> model.predict(np.array([[0.5], [10.5]]))
    array(['low', 'high'], dtype='<U4')

    With k=3 the vote reaches further, and a query near the boundary is
    outvoted by whichever side has more neighbours:

    >>> KNN(k=3).fit(X, y).predict(np.array([[9.0]]))
    array(['high'], dtype='<U4')
    >>> KNN(k=3).fit(X, y).predict(np.array([[2.0]]))
    array(['low'], dtype='<U3')

    Learned state carries the underscore, and there is none before fit:

    >>> hasattr(KNN(), "X_")
    False
    >>> sorted(KNN().get_params())
    ['k', 'metric']

    score comes from ClassifierMixin, and is accuracy:

    >>> round(KNN(k=1).fit(X, y).score(X, y), 3)
    1.0
    """

    def __init__(self, k=5, metric="euclidean"):
        self.k = k
        self.metric = metric

    def fit(self, X, y):
        """Remember the training set. That is the whole of fitting."""
        self.X_ = np.asarray(X, dtype=float)
        self.y_ = np.asarray(y)
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        """One label per row of X, by majority vote of its k nearest rows.

        cdist is Week 8's closing built-in: every query row against every
        training row in one call, giving a (n_query, n_train) matrix. Then
        argsort along each row puts the nearest training rows first, exactly
        as most_similar did, and the first k of them are the voters.
        """
        distances = cdist(np.asarray(X, dtype=float), self.X_, metric=self.metric)
        nearest = np.argsort(distances, axis=1)[:, :self.k]
        return np.array([Counter(self.y_[row]).most_common(1)[0][0]
                         for row in nearest])


def build(norm, metric, k):
    """One estimator for one cell of the design.

    The scaler goes *inside* a Pipeline rather than being applied to the data
    beforehand. That matters: inside, it learns its mean and standard
    deviation from the training fold alone, so no fact about the test fold
    can leak into the training of the model. Scaling the whole table first
    would leak, quietly, and flatter every result.

    >>> build(False, "euclidean", 3)
    KNN(k=3)
    >>> type(build(True, "euclidean", 3)).__name__
    'Pipeline'
    """
    model = KNN(k=k, metric=METRICS[metric])
    return make_pipeline(StandardScaler(), model) if norm else model


# ------------------------------------------------------------- the experiment ---

def protocol(y):
    """Split the penguins once, and build the cross-validator for everything else.

    This is the part that is easy to get wrong and impossible to fix
    afterwards, so it happens once, here, before any model is built.

    It splits *row numbers*, not a table of features. That is what keeps the
    feature-set factor honest: both feature sets are then scored on exactly
    the same penguins, so a difference between them is a difference between
    the columns and not an accident of who landed in which fold.

    The test set is put away now and touched exactly once, at the very end.
    Everything -- choosing k, choosing a metric, deciding whether to
    normalise, deciding which columns to use -- happens on the development
    set. stratify keeps the male/female balance the same in both halves.

    >>> X, y = clean(load_raw())
    >>> dev, test, cv = protocol(y)
    >>> len(dev), len(test)
    (266, 67)
    >>> set(dev) & set(test)                 # nothing is in both
    set()
    >>> cv.get_n_splits()
    30
    """
    rows = np.arange(len(y))
    dev, test = train_test_split(rows, test_size=0.2, stratify=y,
                                 random_state=SEED)
    # Five folds, and the whole thing repeated five times with the rows
    # shuffled differently each time. That is 5 x 6 = 30 train/test splits,
    # so 30 scores -- not 30 folds: a fold is one part of one cut, and there
    # are only ever five of those at a time. With only 266 development rows a
    # single round of 5-fold is too noisy to tell the metrics apart, and
    # repeating costs nothing but time.
    cv = RepeatedStratifiedKFold(n_splits=SPLITS, n_repeats=REPEATS,
                                 random_state=SEED)
    return dev, test, cv


def score_cell(estimator, X, y, cv, n_jobs=1):
    """Run one estimator over every split and return the raw scores.

    >>> X, y = clean(load_raw(), use_categoricals=False)
    >>> dev, _, cv = protocol(y)
    >>> scores = score_cell(build(True, "euclidean", 5), X.iloc[dev], y[dev], cv)
    >>> len(scores)
    30
    >>> print(round(scores.mean(), 3))
    0.919
    """
    return cross_val_score(estimator, X, y, cv=cv, n_jobs=n_jobs)


# What identifies one cell of the design. Everything else in a results row
# is either a setting these imply, or a number the run produced.
CELL = ["model", "cats", "norm", "metric", "k"]

# The reference models have no metric and no k. They need *some* value in
# those columns, because a tidy table has the same columns in every row, and
# "-" reads better in the csv than an empty field -- which pandas would read
# back as a missing value and refuse to match.
NONE = "-"


def reference_models():
    """The rows at the bottom of the table: what our classifier has to beat.

    DummyClassifier does no learning at all -- it answers with whichever
    label was commoner in training. Every other number in the paper is
    meaningless until you know this one.

    The two tree models are here for a second reason. A tree splits on one
    feature at a time and compares it against a threshold, so multiplying a
    column by a thousand cannot change which way any split goes. They should
    therefore be unaffected by normalisation, and the table is where we check
    that rather than assert it. The check very nearly passes: the two columns
    agree to three decimal places but not exactly, because rescaling shifts
    the candidate thresholds by a hair and occasionally flips a tie between
    two equally good splits. A difference that small is floating-point
    arithmetic, not an effect.
    """
    return {"Dummy (most frequent)": DummyClassifier(strategy="most_frequent"),
            "Decision tree": DecisionTreeClassifier(random_state=SEED),
            "Random forest": RandomForestClassifier(n_estimators=100,
                                                    random_state=SEED)}


def planned_cells():
    """Every cell this experiment intends to run, as a set of keys.

    Three reference models over two feature sets and two normalisations, plus
    our own classifier over those and three metrics and seven values of k.

    >>> len(planned_cells())
    96
    >>> ("KNN", False, True, "euclidean", 5) in planned_cells()
    True
    >>> ("KNN", False, True, "euclidean", 7) in planned_cells()
    False
    """
    cells = {(name, cats, norm, NONE, 0)
             for name in reference_models()
             for cats, norm in itertools.product(CATEGORICALS, NORMS)}
    return cells | {("KNN", cats, norm, metric, k)
                    for cats, norm, metric, k
                    in itertools.product(CATEGORICALS, NORMS, METRICS, KS)}


def estimator_for(model, cats, norm, metric, k):
    """The estimator one cell of the design calls for.

    The reference models get the same treatment as our own classifier, for
    the same reason a control group gets the same everything: a comparison
    is only a comparison if the two sides differ in one thing.

    >>> estimator_for("KNN", False, False, "euclidean", 3)
    KNN(k=3)
    >>> type(estimator_for("Decision tree", False, True, NONE, 0)).__name__
    'Pipeline'
    """
    if model == "KNN":
        return build(norm, metric, k)
    estimator = reference_models()[model]
    return make_pipeline(StandardScaler(), estimator) if norm else estimator


def run_cells(todo, tables, y, cv, path, n_jobs=1):
    """Run each outstanding cell, appending its rows the moment it finishes.

    Writing as we go, rather than once at the end, is what makes the run
    resumable: whatever has finished is already on disk, so a crash costs at
    most the cell that was in flight. mode="a" appends, and the header is
    written only when the file is new.
    """
    for i, key in enumerate(sorted(todo), 1):
        model, cats, norm, metric, k = key
        scores = score_cell(estimator_for(*key), tables[cats], y, cv, n_jobs)
        rows = [{"model": model, "cats": cats, "norm": norm, "metric": metric,
                 "k": k, "setting": label(cats, norm), "seed": SEED,
                 "splits": SPLITS, "repeats": REPEATS,
                 "split": split, "accuracy": score}
                for split, score in enumerate(scores)]
        pd.DataFrame(rows).to_csv(path, mode="a", index=False,
                                  header=not path.exists())
        print(f"\r  cell {i} of {len(todo)}", end="", flush=True)
    print()


# --------------------------------------------------------- tables and figure ---

def load_checkpoint(path):
    """The saved results, or None if the file is missing or unusable.

    A file produced under a different seed, or a different cross-validation
    setup, describes a different experiment. Nothing in it can be reused, so
    it is deleted and we start over. That is safe precisely because there is
    nothing to salvage -- every number in it is stale.

    >>> tmp = HERE / "_tmp_results.csv"
    >>> def save(**kwargs):
    ...     pd.DataFrame(dict(accuracy=[0.9], **kwargs)).to_csv(tmp, index=False)
    >>> save(seed=SEED, splits=SPLITS, repeats=REPEATS)
    >>> len(load_checkpoint(tmp))
    1

    >>> save(seed=SEED + 1, splits=SPLITS, repeats=REPEATS)
    >>> load_checkpoint(tmp) is None
    _tmp_results.csv: seed was 1, now 0. Starting again.
    True
    >>> tmp.exists()                      # and the stale file is gone
    False

    >>> load_checkpoint(HERE / "_no_such_file.csv") is None
    True
    """
    if not path.exists():
        return None
    df = pd.read_csv(path)
    for column, now in [("seed", SEED), ("splits", SPLITS),
                        ("repeats", REPEATS)]:
        if column not in df.columns:
            print(f"{path.name} predates the {column} column. Starting again.")
            path.unlink()
            return None
        was = sorted(set(df[column]))
        if was != [now]:
            print(f"{path.name}: {column} was "
                  f"{was[0] if len(was) == 1 else was}, now {now}. "
                  f"Starting again.")
            path.unlink()
            return None
    return df


def resume(path):
    """Work out what is already done, and what is left to run.

    A cell counts as done only when all of its rows are there. A cell with
    some of them was interrupted half way through being written, so its rows
    are dropped and it will be run again -- otherwise appending to it would
    leave the file with that cell recorded twice.

    A file containing a cell we are *not* planning to run is a different
    matter. It means the design has changed since the file was written --- a
    value removed from KS, say --- and mixing the two would give a table
    that never came from any one experiment. There is no safe guess to make,
    so this stops and says so.

    >>> tmp = HERE / "_tmp_results.csv"
    >>> def rows(key, n):
    ...     m, c, nm, me, k = key
    ...     return pd.DataFrame({"model": m, "cats": c, "norm": nm,
    ...                          "metric": me, "k": k, "seed": SEED,
    ...                          "splits": SPLITS, "repeats": REPEATS,
    ...                          "split": range(n), "accuracy": 0.9})

    One finished cell, so one fewer to run:

    >>> done = ("KNN", False, True, "euclidean", 5)
    >>> rows(done, SPLITS * REPEATS).to_csv(tmp, index=False)
    >>> df, todo = resume(tmp)
    >>> len(planned_cells()) - len(todo), done in todo
    (1, False)

    A half-written cell is dropped and run again:

    >>> rows(done, 4).to_csv(tmp, index=False)
    >>> df, todo = resume(tmp)
    dropping 1 unfinished cell from _tmp_results.csv
    >>> done in todo
    True
    >>> tmp.unlink()
    """
    df = load_checkpoint(path)
    if df is None:
        return None, planned_cells()

    counts = df.groupby(CELL, dropna=False).size()
    have = {key: int(n) for key, n in counts.items()}
    unplanned = sorted(set(have) - planned_cells())
    if unplanned:
        raise SystemExit(
            f"{path.name} holds {len(unplanned)} cell(s) this experiment is "
            f"not running, for example {unplanned[0]}.\n"
            f"The design has changed since it was written. Re-run with "
            f"--fresh to start over, or put the design back.")

    complete = {key for key, n in have.items() if n == SPLITS * REPEATS}
    partial = set(have) - complete
    if partial:
        print(f"dropping {len(partial)} unfinished cell from {path.name}"
              if len(partial) == 1 else
              f"dropping {len(partial)} unfinished cells from {path.name}")
        keep = df[CELL].apply(tuple, axis=1).isin(complete)
        df = df[keep]
        df.to_csv(path, index=False)
    return df, planned_cells() - complete


def mean_sd(df, by):
    """Mean and standard deviation of accuracy, grouped however you ask.

    Tidy data -- one row per split, one column per thing we varied -- is what
    makes this a one-liner, and it is why results.csv is shaped the way it is
    rather than being a table already.

    >>> df = pd.DataFrame({"k": [1, 1, 2, 2], "accuracy": [0.8, 0.9, 0.5, 0.7]})
    >>> mean_sd(df, "k").round(3).to_dict("list")
    {'mean': [0.85, 0.6], 'sd': [0.071, 0.141]}
    """
    out = df.groupby(by)["accuracy"].agg(["mean", "std"])
    return out.rename(columns={"std": "sd"})


def table_references(df):
    """Reference rows, one column per setting.

    pivot_table takes the long results and swings one column out across the
    top: index says what goes down the side, columns what goes across, and
    values what fills the middle. The mean over the 30 splits is taken for
    us. The one reindex puts the models back in the order we introduced them
    rather than alphabetical.

    >>> df = pd.DataFrame({"model": ["Dummy (most frequent)"] * 2,
    ...                    "setting": ["cats off, norm on"] * 2,
    ...                    "accuracy": [0.4, 0.6]})
    >>> table_references(df).round(3).to_dict()
    {'cats off, norm on': {'Dummy (most frequent)': 0.5}}
    """
    ref = df[df["model"] != "KNN"]
    table = ref.pivot_table(index="model", columns="setting", values="accuracy")
    return table.reindex([m for m in reference_models() if m in table.index])


def table_factorial(df):
    """The whole factorial, in one pivot_table call.

    Two of the four factors go down the side and two across the top. That is
    a choice about shape, not about content -- every cell of the design is in
    here either way -- and down the side is the better place for the two with
    the most levels, because a page is taller than it is wide.
    """
    knn = df[df["model"] == "KNN"]
    return knn.pivot_table(index=["metric", "k"], columns="setting",
                           values="accuracy")


def make_figure(df, path):
    """One panel per (feature set, normalisation); k across, metric by colour.

    Four factors do not fit on one pair of axes, so two of them become the
    grid of panels and two live inside each panel. Reading it is then a
    matter of comparing rows for one factor and columns for another.

    Error bars are the standard deviation over the 30 splits. A single
    number with no error bar is not a result; it is an anecdote.
    """
    knn = mean_sd(df[df["model"] == "KNN"],
                  ["cats", "norm", "metric", "k"]).reset_index()
    refs = mean_sd(df[df["model"] != "KNN"], ["cats", "model"])["mean"]

    fig, axes = plt.subplots(len(CATEGORICALS), len(NORMS),
                             figsize=(11, 8), sharex=True, sharey=True)
    for row, cats in enumerate(CATEGORICALS):
        for col, norm in enumerate(NORMS):
            ax = axes[row][col]
            for metric in METRICS:
                cell = knn[(knn["cats"] == cats)
                           & (knn["norm"] == norm) & (knn["metric"] == metric)]
                ax.errorbar(cell["k"], cell["mean"], yerr=cell["sd"],
                            marker="o", markersize=4, capsize=3, label=metric)
            for name, style in zip(reference_models(), [":", "--", "-."]):
                ax.axhline(refs[cats][name], color="grey",
                           linestyle=style, linewidth=1)
                # Label them in the left column only, against the left-hand
                # edge. The legend then goes in the empty band between the
                # dummy classifier and the data, which no panel uses.
                if not norm:
                    ax.annotate(name, (KS[0], refs[cats][name]),
                                fontsize=7, color="grey", ha="left", va="bottom")
            ax.set_title(f"categorical vars {'on' if cats else 'off'}; "
                         f"normalisation {'on' if norm else 'off'}", fontsize=10)
            ax.set_xscale("log")
            ax.set_xticks(KS)
            ax.set_xticklabels(KS)
        axes[row][0].set_ylabel(f"accuracy ({SPLITS}-fold CV, "
                                f"{REPEATS} repeats)")
    for ax in axes[-1]:
        ax.set_xlabel("k (neighbours voting)")
    # One legend for the whole figure: the three metrics are the same in
    # every panel, and a legend inside one would sit on top of a line.
    # One legend for the whole figure, put inside the panel that has room for
    # it rather than in a strip underneath: the panels are what the reader is
    # looking at, and space below the axes is space not spent on data.
    axes[-1][0].legend(loc="center", bbox_to_anchor=(0.5, 0.25),
                       ncol=len(METRICS), fontsize=9)
    # No overall title. What the figure shows belongs in the caption, where a
    # reader looking at the list of figures will find it, and where it can be
    # a sentence rather than a label.
    fig.tight_layout()

    # The same figure in both formats, because the right one depends on where
    # it is going. PNG is pixels: fine on a slide or a web page, and it blurs
    # if anyone enlarges it. PDF is vector -- the lines are stored as lines --
    # so it stays sharp at any size and is what a LaTeX paper wants. Write
    # both once and choose later.
    for suffix in (".png", ".pdf"):
        fig.savefig(path.with_suffix(suffix), dpi=200)
        print(f"wrote {path.with_suffix(suffix).name}")


# --------------------------------------------------------------------- main ---

def best_cell(df):
    """The winning combination, chosen on the development set alone.

    >>> df = pd.DataFrame({"model": ["KNN"] * 3, "cats": [False] * 3,
    ...                    "norm": [True, True, False],
    ...                    "metric": ["euclidean"] * 3, "k": [1, 5, 5],
    ...                    "accuracy": [0.7, 0.9, 0.8]})
    >>> print(*best_cell(df))
    False True euclidean 5
    """
    knn = df[df["model"] == "KNN"]
    means = knn.groupby(["cats", "norm", "metric", "k"])["accuracy"].mean()
    return means.idxmax()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fresh", action="store_true",
                   help="delete results.csv and run the whole grid again. "
                        "Changing SEED already does this for you")
    p.add_argument("--jobs", type=int, default=1,
                   help="cores to use; -1 means all of them (default: 1). "
                        "This grid is small enough not to need it")
    args = p.parse_args(argv)

    raw = load_raw()
    # One cleaned table per feature set, and one y shared by both: the rows
    # are the same penguins in the same order either way.
    tables = {cats: clean(raw, use_categoricals=cats)[0]
              for cats in CATEGORICALS}
    _, y = clean(raw)
    print(f"{len(raw)} penguins measured, {len(y)} of them sexed")
    for cats, table in tables.items():
        print(f"  categorical vars {'on ' if cats else 'off'}: "
              f"{table.shape[1]} columns: {list(table.columns)}")
    # After dropping the unlabelled rows there is nothing left to impute: the
    # two penguins that were never weighed are among the eleven that were
    # never sexed. Worth checking rather than assuming.
    print(f"missing values remaining: "
          f"{sum(int(t.isna().sum().sum()) for t in tables.values())}")

    dev, test, cv = protocol(y)
    print(f"development set {len(dev)}, test set {len(test)} "
          f"(put away until the last line of this program)")
    print(f"cross-validation: {SPLITS} folds x {REPEATS} repeats "
          f"= {cv.get_n_splits()} train/test splits, so that many scores "
          f"per cell\n")

    devs = {cats: table.iloc[dev] for cats, table in tables.items()}
    ydev, ytest = y[dev], y[test]

    results = HERE / "results.csv"
    if args.fresh and results.exists():
        results.unlink()            # --fresh means start the file over, not
                                    # append a second run onto the first
    df, todo = resume(results)
    if df is not None:
        print(f"{results.name}: {len(df)} rows already done, "
              f"{len(todo)} cells left")
    if todo:
        start = perf_counter()
        run_cells(todo, devs, ydev, cv, results, args.jobs)
        print(f"  {len(todo)} cells in {perf_counter() - start:.1f}s")
    df = pd.read_csv(results)
    print(f"{len(df)} rows in {results.name}")

    t1, t2 = table_references(df), table_factorial(df)
    for name, table in [("table1", t1), ("table2", t2)]:
        # multirow=False: pandas would otherwise write \multirow to span the
        # metric name down its seven rows, and that needs a LaTeX package the
        # paper does not load. Writing the name once and leaving the rest
        # blank looks the same and needs nothing.
        (HERE / f"{name}.tex").write_text(
            table.to_latex(float_format="%.3f", multirow=False))
        table.to_csv(HERE / f"{name}.csv", float_format="%.3f")

    print("\nWhat we have to beat\n")
    print(t1.to_string(float_format="%.4f"))
    print("\nOur own classifier, every setting\n")
    print(t2.to_string(float_format="%.3f"))

    print("\nWhat each factor did, pooled over the others:")
    knn = df[df["model"] == "KNN"]
    for factor in ["cats", "norm", "metric", "k"]:
        print()
        print(mean_sd(knn, factor).to_string(float_format="%.4f"))
    cells = ["cats", "norm", "metric", "k"]
    print(f"\ntypical spread within a cell (sd over its splits): "
          f"{knn.groupby(cells)['accuracy'].std().median():.4f}")

    make_figure(df, HERE / "accuracy.png")

    # Ours against theirs: same data, same splits, same answer. Nothing in
    # cross_val_score ever asks what type either object is. It calls fit,
    # predict and score, and anything with those three methods will do.
    print("\nOurs against scikit-learn's, k=5, normalised, measurements only:")
    for name, model in [("our KNN", KNN(k=5)),
                        ("KNeighborsClassifier", KNeighborsClassifier(5))]:
        scores = score_cell(make_pipeline(StandardScaler(), model),
                            devs[False], ydev, cv, args.jobs)
        print(f"  {name:22s} {scores.mean():.6f} +- {scores.std():.6f}")

    # The test set, once. Everything above chose this configuration without
    # ever seeing these penguins, which is the only reason the number means
    # anything. It will usually come in below the cross-validated one: we
    # picked the best of 84 cells, and the best of 84 is flattered by
    # whichever way the noise happened to fall.
    cats, norm, metric, k = best_cell(df)
    final = build(norm, metric, k).fit(devs[cats], ydev)
    chosen = knn[(knn["cats"] == cats) & (knn["norm"] == norm)
                 & (knn["metric"] == metric) & (knn["k"] == k)]
    print(f"\nBest on development: {label(cats, norm)}, {metric}, k={k}")
    print(f"  cross-validated {chosen['accuracy'].mean():.4f}")
    print(f"  held-out test   "
          f"{final.score(tables[cats].iloc[test], ytest):.4f}   "
          f"({len(ytest)} penguins, used once)")


if __name__ == "__main__":
    main()
