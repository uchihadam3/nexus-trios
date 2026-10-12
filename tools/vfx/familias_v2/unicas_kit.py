"""O kit das Mecânicas únicas: as formas (coração, espada, olho, relógio, corrente…) e os movimentos (abrir,
estourar, subir, chover, voar, cortar) que as famílias mu_* combinam, cada uma do seu jeito.

As formas vêm no tamanho 1 (cabem num quadrado de -1 a 1) e são postas no lugar com `poe(pts, cx, cy, s, ang)`.
"""
from __future__ import annotations

import math

import numpy as np

from .base import TAU, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel  # noqa: F401
from .rodada13 import _borda


def poe(pts, cx=0.0, cy=0.0, s=1.0, ang=0.0):
    c, n = math.cos(ang), math.sin(ang)
    return [(cx + (x * c - y * n) * s, cy + (x * n + y * c) * s) for x, y in pts]


def circulo(n=24, r=1.0, sq=1.0):
    return [(r * math.cos(TAU * k / n), r * math.sin(TAU * k / n) * sq) for k in range(n)]


# ---------------------------------------------------------------- formas (tamanho 1, de pé, centro na origem)
CORACAO = [(16 * math.sin(a) ** 3 / 17, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 17)
           for a in np.linspace(0, TAU, 32, endpoint=False)]
ESPADA = [(0, -1), (0.09, -0.75), (0.09, 0.3), (0.35, 0.3), (0.35, 0.42), (0.07, 0.42), (0.07, 0.85), (0.14, 0.92),
          (0, 1.0), (-0.14, 0.92), (-0.07, 0.85), (-0.07, 0.42), (-0.35, 0.42), (-0.35, 0.3), (-0.09, 0.3), (-0.09, -0.75)]
ESCUDO = [(-0.8, -0.85), (0, -1.0), (0.8, -0.85), (0.8, -0.1), (0.55, 0.45), (0, 1.0), (-0.55, 0.45), (-0.8, -0.1)]
COROA = [(-0.9, 0.5), (-0.9, -0.5), (-0.5, -0.05), (-0.25, -0.75), (0, -0.1), (0.25, -0.75), (0.5, -0.05), (0.9, -0.5), (0.9, 0.5)]
CHAMA = [(0, -1), (0.25, -0.55), (0.55, -0.2), (0.6, 0.25), (0.42, 0.65), (0, 0.85), (-0.42, 0.65), (-0.6, 0.25), (-0.5, -0.1),
         (-0.3, 0.05), (-0.25, -0.45)]
RAIO = [(0.15, -1), (-0.45, 0.1), (-0.05, 0.1), (-0.25, 1.0), (0.45, -0.2), (0.05, -0.2), (0.35, -1)]
GOTA = [(0, -1)] + [(0.55 * math.cos(a), 0.35 + 0.55 * math.sin(a)) for a in np.linspace(-0.25, math.pi + 0.25, 16)]
AMPULHETA = [(-0.6, -1), (0.6, -1), (0.6, -0.85), (0.08, -0.05), (0.08, 0.05), (0.6, 0.85), (0.6, 1), (-0.6, 1), (-0.6, 0.85),
             (-0.08, 0.05), (-0.08, -0.05), (-0.6, -0.85)]
DIAMANTE = [(-0.6, -0.35), (-0.3, -0.8), (0.3, -0.8), (0.6, -0.35), (0, 0.9)]
ASA = [(0, 0), (0.3, -0.5), (0.7, -0.85), (1.0, -0.9), (0.9, -0.6), (1.0, -0.45), (0.85, -0.3), (0.95, -0.1), (0.75, 0.0),
       (0.8, 0.2), (0.5, 0.15), (0.3, 0.25)]
PENA = [(0, -1)] + [(0.28 * math.sin(math.pi * u) * (1 - 0.3 * u), -1 + 2 * u) for u in np.linspace(0.05, 1, 10)] + \
       [(-0.28 * math.sin(math.pi * u) * (1 - 0.3 * u), -1 + 2 * u) for u in np.linspace(1, 0.05, 10)]
FOLHA = [(0, -1)] + [(0.45 * math.sin(math.pi * u), -1 + 2 * u) for u in np.linspace(0.05, 0.95, 10)] + [(0, 1)] + \
        [(-0.45 * math.sin(math.pi * u), -1 + 2 * u) for u in np.linspace(0.95, 0.05, 10)]
CARTA = [(-0.62, -0.9), (0.62, -0.9), (0.62, 0.9), (-0.62, 0.9)]
CRUZ = [(-0.2, -1), (0.2, -1), (0.2, -0.2), (1, -0.2), (1, 0.2), (0.2, 0.2), (0.2, 1), (-0.2, 1), (-0.2, 0.2), (-1, 0.2), (-1, -0.2),
        (-0.2, -0.2)]
SETA = [(1, 0), (0.3, -0.5), (0.3, -0.18), (-1, -0.18), (-1, 0.18), (0.3, 0.18), (0.3, 0.5)]
LUA = [(math.cos(a), math.sin(a)) for a in np.linspace(-2.3, 2.3, 18)] + \
      [(0.45 + 0.75 * math.cos(a), 0.8 * math.sin(a)) for a in np.linspace(1.85, -1.85, 14)]
OSSO = [(-1, -0.25), (-0.75, -0.4), (-0.6, -0.15), (0.6, -0.15), (0.75, -0.4), (1, -0.25), (0.85, 0), (1, 0.25), (0.75, 0.4),
        (0.6, 0.15), (-0.6, 0.15), (-0.75, 0.4), (-1, 0.25), (-0.85, 0)]
CHAVE = [(-1, -0.3), (-0.4, -0.3), (-0.4, -0.1), (0.5, -0.1), (0.5, 0.1), (0.35, 0.1), (0.35, 0.35), (0.2, 0.35), (0.2, 0.1),
         (-0.4, 0.1), (-0.4, 0.3), (-1, 0.3)]
NOTA = [(0.1, -1), (0.55, -0.75), (0.55, -0.5), (0.25, -0.65), (0.25, 0.55)] + \
       [(0.25 + 0.0 * 0, 0.55)] + [(-0.05 + 0.3 * math.cos(a), 0.6 + 0.22 * math.sin(a)) for a in np.linspace(0, TAU, 14)] + [(0.1, 0.55)]
MOEDA = circulo(24, 1.0)
GEMA = [(0, -1), (0.7, -0.35), (0.45, 0.8), (-0.45, 0.8), (-0.7, -0.35)]


def engrenagem(dentes=8, r=1.0, fundo=0.78):
    pts = []
    for k in range(dentes * 4):
        a = TAU * k / (dentes * 4)
        rr = r if (k % 4) in (1, 2) else r * fundo
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def flor(petalas=5, r=1.0, miolo=0.3):
    pts = []
    for k in range(petalas * 12):
        a = TAU * k / (petalas * 12)
        rr = miolo + (r - miolo) * abs(math.sin(petalas * a / 2))
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def estrela_pts(n=5, interno=0.45):
    return estrela(0, 0, 1.0, -math.pi / 2, n, interno)


# ---------------------------------------------------------------- desenhar
def icone(T, pts, k=1.0, cheio=0.35, borda=1.25, fino=0.007):
    """Uma forma acesa: o miolo translúcido e a borda brilhando. Devolve (G, H)."""
    if k <= 0:
        return 0.0, 0.0
    P = T.polys([(pts, 1.0)])
    B = _borda(T, P, fino)
    return (P * cheio + B * borda) * k, B * 0.45 * k


def cheio(T, pts, k=1.0):
    """A forma toda acesa (sólida)."""
    if k <= 0:
        return 0.0, 0.0
    P = T.polys([(pts, 1.0)], 0.004)
    return P * k, P * 0.35 * k


def contorno(pts, w=1.0):
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], w) for i in range(len(pts))]


def surge(t, a, b):
    """O tamanho de quem aparece: cresce passando um pouco do ponto e volta (0 → 1)."""
    u = rel(t, a, b)
    return back(u) if u > 0 else 0.0


# ---------------------------------------------------------------- movimentos
def aura(T, t, a, b, r=0.38, cy=0.0, forca=1.0):
    """O brilho que acende em volta de quem ativa."""
    k = pulso(t, a, b) * forca
    return T.gauss(0, cy, r, r * 1.15) * 0.55 * k, T.gauss(0, cy, r * 0.3) * 0.8 * k


def anel(T, t, a, b, r0=0.08, r1=0.7, w=0.035, cy=0.0, sq=1.0, forca=1.3):
    """Um anel que abre e some."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    return T.ring(r0 + (r1 - r0) * ease_out(u, 2.2), w * (1 - 0.5 * u), 0, cy, sq) * (1 - u) * forca


def onda_no_chao(T, t, a, b, r1=0.8, cy=0.38, forca=1.4):
    return anel(T, t, a, b, 0.1, r1, 0.035, cy, 3.0, forca)


def clarao(T, t, a, b, cx=0.0, cy=0.0, tam=0.8, forca=1.0):
    """O clarão em cruz do impacto. Devolve (G, H)."""
    k = pulso(t, a, b) * forca
    if k <= 0:
        return 0.0, 0.0
    return T.gauss(cx, cy, 0.22) * k * 1.3, (T.flare(cx, cy, tam * k + 0.01, 0.3, 0.014) + T.flare(cx, cy, tam * 0.6 * k + 0.01, 0.3 + math.pi / 4, 0.01)) * k * 1.5


def particulas(T, t, a, b, n, seed, cx=0.0, cy=0.0, espalha=0.3, sobe=0.6, sigma=0.013, vento=0.0):
    """Faíscas que sobem (sobe > 0) ou caem (sobe < 0) e somem."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        x0, y0, v, f = q.uniform(-espalha, espalha), q.uniform(-espalha, espalha) * 0.6, q.uniform(0.6, 1.2), q.uniform(0.4, 1)
        pts.append((cx + x0 + vento * u * v, cy + y0 - sobe * u * v, f * (1 - u)))
    return T.splats(pts, sigma) * 1.3


def estouro(T, t, a, b, n, seed, cx=0.0, cy=0.0, alcance=0.6, largura=0.012):
    """Riscos que saem do centro para fora (a explosão)."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    q = np.random.default_rng(seed)
    segs = []
    for _ in range(n):
        ang = q.uniform(0, TAU)
        d = alcance * q.uniform(0.6, 1)
        r1, r0 = d * ease_out(u, 2), d * ease_out(u, 2) * 0.55
        segs.append((cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), 1 - u))
    return T.tapered(segs, largura)


def converge(T, t, a, b, n, seed, cx=0.0, cy=0.0, alcance=0.7, largura=0.012):
    """Riscos que vêm de fora e entram no centro (carregando)."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    q = np.random.default_rng(seed)
    segs = []
    for _ in range(n):
        ang = q.uniform(0, TAU)
        d0 = alcance * (1 - ease_in(u, 1.6)) + 0.05
        d1 = d0 + 0.15 * (1 - u)
        segs.append((cx + d1 * math.cos(ang), cy + d1 * math.sin(ang), cx + d0 * math.cos(ang), cy + d0 * math.sin(ang), 0.5 + 0.5 * u))
    return T.tapered(segs, largura)


def orbita(T, t, pts, n, r, vel, s, cx=0.0, cy=0.0, sq=0.45, k=1.0, gira_forma=False):
    """n formas girando em volta (num círculo achatado: parece de pé no chão)."""
    G, H = 0.0, 0.0
    for j in range(n):
        ang = TAU * j / n + vel * t
        g, h = icone(T, poe(pts, cx + r * math.cos(ang), cy + r * math.sin(ang) * sq, s * (0.85 + 0.15 * math.sin(ang)), ang if gira_forma else 0), k)
        G, H = G + g, H + h
    return G, H


def chuva(T, t, a, b, pts, n, seed, s=0.06, de=-0.95, ate=0.3, espalha=0.6, gira=0.0, k=1.0):
    """Formas caindo do alto até o chão, cada uma no seu tempo."""
    G, H = 0.0, 0.0
    q = np.random.default_rng(seed)
    for j in range(n):
        x, atraso, ang = q.uniform(-espalha, espalha), q.uniform(0, 0.4), q.uniform(0, TAU)
        u = rel(t, a + (b - a) * atraso, a + (b - a) * (atraso + 0.6))
        if 0 < u < 1:
            y = de + (ate - de) * ease_in(u, 1.5)
            g, h = icone(T, poe(pts, x, y, s, ang + gira * u), k * (1 - rel(u, 0.85, 1)))
            G, H = G + g, H + h
    return G, H


def voa(T, t, a, b, pts, x0, y0, x1, y1, s=0.1, gira=0.0, rastro=True, k=1.0):
    """Uma forma voando de (x0, y0) até (x1, y1), com o rastro atrás. Devolve (G, H, chegou)."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0, 0.0, u >= 1
    e = ease_in(u, 1.4)
    x, y = x0 + (x1 - x0) * e, y0 + (y1 - y0) * e
    ang = math.atan2(y1 - y0, x1 - x0)
    g, h = icone(T, poe(pts, x, y, s, ang + gira * u), k)
    if rastro:
        xr, yr = x0 + (x1 - x0) * max(0, e - 0.25), y0 + (y1 - y0) * max(0, e - 0.25)
        g = g + T.tapered([(xr, yr, x, y, 0.8)], s * 0.8) * k
    return g, h, False


def corte(T, t, a, b, ang, comp=1.1, larg=0.05, cx=0.0, cy=0.0, curva=0.0):
    """Um corte: a lâmina de luz que atravessa e some. Devolve (G, H)."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0, 0.0
    c, s = math.cos(ang), math.sin(ang)
    x1, y1 = cx - c * comp / 2, cy - s * comp / 2
    x2, y2 = cx + c * comp / 2, cy + s * comp / 2
    P = T.polys([(lamina(x1, y1, x2 + curva * -s, y2 + curva * c, larg * (1 - 0.6 * u), min(1, u * 2.2), max(0, u * 2 - 1)), 1.0)])
    return P * 1.3, P * 0.9


def raios(T, t, a, b, n, seed, cx=0.0, cy=0.0, r=0.45, largura=0.01):
    """Raios elétricos saindo do centro (mudam a cada quadro)."""
    k = pulso(t, a, b)
    if k <= 0:
        return 0.0
    q = np.random.default_rng(seed + int(t * 37))
    out = 0.0
    for _ in range(n):
        ang = q.uniform(0, TAU)
        out = out + T.polyline(jagged(q, cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang), 4, 0.3), largura)
    return out * k * 1.3


def runas(T, t, a, b, r=0.5, n=8, cy=0.0, sq=1.0, gira=1.5, forma=None, s=0.05):
    """O círculo mágico: dois anéis e as marcas (ou formas) girando entre eles."""
    abre = ease_out(rel(t, a, a + (b - a) * 0.35), 3)
    k = abre * (1 - rel(t, b - (b - a) * 0.25, b))
    if k <= 0:
        return 0.0, 0.0
    rr = r * abre
    G = (T.ring(rr, 0.018, 0, cy, sq) + T.ring(rr * 0.78, 0.01, 0, cy, sq) * 0.8) * k * 1.2
    H = 0.0
    segs = []
    for j in range(n):
        ang = TAU * j / n + gira * t
        x, y = rr * 0.89 * math.cos(ang), cy + rr * 0.89 * math.sin(ang) / sq
        if forma is None:
            segs += [(x - s * 0.5, y, x + s * 0.5, y, 1.0), (x, y - s * 0.5, x, y + s * 0.5, 1.0)]
        else:
            g, h = icone(T, poe(forma, x, y, s, ang + math.pi / 2), k)
            G, H = G + g, H + h
    if segs:
        G = G + T.lines(segs, 0.009) * k
    return G, H
