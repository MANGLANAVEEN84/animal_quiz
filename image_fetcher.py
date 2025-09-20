import io
import os
import random
import textwrap
from typing import Optional

import requests
from PIL import Image, ImageDraw, ImageFont

from animals import normalize_name

# Simple cache directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

USER_AGENT = "AnimalQuiz/1.0 (Educational app; contact: example@example.com)"
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"


def _safe_filename(name: str) -> str:
    return f"{normalize_name(name)}.png"


def _download_image(url: str) -> Optional[Image.Image]:
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception:
        return None


def _fetch_wikipedia_thumbnail(animal_name: str) -> Optional[Image.Image]:
    # Use Wikipedia summary endpoint which often includes a thumbnail
    title = animal_name.replace(" ", "%20")
    try:
        resp = requests.get(WIKI_SUMMARY_URL.format(title), headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        thumb = data.get("thumbnail", {})
        source = thumb.get("source")
        if source:
            img = _download_image(source)
            return img
    except Exception:
        return None
    return None


def _random_bg_color() -> tuple[int, int, int]:
    palette = [
        (66, 165, 245),  # blue
        (102, 187, 106),  # green
        (255, 202, 40),   # amber
        (239, 83, 80),    # red
        (171, 71, 188),   # purple
    ]
    return random.choice(palette)


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    # Try common fonts, fall back to default
    candidates = [
        "arial.ttf",  # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "/Library/Fonts/Arial.ttf",  # macOS
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _generate_placeholder(animal_name: str, size: tuple[int, int] = (320, 240)) -> Image.Image:
    img = Image.new("RGB", size, _random_bg_color())
    draw = ImageDraw.Draw(img)

    # Big letter
    letter = animal_name[0].upper()
    big_font = _load_font(int(size[1] * 0.6))
    w, h = draw.textbbox((0, 0), letter, font=big_font)[2:]
    draw.text(((size[0]-w)//2, int(size[1]*0.05)), letter, fill=(255, 255, 255), font=big_font)

    # Name wrapped at bottom
    small_font = _load_font(24)
    wrapped = textwrap.fill(animal_name, width=12)
    text_w, text_h = draw.multiline_textbbox((0, 0), wrapped, font=small_font, align="center")[2:]
    draw.multiline_text(((size[0]-text_w)//2, size[1]-text_h-10), wrapped, fill=(255, 255, 255), font=small_font, align="center")
    return img


def get_animal_image(animal_name: str, size: tuple[int, int] = (320, 240)) -> Image.Image:
    """
    Returns a PIL.Image for the given animal name.
    Order of attempts:
    - If cached, load from disk.
    - Try Wikipedia summary thumbnail.
    - Fallback to generated placeholder.

    Result is cached to disk as PNG.
    """
    fname = _safe_filename(animal_name)
    fpath = os.path.join(CACHE_DIR, fname)

    # Load from cache
    if os.path.exists(fpath):
        try:
            img = Image.open(fpath).convert("RGB")
            return img
        except Exception:
            pass

    # Try fetch
    img = _fetch_wikipedia_thumbnail(animal_name)
    if img is None:
        img = _generate_placeholder(animal_name, size)

    # Resize to consistent size while keeping aspect ratio and padding
    img = _fit_image(img, size)

    # Save to cache
    try:
        img.save(fpath, format="PNG")
    except Exception:
        pass
    return img


def _fit_image(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    img = img.copy()
    img.thumbnail((target_w, target_h), Image.LANCZOS)
    canvas = Image.new("RGB", size, (240, 240, 240))
    x = (target_w - img.width) // 2
    y = (target_h - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas
