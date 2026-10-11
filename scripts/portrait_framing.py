"""Fill circular portrait windows with selected opaque illustrations."""
import json
from pathlib import Path

from PIL import Image

FRAMING = json.loads((Path(__file__).resolve().parents[1] /
                      'assets/portraits/circle-framing.json').read_text())


def frame_for_circle(art: Image.Image, character_id: str, size: int) -> Image.Image | None:
    settings = FRAMING.get(character_id)
    if settings is None:
        return None
    if art.getchannel('A').getextrema() != (255, 255):
        raise ValueError(f'Circular fill requires an opaque source: {character_id}')
    side = min(art.size) / settings['zoom']
    x, y = settings['centering']
    left, top = (art.width-side)*x, (art.height-side)*y
    return art.crop((left, top, left+side, top+side)).resize(
        (size, size), Image.Resampling.LANCZOS)
