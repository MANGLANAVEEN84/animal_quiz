# Animal Alphabet Photo Quiz (Python)

A simple Tkinter-based quiz for kids that shows a question like "Identify the animal: Cow" and three pictures (e.g., Cat, Horse, Cow). When the user clicks an image, the app displays whether the answer is correct or incorrect. Images are fetched from free Wikipedia/Wikimedia thumbnails when available and cached locally; if offline or not available, the app generates a placeholder image with the animal name.

## Features
- Three-image multiple choice quiz per question.
- Immediate feedback: Correct / Incorrect.
- Next Question button to continue practice.
- Free-to-use images via Wikipedia/Wikimedia thumbnails when available.
- Offline-friendly: automatic placeholder image generation.
- Local cache to speed up subsequent runs in `animal_quiz/cache/`.

## Requirements
- Python 3.10+
- Windows, macOS, or Linux

## Install
```bash
cd animal_quiz
python -m venv .venv
# Windows PowerShell
. .venv\\Scripts\\Activate.ps1
# Or cmd
.venv\\Scripts\\activate.bat

pip install -r requirements.txt
```

## Run
```bash
python quiz.py
```

## Project Structure
```
animal_quiz/
  animals.py         # Animal list and question generator
  image_fetcher.py   # Fetches images from Wikipedia; generates placeholders if needed
  quiz.py            # Tkinter GUI app
  requirements.txt   # Dependencies: requests, Pillow
  cache/             # Auto-created; stores downloaded/resized images
```

## Notes on Images and Licensing
- The app uses Wikipedia's REST summary endpoint to obtain small thumbnails when available.
- Thumbnails returned are typically from Wikimedia Commons and are free to use under their respective licenses, but always verify the specific license if you distribute content.
- The app caches processed images locally for performance and offline use.

## Troubleshooting
- If fonts on placeholders look odd, install common fonts (e.g., Arial) or adjust `_load_font` in `image_fetcher.py`.
- If you see connection errors, the app will still work using placeholder images.
- To clear the cache, delete the `animal_quiz/cache/` folder; it will be recreated automatically.

## Customization
- Add or remove animals in `animals.py` (`ANIMALS` list).
- Change image size via `IMG_SIZE` in `quiz.py`.
- Modify colors or fonts in `image_fetcher.py`.
