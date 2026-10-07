#!/usr/bin/env python3
"""Split a transparent 3-column skill grid into one source strip per character."""
import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    source = Image.open(sys.argv[1]).convert('RGBA')
    ids = sys.argv[2:]
    assert ids and source.width > 500 and source.height > 500
    root = Path(__file__).resolve().parents[1] / 'assets/ai-source/skills'
    root.mkdir(parents=True, exist_ok=True)
    for row, character_id in enumerate(ids):
        y0 = round(row * source.height / len(ids))
        y1 = round((row + 1) * source.height / len(ids))
        strip = source.crop((0, y0, source.width, y1))
        minimum, maximum = strip.getchannel('A').getextrema()
        assert minimum == 0 and maximum > 200, character_id
        strip.resize((768, 256), Image.Resampling.LANCZOS).save(root / f'{character_id}.png', optimize=True)
        print(character_id)


if __name__ == '__main__':
    main()
