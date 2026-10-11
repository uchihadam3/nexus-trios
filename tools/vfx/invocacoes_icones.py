"""Os ícones das invocações (pedido do jogador: "quando eles invocar aparecer uma bolinha… menorzinha… com
o desenho do que eles invoca realmente… muito bem feita").

Cada criatura vira um medalhão pequeno desenhado por código: o fundo escuro na cor da criatura, a
silhueta com luz de cima, o contorno escuro e os detalhes acesos (olhos, joia, cérebro). Sai em
public/assets/invocacoes/<id>.webp (160 px), usado por src/components/Invocacoes.tsx.

    python3 tools/vfx/invocacoes_icones.py
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/invocacoes"
S = 640  # desenha grande e reduz (bordas lisas)


def P(pts):
    return [(x * S, y * S) for x, y in pts]


def cor(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def mistura(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)


def fundo(base):
    """O disco: escuro na cor da criatura, mais claro no alto, com um brilho atrás da silhueta."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    y, x = np.mgrid[0:S, 0:S] / S
    r = np.hypot(x - 0.5, y - 0.5)
    c = np.array(cor(base)[:3], float)
    escuro = c * 0.18 + 6
    claro = c * 0.42 + 10
    t = np.clip(1 - y * 1.1, 0, 1)[..., None]
    rgb = escuro * (1 - t) + claro * t
    halo = np.exp(-((x - 0.5) ** 2 + (y - 0.45) ** 2) / 0.06)[..., None]
    rgb = rgb + c * 0.35 * halo
    a = (r < 0.5).astype(float) * 255
    arr = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def silhueta(im, pts, base, contorno=(10, 8, 18, 255), largura=0.018):
    """Forma preenchida com luz de cima (gradiente vertical) e contorno escuro."""
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon(P(pts), fill=255)
    y = np.linspace(0, 1, S)[:, None] * np.ones((1, S))
    c1 = np.array(mistura(cor(base), (255, 255, 255), 0.55)[:3], float)
    c2 = np.array(mistura(cor(base), (0, 0, 0), 0.35)[:3], float)
    ys = [p[1] for p in pts]
    t = np.clip((y - min(ys)) / max(1e-3, max(ys) - min(ys)), 0, 1)[..., None]
    rgb = c1 * (1 - t) + c2 * t
    camada = Image.fromarray(np.dstack([rgb, np.full((S, S), 255)]).astype(np.uint8), "RGBA")
    camada.putalpha(mask)
    borda = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(borda).line(P(pts + pts[:1]), fill=contorno, width=int(largura * S), joint="curve")
    im.alpha_composite(borda)
    im.alpha_composite(camada)


def linha(im, pts, c, w):
    d = ImageDraw.Draw(im)
    d.line(P(pts), fill=c, width=int(w * S), joint="curve")


def disco(im, cx, cy, r, c):
    ImageDraw.Draw(im).ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=c)


def brilho(im, cx, cy, r, c):
    """Um ponto aceso com halo (olho, joia)."""
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    disco(g, cx, cy, r * 2.6, c[:3] + (90,))
    g = g.filter(ImageFilter.GaussianBlur(r * S * 1.2))
    im.alpha_composite(g)
    disco(im, cx, cy, r, c)
    disco(im, cx - r * 0.3, cy - r * 0.3, r * 0.35, (255, 255, 255, 230))


def arco(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in np.linspace(a0, a1, n)]


# ------------------------------------------------------------------ as criaturas
def cao(im):
    """Os Cães Divinos (Megumi): cabeça de lobo de perfil, branca com as marcas pretas e o olho aceso."""
    cabeca = [(0.24, 0.62), (0.30, 0.47), (0.34, 0.36), (0.36, 0.20), (0.44, 0.31), (0.50, 0.24), (0.55, 0.36),
              (0.66, 0.40), (0.80, 0.47), (0.84, 0.53), (0.80, 0.57), (0.66, 0.60), (0.60, 0.66), (0.52, 0.80),
              (0.30, 0.80)]
    silhueta(im, cabeca, "#e8eef8")
    linha(im, [(0.42, 0.36), (0.50, 0.44), (0.62, 0.46)], (20, 20, 30, 255), 0.022)
    linha(im, [(0.36, 0.56), (0.44, 0.62), (0.40, 0.72)], (20, 20, 30, 255), 0.02)
    disco(im, 0.83, 0.52, 0.025, (20, 20, 30, 255))
    linha(im, [(0.66, 0.60), (0.76, 0.58)], (20, 20, 30, 255), 0.012)
    brilho(im, 0.56, 0.42, 0.028, (120, 200, 255, 255))


def sombras(im):
    """Os Soldados das Sombras (Jinwoo): o elmo do cavaleiro de sombra, a pluma e os olhos roxos acesos."""
    elmo = [(0.30, 0.80), (0.30, 0.46), (0.36, 0.32), (0.50, 0.25), (0.64, 0.32), (0.70, 0.46), (0.70, 0.80),
            (0.60, 0.74), (0.50, 0.82), (0.40, 0.74)]
    pluma = [(0.50, 0.25), (0.46, 0.14), (0.54, 0.08), (0.64, 0.12), (0.58, 0.18), (0.56, 0.27)]
    silhueta(im, pluma, "#6a3cff")
    silhueta(im, elmo, "#3a2a68")
    linha(im, [(0.34, 0.50), (0.66, 0.50)], (8, 6, 16, 255), 0.05)
    linha(im, [(0.50, 0.50), (0.50, 0.74)], (8, 6, 16, 255), 0.03)
    brilho(im, 0.41, 0.50, 0.026, (190, 120, 255, 255))
    brilho(im, 0.59, 0.50, 0.026, (190, 120, 255, 255))


def mago(im):
    """O Mago Negro (Yugi): o chapéu pontudo dobrado, o rosto, e o cetro com a joia verde."""
    linha(im, [(0.78, 0.86), (0.70, 0.30)], (40, 30, 60, 255), 0.04)
    linha(im, [(0.78, 0.86), (0.70, 0.30)], (150, 120, 220, 255), 0.022)
    brilho(im, 0.70, 0.27, 0.045, (90, 255, 150, 255))
    rosto = [(0.38, 0.52), (0.58, 0.52), (0.56, 0.68), (0.48, 0.74), (0.40, 0.68)]
    silhueta(im, rosto, "#d9c4ff")
    chapeu = [(0.26, 0.56), (0.34, 0.44), (0.40, 0.30), (0.50, 0.14), (0.64, 0.10), (0.58, 0.20), (0.60, 0.40),
              (0.70, 0.56), (0.48, 0.52)]
    silhueta(im, chapeu, "#7a4cff")
    linha(im, [(0.30, 0.54), (0.66, 0.54)], (220, 200, 255, 255), 0.018)
    disco(im, 0.44, 0.60, 0.014, (30, 20, 60, 255))
    disco(im, 0.53, 0.60, 0.014, (30, 20, 60, 255))
    corpo = [(0.32, 0.74), (0.48, 0.72), (0.64, 0.74), (0.70, 0.90), (0.26, 0.90)]
    silhueta(im, corpo, "#5a34c8")


def dragao(im):
    """O Dragão Branco de Olhos Azuis (Kaiba): cabeça de dragão de perfil, chifres para trás, a boca
    aberta com dentes e o olho azul."""
    cabeca = [(0.20, 0.62), (0.26, 0.44), (0.40, 0.34), (0.56, 0.36), (0.70, 0.40), (0.86, 0.46), (0.88, 0.52),
              (0.70, 0.54), (0.84, 0.60), (0.80, 0.66), (0.62, 0.64), (0.50, 0.70), (0.40, 0.84), (0.24, 0.84)]
    chifre1 = [(0.36, 0.36), (0.20, 0.16), (0.30, 0.18), (0.44, 0.34)]
    chifre2 = [(0.46, 0.34), (0.40, 0.12), (0.50, 0.16), (0.54, 0.35)]
    silhueta(im, chifre1, "#bfe6ff")
    silhueta(im, chifre2, "#bfe6ff")
    silhueta(im, cabeca, "#e6f4ff")
    for k in range(4):
        x = 0.68 + k * 0.045
        ImageDraw.Draw(im).polygon(P([(x, 0.54), (x + 0.018, 0.54), (x + 0.009, 0.585)]), fill=(250, 250, 255, 255))
    linha(im, [(0.42, 0.48), (0.60, 0.46)], (60, 90, 140, 255), 0.012)
    brilho(im, 0.56, 0.43, 0.03, (60, 170, 255, 255))


def gomorrah(im):
    """Gomorrah (Bayonetta): a bocarra do demônio de cabelo, dentes afiados e os olhos vermelhos."""
    cabeca = [(0.16, 0.40), (0.30, 0.24), (0.50, 0.18), (0.70, 0.24), (0.84, 0.40), (0.80, 0.50), (0.70, 0.46),
              (0.50, 0.44), (0.30, 0.46), (0.20, 0.50)]
    mandibula = [(0.22, 0.58), (0.36, 0.56), (0.50, 0.58), (0.64, 0.56), (0.78, 0.58), (0.70, 0.74), (0.50, 0.84),
                 (0.30, 0.74)]
    silhueta(im, cabeca, "#6a1830")
    silhueta(im, mandibula, "#521226")
    d = ImageDraw.Draw(im)
    for k in range(7):
        x = 0.26 + k * 0.075
        d.polygon(P([(x, 0.46), (x + 0.04, 0.46), (x + 0.02, 0.55)]), fill=(250, 240, 230, 255))
        d.polygon(P([(x + 0.01, 0.59), (x + 0.05, 0.59), (x + 0.03, 0.51)]), fill=(250, 240, 230, 255))
    brilho(im, 0.36, 0.33, 0.03, (255, 60, 60, 255))
    brilho(im, 0.64, 0.33, 0.03, (255, 60, 60, 255))
    linha(im, [(0.30, 0.24), (0.22, 0.10)], (90, 20, 40, 255), 0.03)
    linha(im, [(0.70, 0.24), (0.78, 0.10)], (90, 20, 40, 255), 0.03)


def ora(im):
    """Star Platinum (Jotaro): o punho fechado vindo para a frente, com as linhas de velocidade."""
    for k, y in enumerate((0.30, 0.42, 0.66, 0.76)):
        linha(im, [(0.10, y), (0.30 - k * 0.02, y)], (150, 170, 255, 200), 0.016)
    punho = [(0.30, 0.34), (0.56, 0.28), (0.74, 0.32), (0.82, 0.42), (0.82, 0.62), (0.74, 0.72), (0.52, 0.74),
             (0.30, 0.68)]
    silhueta(im, punho, "#6f8cff")
    for k in range(4):
        y = 0.36 + k * 0.09
        linha(im, [(0.62, y), (0.80, y + 0.01)], (30, 30, 80, 255), 0.012)
    polegar = [(0.40, 0.60), (0.60, 0.56), (0.66, 0.64), (0.44, 0.70)]
    silhueta(im, polegar, "#8aa2ff")
    linha(im, [(0.30, 0.34), (0.22, 0.36), (0.22, 0.66), (0.30, 0.68)], (240, 220, 120, 255), 0.03)


def feras(im):
    """O Caminho Animal (Pain): o rinoceronte invocado de frente, o chifre e o Rinnegan no olho."""
    cabeca = [(0.22, 0.46), (0.32, 0.32), (0.50, 0.28), (0.68, 0.32), (0.78, 0.46), (0.74, 0.66), (0.62, 0.80),
              (0.38, 0.80), (0.26, 0.66)]
    chifre = [(0.44, 0.58), (0.50, 0.20), (0.56, 0.58)]
    orelha1 = [(0.28, 0.36), (0.18, 0.22), (0.34, 0.30)]
    orelha2 = [(0.72, 0.36), (0.82, 0.22), (0.66, 0.30)]
    silhueta(im, orelha1, "#a88a68")
    silhueta(im, orelha2, "#a88a68")
    silhueta(im, cabeca, "#c8a070")
    silhueta(im, chifre, "#f0e6d0")
    for x in (0.36, 0.64):
        disco(im, x, 0.48, 0.045, (230, 220, 255, 255))
        for r in (0.032, 0.02, 0.009):
            ImageDraw.Draw(im).ellipse([(x - r) * S, (0.48 - r) * S, (x + r) * S, (0.48 + r) * S], outline=(110, 80, 200, 255), width=4)
    disco(im, 0.44, 0.72, 0.02, (60, 40, 30, 255))
    disco(im, 0.56, 0.72, 0.02, (60, 40, 30, 255))


def vassouras(im):
    """As vassouras encantadas (Mickey): a vassoura em pé com braços, carregando os dois baldes d'água."""
    linha(im, [(0.50, 0.18), (0.50, 0.62)], (110, 70, 30, 255), 0.05)
    linha(im, [(0.50, 0.18), (0.50, 0.62)], (180, 120, 60, 255), 0.03)
    palha = [(0.38, 0.60), (0.62, 0.60), (0.70, 0.86), (0.30, 0.86)]
    silhueta(im, palha, "#e0b060")
    for k in range(6):
        x = 0.36 + k * 0.056
        linha(im, [(x, 0.64), (x - 0.02 + k * 0.008, 0.84)], (150, 100, 40, 255), 0.008)
    linha(im, [(0.50, 0.38), (0.30, 0.44), (0.24, 0.54)], (110, 70, 30, 255), 0.03)
    linha(im, [(0.50, 0.38), (0.70, 0.44), (0.76, 0.54)], (110, 70, 30, 255), 0.03)
    for x in (0.24, 0.76):
        balde = [(x - 0.08, 0.54), (x + 0.08, 0.54), (x + 0.06, 0.70), (x - 0.06, 0.70)]
        silhueta(im, balde, "#9aa8b8")
        linha(im, [(x - 0.07, 0.56), (x + 0.07, 0.56)], (90, 170, 255, 255), 0.018)


def clones(im):
    """O exército de clones do Plankton: o corpinho verde de um olho só, as antenas, e dois clones atrás."""
    def plankton(cx, cy, e, base):
        corpo = [(cx - 0.10 * e, cy + 0.26 * e), (cx - 0.12 * e, cy - 0.02 * e), (cx - 0.08 * e, cy - 0.14 * e),
                 (cx, cy - 0.18 * e), (cx + 0.08 * e, cy - 0.14 * e), (cx + 0.12 * e, cy - 0.02 * e), (cx + 0.10 * e, cy + 0.26 * e)]
        linha(im, [(cx - 0.04 * e, cy - 0.16 * e), (cx - 0.10 * e, cy - 0.34 * e)], (40, 90, 40, 255), 0.012 * e)
        linha(im, [(cx + 0.04 * e, cy - 0.16 * e), (cx + 0.10 * e, cy - 0.34 * e)], (40, 90, 40, 255), 0.012 * e)
        silhueta(im, corpo, base, largura=0.014 * e)
        disco(im, cx, cy - 0.04 * e, 0.07 * e, (250, 240, 200, 255))
        disco(im, cx, cy - 0.04 * e, 0.035 * e, (200, 30, 30, 255))
        disco(im, cx, cy - 0.04 * e, 0.014 * e, (10, 10, 10, 255))
        linha(im, [(cx - 0.05 * e, cy + 0.10 * e), (cx + 0.05 * e, cy + 0.10 * e)], (30, 60, 30, 255), 0.01 * e)
    plankton(0.30, 0.52, 0.85, "#4a9a4a")
    plankton(0.70, 0.52, 0.85, "#4a9a4a")
    plankton(0.50, 0.56, 1.25, "#6fd06f")


def androide(im):
    """O androide de combate do Krang: o tronco de robô, os ombros largos e o Krang rosa na janela do
    peito, com o olho aceso."""
    tronco = [(0.26, 0.36), (0.40, 0.30), (0.60, 0.30), (0.74, 0.36), (0.70, 0.80), (0.30, 0.80)]
    ombro1 = [(0.12, 0.40), (0.26, 0.34), (0.30, 0.50), (0.16, 0.54)]
    ombro2 = [(0.88, 0.40), (0.74, 0.34), (0.70, 0.50), (0.84, 0.54)]
    cabeca = [(0.42, 0.30), (0.42, 0.18), (0.58, 0.18), (0.58, 0.30)]
    silhueta(im, ombro1, "#9aa4b8")
    silhueta(im, ombro2, "#9aa4b8")
    silhueta(im, cabeca, "#c0c8d8")
    silhueta(im, tronco, "#b8c0d0")
    janela = arco(0.50, 0.56, 0.15, 0.13, 0, math.tau, 30)
    silhueta(im, janela, "#3a4a5a")
    cerebro = arco(0.50, 0.57, 0.11, 0.09, 0, math.tau, 24)
    silhueta(im, cerebro, "#ff8ac8")
    linha(im, [(0.42, 0.55), (0.48, 0.52), (0.52, 0.58), (0.58, 0.54)], (180, 60, 120, 255), 0.01)
    brilho(im, 0.50, 0.24, 0.022, (255, 80, 80, 255))


CRIATURAS = {
    "megumi": (cao, "#e8eef8"), "jinwoo": (sombras, "#7a4cff"), "yugi": (mago, "#8a5cff"), "kaiba": (dragao, "#7fc8ff"),
    "bayonetta": (gomorrah, "#c0304e"), "jotaro": (ora, "#6f8cff"), "pain": (feras, "#c8a070"),
    "mickey": (vassouras, "#e0b060"), "plankton": (clones, "#6fd06f"), "krang": (androide, "#ff8ac8"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    folha = Image.new("RGBA", (160 * 5, 160 * 2), (40, 44, 56, 255))
    for k, (id_, (fn, base)) in enumerate(CRIATURAS.items()):
        im = fundo(base)
        fn(im)
        # recorta no círculo (nada sai do medalhão)
        m = Image.new("L", (S, S), 0)
        ImageDraw.Draw(m).ellipse([0, 0, S - 1, S - 1], fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel("A")), np.asarray(m))))
        final = im.resize((160, 160), Image.LANCZOS)
        final.save(OUT / f"{id_}.webp", quality=92)
        folha.alpha_composite(final, ((k % 5) * 160, (k // 5) * 160))
        print(id_, (OUT / f"{id_}.webp").stat().st_size // 1024, "KB")
    folha.save("/tmp/claude-0/sp/invocacoes-folha.png")


if __name__ == "__main__":
    main()
