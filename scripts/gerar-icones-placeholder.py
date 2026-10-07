#!/usr/bin/env python3
"""Ícones de habilidade placeholder para personagens sem arte-fonte ainda.

O empacotador oficial (``pack-ai-assets.py``) recorta folhas que vêm de
``assets/ai-source/skills``. Enquanto a arte real de um personagem novo não
chega, este script desenha um glifo por tipo de Visual, na cor do personagem,
no mesmo formato que o empacotador entrega — 160x160 na folha, 128x128 no
ícone solto — e acrescenta as entradas aos dois manifestos.

Não substitui arte final: quando a folha real existir em ``ai-source``, o
empacotador oficial sobrescreve o placeholder e as entradas são regeradas.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CELL, ICON, GUTTER, MARGIN = 160, 128, 8, 8


def ler_roster() -> list[dict]:
    """Pergunta ao próprio catálogo quem existe e o que cada habilidade é."""
    script = (
        "import {characters} from './src/data/characters.ts';"
        "process.stdout.write(JSON.stringify(characters.map(c=>({"
        "id:c.id,color:c.color,"
        "skills:c.skills.map(s=>({id:s.id,name:s.name,icon:s.icon}))"
        "}))));"
    )
    saida = subprocess.run(
        ["node", "--import", "tsx", "--input-type=module", "-e", script],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return json.loads(saida.stdout)


def cor(hex_: str, alpha: int) -> tuple[int, int, int, int]:
    h = hex_.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def glifo(visual: str, base: str, semente: int) -> Image.Image:
    """Um desenho por tipo de Visual. O mesmo vocabulário dos oito ícones.

    O ``giro`` entra em **todos** os ramos, e não só em alguns. Dois
    personagens da mesma cor com a mesma habilidade estavam gerando o mesmo
    PNG byte a byte, e o teste de unicidade de arte pegava isso — corretamente,
    porque dois ícones idênticos no catálogo são dois ícones que o jogador não
    consegue distinguir.
    """
    # O desenho nasce maior e gira: duas habilidades do mesmo personagem com o
    # mesmo Visual dependiam só do `giro`, e quando ele coincidia os dois PNGs
    # saíam byte a byte iguais. A rotação garante o que a variação de geometria
    # só tornava provável.
    escala = 2
    img = Image.new("RGBA", (ICON * escala, ICON * escala), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, fraco, forte = cor(base, 235), cor(base, 90), (255, 255, 255, 225)
    m = ICON
    giro = (semente % 13) - 6
    dx, dy = ((semente // 13) % 7) - 3, ((semente // 91) % 7) - 3
    m += dx

    if visual == "beam":
        d.polygon([(14, m - 9 + dy), (104, m - 20 + dy), (118 + giro, m + dy), (104, m + 20 + dy), (14, m + 9 + dy)], fill=c)
        d.ellipse([96 + giro, m - 26 + dy, 124 + giro, m + 26 + dy], fill=forte)
    elif visual == "bolt":
        d.polygon([(72 + giro, 10), (40 + dx, 66), (62, 66), (48 + dy, 118), (92 + giro, 56), (68, 56)], fill=c)
    elif visual == "slash":
        d.arc([6 + giro, 10, 150 + giro, 154], start=205, end=330, fill=c, width=16)
        d.arc([22 + giro, 26, 134 + giro, 138], start=210, end=325, fill=forte, width=5)
    elif visual == "web":
        for i in range(8):
            a = math.radians(i * 45 + giro)
            d.line([m, m, m + math.cos(a) * 56, m + math.sin(a) * 56], fill=fraco, width=4)
        for r in (22, 38, 54):
            d.ellipse([m - r, m - r, m + r, m + r], outline=c, width=3)
    elif visual == "shield":
        d.polygon([(m, 12 + dy), (116 + giro, 40), (116 + giro, 78), (m, 120 + dy), (12 - giro, 78), (12 - giro, 40)], fill=fraco, outline=c, width=5)
        d.line([m, 34 + dy, m, 98 + dy], fill=forte, width=5)
    elif visual == "wave":
        for i, r in enumerate((26, 44, 62)):
            d.arc([m - r, m - r, m + r, m + r], start=200 + giro, end=340 + giro, fill=c if i else forte, width=7)
    elif visual == "psychic":
        d.ellipse([18 - giro, 36 + dy, 110 + giro, 92 + dy], outline=c, width=6)
        d.ellipse([m - 20, m - 20, m + 20, m + 20], fill=c)
        d.ellipse([m - 8, m - 8, m + 8, m + 8], fill=forte)
    else:  # impact
        for i in range(10):
            a = math.radians(i * 36 + giro)
            r1, r2 = (20, 60 + giro) if i % 2 == 0 else (16, 42 + dy)
            d.line([m + math.cos(a) * r1, m + math.sin(a) * r1,
                    m + math.cos(a) * r2, m + math.sin(a) * r2], fill=c, width=9)
        d.ellipse([m - 18, m - 18, m + 18, m + 18], fill=forte)
    angulo = (semente % 360) * 0.0 + ((semente // 7) % 24) * 15
    img = img.rotate(angulo, resample=Image.Resampling.BICUBIC, expand=False)
    return img.resize((ICON, ICON), Image.Resampling.LANCZOS)


def main() -> None:
    roster = ler_roster()
    manifesto_icones = json.loads((PUBLIC / "assets/skills/manifest.json").read_text())
    manifesto_folhas = json.loads((PUBLIC / "assets/sheets/skills/manifest.json").read_text())
    ja_tem = {p["character"] for p in manifesto_folhas["pages"]}

    largura = MARGIN * 2 + CELL * 3 + GUTTER * 2
    altura = MARGIN * 2 + CELL
    novos = 0

    for i, c in enumerate(roster):
        if c["id"] in ja_tem:
            continue
        folha = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        icones = []
        destino = PUBLIC / "assets/skills" / c["id"]
        destino.mkdir(parents=True, exist_ok=True)

        for col, s in enumerate(c["skills"]):
            # FNV-1a: soma ponderada colidia entre ids diferentes, e dois
            # ícones byte a byte iguais reprovam no teste de unicidade de arte.
            h = 2166136261
            for ch in f'{c["id"]}:{col}:{c["color"]}':
                h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
            semente = h % 100003
            arte = glifo(s["icon"], c["color"], semente)
            x = MARGIN + col * (CELL + GUTTER) + (CELL - ICON) // 2
            folha.paste(arte, (x, MARGIN + (CELL - ICON) // 2), arte)
            caminho = f"/assets/skills/{c['id']}/{s['id']}.png"
            arte.save(PUBLIC / caminho.lstrip("/"))
            icones.append({
                "id": s["id"], "character": c["id"], "name": s["name"],
                "path": caminho, "sheet": f"/assets/sheets/skills/pages/{c['id']}.png",
                "row": 0, "column": col,
                "cell": {"x": MARGIN + col * (CELL + GUTTER), "y": MARGIN, "width": CELL, "height": CELL},
                "sourceCrop": {"x": 0, "y": 0, "width": CELL, "height": CELL},
                "placeholder": True,
            })
            manifesto_icones["skills"].append({
                "id": s["id"], "character": c["id"], "name": s["name"], "path": caminho,
                "sheet": f"/assets/sheets/skills/pages/{c['id']}.png", "row": 0, "column": col,
                "crop": {"x": 0, "y": 0, "width": ICON, "height": ICON},
            })

        folha.save(PUBLIC / f"assets/sheets/skills/pages/{c['id']}.png")
        manifesto_folhas["pages"].append({
            "character": c["id"],
            "sourceSheet": f"/assets/sheets/skills/pages/{c['id']}.png",
            "sheet": f"/assets/sheets/skills/pages/{c['id']}.png",
            "sourceResolution": [largura, altura], "category": "skills", "format": "PNG RGBA",
            "resolution": [largura, altura], "columns": 3, "rows": 1,
            "cell": [CELL, CELL], "gutter": GUTTER, "margin": MARGIN,
            "icons": icones, "placeholder": True,
        })
        novos += 1

    manifesto_icones["count"] = len(manifesto_icones["skills"])
    manifesto_folhas["count"] = sum(len(p["icons"]) for p in manifesto_folhas["pages"])
    (PUBLIC / "assets/skills/manifest.json").write_text(json.dumps(manifesto_icones, indent=2) + "\n")
    (PUBLIC / "assets/sheets/skills/manifest.json").write_text(json.dumps(manifesto_folhas, indent=2) + "\n")
    print(f"personagens novos com ícones placeholder: {novos}")
    print(f"ícones no total: {manifesto_icones['count']} | páginas: {len(manifesto_folhas['pages'])}")


if __name__ == "__main__":
    sys.exit(main())
