
import requests
import os
from PIL import Image
from io import BytesIO

# Fruit names for A-Z
fruits = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew", "Indian Fig", "Jackfruit", "Kiwi", "Lemon", "Mango", "Nectarine", "Orange", "Papaya", "Quince", "Raspberry", "Strawberry", "Tomato", "Ugli Fruit", "Vanilla", "Watermelon", "Xigua", "Yellow Passion Fruit", "Zucchini"
]
letters = [chr(ord('A') + i) for i in range(26)]

os.makedirs("fruit_photos", exist_ok=True)

UNSPLASH_ACCESS_KEY = "iaK-BURCNGS9vFqcT8zzKxXDbdTnWbKCKGlkllAJMe4"
headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}

for letter, fruit in zip(letters, fruits):
    query = f"{fruit} fruit"
    url = f"https://api.unsplash.com/search/photos?query={query}&orientation=squarish&per_page=1"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data['results']:
            img_url = data['results'][0]['urls']['regular']
            img_resp = requests.get(img_url, timeout=10)
            img = Image.open(BytesIO(img_resp.content)).convert("RGB")
            img.save(f"fruit_photos/{letter}.jpg")
            print(f"Downloaded Unsplash image for {fruit} ({letter})")
        else:
            print(f"No Unsplash image found for {fruit} ({letter})")
    except Exception as e:
        print(f"Failed to download Unsplash image for {fruit} ({letter}): {e}")
print("All Unsplash fruit images attempted.")
