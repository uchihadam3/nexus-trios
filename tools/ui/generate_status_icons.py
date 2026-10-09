"""Ícones dos 14 Status, desenhados em Python para ler em 16–22 px.

Os ícones anteriores eram pinturas detalhadas: bonitas grandes, um borrão no
tamanho em que a arena mostra. Aqui cada Status é um símbolo de silhueta
forte — chama, raio, escudo, cadeado, ampulheta — na cor do Status, com
degradê, contorno escuro (para destacar sobre qualquer fundo) e um brilho
suave em volta.

Uso: python3 tools/ui/generate_status_icons.py   (grava public/assets/statuses/*.png)
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/statuses"
N = 512          # tela de trabalho
FINAL = 128      # tamanho gravado
ESCALA = 0.47    # quanto do quadro o símbolo ocupa

CORES = {
    "exposed": "#ff8a66", "paralyzed": "#ffd75e", "protected": "#6fe3cf", "marked": "#ff6b7d",
    "slow": "#9fa8ff", "haste": "#c8f560", "confused": "#d68cff", "rooted": "#d9dde6",
    "regen": "#7fe88f", "burning": "#ff8a3d", "electric": "#ffe45c", "silenced": "#b49cff",
    "strengthened": "#ffd166", "weakened": "#b8a2d6", "provoked": "#ff7048",
}


def hexrgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def P(x: float, y: float):
    """Coordenada normalizada (-1..1) → pixel."""
    return (N / 2 + x * N * ESCALA, N / 2 + y * N * ESCALA)


def poly(d: ImageDraw.ImageDraw, pts, fill=255):
    d.polygon([P(x, y) for x, y in pts], fill=fill)


def circ(d, x, y, r, fill=255, width=0):
    cx, cy = P(x, y)
    rr = r * N * ESCALA
    if width:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=fill, width=int(width * N * ESCALA))
    else:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=fill)


def linha(d, pts, w, fill=255):
    d.line([P(x, y) for x, y in pts], fill=fill, width=int(w * N * ESCALA), joint="curve")
    for x, y in (pts[0], pts[-1]):
        circ(d, x, y, w / 2, fill)


# ------------------------------------------------------------------ símbolos
def chama(d):
    poly(d, [(0.04, -1.0), (0.24, -0.62), (0.46, -0.42), (0.6, -0.08), (0.64, 0.28), (0.52, 0.62), (0.28, 0.86), (0.0, 0.94),
             (-0.28, 0.86), (-0.52, 0.62), (-0.64, 0.28), (-0.58, -0.06), (-0.42, -0.34), (-0.34, -0.06), (-0.2, -0.44), (-0.06, -0.7)])


def chama_miolo(d):
    poly(d, [(0.02, -0.22), (0.18, 0.08), (0.3, 0.38), (0.22, 0.62), (0.0, 0.72), (-0.22, 0.62), (-0.3, 0.38), (-0.16, 0.12)], 0)


def espiral(d):
    pts = []
    for i in range(220):
        t = i / 219 * 4.3 * math.pi
        r = 0.08 + 0.75 * t / (4.3 * math.pi)
        pts.append((r * math.cos(t), r * math.sin(t)))
    linha(d, pts, 0.17)


def raio(d):
    poly(d, [(0.18, -0.95), (-0.5, 0.12), (-0.04, 0.12), (-0.22, 0.95), (0.52, -0.18), (0.06, -0.18), (0.32, -0.95)])


def escudo_pts(esc=1.0):
    pts = []
    for i in range(60):
        t = i / 59
        x = -0.72 + 1.44 * t
        y = -0.72 + 0.12 * math.sin(math.pi * t)  # topo levemente curvo
        pts.append((x * esc, y * esc - 0.05))
    for i in range(60):
        t = i / 59
        a = math.pi * t
        x = 0.72 * math.cos(a)
        y = -0.1 + 0.95 * math.sin(a) ** 0.9 * (1 if abs(math.cos(a)) < 0.999 else 1)
        pts.append((x * esc, y * esc - 0.05))
    return pts


def escudo(d):
    poly(d, escudo_pts())
    poly(d, escudo_pts(0.62), 0)
    poly(d, escudo_pts(0.42))


def escudo_rachado(d):
    poly(d, escudo_pts())
    # racha em zigue-zague que parte o escudo
    poly(d, [(-0.05, -1.0), (0.12, -0.4), (-0.12, -0.05), (0.14, 0.35), (-0.02, 1.0), (0.08, 1.0), (0.26, 0.35), (0.0, -0.05), (0.24, -0.4), (0.07, -1.0)], 0)


def setas(d):
    for dx in (-0.36, 0.22):
        poly(d, [(dx - 0.25, -0.7), (dx + 0.25, 0.0), (dx - 0.25, 0.7), (dx - 0.02, 0.7), (dx + 0.48, 0.0), (dx - 0.02, -0.7)])


def mira(d):
    circ(d, 0, 0, 0.62, 255, 0.17)
    for a in range(4):
        ang = a * math.pi / 2
        linha(d, [(0.45 * math.cos(ang), 0.45 * math.sin(ang)), (0.98 * math.cos(ang), 0.98 * math.sin(ang))], 0.17)
    circ(d, 0, 0, 0.15)


def pausa(d):
    for dx in (-0.27, 0.27):
        poly(d, [(dx - 0.15, -0.7), (dx + 0.15, -0.7), (dx + 0.15, 0.7), (dx - 0.15, 0.7)])
    # faíscas: o corpo travado
    for (x, y, s) in ((-0.78, -0.55, 1), (0.78, 0.5, -1), (0.75, -0.72, 1)):
        poly(d, [(x, y - 0.18), (x + 0.07 * s, y - 0.02), (x - 0.03 * s, y + 0.02), (x + 0.06 * s, y + 0.2), (x - 0.08 * s, y + 0.0), (x + 0.02 * s, y - 0.04)])


def coracao_mais(d):
    pts = []
    for i in range(120):
        t = i / 119 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((x / 17 * 0.92, y / 17 * 0.92 + 0.06))
    poly(d, pts)
    poly(d, [(-0.09, -0.36), (0.09, -0.36), (0.09, -0.09), (0.36, -0.09), (0.36, 0.09), (0.09, 0.09), (0.09, 0.36), (-0.09, 0.36), (-0.09, 0.09), (-0.36, 0.09), (-0.36, -0.09), (-0.09, -0.09)], 0)


def cadeado(d):
    poly(d, [(-0.66, -0.1), (0.66, -0.1), (0.66, 0.85), (-0.66, 0.85)])
    # alça
    pts = [(0.42 * math.cos(math.pi * (1 + t / 59)), -0.1 + 0.62 * math.sin(math.pi * (1 + t / 59))) for t in range(60)]
    linha(d, [(-0.42, 0.0)] + pts + [(0.42, 0.0)], 0.2)
    circ(d, 0, 0.3, 0.13, 0)
    poly(d, [(-0.06, 0.32), (0.06, 0.32), (0.08, 0.62), (-0.08, 0.62)], 0)


def balao_riscado(d):
    cx, cy = P(0, -0.12)
    rx, ry = 0.82 * N * ESCALA, 0.6 * N * ESCALA
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    poly(d, [(-0.45, 0.3), (-0.6, 0.9), (-0.05, 0.42)])
    # traço que cala
    linha(d, [(-0.85, 0.75), (0.85, -0.95)], 0.2, 0)
    linha(d, [(-0.72, 0.62), (0.72, -0.82)], 0.1, 255)


def ampulheta(d):
    poly(d, [(-0.62, -0.9), (0.62, -0.9), (0.62, -0.72), (-0.62, -0.72)])
    poly(d, [(-0.62, 0.72), (0.62, 0.72), (0.62, 0.9), (-0.62, 0.9)])
    poly(d, [(-0.5, -0.72), (0.5, -0.72), (0.08, 0.0), (0.5, 0.72), (-0.5, 0.72), (-0.08, 0.0)])
    poly(d, [(-0.3, -0.6), (0.3, -0.6), (0.05, -0.12), (-0.05, -0.12)], 0)
    poly(d, [(0.0, 0.25), (0.32, 0.6), (-0.32, 0.6)], 0)


def espada(d, quebrada=False, invertida=False):
    s = -1 if invertida else 1
    lamina = [(-0.2, 0.25 * s), (-0.2, -0.6 * s), (0.0, -0.98 * s), (0.2, -0.6 * s), (0.2, 0.25 * s)]
    poly(d, lamina)
    poly(d, [(-0.58, 0.22 * s), (0.58, 0.22 * s), (0.58, 0.4 * s), (-0.58, 0.4 * s)])   # guarda
    poly(d, [(-0.12, 0.4 * s), (0.12, 0.4 * s), (0.12, 0.78 * s), (-0.12, 0.78 * s)])  # cabo
    circ(d, 0, 0.86 * s, 0.16)
    if quebrada:
        poly(d, [(-0.4, -0.12 * s), (0.4, -0.42 * s), (0.4, -0.26 * s), (-0.4, 0.04 * s)], 0)
    else:
        # brilho: chevron subindo ao lado
        for x in (-0.66, 0.66):
            poly(d, [(x - 0.2, -0.28), (x, -0.58), (x + 0.2, -0.28), (x + 0.2, -0.1), (x, -0.38), (x - 0.2, -0.1)])


def raiva(d):
    """A marca de raiva dos desenhos: quatro arcos se encarando, com um vão em cruz no meio."""
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * 0.86, sy * 0.86
            pts = []
            for i in range(40):
                # o arco que olha para o centro, de um eixo ao outro
                a0 = math.atan2(-sy, -sx)
                a = a0 - 0.72 + 1.44 * i / 39
                pts.append((cx + 0.6 * math.cos(a), cy + 0.6 * math.sin(a)))
            linha(d, pts, 0.33)


SIMBOLOS = {
    "burning": chama, "confused": espiral, "electric": raio, "exposed": escudo_rachado,
    "haste": setas, "marked": mira, "paralyzed": pausa, "protected": escudo,
    "regen": coracao_mais, "rooted": cadeado, "silenced": balao_riscado, "slow": ampulheta,
    "strengthened": espada, "weakened": lambda d: espada(d, quebrada=True, invertida=True),
    "provoked": raiva,
}


def desenha(nome: str) -> Image.Image:
    mascara = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(mascara)
    SIMBOLOS[nome](d)
    if nome == "burning":
        chama_miolo(d)
    cor = np.array(hexrgb(CORES[nome]), np.float32) / 255

    # degradê: mais claro em cima, mais fundo embaixo
    y = np.linspace(0, 1, N, dtype=np.float32)[:, None]
    claro = np.clip(cor + (1 - cor) * 0.6, 0, 1)
    escuro = np.clip(cor * 0.92, 0, 1)
    grad = claro[None, None, :] * (1 - y[..., None]) + escuro[None, None, :] * y[..., None]
    grad = np.broadcast_to(grad, (N, N, 3))

    m = np.asarray(mascara, np.float32) / 255
    # contorno escuro (dilatação) e brilho em volta
    contorno = np.asarray(mascara.filter(ImageFilter.MaxFilter(23)), np.float32) / 255
    brilho = np.asarray(mascara.filter(ImageFilter.MaxFilter(23)).filter(ImageFilter.GaussianBlur(26)), np.float32) / 255
    # realce interno: borda superior do símbolo mais clara
    acima = np.asarray(ImageChops.subtract(mascara, ImageChops.offset(mascara, 0, 10)), np.float32) / 255

    rgb = np.zeros((N, N, 3), np.float32)
    a = np.zeros((N, N), np.float32)
    # brilho colorido
    rgb += cor * brilho[..., None] * 0.55
    a = np.maximum(a, brilho * 0.5)
    # contorno
    rgb = rgb * (1 - contorno[..., None]) + np.array([0.04, 0.06, 0.07]) * contorno[..., None]
    a = np.maximum(a, contorno)
    # símbolo
    sim = np.clip(grad + acima[..., None] * 0.35, 0, 1)
    rgb = rgb * (1 - m[..., None]) + sim * m[..., None]
    a = np.maximum(a, m)

    im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), np.clip(a, 0, 1)]) * 255 + 0.5).astype(np.uint8), "RGBA")
    return im.resize((FINAL, FINAL), Image.LANCZOS)


NOMES = {
    "exposed": "Exposto", "paralyzed": "Paralisado", "protected": "Protegido", "marked": "Marcado", "slow": "Lento",
    "haste": "Acelerado", "confused": "Confuso", "rooted": "Preso", "regen": "Regeneração", "burning": "Queimando",
    "electric": "Eletrificado", "silenced": "Silenciado", "strengthened": "Fortalecido", "weakened": "Enfraquecido",
    "provoked": "Provocado",
}


def folha():
    """A folha com todos os ícones (4 por linha) e o manifesto de recorte, na ordem do jogo."""
    import json
    cols, cel, margem = 4, 160, 8
    ordem = list(NOMES)
    linhas = math.ceil(len(ordem) / cols)
    W, H = margem + cols * (cel + margem), margem + linhas * (cel + margem)
    sheet = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    itens = []
    for i, nome in enumerate(ordem):
        r, c = divmod(i, cols)
        x, y = margem + c * (cel + margem), margem + r * (cel + margem)
        sheet.alpha_composite(Image.open(OUT / f"{nome}.png").convert("RGBA"), (x + 16, y + 16))
        itens.append({"id": nome, "name": NOMES[nome], "path": f"/assets/statuses/{nome}.png", "row": r, "column": c,
                      "cell": {"x": x, "y": y, "width": cel, "height": cel}, "crop": {"x": x + 16, "y": y + 16, "width": FINAL, "height": FINAL}})
    sheet.save(ROOT / "public/assets/sheets/statuses.png", optimize=True)
    manifesto = {"category": "statuses", "sourceSheet": "/assets/sheets/statuses.png", "format": "PNG RGBA", "resolution": [W, H],
                 "columns": cols, "rows": linhas, "cell": [cel, cel], "gutter": margem, "margin": margem, "count": len(ordem), "items": itens}
    (ROOT / "public/assets/sheets/statuses/manifest.json").write_text(json.dumps(manifesto, indent=2, ensure_ascii=False) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for nome in SIMBOLOS:
        destino = OUT / f"{nome}.png"
        desenha(nome).save(destino, optimize=True)
        print(f"{nome:13s} {destino.stat().st_size / 1024:5.1f} KB")
    folha()


if __name__ == "__main__":
    main()
