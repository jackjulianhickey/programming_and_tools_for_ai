"""Given code. Aaronson's oracle, from the lecture: run it, or import it.

Play against each of the three models in turn, and see which one beats you:

    python W02/E01_oracle.py --no-information      # ignores you completely
    python W02/E01_oracle.py --no-3-repeats        # one hand-written rule
    python W02/E01_oracle.py --n-gram 5           # counts, and learns

Type f or d as randomly as you can. Any other key ends the game.

The learned counts can outlive the program:

    python W02/E01_oracle.py --write me.txt        # save what it learned
    python W02/E01_oracle.py --read me.txt         # start knowing it
    python W02/E01_oracle.py --read-write me.txt   # both: keep improving

Run its tests with:

    python -m doctest W02_Solutions/E01_oracle.py

Nothing in this file is your work, so read as much or as little of it as you
like. The command line handling at the bottom uses `argparse`, which we do
not cover; you never have to write anything like it.
"""

import argparse
import random
from collections import Counter
from pathlib import Path

from oracle_keys import read_key

KEYS = "fd"
K = 4                       # context length. An n-gram is K + 1 long.
DATA = Path(__file__).parent / "data"


# ---------------------------------------------------------------- models ---
#
# Every model has the same two-argument shape, so `play` can call any of them
# without knowing which it has.

def predict_no_information(counts, history):
    """Ignore the history entirely and guess. Scores 50%, by construction.

    >>> predict_no_information(Counter(), "fdfd") in KEYS
    True
    """
    return random.choice(KEYS)


def predict_no_3_repeats(counts, history):
    """Assume the human never types the same key three times in a row.

    >>> predict_no_3_repeats(Counter(), "fdff")
    'd'
    >>> predict_no_3_repeats(Counter(), "fddd")
    'f'

    With no opinion, it falls back to a guess:

    >>> predict_no_3_repeats(Counter(), "fdfd") in KEYS
    True
    """
    if history[-2:] == "ff":
        return "d"
    elif history[-2:] == "dd":
        return "f"
    else:
        return random.choice(KEYS)


def predict_ngram(counts, history):
    """Guess whatever usually followed this context before.

    With no counts at all it has no opinion, so either key may come back:

    >>> predict_ngram(Counter(), "fdfd") in KEYS
    True

    Once one continuation is commoner than the other, it wins:

    >>> counts = Counter({"fdfdf": 7, "fdfdd": 2})
    >>> predict_ngram(counts, "fdfd")
    'f'
    >>> predict_ngram(counts, "ddfdfd")     # only the last K characters count
    'f'
    """
    context = history[-K:]
    f = counts[context + "f"]
    d = counts[context + "d"]
    if f > d:
        return "f"
    elif d > f:
        return "d"
    else:
        return random.choice(KEYS)


def update(counts, history, key):
    """Record that `key` followed the end of `history`.

    >>> counts = Counter()
    >>> update(counts, "fdfd", "f")
    >>> update(counts, "fdfd", "f")
    >>> update(counts, "fdfd", "d")
    >>> counts["fdfdf"]
    2
    >>> counts["fdfdd"]
    1
    """
    counts[history[-K:] + key] += 1


# ------------------------------------------------------------------ files ---

def save(counts, path):
    """Write the counts, one n-gram per line."""
    with open(path, "w") as f:
        for ngram in sorted(counts):
            f.write(f"{ngram} {counts[ngram]}\n")


def load(path):
    """Read back what save wrote.

    Saving and loading must compose to nothing:

    >>> counts = Counter({"fdfdf": 7, "fdfdd": 2})
    >>> save(counts, "_tmp_ngrams.txt")
    >>> load("_tmp_ngrams.txt") == counts
    True
    >>> import os; os.remove("_tmp_ngrams.txt")
    """
    counts = Counter()
    with open(path) as f:
        for line in f:
            ngram, n = line.split()
            counts[ngram] = int(n)
    return counts


# ------------------------------------------------------------------- game ---

def report(guess, key, correct, n):
    print(f"guessed {guess}, you typed {key}: {correct}/{n} = {correct / n:.0%}")


def play(predict, counts):
    """The game loop. Returns the history of what was typed."""
    history = ""
    correct = 0
    while True:
        guess = predict(counts, history)
        key = read_key()
        if key not in KEYS:
            break
        if guess == key:
            correct += 1
        update(counts, history, key)
        history = history + key
        report(guess, key, correct, len(history))
    return history


# ------------------------------------------------------------ command line ---

def parse_args(argv=None):
    """Read the command line. See the module docstring for examples.
    You don't need to read this function. argparse is not examinable.

    >>> parse_args(["--ngram", "3"]).ngram
    3
    >>> parse_args([]).ngram                  # 5-grams unless you say otherwise
    5
    >>> parse_args(["--no-3-repeats"]).model
    'no-3-repeats'
    >>> parse_args([]).model
    'ngram'
    """
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    models = p.add_mutually_exclusive_group()
    models.add_argument("--no-information", dest="model", action="store_const",
                        const="no-information",
                        help="ignore the history and guess")
    models.add_argument("--no-3-repeats", dest="model", action="store_const",
                        const="no-3-repeats",
                        help="assume you never type three of the same in a row")
    models.add_argument("--ngram", "--n-gram", type=int, metavar="N",
                        help="count N-grams and learn (the default, with N=5)")
    p.add_argument("--read", metavar="FILE",
                   help="load counts from FILE before playing")
    p.add_argument("--write", metavar="FILE",
                   help="save counts to FILE afterwards")
    p.add_argument("--read-write", dest="read_write", metavar="FILE",
                   help="both, using one file (which need not exist yet)")
    args = p.parse_args(argv)

    if args.model is None:
        args.model = "ngram"
    if args.ngram is None:
        args.ngram = 5
    if args.ngram < 2:
        p.error("--ngram needs N of 2 or more: an n-gram is a context plus "
                "the key that followed it")
    if args.read_write:
        args.read = args.write = args.read_write
    return args


MODELS = {"no-information": predict_no_information,
          "no-3-repeats": predict_no_3_repeats,
          "ngram": predict_ngram}


if __name__ == "__main__":
    args = parse_args()

    # An n-gram of length N has a context of length N - 1. `global` is not
    # needed here because this is module level, but note that we are reaching
    # in and changing a module-wide setting -- exactly the kind of thing an
    # object would hold for us instead. That is Week 4.
    K = args.ngram - 1

    counts = Counter()
    if args.read:
        try:
            counts = load(args.read)
            print(f"read {len(counts)} n-grams from {args.read}")
        except FileNotFoundError:
            if not args.read_write:
                # --read means "I have a model already". --read-write is the
                # one that is allowed to start a new file.
                raise SystemExit(f"no such file: {args.read}\n"
                                 f"use --read-write to start a new one")
            print(f"{args.read} does not exist yet; starting from nothing")

    print(f"model: {args.model}", end="")
    print(f", n={args.ngram}" if args.model == "ngram" else "")
    print("Type f or d as randomly as you can. Any other key stops.")

    history = play(MODELS[args.model], counts)

    print(f"\n{len(history)} keypresses.")
    if history:
        print("your commonest patterns:", counts.most_common(3))
    if args.write:
        save(counts, args.write)
        print(f"wrote {len(counts)} n-grams to {args.write}")
