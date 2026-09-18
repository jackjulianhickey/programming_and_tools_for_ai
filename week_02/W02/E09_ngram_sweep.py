"""Extension. Which value of n is best -- for you? SOLUTION.

Run the tests:

    python -m doctest W02/E09_ngram_sweep.py

No output means every test passed.

Playing a game takes minutes. Replaying a saved one takes milliseconds, so we
can try every value of n on the same keypresses and compare them fairly. This
is what "run an experiment" means, and Week 7 does it properly.

QUESTION: run the sweep on your own history and write the numbers into the
comment at the bottom. Which n was best, and why do the big ones fall away?
"""

from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent / "data"

# Given: the model from the lecture, with two changes.
#
#   1. The context length k is an argument, not a global, so one run of the
#      program can try several values.
#   2. A tie goes to "f" rather than being broken at random. The real oracle
#      guesses, which is right for a game but wrong for an experiment: we need
#      the same input to give the same number every time we run it.
def predict(counts, history, k):
    context = history[-k:]
    if counts[context + "d"] > counts[context + "f"]:
        return "d"
    return "f"


def update(counts, history, key, k):
    counts[history[-k:] + key] += 1


def accuracy(history, k):
    """Replay `history` past the model and return the fraction it got right.

    Exactly the lecture's loop: predict, score, learn, move on. The model
    starts empty and learns as it goes, so it is being tested only on
    keypresses it has not seen -- which is the honest way to do it.

    An empty model predicts "f", so a history of all f's is a clean sweep:

    >>> accuracy("ffffffffff", 1)
    1.0

    Alternating is learned after one mistake at the start:

    >>> accuracy("fdfdfdfdfd", 1)
    0.9

    A longer context has more to learn, so it takes longer to get going:

    >>> accuracy("fdfdfdfdfd", 2)
    0.8
    >>> accuracy("ffddffddff", 2)
    0.8
    >>> accuracy("ffddffddff", 4)
    0.6

    Nothing to predict, nothing to score:

    >>> accuracy("", 3)
    0.0
    """
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
    """Return {k: accuracy} for each k, so the values can be compared.

    >>> sweep("fdfdfdfdfd", [1, 2, 3])
    {1: 0.9, 2: 0.8, 3: 0.8}
    """
    dict = {}
    for i in ks:
        dict[i] = accuracy(history, i)
    return dict


if __name__ == "__main__":
    # Replay the sample session that ships with the exercise. Swap in your own
    # by using E08's load_histories("your_id") instead.
    history = (DATA / "history_sample.txt").read_text().strip()
    print(f"{len(history)} keypresses")
    for k, score in sweep(history).items():
        print(f"  n = {k + 1:2d}  (k = {k})   {score:.1%}")


# ANSWER: (the QUESTION is at the top of this file)
