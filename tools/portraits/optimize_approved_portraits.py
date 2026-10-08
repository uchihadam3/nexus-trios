#!/usr/bin/env python3
"""Prepare the seven portraits selected from the numbered review gallery."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/portraits/approved-sources"
OUTPUT = ROOT / "public/assets/portraits"
SIZE = (768, 896)

# Keep the source files untouched. These crops frame faces and action in cards.
PORTRAITS = {
    "wolverine": ("jpg", (0, 0, 740, 675)),
    "batman": ("png", None),
    "scarletwitch": ("jpg", None),
    "vision": ("jpg", None),
    "antman": ("jpg", None),
    "carnage": ("jpg", None),
    "cyborg": ("jpg", (330, 0, 1590, 1080)),
}

for name, (extension, crop) in PORTRAITS.items():
    with Image.open(SOURCE / f"{name}.{extension}") as original:
        image = original.convert("RGBA")
        if crop:
            image = image.crop(crop)
        artwork = ImageOps.contain(image, SIZE, Image.Resampling.LANCZOS)
        # Transparent Batman retains the game's own portrait background.
        color = (0, 0, 0, 0) if name == "batman" else (31, 38, 55, 255)
        portrait = Image.new("RGBA", SIZE, color)
        portrait.alpha_composite(artwork, ((SIZE[0] - artwork.width) // 2, max(0, (SIZE[1] - artwork.height) // 3)))
        portrait.save(OUTPUT / f"{name}.webp", "WEBP", quality=88, method=5)

print(f"Prepared {len(PORTRAITS)} approved portraits.")
