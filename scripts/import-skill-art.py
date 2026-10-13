#!/usr/bin/env python3
"""Import approved single-character three-skill strips into the Nexus game.

Reads assets/ai-source/skill-art-imports.json. Every entry represents exactly
one character and its three real skill names in roster order. Writes an
RGBA 3:1 source strip consumed by create-expanded-skill-art.py.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / 'assets/ai-source/skill-art-imports.json'
SOURCE = ROOT / 'assets/ai-source/skills'
SIDE = 512
MAX_FILE = 16 * 1024 * 1024


def roster() -> list[dict]:
    js = ("import {characters} from './src/data/characters.ts';"
          "process.stdout.write(JSON.stringify(characters.map(c=>"
          "({id:c.id,skills:c.skills.map(s=>s.name)}))));")
    p = subprocess.run(['node', '--import', 'tsx', '--input-type=module',
                        '-e', js], cwd=ROOT, check=True, capture_output=True,
                       text=True)
    return json.loads(p.stdout)


def download(url: str) -> Image.Image:
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not (
            parsed.hostname == 'dnznrvs05pmza.cloudfront.net'
            or parsed.hostname == 'assets.runwayml.com'
            or (parsed.hostname or '').endswith('.runwayml.com')):
        raise ValueError('Unapproved image origin')
    req = Request(url, headers={'User-Agent': 'NexusTriosSkillAssetImporter/1.0'})
    with urlopen(req, timeout=90) as response:
        raw = response.read(MAX_FILE + 1)
    if len(raw) > MAX_FILE:
        raise ValueError('Source image too large')
    image = Image.open(io.BytesIO(raw))
    image.load()
    if image.width < 900 or image.height < 300:
        raise ValueError('Source image resolution too small')
    return image.convert('RGBA')


def isolate(image: Image.Image) -> Image.Image:
    """Preserve luminous details; softly remove dark backdrop around the art."""
    alpha = image.getchannel('A')
    rgb = image.convert('RGB')
    r, g, b = rgb.split()
    peak = ImageChops.lighter(r, ImageChops.lighter(g, b))
    # Bright subject and crisp outlines stay opaque; very dark space goes clear.
    inferred = peak.point(lambda n: 0 if n <= 9 else
                          min(255, int((n - 9) * 255 / 47)))
    alpha = ImageChops.multiply(alpha, inferred)
    image.putalpha(alpha)
    return image


def render_strip(image: Image.Image) -> Image.Image:
    if image.width / image.height < 2.0:
        raise ValueError('Expected a horizontal three-panel image')
    result = Image.new('RGBA', (SIDE * 3, SIDE), (0, 0, 0, 0))
    for index in range(3):
        left = round(index * image.width / 3)
        right = round((index + 1) * image.width / 3)
        part = isolate(image.crop((left, 0, right, image.height)))
        bounds = part.getchannel('A').point(lambda a: 255 if a > 16 else 0).getbbox()
        if bounds is None:
            raise ValueError(f'Empty artwork panel {index + 1}')
        part = part.crop(bounds)
        part.thumbnail((SIDE - 32, SIDE - 32), Image.Resampling.LANCZOS)
        panel = Image.new('RGBA', (SIDE, SIDE), (0, 0, 0, 0))
        panel.alpha_composite(part, ((SIDE - part.width) // 2,
                                     (SIDE - part.height) // 2))
        if panel.getchannel('A').getbbox() is None:
            raise ValueError(f'Blank panel {index + 1}')
        result.alpha_composite(panel, (index * SIDE, 0))
    if result.getchannel('A').getpixel((0, 0)) != 0:
        raise ValueError('Nontransparent top-left corner')
    return result


def main() -> None:
    data = json.loads(INBOX.read_text(encoding='utf-8'))
    entries = data.get('imports', [])
    if not 1 <= len(entries) <= 30:
        raise ValueError('Require between 1 and 30 character sheets per batch')
    members = roster()
    if len(members) < 400:
        raise ValueError('Unexpected roster size')
    ids = set()
    report = list(data.get('imported', []))
    for entry in entries:
        char = entry['character']
        if char in ids:
            raise ValueError(f'Duplicate character {char}')
        ids.add(char)
        indices = [i for i, c in enumerate(members) if c['id'] == char]
        if len(indices) != 1 or not 250 <= indices[0] < 400:
            raise ValueError(f'Not one of the 150 pending characters: {char}')
        if entry['skills'] != members[indices[0]]['skills']:
            raise ValueError(f'Skill names/order mismatch for {char}')
        destination = SOURCE / f'{char}.png'
        if destination.exists():
            raise FileExistsError(f'Never overwrite existing approved art: {char}')
        sheet = render_strip(download(entry['url']))
        destination.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(destination, optimize=True)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        report.append({'character': char, 'skills': entry['skills'],
                       'task_id': entry.get('task_id'), 'sha256': digest,
                       'source': str(destination.relative_to(ROOT))})
        print(f'Imported {char} 3 skills -> {destination}')
    data['imports'] = []
    data['imported'] = report
    INBOX.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                     encoding='utf-8')
    print(f'Validated {len(entries)} character sheets; previous approved art intact')


if __name__ == '__main__':
    main()
