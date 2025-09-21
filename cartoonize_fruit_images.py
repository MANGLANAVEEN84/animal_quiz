from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os

src_dir = "fruit_photos"
dst_dir = "fruit_photos_cartoon"
os.makedirs(dst_dir, exist_ok=True)

for fname in os.listdir(src_dir):
    if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(src_dir, fname)
        img = Image.open(img_path).convert("RGB")
        # Edge enhancement for cartoon effect
        edge = img.filter(ImageFilter.FIND_EDGES)
        edge = ImageOps.invert(edge)
        edge = edge.convert("L").point(lambda x: 0 if x < 180 else 255, '1')
        # Posterize for flat color effect
        img_poster = ImageOps.posterize(img, 3)
        # Blend edge and posterized image
        img_cartoon = Image.composite(img_poster, Image.new("RGB", img.size, (255,255,255)), edge)
        # Slightly boost color
        enhancer = ImageEnhance.Color(img_cartoon)
        img_cartoon = enhancer.enhance(1.5)
        # Save cartoonized image
        img_cartoon.save(os.path.join(dst_dir, fname))
        print(f"Cartoonized {fname}")
print("All fruit images cartoonized.")
