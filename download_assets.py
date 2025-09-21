import os
import time
from typing import Tuple

from PIL import Image

from animals import ANIMALS, normalize_name
import image_fetcher as fetcher

ASSETS_DIR = fetcher.ASSETS_DIR  # use the same directory as the app
IMG_SIZE: Tuple[int, int] = (320, 240)


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def save_image(img: Image.Image, path: str) -> None:
    tmp = path + ".tmp"
    img.save(tmp, format="PNG")
    os.replace(tmp, path)


def main() -> None:
    ensure_dir(ASSETS_DIR)
    print(f"Building local assets library in: {ASSETS_DIR}")

    total = len(ANIMALS)
    ok = 0
    for i, name in enumerate(ANIMALS, start=1):
        fname = f"{normalize_name(name)}.png"
        fpath = os.path.join(ASSETS_DIR, fname)

        # Try to fetch from Wikipedia; fall back to placeholder
        img = fetcher._fetch_wikipedia_thumbnail(name)  # type: ignore[attr-defined]
        if img is None:
            img = fetcher._generate_placeholder(name, IMG_SIZE)  # type: ignore[attr-defined]
        img = fetcher._fit_image(img, IMG_SIZE)  # type: ignore[attr-defined]

        try:
            save_image(img, fpath)
            ok += 1
            print(f"[{i}/{total}] Saved {fname}")
        except Exception as e:
            print(f"[{i}/{total}] Failed {fname}: {e}")
        # Be nice to Wikipedia; short pause
        time.sleep(0.2)

    print(f"Done. Saved {ok}/{total} images to {ASSETS_DIR}.")
    print("Run the app; it will prefer local assets first.")


if __name__ == "__main__":
    main()
