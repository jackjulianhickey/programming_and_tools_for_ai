"""Extension. Sorting the photos from darkest to brightest. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E07_brightness.py

No output means every test passed. Then run the file itself, which needs
the photos:

    python prep_data.py
    python E07_brightness.py

A photo's brightness is just the mean of all its numbers, across height,
width and all three colour channels at once. Sorting by it introduces the
other half of argsort: it hands you the *order*, and you then use that order
to index something else. Indexing one array with an array of positions is
called fancy indexing, and it is how a sorted list of names is built here.
"""
import numpy as np

from E01_photos import DATA, load


def brightness(image):
    """The mean of every number in the image, as an ordinary float.

    >>> image = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    >>> brightness(image)
    127.5
    >>> brightness(np.zeros((4, 4, 3), dtype=np.uint8))
    0.0
    """
    return float(image.mean())


def darkest_first(names, values):
    """Return the names as an array, reordered from smallest value to largest.

    np.argsort(values) gives the positions in sorted order; use that array to
    index the names.

    >>> darkest_first(["a", "b", "c"], [5.0, 1.0, 3.0])
    array(['b', 'c', 'a'], dtype='<U1')
    >>> darkest_first(["a", "b", "c"], [1.0, 2.0, 3.0])
    array(['a', 'b', 'c'], dtype='<U1')
    """
    return np.array(names)[np.argsort(values)]


def main():
    paths = sorted((DATA / "photos").glob("*full.png"))
    if not paths:
        print("No photos yet. Run:  python prep_data.py")
        return
    values = [brightness(load(p)) for p in paths]
    order = darkest_first([p.stem for p in paths], values)
    if order is None:
        print("write brightness and darkest_first first")
        return
    print("darkest: ", order[:3])
    print("brightest:", order[-3:])


if __name__ == "__main__":
    main()
