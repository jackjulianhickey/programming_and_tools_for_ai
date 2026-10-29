"""Extension. Every pair of photos at once, drawn as a heatmap. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E06_heatmap.py

No output means every test passed. Then run the file itself to write
distances.png, which needs the photos:

    python prep_data.py
    python E06_heatmap.py

The lecture compared one photo against all the others. Here we want all
against all: an n by n table whose entry (i, j) is the distance from photo i
to photo j. Writing that yourself would mean a loop inside a loop, so we
meet the built-in instead. scipy.spatial.distance.cdist takes two matrices
of rows and returns the distance from every row of the first to every row of
the second, and cdist(X, X) is the table we want.

QUESTION: in the picture, the diagonal running from the top left to the
bottom right is a different colour from everything around it. Why?
Answer in the comment at the bottom.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

from E01_photos import DATA, as_proportions, build_matrix


def distance_matrix(X):
    """Euclidean distance between every pair of rows of X.

    The result is square, symmetric, and zero down the diagonal.

    >>> X = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
    >>> distance_matrix(X)
    array([[ 0.,  5., 10.],
           [ 5.,  0.,  5.],
           [10.,  5.,  0.]])
    >>> distance_matrix(np.array([[1.0], [4.0]]))
    array([[0., 3.],
           [3., 0.]])
    """
    return cdist(X, X)


# Given: the picture. imshow draws a 2-D array as an image, one pixel per
# entry, with the values mapped onto a colour scale.
def plot_heatmap(D, names, filename="distances.png"):
    """Draw the distance matrix and save it to a file."""
    plt.figure(figsize=(9, 8))
    plt.imshow(D)
    plt.colorbar(label="distance")
    plt.xticks(range(len(names)), names, rotation=90, fontsize=4)
    plt.yticks(range(len(names)), names, fontsize=4)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    print("wrote", filename)


def main():
    paths = sorted((DATA / "photos").glob("*.png"))
    if not paths:
        print("No photos yet. Run:  python prep_data.py")
        return
    X = as_proportions(build_matrix(paths))
    D = distance_matrix(X)
    if D is None:
        print("write distance_matrix first")
        return
    print("shape", D.shape)
    plot_heatmap(D, [p.stem for p in paths])


if __name__ == "__main__":
    main()


# ANSWER:
# Every photo is at distance zero from itself, so the diagonal is all zeros,
# and zero is smaller than any other entry. It therefore sits at the very end
# of the colour scale, and the whole diagonal takes that one extreme colour.
# You can also see faint three-by-three blocks along it: the full, half and
# thumbnail versions of one photo, which are nearly but not exactly identical.
