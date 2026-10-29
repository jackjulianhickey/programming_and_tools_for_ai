"""Drill. One function, a scalar or a whole array. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E02_vectorise.py

No output means every test passed.

You do not have to do anything special to make a function work on an array.
Write it for a number, and if the only operations inside are arithmetic, it
works on an array too, element by element. That is vectorisation, and it is
why Numpy code so often has no loop in it.

Run the file (not the doctests) to write softplus.png and look at the curve.
"""
import matplotlib.pyplot as plt
import numpy as np


def softplus(x):
    """Return log(1 + exp(x)), using np.log and np.exp.

    A robot's motor takes a control signal in [0, infinity), but the neural
    network driving it outputs anything in (-infinity, infinity). We need to
    remap. Clipping at zero would do it, but it throws away every negative
    value and has a corner at 0, which makes it awkward to train through.
    softplus is the smooth version: always positive, and for large x it is
    almost exactly x, so a big command passes through nearly unchanged.

    >>> round(float(softplus(0)), 4)
    0.6931
    >>> round(float(softplus(3)), 4)
    3.0486
    >>> round(float(softplus(-3)), 4)
    0.0486

    The same function, one call, on a whole array of signals:

    >>> np.round(softplus(np.array([-2.0, 0.0, 2.0, 5.0])), 3)
    array([0.127, 0.693, 2.127, 5.007])
    """
    return np.log(1 + np.exp(x))


# Given: the plot. Notice that it never loops: linspace makes 200 x values,
# softplus turns all 200 into y values at once, and plt.plot draws the pairs.
def plot(filename="softplus.png"):
    """Draw softplus over -5 to 5 and save it to a file."""
    x = np.linspace(-5, 5, 200)
    y = softplus(x)
    if y is None:
        print("write softplus first")
        return
    plt.figure()
    plt.plot(x, y)
    plt.axhline(0, color="grey", linewidth=0.5)
    plt.xlabel("x")
    plt.ylabel("softplus(x)")
    plt.savefig(filename)
    print("wrote", filename)


if __name__ == "__main__":
    plot()
