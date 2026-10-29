"""Extension. Turning a colour photo into a grey one, with `@`. SOLUTION.

Run the tests:

    python -m doctest W08_Solutions/E08_grayscale.py

No output means every test passed. Then run the file itself, which needs
the photos:

    python prep_data.py
    python E08_grayscale.py

A grey pixel is a weighted average of the red, green and blue values of the
colour pixel. The eye is far more sensitive to green than to blue, so the
weights are not equal; the standard ones are given below and add to 1.

Written out for a single pixel, grey = 0.2126r + 0.7152g + 0.0722b. That is
a dot product, and `@` is Python's operator for it. Applied to the whole
(height, width, 3) image at once, `image @ WEIGHTS` takes the dot product
along the last axis and hands back a (height, width) array. The same
operator multiplies two matrices when both sides are 2-D.

Your solution should be one line of Numpy, with no loop.
"""
import matplotlib.pyplot as plt
import numpy as np

from E01_photos import DATA, load

# Given: the standard luminance weights, red, green, blue.
WEIGHTS = np.array([0.2126, 0.7152, 0.0722])


def to_gray(image):
    """Collapse the three colour channels into one grey value per pixel.

    The result has one axis fewer than the image, and is float, not uint8.

    >>> image = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    >>> to_gray(image)
    array([[  0., 255.]])
    >>> to_gray(image).shape
    (1, 2)
    >>> red = np.array([[[255, 0, 0]]], dtype=np.uint8)
    >>> round(float(to_gray(red)[0, 0]), 2)
    54.21
    >>> green = np.array([[[0, 255, 0]]], dtype=np.uint8)
    >>> round(float(to_gray(green)[0, 0]), 2)
    182.38
    """
    return image @ WEIGHTS


# Given: the picture. cmap="gray" tells imshow to read the single number per
# pixel as a shade of grey rather than as a position on a colour scale.
def plot_gray(gray, filename="gray.png"):
    """Draw a grey image and save it to a file."""
    plt.figure()
    plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print("wrote", filename)


def main():
    paths = sorted((DATA / "photos").glob("*full.png"))
    if not paths:
        print("No photos yet. Run:  python prep_data.py")
        return
    image = load(paths[0])
    gray = to_gray(image)
    if gray is None:
        print("write to_gray first")
        return
    print(f"colour {image.shape} {image.dtype}  ->  grey {gray.shape} {gray.dtype}")
    plot_gray(gray)


if __name__ == "__main__":
    main()
