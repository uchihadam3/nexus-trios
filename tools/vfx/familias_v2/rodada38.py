"""Rodada 38 das habilidades próprias: Macaco Louco, Capitão Planeta, Inspetor Bugiganga, Danny Phantom, Coragem e Senhor Frio.

Macaco Louco
- robo_gigante_mojo: o punho do robô gigante com os parafusos descendo no rival (Exposto).
- raio_adaptador: o capacete disparando o raio colorido e o escudo no aliado (Escudo e Protegido).
- mojo_preparo: o Preparo do Discurso interminável — o capacete-cérebro e os balões de fala crescendo (laço).
- discurso_interminavel: os balões de fala sem fim cobrindo os rivais (Lento e Exposto).

Capitão Planeta
- poder_dos_aneis: os cinco anéis (fogo, água, terra, vento e coração) girando e virando escudo no trio (Protegido e Escudo).
- forca_da_natureza: o redemoinho de folhas e as raízes saindo do chão nos rivais (Enfraquecido e Lento).
- capitao_preparo: o Preparo do O poder é de vocês — os cinco raios se juntando no meio (laço).
- o_poder_e_de_voces: o planeta verde no alto, a luz curando o trio e o golpe nos rivais (Vida, Fortalecido e dano).

Inspetor Bugiganga
- braco_extensivel: o braço mecânico de gomos se esticando e a garra prendendo o rival (Preso e Lento).
- bugiganga_preparo: o Preparo do Vai, vai, Bugiganga! — o chapéu abrindo e as engenhocas saindo (laço).
- vai_vai_bugiganga: as engenhocas para todo lado — molas, guarda-chuvas e mãozinhas — em todos (Confuso e Preso).

Danny Phantom
- intangibilidade: o contorno fantasma transparente com as ondinhas e o escudo no aliado (Escudo, Acelerado e Lento).
- danny_preparo: o Preparo do Lamento fantasma — os dois anéis brancos da transformação (laço).
- lamento_fantasma: o grito fantasma em cone verde enorme varrendo todos (Silenciado e Enfraquecido).

Coragem
- grito_de_pavor: o grito de pavor em riscos tremidos e a cura no aliado (Vida, Escudo e o dano nele mesmo).
- correr_para_o_perigo: o Coragem correndo com as gotas de suor e a bolha protegendo o trio (Protegido e Regeneração).

Senhor Frio
- pistola_de_gelo: o feixe da pistola de gelo e o bloco de gelo se formando no rival (Congelado).
- armadura_de_gelo: as placas de cristal de gelo cobrindo o corpo e a névoa fria (Escudo e Protegido).
- frio_preparo: o Preparo do Zero absoluto — o capacete com a névoa e a pistola carregando (laço).
- zero_absoluto_frio: a onda de frio que congela tudo e os flocos (Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, CORACAO, ESCUDO, FOLHA, GOTA, anel, cheio, circulo, clarao, converge, estouro, estrela_pts, icone,
                         onda_no_chao, particulas, poe, surge)


def _tontas(T, t, a, b, cx, cy, n=3, r=0.12, s=0.035):
    G, H = 0.0, 0.0
    k = pulso(t, a, b)
    if k <= 0:
        return G, H
    for j in range(n):
        ang = t * 9 + TAU * j / n
        g, h = cheio(T, poe(estrela_pts(5, 0.45), cx + r * math.cos(ang), cy + r * 0.4 * math.sin(ang), s), k * 1.3)
        G, H = G + g, H + h
    return G, H


def _balao(T, cx, cy, s, k, seed=0):
    """O balão de fala com os rabiscos de texto dentro."""
    if k <= 0 or s <= 0.002:
        return 0.0, 0.0
    pts = [(cx + s * math.cos(a), cy + s * 0.6 * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
    pts = pts[:14] + [(cx - s * 0.2, cy + s * 0.9)] + pts[14:]
    g, h = icone(T, pts, k * 1.0, 0.35)
    q = np.random.default_rng(seed)
    linhas = []
    for m in range(3):
        y = cy - s * 0.25 + s * 0.25 * m
        x0 = cx - s * 0.6
        while x0 < cx + s * 0.5:
            w = q.uniform(0.1, 0.3) * s
            linhas.append((x0, y, x0 + w, y, 1.0))
            x0 += w + 0.06 * s
    return g + T.lines(linhas, s * 0.05) * k * 1.1, h


def _cristal(cx, cy, s, ang):
    pts = [(0, -1), (0.3, 0), (0, 1), (-0.3, 0)]
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + s * (x * c - y * sn), cy + s * (x * sn + y * c)) for x, y in pts]


def _floco(T, cx, cy, s, ang, k):
    segs = []
    for j in range(6):
        a = ang + TAU * j / 6
        x1, y1 = cx + s * math.cos(a), cy + s * math.sin(a)
        segs.append((cx, cy, x1, y1, 1.0))
        for lado in (-1, 1):
            xm, ym = cx + s * 0.6 * math.cos(a), cy + s * 0.6 * math.sin(a)
            segs.append((xm, ym, xm + s * 0.3 * math.cos(a + lado * 0.8), ym + s * 0.3 * math.sin(a + lado * 0.8), 0.8))
    return T.lines(segs, s * 0.08) * k * 1.3


# ------------------------------------------------------------------ Macaco Louco

def robo_gigante_mojo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.32), 2.4)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        y = -0.85 + 0.85 * desce
        P, nos = _punho(T, 0.35, y, 3.4, math.pi / 2)
        G += P * 0.95 * k
        H += nos * 0.45 * k
        for j in range(3):
            G += T.ring(0.025, 0.01, 0.2 + 0.15 * j, y - 0.2) * k * 1.3
        G += T.lines([(0.35, -1.0, 0.35, y - 0.25, 1.0)], 0.06) * k * 0.8
    g, h = clarao(T, t, 0.3, 0.52, 0.35, 0.1, 1.4, 1.4)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.9, 1.0, 0.35, 1.7)
    G += estouro(T, t, 0.32, 0.85, 16, 5, 0.35, 0.1, 0.6, 0.014)
    return G * env, H * env


def raio_adaptador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        G += T.arc_band(0.14 * s, 0.04, math.pi, TAU, 1.0, 0, -0.6, -0.1, 0.0) * 1.3
        G += T.gauss(-0.6, -0.15, 0.08 * s) * 0.9
    k = pulso(t, 0.15, 0.6)
    if k > 0:
        for j in range(3):
            dy = (j - 1) * 0.03
            G += T.tapered([(-0.5, -0.1 + dy, 0.55, 0.0 + dy, 1.0)], 0.03) * k * 1.1
        H += T.lines([(-0.5, -0.1, 0.55, 0.0, 1.0)], 0.01) * k * 1.4
    g, h = clarao(T, t, 0.25, 0.5, 0.55, 0.0, 0.8)
    G, H = G + g, H + h
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g2, h2 = icone(T, poe(ESCUDO, -0.3, 0.1, 0.16 * m), 1.1, 0.4)
        G, H = G + g2, H + h2
    return G * env, H * env


def mojo_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.arc_band(0.2, 0.05, math.pi, TAU, 1.0, 0, 0.0, 0.1, 0.0) * 1.2
    G += T.gauss(0, 0.0, 0.12) * (0.6 + 0.2 * math.sin(t * 8))
    u = (t * 1.5) % 1
    g, h = _balao(T, 0.15, -0.3, 0.08 + 0.12 * u, 1 - rel(u, 0.8, 1), int(t * 1.5))
    return G + g, H + h


def discurso_interminavel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(5)
    for j in range(9):
        a0 = 0.03 + 0.07 * j
        s = surge(t, a0, a0 + 0.2) * (1 - rel(t, 0.85, 1))
        x = -0.6 + q.uniform(0, 1.3)
        y = -0.55 + q.uniform(0, 0.5)
        g, h = _balao(T, x, y, 0.16 * s, 1.0 if s > 0 else 0, j)
        G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.5, 1.0)
        for m in range(2):
            u = ((t * 1.2) + m / 2) % 1
            G += T.lines([(x + 0.1 + 0.05 * m, 0.0 - 0.15 * u, x + 0.15 + 0.05 * m, 0.0 - 0.15 * u, 1.0),
                          (x + 0.15 + 0.05 * m, 0.0 - 0.15 * u, x + 0.1 + 0.05 * m, 0.05 - 0.15 * u, 1.0),
                          (x + 0.1 + 0.05 * m, 0.05 - 0.15 * u, x + 0.15 + 0.05 * m, 0.05 - 0.15 * u, 1.0)], 0.01) * k * (1 - u) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Capitão Planeta

def _simbolo_anel(T, j, cx, cy, s, k):
    """Os cinco anéis: fogo, água, terra, vento e coração."""
    if k <= 0:
        return 0.0, 0.0
    G = T.ring(s, s * 0.18, cx, cy) * k * 1.2
    formas = [CHAMA, GOTA, [(-1, 0.6), (0, -0.8), (1, 0.6)], None, CORACAO]
    f = formas[j]
    if f is None:
        g = T.arc_band(s * 0.55, s * 0.12, 0, 4.5, 1.0, 0, cx, cy, 0.8) * k * 1.2
        return G + g, 0.0
    g, h = cheio(T, poe(f, cx, cy, s * 0.55), k * 1.2)
    return G + g, h


def poder_dos_aneis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    junta = ease_in(rel(t, 0.35, 0.6), 2)
    for j in range(5):
        a = t * 3 + TAU * j / 5
        r = 0.4 * (1 - junta)
        s = surge(t, 0.03 * j, 0.2 + 0.03 * j) * (1 - rel(t, 0.58, 0.65))
        g, h = _simbolo_anel(T, j, r * math.cos(a), -0.2 + r * 0.6 * math.sin(a), 0.07 * s, 1.0 if s > 0 else 0)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.55, 0.72, 0.0, -0.2, 1.0)
    G, H = G + g2, H + h2
    for x in (-0.55, 0.0, 0.55):
        m = surge(t, 0.6, 0.8) * (1 - rel(t, 0.88, 1))
        if m > 0:
            G += T.arc_band(0.22 * m, 0.03, -2.6, -0.5, 1.0, 0, x, 0.3, 0.0) * 1.2
            G += T.gauss(x, 0.15, 0.15, 0.2) * m * 0.45
    return G * env, H * env


def forca_da_natureza(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(6)
    for j in range(16):
        a = q.uniform(0, TAU) + t * 6
        r = 0.2 + 0.7 * ease_out(rel(t, 0.0, 0.6)) * q.uniform(0.5, 1)
        g, h = icone(T, poe(FOLHA, r * math.cos(a), -0.1 + r * 0.5 * math.sin(a), 0.05, a), pulso(t, 0.0, 0.9) * 1.1, 0.6)
        G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        sobe = ease_out(rel(t, 0.35, 0.6), 2) * (1 - rel(t, 0.85, 1))
        if sobe > 0:
            for lado in (-1, 1):
                pts = [(x + lado * 0.08 + lado * 0.06 * math.sin(v * 6), 0.35 - 0.4 * sobe * v) for v in np.linspace(0, 1, 12)]
                G += T.polyline(pts, 0.018) * 1.2
    G += onda_no_chao(T, t, 0.35, 0.8, 0.95, 0.35, 1.3)
    return G * env, H * env


def capitao_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.55
        x0, y0 = 0.5 * math.cos(a), 0.3 + 0.5 * math.sin(a) * -1
        u = (t * 2 + j / 5) % 1
        G += T.tapered([(x0, y0 - 0.5, x0 * (1 - u), (y0 - 0.5) * (1 - u), 1.0)], 0.02) * 1.0
        g, h = _simbolo_anel(T, j, x0, y0 - 0.5, 0.05, 1.0)
        G, H = G + g, H + h
    H += T.gauss(0, 0, 0.05) * (1.4 + 0.6 * math.sin(t * 10))
    G += T.gauss(0, 0, 0.2) * 0.6
    return G, H


def o_poder_e_de_voces(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        r = 0.22 * s
        G += T.ring(r, 0.025, 0, -0.5) * 1.3
        for m, (dx, dy, rx) in enumerate(((-0.06, -0.05, 0.08), (0.08, 0.04, 0.06), (-0.02, 0.1, 0.05))):
            g, h = cheio(T, poe(circulo(14, 1.0, 0.7), dx * s * 2.5, -0.5 + dy * s * 2.5, rx * s * 2), 0.9)
            G, H = G + g, H + h
        G += T.gauss(0, -0.5, 0.4 * s) * 0.4
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.35, 0.95)
        G += T.gauss(x, 0.1, 0.15, 0.22) * k * 0.55
        G += particulas(T, t, 0.35, 0.95, 6, int(x * 10) + 30, x, 0.3, 0.12, 0.5, 0.012)
    for j in range(3):
        u = rel(t, 0.4 + 0.06 * j, 0.6 + 0.06 * j)
        if 0 < u < 1:
            x = 0.0 + 0.85 * ease_in(u)
            G += T.tapered([(x - 0.3, -0.35 + 0.35 * u - 0.1 * j, x, -0.3 + 0.3 * u, 1.0)], 0.04) * 1.2
    g2, h2 = clarao(T, t, 0.55, 0.75, 0.85, 0.0, 0.9)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Inspetor Bugiganga

def braco_extensivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.4), 2)
    volta = rel(t, 0.75, 0.9)
    alc = u * (1 - volta)
    if alc > 0.02:
        x0, x1 = -0.7, -0.7 + 1.25 * alc
        n = 6
        for m in range(n):
            a = x0 + (x1 - x0) * m / n
            b = x0 + (x1 - x0) * (m + 0.85) / n
            g, h = icone(T, [(a, -0.04 - 0.005 * m), (b, -0.04 - 0.005 * m), (b, 0.04 + 0.005 * m), (a, 0.04 + 0.005 * m)], 1.0, 0.5)
            G, H = G + g, H + h
        fecha = ease_in(rel(t, 0.35, 0.45), 2)
        for lado in (-1, 1):
            ab = 0.6 * (1 - fecha) + 0.15
            G += T.polyline([(x1, 0.0), (x1 + 0.1 * math.cos(lado * ab), 0.1 * math.sin(lado * ab)),
                             (x1 + 0.18 * math.cos(lado * ab * 0.4), 0.18 * math.sin(lado * ab * 0.4))], 0.018) * 1.3
    g2, h2 = clarao(T, t, 0.38, 0.55, 0.55, 0.0, 0.7)
    G, H = G + g2, H + h2
    m = surge(t, 0.42, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.02, 0.6, 0.0, 0.5) * 1.2
    return G * env, H * env


def bugiganga_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.25, 0.1, 0.25, 0.1, 1.0)], 0.03) * 1.1
    G += T.arc_band(0.15, 0.04, math.pi, TAU, 1.0, 0, 0.0, 0.08, 0.0) * 1.2
    a = t * 30
    G += T.lines([(0.0, -0.15, 0.0, -0.3, 1.0)], 0.015) * 1.2
    G += T.lines([(-0.25 * math.cos(a), -0.3 - 0.03 * math.sin(a), 0.25 * math.cos(a), -0.3 + 0.03 * math.sin(a), 1.0)], 0.02) * 1.2
    q = np.random.default_rng(int(t * 6))
    for _ in range(3):
        x = q.uniform(-0.3, 0.3)
        G += T.gauss(x, -0.05 - 0.2 * q.uniform(0, 1), 0.02) * 1.2
    return G, H


_GUARDA_CHUVA = [(-1, 0.1)] + [(math.cos(a), -0.1 - 0.8 * math.sin(a)) for a in np.linspace(math.pi, 0, 10)] + [(1, 0.1)]


def vai_vai_bugiganga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(9)
    for j in range(9):
        a = q.uniform(-math.pi, 0)
        u = rel(t, 0.03 * j, 0.5 + 0.03 * j)
        if not 0 < u < 1:
            continue
        r = 0.2 + 0.7 * ease_out(u)
        x, y = -0.5 + r * math.cos(a) * 1.3 + 0.5 * u, -0.1 + r * 0.7 * math.sin(a) + 0.4 * u * u
        k = 1 - rel(u, 0.8, 1)
        tipo = j % 3
        if tipo == 0:
            pts = [(x + 0.03 * (1 if m % 2 else -1), y + 0.02 * m) for m in range(7)]
            G += T.polyline(pts, 0.012) * k * 1.3
        elif tipo == 1:
            g, h = icone(T, poe(_GUARDA_CHUVA, x, y, 0.07, u * 4), k * 1.1, 0.5)
            G, H = G + g, H + h
        else:
            P, nos = _punho(T, x, y, 0.9, a)
            G += P * 0.8 * k
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.45, 0.6, x, 0.05, 0.5)
        G, H = G + g2, H + h2
        g3, h3 = _tontas(T, t, 0.55, 1.0, x, -0.25, 3, 0.1, 0.03)
        G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Danny Phantom

def intangibilidade(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.8)
    for m in range(4):
        dy = 0.03 * math.sin(t * 12 + m)
        G += T.ring(0.2 + 0.04 * m, 0.012, -0.55 + 0.03 * math.sin(t * 9 + m), 0.0 + dy, 0.5) * k * (1 - m / 4) * 1.2
    G += T.gauss(-0.55, 0.0, 0.12, 0.25) * k * 0.4
    m = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g, h = icone(T, poe(ESCUDO, 0.0, 0.05, 0.17 * m), 1.0, 0.35)
        G, H = G + g, H + h
    G += T.ring(0.15, 0.02, 0.55, 0.0) * pulso(t, 0.5, 1.0) * 0.8
    return G * env, H * env


def danny_preparo(T, t, rng):
    G, H = vazio(T)
    u = (t * 1.5) % 1
    for lado in (-1, 1):
        y = lado * 0.35 * (1 - u)
        G += T.ring(0.25, 0.025, 0.0, y, 4.0) * 1.3
        H += T.gauss(0.0, y, 0.25, 0.012) * 1.0
    G += T.gauss(0, 0, 0.15, 0.3) * 0.5
    return G, H


def lamento_fantasma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.05, 0.8)
    if k > 0:
        for j in range(5):
            v = ((t * 2.5) + j / 5) % 1
            r = 0.1 + 1.0 * v
            G += T.arc_band(r, 0.035 * (1 - 0.5 * v), -0.55, 0.55, 1.0, 0, -0.7, 0.0, 0.0) * k * (1 - v) * 1.4
        G += T.polys([([(-0.7, -0.03), (0.9, -0.55), (0.9, 0.55), (-0.7, 0.03)], 1.0)], 0.05) * k * 0.3
    for x in (-0.55, 0.0, 0.55):
        g, h = clarao(T, t, 0.3, 0.5, x + 0.2, 0.0, 0.4)
        G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Coragem

def grito_de_pavor(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.55)
    if k > 0:
        q = np.random.default_rng(int(t * 30))
        for j in range(10):
            a = TAU * j / 10
            r0, r1 = 0.12, 0.45 + 0.1 * math.sin(j * 3)
            pts = [(-0.4 + (r0 + (r1 - r0) * v) * math.cos(a) + q.normal(0, 0.012), -0.2 + (r0 + (r1 - r0) * v) * math.sin(a) * 0.8 + q.normal(0, 0.012))
                   for v in np.linspace(0, 1, 6)]
            G += T.polyline(pts, 0.012) * k * 1.3
    for j in range(3):
        u = ((t * 3) + j / 3) % 1
        g, h = cheio(T, poe(GOTA, -0.55 + 0.15 * j, -0.5 + 0.2 * u, 0.04), pulso(t, 0.0, 0.55) * (1 - u) * 1.3)
        G, H = G + g, H + h
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g2, h2 = icone(T, poe(CORACAO, 0.45, -0.25, 0.1 * s), 1.3, 0.5)
        G, H = G + g2, H + h2
    G += T.gauss(0.45, 0.0, 0.18, 0.25) * pulso(t, 0.45, 1.0) * 0.4
    return G * env, H * env


def correr_para_o_perigo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.45), 1.3)
    k = 1 - rel(t, 0.5, 0.65)
    if u > 0 and k > 0:
        x = -0.85 + 1.4 * u
        G += T.gauss(x, 0.15, 0.08, 0.06) * k * 1.0
        for m in range(4):
            G += T.lines([(x - 0.15 - 0.06 * m, 0.05 + 0.04 * m, x - 0.45 - 0.06 * m, 0.05 + 0.04 * m, 1.0)], 0.006) * k
        for j in range(2):
            g, h = cheio(T, poe(GOTA, x + 0.05 + 0.06 * j, 0.0 - 0.06 * math.sin(t * 20 + j), 0.03), k * 1.3)
            G, H = G + g, H + h
    s = ease_out(rel(t, 0.45, 0.7), 2) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.85 * s, 0.03, 0.0, 0.1, 2.2) * 1.2
        G += T.gauss(0, 0.1, 0.8 * s, 0.35 * s) * 0.25
    for x in (-0.55, 0.0, 0.55):
        G += particulas(T, t, 0.5, 1.0, 6, int(x * 10) + 40, x, 0.3, 0.12, 0.5, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Senhor Frio

def pistola_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.08, 0.55)
    if k > 0:
        G += T.tapered([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.07 * k + 0.01) * 1.3
        H += T.lines([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.014) * k * 1.6
        q = np.random.default_rng(int(t * 20))
        for _ in range(6):
            x = q.uniform(-0.6, 0.5)
            g, h = cheio(T, _cristal(x, q.normal(0, 0.05), 0.025, q.uniform(0, TAU)), k * 1.2)
            G, H = G + g, H + h
    s = surge(t, 0.35, 0.6) * (1 - rel(t, 0.88, 1))
    if s > 0:
        bloco = [(0.55 - 0.17 * s, -0.25), (0.55 + 0.15 * s, -0.28), (0.55 + 0.18 * s, 0.3), (0.55 - 0.15 * s, 0.32)]
        g2, h2 = icone(T, bloco, 1.1, 0.4)
        G, H = G + g2, H + h2
        G += T.lines([(0.5, -0.15, 0.58, 0.0, 1.0), (0.6, 0.05, 0.63, 0.2, 1.0)], 0.008) * s * 1.2
    g3, h3 = clarao(T, t, 0.3, 0.5, 0.55, 0.0, 0.8)
    return (G + g3) * env, (H + h3) * env


def armadura_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(4)
    for j in range(10):
        a = TAU * j / 10 + q.uniform(-0.15, 0.15)
        s = surge(t, 0.04 * j, 0.2 + 0.04 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            r = 0.3
            g, h = icone(T, _cristal(r * math.cos(a), r * math.sin(a), 0.12 * s, a), 1.1, 0.5)
            G, H = G + g, H + h
            H += T.gauss(r * math.cos(a), r * math.sin(a) - 0.04 * s, 0.01) * 1.5
    pts = [(q.normal(0, 0.3), 0.25 + q.normal(0, 0.08) - 0.2 * rel(t, 0.0, 1.0), pulso(t, 0.1, 1.0) * q.uniform(0.3, 0.7)) for _ in range(20)]
    G += T.splats(pts, 0.06) * 0.35
    G += anel(T, t, 0.4, 0.85, 0.1, 0.55, 0.03, 0.0)
    return G * env, H * env


def frio_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.17, 0.02, 0.0, -0.15) * 1.2
    G += T.gauss(0, -0.15, 0.12) * (0.5 + 0.2 * math.sin(t * 6))
    G += T.lines([(0.1, 0.2, 0.4, 0.2, 1.0)], 0.045) * 1.0
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    H += T.gauss(0.42, 0.2, 0.03 + 0.01 * b) * (1.5 + b)
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 8, int(t * 2), 0.42, 0.2, 0.25)
    for j in range(3):
        u = ((t * 1.2) + j / 3) % 1
        G += T.gauss(-0.1 + 0.1 * j, -0.35 - 0.2 * u, 0.04 + 0.04 * u) * (1 - u) * 0.6
    return G, H


def zero_absoluto_frio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            G += T.ring(0.05 + 1.0 * ease_out(u, 2), 0.05 * (1 - 0.6 * u), -0.6, 0.1, 1.0) * (1 - u) * 1.3
    q = np.random.default_rng(7)
    for j in range(12):
        x, y = q.uniform(-0.8, 0.9), q.uniform(-0.6, 0.3)
        a0 = 0.2 + 0.4 * (x + 0.8) / 1.7
        s = surge(t, a0, a0 + 0.2) * (1 - rel(t, 0.88, 1))
        if s > 0:
            G += _floco(T, x, y, 0.06 * s, t + j, 1.0)
    for x in (-0.55, 0.0, 0.55):
        s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
        if s > 0:
            for m in range(4):
                a = math.pi * (0.2 + 0.2 * m)
                g, h = cheio(T, _cristal(x + 0.12 * math.cos(a) * (m - 1.5), 0.3 - 0.08 * s, 0.07 * s, 0.2 * (m - 1.5)), 1.1)
                G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.9, 1.0, 0.35, 1.3)
    return G * env, H * env


REGISTRO = [
    ("robo_gigante_mojo", robo_gigante_mojo, GRANDE, "Macaco Louco · o punho do robô gigante", False),
    ("raio_adaptador", raio_adaptador, GRANDE, "Macaco Louco · o raio do capacete e o escudo", False),
    ("mojo_preparo", mojo_preparo, MEDIA, "Macaco Louco · o capacete e os balões (Preparo, laço)", True),
    ("discurso_interminavel", discurso_interminavel, GRANDE, "Macaco Louco · os balões de fala sem fim", False),
    ("poder_dos_aneis", poder_dos_aneis, GRANDE, "Capitão Planeta · os cinco anéis e o escudo", False),
    ("forca_da_natureza", forca_da_natureza, GRANDE, "Capitão Planeta · as folhas e as raízes", False),
    ("capitao_preparo", capitao_preparo, MEDIA, "Capitão Planeta · os cinco raios se juntando (Preparo, laço)", True),
    ("o_poder_e_de_voces", o_poder_e_de_voces, GRANDE, "Capitão Planeta · o planeta e a luz", False),
    ("braco_extensivel", braco_extensivel, GRANDE, "Inspetor Bugiganga · o braço de gomos e a garra", False),
    ("bugiganga_preparo", bugiganga_preparo, MEDIA, "Inspetor Bugiganga · o chapéu-hélice (Preparo, laço)", True),
    ("vai_vai_bugiganga", vai_vai_bugiganga, GRANDE, "Inspetor Bugiganga · as engenhocas para todo lado", False),
    ("intangibilidade", intangibilidade, GRANDE, "Danny Phantom · o contorno fantasma e o escudo", False),
    ("danny_preparo", danny_preparo, MEDIA, "Danny Phantom · os anéis da transformação (Preparo, laço)", True),
    ("lamento_fantasma", lamento_fantasma, GRANDE, "Danny Phantom · o grito fantasma em cone", False),
    ("grito_de_pavor", grito_de_pavor, GRANDE, "Coragem · o grito tremido e o coração", False),
    ("correr_para_o_perigo", correr_para_o_perigo, GRANDE, "Coragem · a corrida suada e a bolha no trio", False),
    ("pistola_de_gelo", pistola_de_gelo, GRANDE, "Senhor Frio · o feixe e o bloco de gelo", False),
    ("armadura_de_gelo", armadura_de_gelo, GRANDE, "Senhor Frio · as placas de cristal", False),
    ("frio_preparo", frio_preparo, MEDIA, "Senhor Frio · o capacete e a pistola carregando (Preparo, laço)", True),
    ("zero_absoluto_frio", zero_absoluto_frio, GRANDE, "Senhor Frio · a onda de frio e os flocos", False),
]
