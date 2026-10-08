#!/usr/bin/env python3
"""Rebuild the lightweight deployable WebP portrait set from reviewed sources."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/portraits/source"
OUTPUT = ROOT / "public/assets/portraits"
ORIGINALS = ("goku", "vegeta", "naruto", "sasuke", "luffy", "gojo", "light", "saitama")
GENERATED = sorted(path.stem for path in SOURCE.glob("*.webp"))
# Tall full-figure illustrations are framed at the waist for the small game cards.
# Keep the untouched source so each crop can be revised independently.
UPPER_BODY_CROP = {
    "alphonse": .78,
    "edward": .78,
    "eren": .82,
    "ghostrider": .72,
    "gon": .77,
    "kaiba": .76,
    "loid": .73,
    "punisher": .68,
    "yor": .76,
}

for name in GENERATED:
    source = SOURCE / f"{name}.webp"
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        if name in ORIGINALS:
            portrait = rgba.resize((768, 896), Image.Resampling.LANCZOS)
        else:
            if name in UPPER_BODY_CROP:
                rgba = rgba.crop((0, 0, rgba.width, round(rgba.height * UPPER_BODY_CROP[name])))
            artwork = ImageOps.contain(rgba, (768, 896), Image.Resampling.LANCZOS)
            portrait = Image.new("RGBA", (768, 896))
            portrait.alpha_composite(artwork, ((768 - artwork.width) // 2, (896 - artwork.height) // 2))
        destination = OUTPUT / f"{name}.webp"
        temporary = OUTPUT / f".{name}.webp.tmp"
        portrait.save(temporary, "WEBP", quality=86, method=4)
        temporary.replace(destination)
print(f"optimized {len(GENERATED)} generated portraits to {OUTPUT}")
