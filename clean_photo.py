import cv2
import numpy as np
from PIL import Image

SRC = "work/photo.jpg"
OUT = "work/photo-ready.png"

# Load
img = cv2.imread(SRC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# CLAHE - pulls real detail out of flat lighting
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
img = clahe.apply(img)

# Push the flat wall background toward pure white so it reads as
# empty space rather than faint dots. Background here is the
# corners/edges of the frame - sample them to find the wall tone,
# then stretch levels so that tone -> 255.
h, w = img.shape
corner_samples = np.concatenate([
    img[0:40, 0:40].flatten(),
    img[0:40, w-40:w].flatten(),
])
bg_level = int(np.median(corner_samples))

# Levels stretch: map bg_level -> 250, keep black point similar
img = img.astype(np.float32)
img = (img - 0) * (255.0 / max(bg_level, 1))
img = np.clip(img, 0, 255).astype(np.uint8)

# Mild denoise so grain doesn't turn into stray glyphs
img = cv2.bilateralFilter(img, d=5, sigmaColor=40, sigmaSpace=40)

Image.fromarray(img).save(OUT)
print("wrote", OUT, img.shape, "bg_level", bg_level)
