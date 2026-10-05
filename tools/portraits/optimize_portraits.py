#!/usr/bin/env python3
"""Rebuild the lightweight deployable WebP portrait set from original alpha PNGs."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/portraits/source"
OUTPUT = ROOT / "public/assets/portraits"
GENERATED = ("goku", "vegeta", "naruto", "sasuke", "luffy", "gojo", "light", "saitama")

for name in GENERATED:
    with Image.open(SOURCE / f"{name}.webp") as image:
        image.convert("RGBA").resize((768, 896), Image.Resampling.LANCZOS).save(
            OUTPUT / f"{name}.webp", "WEBP", quality=86, method=4
        )
print(f"optimized {len(GENERATED)} generated portraits to {OUTPUT}")
