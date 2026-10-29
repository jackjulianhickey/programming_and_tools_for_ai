"""Download the Kodak True Color suite and build the photo folder.

Not an exercise. Run once; the images are cached in data/photos/.
Each source photo is saved at three sizes, so we know in advance which
pairs *ought* to come out as most similar.

    python prep_data.py
"""
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image

DATA = Path(__file__).parent / "data"
ORIGINALS = DATA / "originals"
PHOTOS = DATA / "photos"
URL = "https://r0k.us/graphics/kodak/kodak/kodim{:02d}.png"
N_PHOTOS = 24
SIZES = [("full", 1.0), ("half", 0.5), ("thumb", 0.125)]


def download(n_photos=N_PHOTOS):
    """Fetch the Kodak images, skipping any we already have."""
    ORIGINALS.mkdir(parents=True, exist_ok=True)
    for i in range(1, n_photos + 1):
        path = ORIGINALS / f"kodim{i:02d}.png"
        if not path.exists():
            print("downloading", path.name)
            urlretrieve(URL.format(i), path)


def make_sizes():
    """Save each original at every size in SIZES, as RGB PNG."""
    PHOTOS.mkdir(parents=True, exist_ok=True)
    for path in sorted(ORIGINALS.glob("*.png")):
        image = Image.open(path).convert("RGB")  # drops alpha, forces 3 channels
        width, height = image.size
        for name, frac in SIZES:
            resized = image.resize((int(width * frac), int(height * frac)),
                                   Image.Resampling.LANCZOS)
            resized.save(PHOTOS / f"{path.stem}_{name}.png")


if __name__ == "__main__":
    download()
    make_sizes()
    print(len(list(PHOTOS.glob("*.png"))), "photos in", PHOTOS)
