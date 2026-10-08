#!/usr/bin/env python3
"""Crop reviewed four-character art grids into transparent expanded portraits.

The approval list is shared with the game. Unreviewed or incorrect portraits
keep their existing placeholders until their grids are corrected.
"""
from __future__ import annotations

import json
import hashlib
import subprocess
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'assets/ai-source/portraits/grids'
OVERRIDES = ROOT / 'assets/ai-source/portraits/overrides'
REQUIRED_OVERRIDES = {'rick'}
DESTINATION = ROOT / 'public/assets/portraits/expanded'
APPROVALS = ROOT / 'src/data/expanded-portrait-approvals.json'


def roster() -> list[dict[str, str]]:
    command = ("import {characters} from './src/data/characters.ts';"
               "console.log(JSON.stringify(characters.slice(100).map(c=>({id:c.id,name:c.name}))))")
    result = subprocess.run(['node', '--import', 'tsx', '--input-type=module', '-e', command],
                            cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def keep_main_silhouette(art: Image.Image) -> Image.Image:
    """Discard isolated generation specks around the two small mascots."""
    alpha = art.getchannel('A')
    width, height = art.size
    pixels = alpha.tobytes()
    seen = bytearray(len(pixels))
    largest: list[int] = []
    for start, value in enumerate(pixels):
        if value < 24 or seen[start]:
            continue
        component, pending = [], [start]
        seen[start] = 1
        while pending:
            index = pending.pop()
            component.append(index)
            x, y = index % width, index // width
            neighbors = (index-1 if x else -1, index+1 if x+1<width else -1,
                         index-width if y else -1, index+width if y+1<height else -1)
            for next_index in neighbors:
                if next_index >= 0 and not seen[next_index] and pixels[next_index] >= 24:
                    seen[next_index] = 1
                    pending.append(next_index)
        if len(component) > len(largest):
            largest = component
    mask_bytes = bytearray(len(pixels))
    for index in largest:
        mask_bytes[index] = 255
    mask = Image.frombytes('L', art.size, bytes(mask_bytes)).filter(ImageFilter.MaxFilter(3))
    alpha.paste(0, (0, 0, width, height), ImageOps.invert(mask))
    art.putalpha(alpha)
    return art


def main() -> None:
    characters = roster()
    assert len(characters) == 150
    approved = set(json.loads(APPROVALS.read_text()))
    assert approved <= {c['id'] for c in characters}
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for stale in DESTINATION.glob('*.webp'):
        stale.unlink()
    digests = set()
    for group in range(38):
        selected = [(slot, c) for slot, c in enumerate(characters[group*4:group*4+4])
                    if c['id'] in approved]
        if not selected:
            continue
        source = SOURCES / f'{group:03d}.webp'
        if not source.exists():
            raise FileNotFoundError(f'Missing four-character portrait grid: {source}')
        with Image.open(source) as image:
            image.load()
            if image.width < 900 or image.height < 900:
                raise ValueError(f'Portrait grid too small: {source} {image.size}')
            for slot, character in selected:
                column, row = slot % 2, slot // 2
                left = round(column * image.width / 2) + 6
                if character['id'] == 'picapau':
                    left += 24  # Keep Hellboy's fist outside this neighboring portrait.
                top = round(row * image.height / 2) + 6
                if group == 11 and row == 1:
                    top += 55  # The upper action portraits extend below the grid midpoint.
                right = round((column+1) * image.width / 2) - 6
                bottom = round((row+1) * image.height / 2) - 6
                override = OVERRIDES / f"{character['id']}.webp"
                if character['id'] in REQUIRED_OVERRIDES and not override.exists():
                    raise FileNotFoundError(f'Missing corrected portrait: {override}')
                art = (Image.open(override).convert('RGBA') if override.exists()
                       else image.crop((left, top, right, bottom)).convert('RGBA'))
                if character['id'] in {'kirby', 'donkeykong', 'finn'}:
                    art = keep_main_silhouette(art)
                if art.getchannel('A').getextrema()[0] != 0:
                    raise ValueError(f'Grid must have true transparency: {source}')
                bounds = art.getbbox()
                if not bounds:
                    raise ValueError(f'Empty portrait: {character["id"]}')
                art = ImageOps.contain(art.crop(bounds), (500, 500), Image.Resampling.LANCZOS)
                canvas = Image.new('RGBA', (512, 512))
                canvas.alpha_composite(art, ((512-art.width)//2, (512-art.height)//2))
                digest = hashlib.sha256(canvas.tobytes()).hexdigest()
                if digest in digests:
                    raise ValueError(f'Duplicate portrait: {character["id"]}')
                digests.add(digest)
                canvas.save(DESTINATION / f"{character['id']}.webp", format='WEBP', quality=88, method=3)
    assert len(digests) == len(approved)
    print(f'Built {len(approved)} reviewed portraits; {150-len(approved)} await correction.')


if __name__ == '__main__':
    main()
