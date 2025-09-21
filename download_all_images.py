import os
from animals import ANIMALS
from image_fetcher import _fetch_wikipedia_thumbnail, _safe_filename

PRELOAD_DIR = os.path.join(os.path.dirname(__file__), "preloaded_images")
os.makedirs(PRELOAD_DIR, exist_ok=True)

def download_all_animal_images():
    for animal in ANIMALS:
        fname = _safe_filename(animal)
        fpath = os.path.join(PRELOAD_DIR, fname)
        if os.path.exists(fpath):
            print(f"Already downloaded: {animal}")
            continue
        img = _fetch_wikipedia_thumbnail(animal)
        if img:
            img.save(fpath, format="PNG")
            print(f"Downloaded: {animal}")
        else:
            print(f"Failed to download: {animal}")

if __name__ == "__main__":
    download_all_animal_images()
