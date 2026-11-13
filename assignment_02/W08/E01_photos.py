"""When are two images similar? The lecture program, complete and working.

Run it, run its doctests, read it. Nothing here is left for you to write.

    python prep_data.py          # once, to fetch the photos
    python E01_photos.py         # find each photo's nearest neighbours
    python -m doctest E01_photos.py

The doctests below run on small hand-made arrays, so they work whether or
not the photos have been downloaded.
"""
from collections import Counter
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

DATA = Path(__file__).parent / "data"

B = 4              # bins per colour channel, so B ** 3 bins in total
WIDTH = 256 // B   # 64: bin i covers the values i * 64 up to (i + 1) * 64


def load(path):
    """Read a photo as a (height, width, 3) array of uint8, 0 to 255.

    plt.imread gives floats between 0 and 1, and a fourth "alpha"
    (transparency) channel if the file has one. We want neither: whole
    numbers 0-255 are what we think of as colour values, and we discard
    alpha because transparency is not part of what an image looks like.
    """
    rgb = plt.imread(path)[:, :, :3]              # drop alpha if present
    return np.round(rgb * 255).astype(np.uint8)   # 0.0-1.0 becomes 0-255


def histogram_python(image):
    """Count the pixels falling in each colour bin, in pure Python.

    This is the definition. A pixel with red 200, green 10, blue 70 goes
    into bin (3, 0, 1), because 200 // 64 is 3, 10 // 64 is 0, 70 // 64 is 1.

    image.reshape(-1, 3) forgets the height and width and leaves a plain
    list of pixels, which is all the count cares about.

    >>> image = np.array([[[200, 10, 70], [0, 0, 0]],
    ...                   [[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    >>> counts = histogram_python(image)
    >>> counts.shape
    (4, 4, 4)
    >>> print(counts[3, 0, 1])     # the one reddish pixel
    1
    >>> print(counts[0, 0, 0])     # the two black pixels
    2
    >>> print(counts[3, 3, 3])     # the one white pixel
    1
    >>> print(counts.sum())        # every pixel landed somewhere
    4
    """
    counts = Counter()
    for red, green, blue in image.reshape(-1, 3):
        counts[red // WIDTH, green // WIDTH, blue // WIDTH] += 1
    return np.array([[[counts[r, g, b] for b in range(B)]
                      for g in range(B)] for r in range(B)])


def histogram_numpy(image):
    """The same counts, one bin at a time, using Numpy.

    The loop runs over the 64 bins, not over the million pixels. Numpy
    handles the pixels inside each comparison: `binned[:, :, 0] == r` is a
    whole-image map of True and False, and summing a boolean array counts
    the Trues.

    >>> image = np.array([[[200, 10, 70], [0, 0, 0]],
    ...                   [[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    >>> np.array_equal(histogram_numpy(image), histogram_python(image))
    True
    """
    binned = image // WIDTH          # every value is now 0, 1, 2 or 3
    counts = np.zeros((B, B, B), dtype=int)
    for r in range(B):
        for g in range(B):
            for b in range(B):
                is_r = binned[:, :, 0] == r
                is_g = binned[:, :, 1] == g
                is_b = binned[:, :, 2] == b
                counts[r, g, b] = np.sum(is_r & is_g & is_b)
    return counts


def build_matrix(paths):
    """One row per photo, one column per colour bin.

    Each photo's (4, 4, 4) counts are reshaped into a row of 64 numbers,
    because from here on we care about comparing photos, not about which
    bin sat next to which.
    """
    rows = [histogram_numpy(load(p)).reshape(B ** 3) for p in paths]
    return np.array(rows, dtype=float)


def as_proportions(X):
    """Divide each row by its own total, so photos of any size compare.

    A thumbnail has one sixty-fourth of the pixels of the original, so its
    raw counts are tiny. What we actually want to compare is the *mix* of
    colours, not how many pixels there were.

    X.sum(axis=1) adds up each row, giving shape (n,). Reshaping that to
    (n, 1) makes it a column, and broadcasting then divides each row by its
    own number.

    >>> X = np.array([[1.0, 3.0], [10.0, 30.0]])
    >>> as_proportions(X)
    array([[0.25, 0.75],
           [0.25, 0.75]])
    """
    return X / X.sum(axis=1).reshape(-1, 1)


def distances_to(X, x):
    """Euclidean distance from the row x to every row of X.

    X - x subtracts one row of d numbers from all n rows at once: that is
    broadcasting. np.linalg.norm with axis=1 then collapses each row of
    differences down to a single distance.

    >>> X = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
    >>> distances_to(X, X[0])
    array([ 0.,  5., 10.])
    >>> distances_to(X, X[1])
    array([5., 0., 5.])
    """
    return np.linalg.norm(X - x, axis=1)


def most_similar(X, i, k=3):
    """Indices of the k rows closest to row i, nearest first.

    >>> X = np.array([[0.0, 0.0], [1.0, 0.0], [5.0, 0.0], [6.0, 0.0]])
    >>> most_similar(X, 0, 2)
    array([1, 2])
    >>> most_similar(X, 3, 2)
    array([2, 1])
    """
    d = distances_to(X, X[i])
    d[i] = np.inf                # a photo is not its own nearest neighbour
    return np.argsort(d)[:k]


def main():
    paths = sorted((DATA / "photos").glob("*.png"))
    if not paths:
        print("No photos yet. Run:  python prep_data.py")
        return
    names = np.array([p.stem for p in paths])

    image = load(paths[0])
    print(f"{paths[0].name}: shape {image.shape}, dtype {image.dtype}")
    for histogram in (histogram_python, histogram_numpy):
        start = perf_counter()
        histogram(image)
        print(f"{histogram.__name__:20s} {(perf_counter() - start) * 1000:8.1f} ms")

    X = build_matrix(paths)
    print(f"\n{X.shape[0]} photos, {X.shape[1]} colour bins")

    query = int(np.flatnonzero(names == "kodim01_thumb")[0])
    print(f"\nnearest neighbours of {names[query]}")
    print("  raw counts: ", names[most_similar(X, query)])
    print("  proportions:", names[most_similar(as_proportions(X), query)])


if __name__ == "__main__":
    main()
