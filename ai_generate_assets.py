import io
import os
import time
import urllib.parse
from typing import Tuple

import requests
from PIL import Image

from animals import ANIMALS, normalize_name
import image_fetcher as fetcher

ASSETS_DIR = fetcher.ASSETS_DIR
IMG_SIZE: Tuple[int, int] = (320, 240)
USER_AGENT = "AnimalQuiz/1.0 (+educational; contact: example@example.com)"

# Pollinations provides a free no-auth image generation endpoint.
# Docs: https://pollinations.ai/ (community service; subject to change/limits)
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{}"


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_prompt(animal: str) -> str:
    return (
        f"Kid-friendly high-quality photo of a single {animal} on a plain light background, "
        f"centered, no text, natural colors, 4k, studio lighting"
    )


def download_pollinations(prompt: str, timeout: int = 40) -> Image.Image | None:
    url = POLLINATIONS_URL.format(urllib.parse.quote(prompt))
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        return img
    except Exception:
        return None


def save_png(img: Image.Image, path: str) -> None:
    tmp = path + ".tmp"
    img.save(tmp, format="PNG")
    os.replace(tmp, path)


def main() -> None:
    ensure_dir(ASSETS_DIR)
    print(f"Generating AI images into: {ASSETS_DIR}")

    total = len(ANIMALS)
    success = 0
    for i, animal in enumerate(ANIMALS, start=1):
        fname = f"{normalize_name(animal)}.png"
        fpath = os.path.join(ASSETS_DIR, fname)

        if os.path.exists(fpath):
            print(f"[{i}/{total}] Skip (exists): {fname}")
            continue

        prompt = build_prompt(animal)
        print(f"[{i}/{total}] Generating: {animal} ...")

        # Try up to 2 attempts (API can be flaky)
        img = download_pollinations(prompt)
        if img is None:
            time.sleep(2)
            img = download_pollinations(prompt)

        # Fallback to placeholder if generation fails
        if img is None:
            img = fetcher._generate_placeholder(animal, IMG_SIZE)  # type: ignore[attr-defined]

        img = fetcher._fit_image(img, IMG_SIZE)  # type: ignore[attr-defined]
        save_png(img, fpath)
        success += 1
        print(f"    Saved: {fname}")

        # Be polite; slight delay to avoid hammering the service
        time.sleep(0.5)

    print(f"Done. Created {success}/{total} images.")
    print("Now run the app; it will use assets/ first.")


if __name__ == "__main__":
    main()
