#!/usr/bin/env python3
"""Reproducible small VFX sprite atlases and neutral arena texture."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/vfx"
SIZE, COLS, ROWS, FRAMES = 96, 4, 3, 12
PALETTES = {
    "impact": (255, 218, 157), "energy": (155, 226, 255), "electric": (255, 240, 139),
    "fire": (255, 147, 82), "grand": (248, 215, 147),
    "slash": (240, 248, 255), "magic": (194, 170, 255), "dark": (186, 140, 255),
    "psychic": (255, 151, 210), "shield": (158, 231, 255), "heal": (157, 255, 198),
    "regen": (159, 242, 174), "prison": (158, 213, 245), "interrupt": (255, 169, 146),
    "ko": (255, 128, 111), "buff": (226, 246, 151), "debuff": (221, 149, 209),
}


def frame(family: str, index: int) -> Image.Image:
    n = SIZE
    y, x = np.mgrid[-1:1:complex(n), -1:1:complex(n)]
    radius = np.sqrt(x*x + y*y)
    angle = np.arctan2(y, x)
    t = index / (FRAMES - 1)
    wave = np.zeros_like(radius)
    if family in {"impact", "ko", "interrupt", "grand"}:
        ring = np.exp(-((radius - (0.12 + .72*t)) / .045)**2) * (1-t)**.25
        core = np.exp(-(radius / max(.12, .44*(1-t)))**2) * (1-t)
        sides=24 if family=="grand" else 12
        rays = np.maximum(0, np.cos(angle*sides + t*4))**(14 if family=="grand" else 18) * np.exp(-((radius-.45)/.3)**2) * (1-t)
        wave = ring + core*.8 + rays*(.82 if family=="grand" else .55)
        if family=="grand":
            wave += np.exp(-((radius-(.18+.34*t))/.022)**2)*.88
            wave += np.maximum(0,np.sin(angle*3-radius*18+t*8))**12*np.exp(-((radius-.52)/.34)**2)*.35
    elif family=="fire":
        tongues=np.maximum(0,np.sin(angle*5+radius*12-t*12))**5
        wave=tongues*np.exp(-((radius-(.22+.24*np.sin(t*math.pi)))/.38)**2)*(1-.35*t)
        wave+=np.exp(-((radius-.2)/.12)**2)*(.8*(1-t))
    elif family in {"electric", "energy", "slash"}:
        if family == "slash":
            wave = np.exp(-((y - .48*x - (.9-1.8*t))/.045)**2) * np.clip(1-np.abs(x)*.5, 0, 1)
        else:
            spokes = np.maximum(0, np.cos(angle*8 + t*18))**16
            wave = spokes * np.exp(-((radius-(.18+.65*t))/.24)**2) + np.exp(-((radius-.18)/.07)**2)*(1-t)
    elif family in {"shield", "prison"}:
        sides = 6 if family == "shield" else 8
        polygon = np.cos((angle+math.pi/sides) % (2*math.pi/sides)-math.pi/sides)
        edge = np.abs(radius*polygon - (.45+.12*math.sin(t*math.pi)))
        wave = np.exp(-(edge/.035)**2) * np.clip(1-t*.38, 0, 1)
        if family == "prison":
            wave += np.exp(-((x*np.sin(t*math.pi*2)+y*np.cos(t*math.pi*2))/.025)**2)*np.exp(-((radius-.62)/.08)**2)*.42
    else:
        turns = 2.3 if family in {"magic", "dark", "psychic"} else 1.3
        spiral = np.sin(angle*turns + radius*23 - t*math.tau)
        wave = np.maximum(0, spiral)**8 * np.exp(-((radius-(.34+.16*math.sin(t*math.tau)))/.29)**2)
        wave += np.exp(-((radius-.13)/.06)**2)*(.5+.5*math.sin(t*math.pi))
        if family in {"heal", "regen", "buff", "debuff"}:
            wave += np.exp(-((radius-(.22+.4*t))/.035)**2)*.72
    wave = np.clip(wave, 0, 1)
    glow = gaussian_filter(wave, sigma=3.8)
    alpha = np.clip(wave*.92 + glow*.48, 0, .96)
    color = np.asarray(PALETTES[family], dtype=np.float32)
    rgb = np.empty((n, n, 3), dtype=np.uint8)
    lift = np.clip(wave[..., None]*.27 + glow[..., None]*.52, 0, .8)
    rgb[:] = (color[None, None, :] * (1-lift) + 255*lift).clip(0, 255).astype(np.uint8)
    rgba = np.dstack((rgb, (alpha*255).astype(np.uint8)))
    return Image.fromarray(rgba, "RGBA")


def arena() -> Image.Image:
    w, h = 768, 1056
    y, x = np.mgrid[0:h, 0:w]
    nx, ny = (x-w/2)/(w/2), (y-h/2)/(h/2)
    radial = np.sqrt(nx*nx + ny*ny)
    base = np.zeros((h, w, 3), dtype=np.float32)
    base[:] = (7, 13, 21)
    center = np.exp(-((nx/.8)**2 + (ny/.52)**2)*2.3)
    left = np.exp(-(((nx+.95)/.65)**2 + (ny/.88)**2)*2.2)
    right = np.exp(-(((nx-.95)/.65)**2 + (ny/.88)**2)*2.2)
    base += center[..., None]*np.array([24, 48, 60])
    base += left[..., None]*np.array([17, 4, 17]) + right[..., None]*np.array([2, 17, 14])
    base *= np.clip(1-radial*.23, .48, 1)[..., None]
    img = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB").convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(overlay)
    cx, cy = w//2, h//2
    # A recessed octagonal dueling dais sits behind the floating card rows.
    draw.polygon([(cx-224,cy-93),(cx-181,cy-124),(cx+181,cy-124),(cx+224,cy-93),
                  (cx+224,cy+93),(cx+181,cy+124),(cx-181,cy+124),(cx-224,cy+93)],
                 fill=(37,71,79,13),outline=(168,218,222,16),width=2)
    draw.ellipse((cx-248, cy-121, cx+248, cy+121), outline=(167, 211, 218, 29), width=3)
    draw.ellipse((cx-211, cy-101, cx+211, cy+101), outline=(183, 224, 201, 20), width=2)
    draw.ellipse((cx-160, cy-75, cx+160, cy+75), outline=(190, 217, 231, 12), width=2)
    draw.line((35, cy, w-35, cy), fill=(169, 212, 216, 21), width=2)
    draw.line((cx, cy-430, cx, cy+430), fill=(169, 212, 216, 8), width=1)
    # Side pylons, perspective floor seams and short calibration ticks add depth
    # without putting a character or symbol into the reusable neutral scenery.
    for side in (0,1):
        sx=34 if side==0 else w-34
        ex=104 if side==0 else w-104
        draw.polygon([(sx,150),(ex,184),(ex,876),(sx,910)],fill=(104,150,165,5),outline=(153,197,206,12))
        for y0 in range(225,865,105):
            draw.line((sx,y0,ex,y0+16),fill=(165,208,210,10),width=1)
        draw.line((sx,150,sx,910),fill=(177,216,220,14),width=2)
    for y0 in range(cy+148,cy+400,38):
        factor=(y0-cy)/410
        draw.line((int(cx-300*factor),y0,int(cx+300*factor),y0),fill=(159,202,207,7),width=1)
    for x0 in range(74, w-73, 74):
        draw.line((x0,cy+125,cx+(x0-cx)*1.3,cy+390),fill=(159,202,207,5),width=1)
    for angle in range(0,360,15):
        a=math.radians(angle);x1=cx+int(250*math.cos(a));y1=cy+int(122*math.sin(a))
        x2=cx+int(268*math.cos(a));y2=cy+int(131*math.sin(a))
        draw.line((x1,y1,x2,y2),fill=(207,232,222,29),width=2)
    for r in range(285, 431, 58):
        draw.ellipse((cx-r, cy-r*.68, cx+r, cy+r*.68), outline=(172, 198, 216, 5), width=1)
    img.alpha_composite(overlay)
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"seed": "deterministic-20261004", "frameSize": [SIZE, SIZE], "columns": COLS,
                "rows": ROWS, "fps": 20, "families": {}}
    for family in PALETTES:
        sheet = Image.new("RGBA", (SIZE*COLS, SIZE*ROWS), (0, 0, 0, 0))
        for i in range(FRAMES):
            sheet.alpha_composite(frame(family, i), ((i % COLS)*SIZE, (i // COLS)*SIZE))
        sheet.save(OUT/f"{family}.webp", "WEBP", quality=84, method=4)
        manifest["families"][family] = {"file": f"{family}.webp", "frames": FRAMES,
                                        "loop": family in {"magic", "dark", "psychic", "shield", "regen"}}
    arena().save(OUT/"arena.webp", "WEBP", quality=86, method=4)
    manifest["arena"] = {"file": "arena.webp", "size": [768, 1056], "containsText": False, "containsFigures": False}
    (OUT/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(f"generated {len(PALETTES)} atlases and arena texture in {OUT}")


if __name__ == "__main__":
    main()
