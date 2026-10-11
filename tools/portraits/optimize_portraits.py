#!/usr/bin/env python3
"""Rebuild the lightweight deployable WebP portrait set from reviewed sources."""
from pathlib import Path
import sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from portrait_framing import frame_for_circle
SOURCE = ROOT / "assets/portraits/source"
APPROVED_GENERATED = ROOT / "assets/portraits/approved-generated"
OUTPUT = ROOT / "public/assets/portraits"
ORIGINALS = ("goku", "vegeta", "naruto", "sasuke", "luffy", "gojo", "light", "saitama")
GENERATED = sorted({path.stem for directory in (SOURCE, APPROVED_GENERATED)
                    for path in directory.glob("*.webp")})
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
    approved_source = APPROVED_GENERATED / f"{name}.webp"
    source = approved_source if approved_source.exists() else SOURCE / f"{name}.webp"
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        framed = frame_for_circle(rgba, name, 768)
        if framed is not None:
            portrait = framed
        elif name in ORIGINALS and not approved_source.exists():
            portrait = rgba.resize((768, 896), Image.Resampling.LANCZOS)
        else:
            if name in UPPER_BODY_CROP and not approved_source.exists():
                rgba = rgba.crop((0, 0, rgba.width, round(rgba.height * UPPER_BODY_CROP[name])))
            artwork = ImageOps.contain(rgba, (768, 896), Image.Resampling.LANCZOS)
            portrait = Image.new("RGBA", (768, 896))
            portrait.alpha_composite(artwork, ((768 - artwork.width) // 2, (896 - artwork.height) // 2))
        destination = OUTPUT / f"{name}.webp"
        temporary = OUTPUT / f".{name}.webp.tmp"
        portrait.save(temporary, "WEBP", quality=86, method=4)
        temporary.replace(destination)
print(f"optimized {len(GENERATED)} generated portraits to {OUTPUT}")
