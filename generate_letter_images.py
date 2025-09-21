from PIL import Image, ImageDraw, ImageFont
import os

# List of fruits for each letter (A-Z)
fruits = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew", "Indian Fig", "Jackfruit", "Kiwi", "Lemon", "Mango", "Nectarine", "Orange", "Papaya", "Quince", "Raspberry", "Strawberry", "Tomato", "Ugli Fruit", "Vanilla", "Watermelon", "Xigua", "Yellow Passion Fruit", "Zucchini"
]

letters = [chr(ord('A') + i) for i in range(26)]

os.makedirs("letterimage", exist_ok=True)

import random
def random_color():
    return tuple(random.randint(100, 255) for _ in range(3))

for letter, fruit in zip(letters, fruits):
    cartoon_path = f"fruit_photos_cartoon/{letter}.jpg"
    if not os.path.exists(cartoon_path):
        print(f"Cartoon image for {letter} not found, skipping.")
        continue
    img = Image.open(cartoon_path).convert('RGB').resize((400, 400))
    draw = ImageDraw.Draw(img)
    # Try to use a bold, large font
    try:
        font = ImageFont.truetype("arial.ttf", 200)
        fruit_font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        fruit_font = ImageFont.load_default()
    # Draw the letter in white with a black outline for contrast
    bbox = draw.textbbox((0, 0), letter, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (400-w)//2
    y = 100
    # Outline
    for dx in [-3,0,3]:
        for dy in [-3,0,3]:
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), letter, font=font, fill=(0,0,0))
    draw.text((x, y), letter, font=font, fill=(255,255,255))
    # Draw the fruit name below in a contrasting color
    bbox_fruit = draw.textbbox((0, 0), fruit, font=fruit_font)
    fw, fh = bbox_fruit[2] - bbox_fruit[0], bbox_fruit[3] - bbox_fruit[1]
    draw.text(((400-fw)/2, 330), fruit, font=fruit_font, fill=(0, 80, 0))
    img.save(f"letterimage/{letter}.png")
print("All letter images generated in 'letterimage/' folder.")
