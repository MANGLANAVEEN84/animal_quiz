import os
from typing import Tuple

from PIL import Image

# Local imports
from animals import ANIMALS, normalize_name
import image_fetcher as fetcher

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
IMG_SIZE: Tuple[int, int] = (320, 240)


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def main() -> None:
    ensure_dir(ASSETS_DIR)
    print(f"Generating assets into: {ASSETS_DIR}")

    count = 0
    for name in ANIMALS:
        fname = f"{normalize_name(name)}.png"
        fpath = os.path.join(ASSETS_DIR, fname)

        # Generate a clean placeholder using fetcher's internal generator and fitter
        # We avoid network here explicitly.
        img = fetcher._generate_placeholder(name, IMG_SIZE)  # type: ignore[attr-defined]
        img = fetcher._fit_image(img, IMG_SIZE)  # type: ignore[attr-defined]
        img.save(fpath, format="PNG")
        count += 1
        print(f"  - Wrote {fname}")

    print(f"Done. Generated {count} images.")
    print("You can now run the app; local assets will be used first.")


if __name__ == "__main__":
    main()
