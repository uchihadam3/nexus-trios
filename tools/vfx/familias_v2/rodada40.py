"""Rodada 40 das habilidades próprias: Orihime, Aerith, Katara, Sailor Mercury, Kurama e Ken Masters.

Orihime Inoue
- santen_kesshun: as três fadas dos grampos formando o escudo em triângulo na frente do trio (Barreira e Escudo).
- souten_kisshun: a cúpula oval dourada entre as duas fadas, curando e desfazendo o mal (Vida e Purificar).
- orihime_preparo: o Preparo da Rejeição total — os seis grampos de flor brilhando em volta (laço).
- rejeicao_total: a cúpula dourada que gira ao contrário, "rejeitando" o que aconteceu, e o aliado levantando (Vida e Reviver).

Aerith
- cura_de_aerith: a matéria verde brilhando e as flores de luz caindo no aliado (Vida).
- esna: os anéis de luz branca subindo e a fita purificando o trio (Purificar e Protegido).
- aerith_preparo: o Preparo da Grande bênção — as mãos em prece e a matéria branca acesa no cabelo (laço).
- grande_bencao: a chuva de penas de luz e o pilar sagrado levantando o aliado (Vida e Reviver).

Katara
- chicote_de_agua_katara: o chicote de água em arco, com as gotas (Lento).
- cura_com_agua: a luva de água brilhando em volta das mãos e as gotas curando (Vida e Regeneração).
- katara_preparo: o Preparo da Prisão de gelo — a água subindo do chão em espiral (laço).
- prisao_de_gelo_katara: a água enrolando no rival e virando gelo (Congelado).

Sailor Mercury
- nevoa_de_bolhas: a névoa de bolhas cobrindo os rivais (Cego).
- spray_de_bolhas: o jato de bolhas no rival (Lento).
- mercury_preparo: o Preparo da Rapsódia aquática — o símbolo de Mercúrio e o anel de água (laço).
- rapsodia_aquatica: as cordas da harpa de água e a onda que congela no rival (Congelado).

Kurama
- chicote_de_rosas: o chicote de espinhos em arco e as pétalas (Sangrando).
- planta_comedora: a planta carnívora abrindo e mordendo o rival (Envenenado).
- kurama_preparo: o Preparo da Árvore da ilusão — a rosa girando e as pétalas em redemoinho (laço).
- arvore_da_ilusao: a árvore de galhos crescendo sobre o rival e as espirais de ilusão (Confuso).

Ken Masters
- hadouken_ken: as mãos juntas e a bola de energia voando no rival.
- tatsumaki_ken: o chute giratório com o redemoinho de fogo (Queimando).
- ken_preparo: o Preparo do Shinryuken — o punho pegando fogo, agachado (laço).
- shinryuken: o gancho subindo como um dragão de fogo em espiral (Queimando).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, CORACAO, FOLHA, GOTA, PENA, anel, aura, cheio, chuva, circulo, clarao, converge, estouro, estrela_pts, flor, icone,
                         onda_no_chao, particulas, poe, surge)


def _cristal(cx, cy, s, ang):
    pts = [(0, -1), (0.3, 0), (0, 1), (-0.3, 0)]
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + s * (x * c - y * sn), cy + s * (x * sn + y * c)) for x, y in pts]


def _fadinha(T, cx, cy, s, k):
    """A fadinha dos grampos: o corpinho e as duas asinhas."""
    g = T.gauss(cx, cy, s * 0.4) * k * 1.3
    for lado in (-1, 1):
        g = g + T.gauss(cx + lado * s * 0.6, cy - s * 0.2, s * 0.45, s * 0.25) * k * 0.7
    return g, T.gauss(cx, cy, s * 0.2) * k * 1.6


def _bolhas(T, pts, k):
    G = 0.0
    for x, y, r in pts:
        G = G + T.ring(r, max(0.004, r * 0.15), x, y) * k * 1.2 + T.gauss(x - r * 0.35, y - r * 0.35, r * 0.2) * k * 1.0
    return G


# ------------------------------------------------------------------ Orihime

def santen_kesshun(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.1, 0.45), 2.2)
    k = 1 - rel(t, 0.88, 1)
    vert = [(0.6, -0.55 * abre - 0.05), (0.8, 0.3 * abre), (0.4, 0.3 * abre)]
    for j, (x, y) in enumerate(vert):
        s = surge(t, 0.04 * j, 0.2 + 0.04 * j)
        if s > 0:
            g, h = _fadinha(T, x, y, 0.05 * s, k)
            G, H = G + g, H + h
    if abre > 0.05:
        G += T.polys([(vert, 1.0)], 0.02) * k * 0.35
        G += T.polyline(vert + [vert[0]], 0.015) * k * 1.2
    for x in (-0.55, 0.0, 0.55):
        m = surge(t, 0.45, 0.65) * k
        if m > 0:
            G += T.arc_band(0.2 * m, 0.025, -2.6, -0.5, 1.0, 0, x, 0.3, 0.0) * 1.0
    return G * env, H * env


def souten_kisshun(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.1, 0.45), 2.2)
    k = 1 - rel(t, 0.88, 1)
    for lado in (-1, 1):
        g, h = _fadinha(T, lado * 0.32 * max(abre, 0.2), 0.0, 0.05, k * surge(t, 0.0, 0.2))
        G, H = G + g, H + h
    if abre > 0.05:
        G += T.ring(0.3 * abre, 0.02, 0.0, 0.0, 1.6) * k * 1.2
        G += T.gauss(0, 0.0, 0.28 * abre, 0.17 * abre) * k * 0.7
        H += T.gauss(0, 0.0, 0.1 * abre, 0.06 * abre) * k * 0.6
    G += particulas(T, t, 0.35, 1.0, 18, 4, 0, 0.1, 0.25, 0.5, 0.012)
    q = np.random.default_rng(3)
    for j in range(5):
        w = rel(t, 0.5 + 0.05 * j, 0.95)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            G += T.gauss(0.5 * math.cos(a) * (1 + w), 0.3 * math.sin(a) * (1 + w), 0.02) * (1 - w) * 1.0
    return G * env, H * env


def orihime_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(6):
        a = TAU * j / 6 + t * 1.5
        b = 0.5 + 0.5 * math.sin(t * TAU * 2 + j)
        g, h = icone(T, poe(flor(6, 1.0, 0.3), 0.25 * math.cos(a), 0.15 * math.sin(a), 0.045), 1.0 + 0.3 * b, 0.6)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.18) * 0.5
    return G, H


def rejeicao_total(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2.2)
    k = 1 - rel(t, 0.85, 1)
    if abre > 0:
        for j in range(3):
            a0 = -t * 6 * (1 + 0.3 * j)
            G += T.arc_band(0.25 + 0.08 * j, 0.02, a0, a0 + 4.0, 0.7, 0, 0.0, 0.05, 1.0) * abre * k * 1.1
        G += T.gauss(0, 0.05, 0.35 * abre, 0.25 * abre) * k * 0.5
        for j in range(12):
            a = -TAU * j / 12 - t * 4
            G += T.lines([(0.3 * math.cos(a), 0.05 + 0.21 * math.sin(a), 0.36 * math.cos(a), 0.05 + 0.25 * math.sin(a), 1.0)], 0.008) * abre * k * 1.2
    sobe = ease_out(rel(t, 0.45, 0.8), 2)
    if sobe > 0:
        G += T.gauss(0.0, 0.3 - 0.35 * sobe, 0.06, 0.12) * k * 1.0
        H += T.gauss(0.0, 0.3 - 0.35 * sobe, 0.03) * k * 1.4
    G += particulas(T, t, 0.4, 1.0, 22, 6, 0, 0.2, 0.4, 0.8, 0.012)
    G += onda_no_chao(T, t, 0.4, 0.9, 0.8, 0.35, 1.2)
    return G * env, H * env


# ------------------------------------------------------------------ Aerith

def _materia(T, cx, cy, s, k):
    G = T.gauss(cx, cy, s) * k * 1.3 + T.ring(s, s * 0.2, cx, cy) * k * 1.1
    return G, T.gauss(cx - s * 0.3, cy - s * 0.3, s * 0.3) * k * 1.8


def cura_de_aerith(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.6))
    if s > 0:
        g, h = _materia(T, -0.5, -0.2, 0.06 * s, 1.0)
        G, H = G + g, H + h
    g2, h2 = chuva(T, t, 0.15, 0.85, flor(5, 1.0, 0.35), 12, 4, 0.05, -0.85, 0.25, 0.4, 2.0, 1.2)
    G, H = G + g2 * 1.0, H + h2
    g3, h3 = aura(T, t, 0.3, 1.0, 0.35, 0.05, 0.9)
    G, H = G + g3, H + h3
    G += anel(T, t, 0.45, 0.9, 0.1, 0.55, 0.03, 0.1)
    return G * env, H * env


def esna(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for x in (-0.55, 0.0, 0.55):
        for j in range(3):
            u = rel(t, 0.05 + 0.1 * j, 0.5 + 0.1 * j)
            if 0 < u < 1:
                G += T.ring(0.18, 0.018, x, 0.3 - 0.6 * u, 3.0) * (1 - u) * 1.3
        m = pulso(t, 0.35, 1.0)
        G += T.gauss(x, 0.1, 0.13, 0.2) * m * 0.45
    u = rel(t, 0.1, 0.8)
    if 0 < u < 1:
        pts = [(-0.85 + 1.7 * v, -0.1 + 0.12 * math.sin(v * 10 + t * 8)) for v in np.linspace(0, u, 30)]
        G += T.polyline(pts, 0.014) * (1 - rel(t, 0.8, 0.95)) * 1.2
    G += particulas(T, t, 0.3, 1.0, 20, 5, 0, 0.0, 0.8, 0.6, 0.011)
    return G * env, H * env


def aerith_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        G += T.lines([(lado * 0.08, 0.15, 0.0, -0.05, 1.0)], 0.03) * 1.0
    g, h = _materia(T, 0.0, -0.3, 0.045 * (1 + 0.2 * math.sin(t * TAU * 2)), 1.2)
    G, H = G + g, H + h
    G += T.gauss(0, -0.1, 0.3) * (0.3 + 0.15 * math.sin(t * 8))
    G += converge(T, (t * 1.5) % 1, 0.0, 1.0, 8, int(t * 1.5), 0.0, -0.3, 0.35)
    return G, H


def grande_bencao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = chuva(T, t, 0.0, 0.9, PENA, 16, 8, 0.06, -0.95, 0.3, 0.85, 1.5, 1.1)
    G, H = G + g, H + h
    k = pulso(t, 0.3, 0.9)
    if k > 0:
        G += T.gauss(0.0, -0.2, 0.12, 0.7) * k * 0.9
        H += T.gauss(0.0, -0.2, 0.04, 0.6) * k * 0.6
    for x in (-0.55, 0.0, 0.55):
        G += T.gauss(x, 0.1, 0.14, 0.2) * pulso(t, 0.4, 1.0) * 0.5
    sobe = ease_out(rel(t, 0.5, 0.85), 2)
    if sobe > 0:
        G += T.gauss(0.0, 0.3 - 0.35 * sobe, 0.06, 0.12) * (1 - rel(t, 0.88, 1)) * 1.0
    G += onda_no_chao(T, t, 0.4, 0.95, 0.95, 0.35, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ Katara

def chicote_de_agua_katara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.5)
    if 0 < u < 1:
        cab = ease_out(u, 1.5)
        pts = []
        for m in range(33):
            v = cab * m / 32
            onda = 0.2 * math.sin(math.pi * v) * math.sin(v * 6 - u * 9) * (1 - u)
            pts.append((-0.75 + 1.35 * v, -0.2 * math.sin(math.pi * v) + onda))
        G += T.polyline(pts, 0.05) * (1 - rel(u, 0.8, 1)) * 1.1
        H += T.polyline(pts, 0.012) * (1 - rel(u, 0.8, 1)) * 1.0
    g, h = clarao(T, t, 0.42, 0.6, 0.6, 0.0, 0.8)
    G, H = G + g, H + h
    q = np.random.default_rng(4)
    for j in range(10):
        w = rel(t, 0.45, 0.9)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0)
            r = 0.1 + 0.35 * w * q.uniform(0.5, 1)
            g2, h2 = cheio(T, poe(GOTA, 0.6 + r * math.cos(a), r * math.sin(a) + 0.3 * w * w, 0.03), (1 - w) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


def cura_com_agua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    for lado in (-1, 1):
        cx = -0.3 + lado * 0.1
        a = t * 8 * lado
        G += T.arc_band(0.08, 0.025, a, a + 4.5, 1.0, 0, cx, 0.05, 1.0) * k * 1.3
        H += T.gauss(cx, 0.05, 0.04) * k * 1.2
    u = rel(t, 0.25, 0.6)
    if 0 < u < 1:
        for j in range(4):
            x = -0.3 + 0.7 * u
            G += T.gauss(x, 0.05 - 0.15 * math.sin(math.pi * u) + 0.03 * j, 0.025) * 1.2
    g, h = aura(T, t, 0.5, 1.0, 0.3, 0.05, 0.9)
    G, H = G + g * 0.8, H + h
    G += T.gauss(0.4, 0.05, 0.15, 0.2) * pulso(t, 0.5, 1.0) * 0.5
    G += particulas(T, t, 0.5, 1.0, 12, 4, 0.4, 0.2, 0.15, 0.5, 0.012)
    return G * env, H * env


def katara_preparo(T, t, rng):
    G, H = vazio(T)
    pts = []
    for m in range(50):
        v = m / 49
        a = v * TAU * 2.5 + t * TAU * 1.5
        pts.append((0.18 * (1 - 0.4 * v) * math.cos(a), 0.35 - 0.6 * v + 0.05 * math.sin(a)))
    G += T.polyline(pts, 0.025) * 1.1
    G += T.ring(0.2, 0.02, 0, 0.35, 3.0) * 1.0
    H += T.gauss(0, -0.25, 0.03) * (1.2 + 0.5 * math.sin(t * 10))
    return G, H


def prisao_de_gelo_katara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.45)
    k = 1 - rel(t, 0.5, 0.6)
    if u > 0 and k > 0:
        pts = []
        for m in range(60):
            v = u * m / 59
            a = v * TAU * 3
            pts.append((0.45 + 0.18 * math.cos(a), 0.3 - 0.6 * v + 0.06 * math.sin(a)))
        G += T.polyline(pts, 0.035) * k * 1.1
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        bloco = [(0.45 - 0.2 * s, -0.3), (0.45 + 0.18 * s, -0.33), (0.45 + 0.21 * s, 0.33), (0.45 - 0.18 * s, 0.34)]
        g, h = icone(T, bloco, 1.1, 0.4)
        G, H = G + g, H + h
        for j in range(5):
            g2, h2 = cheio(T, _cristal(0.45 + 0.08 * (j - 2), -0.3 - 0.06 * s, 0.05 * s, 0.2 * (j - 2)), 1.1)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.45, 0.62, 0.45, 0.0, 0.8)
    return (G + g3) * env, (H + h3) * env


# ------------------------------------------------------------------ Sailor Mercury

def nevoa_de_bolhas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(7)
    espalha = ease_out(rel(t, 0.0, 0.5), 2)
    k = 1 - rel(t, 0.85, 1)
    pts = []
    for _ in range(30):
        x0, y0 = q.uniform(-0.2, 0.2), q.uniform(-0.1, 0.1)
        x1, y1 = q.uniform(-0.85, 0.85), q.uniform(-0.45, 0.25)
        pts.append((-0.6 + (x1 + 0.6) * espalha + x0 * (1 - espalha), y0 + (y1 - y0) * espalha, q.uniform(0.02, 0.05)))
    G += _bolhas(T, pts, k)
    G += T.gauss(0, -0.1, 0.8 * espalha + 0.05, 0.35 * espalha + 0.05) * k * 0.35
    return G * env, H * env


def spray_de_bolhas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.05, 0.6)
    q = np.random.default_rng(int(t * 20))
    if k > 0:
        pts = []
        for _ in range(16):
            v = q.uniform(0, 1)
            pts.append((-0.6 + 1.15 * v, q.normal(0, 0.04 + 0.05 * v), 0.015 + 0.03 * v))
        G += _bolhas(T, pts, k)
        G += T.tapered([(-0.6, 0.0, 0.55, 0.0, 1.0)], 0.05) * k * 0.4
    g, h = clarao(T, t, 0.25, 0.5, 0.55, 0.0, 0.8)
    G, H = G + g, H + h
    G += estouro(T, t, 0.3, 0.8, 12, 3, 0.55, 0.0, 0.4, 0.011)
    return G * env, H * env


def mercury_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    G += T.ring(0.07, 0.015, 0, -0.02) * (1.1 + 0.3 * b)
    G += T.arc_band(0.06, 0.015, math.pi * 1.15, math.pi * 1.85, 1.0, 0, 0.0, -0.12, 0.0) * 1.2
    G += T.lines([(0, 0.05, 0, 0.18, 1.0), (-0.05, 0.12, 0.05, 0.12, 1.0)], 0.015) * 1.2
    a = t * TAU
    G += T.arc_band(0.28, 0.025, a, a + 4.5, 1.0, 0, 0, 0, 1.0) * 1.0
    H += T.gauss(0, -0.02, 0.03) * (1.2 + b)
    return G, H


def rapsodia_aquatica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.45, 0.55))
    if s > 0:
        G += T.arc_band(0.25 * s, 0.025, math.pi * 0.6, math.pi * 1.4, 1.0, 0, -0.35, 0.0, 0.0) * 1.2
        cordas = [(-0.6 + 0.06 * m, -0.18 * s, -0.6 + 0.06 * m, 0.18 * s, 1.0) for m in range(5)]
        G += T.lines(cordas, 0.006) * (1.0 + 0.4 * math.sin(t * 40)) * 1.2
    u = ease_in(rel(t, 0.25, 0.55), 1.5)
    if 0 < u < 1:
        x = -0.4 + 0.9 * u
        G += T.arc_band(0.35, 0.07, -1.2, 1.2, 1.0, 0, x - 0.3, 0.0, 0.0) * 1.2
        H += T.arc_band(0.35, 0.015, -1.0, 1.0, 1.0, 0, x - 0.3, 0.0, 0.0) * 1.0
    g, h = clarao(T, t, 0.52, 0.7, 0.5, 0.0, 1.0)
    G, H = G + g, H + h
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(7):
            a = TAU * j / 7
            g2, h2 = icone(T, _cristal(0.5 + 0.13 * math.cos(a), 0.13 * math.sin(a), 0.08 * m, a + math.pi / 2), 1.1, 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Kurama

def chicote_de_rosas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        cab = ease_out(u, 1.5)
        pts = []
        for m in range(33):
            v = cab * m / 32
            pts.append((-0.75 + 1.35 * v, -0.25 * math.sin(math.pi * v) + 0.15 * math.sin(v * 7 - u * 10) * (1 - u)))
        G += T.polyline(pts, 0.02) * (1 - rel(u, 0.8, 1)) * 1.3
        espinhos = []
        for m in range(2, 32, 3):
            if m < len(pts):
                x, y = pts[m]
                espinhos.append((x, y, x + 0.025, y - 0.035, 1.0))
        if espinhos:
            G += T.lines(espinhos, 0.007) * (1 - rel(u, 0.8, 1)) * 1.3
    g, h = clarao(T, t, 0.38, 0.58, 0.6, 0.0, 0.9)
    G, H = G + g, H + h
    q = np.random.default_rng(6)
    for j in range(12):
        w = rel(t, 0.4 + 0.02 * j, 0.95)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            r = 0.1 + 0.4 * w
            g2, h2 = cheio(T, poe(FOLHA, 0.6 + r * math.cos(a), r * 0.7 * math.sin(a) + 0.2 * w, 0.035, a + w * 5), (1 - w) * 1.2)
            G, H = G + g2, H + h2
    return G * env, H * env


def planta_comedora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        G += T.polyline([(0.45 + 0.04 * math.sin(v * 6), 0.35 - 0.35 * sobe * v) for v in np.linspace(0, 1, 12)], 0.04) * k * 1.2
        fecha = ease_in(rel(t, 0.3, 0.45), 2)
        cy = 0.35 - 0.35 * sobe - 0.12
        ab = 0.7 * (1 - fecha) + 0.05
        for lado in (-1, 1):
            a = -math.pi / 2 + lado * ab
            boca = [(0.45, cy + 0.1)] + [(0.45 + 0.36 * math.cos(a + lado * 0.5 * v) * v * 1.1, cy + 0.1 + 0.36 * math.sin(a + lado * 0.5 * v) * v * 1.1)
                                         for v in np.linspace(0.2, 1, 8)]
            g, h = icone(T, boca + [(0.45, cy + 0.1)], k * 1.1, 0.5)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.42, 0.6, 0.45, -0.1, 0.8)
    G, H = G + g2, H + h2
    m = pulso(t, 0.5, 1.0)
    for j in range(6):
        u = ((t * 1.5) + j / 6) % 1
        G += T.gauss(0.45 + 0.12 * math.sin(j * 2), -0.05 - 0.25 * u, 0.018) * m * (1 - u) * 1.2
    return G * env, H * env


def kurama_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(flor(5, 1.0, 0.4), 0, 0, 0.1, t * TAU), 1.2, 0.6)
    G, H = G + g, H + h
    for j in range(8):
        a = t * TAU * 1.2 + TAU * j / 8
        r = 0.18 + 0.12 * ((t + j / 8) % 1)
        g2, h2 = cheio(T, poe(FOLHA, r * math.cos(a), r * math.sin(a) * 0.7, 0.03, a), 1.1)
        G, H = G + g2, H + h2
    return G, H


def arvore_da_ilusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    cresce = ease_out(rel(t, 0.0, 0.55), 2)
    k = 1 - rel(t, 0.88, 1)
    if cresce > 0:
        segs = []

        def galho(x, y, ang, comp, nivel):
            if nivel > 4 or comp < 0.03:
                return
            fim = comp * min(1.0, max(0.0, cresce * 5 - nivel))
            if fim <= 0:
                return
            x2, y2 = x + fim * math.cos(ang), y + fim * math.sin(ang)
            segs.append((x, y, x2, y2, 1.0 - 0.15 * nivel))
            if fim >= comp * 0.99:
                galho(x2, y2, ang - 0.5, comp * 0.68, nivel + 1)
                galho(x2, y2, ang + 0.45, comp * 0.68, nivel + 1)
        galho(0.45, 0.35, -math.pi / 2, 0.3, 0)
        G += T.lines(segs, 0.016) * k * 1.3
    for j in range(3):
        a0 = t * 6 * (1 if j % 2 else -1)
        pts = [(0.45 + 0.03 * (a / 12) * 3 * math.cos(a + a0) * (1 + j * 0.4), -0.1 + 0.03 * (a / 12) * 3 * math.sin(a + a0) * (1 + j * 0.4))
               for a in np.linspace(0.3, 12, 40)]
        G += T.polyline(pts, 0.008) * pulso(t, 0.4, 1.0) * 1.1
    G += T.gauss(0.45, -0.1, 0.3) * pulso(t, 0.4, 1.0) * 0.3
    return G * env, H * env


# ------------------------------------------------------------------ Ken Masters

def hadouken_ken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.25, 10, 3, -0.65, 0.0, 0.25)
    for lado in (-1, 1):
        G += T.gauss(-0.7, lado * 0.06, 0.04) * pulso(t, 0.0, 0.35) * 1.0
    u = ease_in(rel(t, 0.22, 0.55), 1.3)
    k = 1 - rel(t, 0.55, 0.6)
    if 0 < u and k > 0:
        x = -0.6 + 1.15 * u
        G += T.gauss(x, 0.0, 0.1) * k * 1.4
        H += T.gauss(x, 0.0, 0.04) * k * 1.6
        G += T.ring(0.11, 0.025, x, 0.0) * k * 1.2
        for m in range(3):
            G += T.tapered([(x - 0.4 + 0.05 * m, -0.07 + 0.07 * m, x - 0.05, -0.04 + 0.04 * m, 1.0)], 0.04) * k * 0.8
    g, h = clarao(T, t, 0.53, 0.72, 0.55, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.55, 0.95, 14, 5, 0.55, 0.0, 0.5, 0.013)
    return G * env, H * env


def tatsumaki_ken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.55)
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        x = -0.5 + 0.9 * ease_out(min(u, 1))
        for m in range(3):
            a = t * 30 + m * 2.1
            G += T.arc_band(0.32, 0.07, a, a + 2.5, 0.35, 0, x, -0.05 + 0.08 * (m - 1), 1.0) * k * 1.3
        for j in range(5):
            a = t * 30 + j * 1.3
            g, h = icone(T, poe(CHAMA, x + 0.32 * math.cos(a), -0.05 + 0.11 * math.sin(a), 0.1), k * 1.1, 0.6)
            G, H = G + g, H + h * 1.4
    for j in range(3):
        g2, h2 = clarao(T, t, 0.2 + 0.12 * j, 0.32 + 0.12 * j, 0.45, -0.05, 0.6)
        G, H = G + g2, H + h2
    return G * env, H * env


def ken_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.05, 0.15, 2.0, -math.pi / 2)
    G += P * 0.85
    H += nos * 0.3
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.35
        tremula = 0.8 + 0.2 * math.sin(t * 30 + j)
        g, h = icone(T, poe(CHAMA, 0.05 + 0.15 * math.cos(a), 0.05 + 0.15 * math.sin(a), 0.07 * tremula), 1.1, 0.6)
        G, H = G + g, H + h * 1.5
    return G, H


def shinryuken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.05, 0.5), 2)
    k = 1 - rel(t, 0.7, 0.88)
    if sobe > 0 and k > 0:
        alto = 1.2 * sobe
        for j in range(18):
            v = j / 17
            if v > sobe:
                break
            a = v * TAU * 3 + t * 20
            y = 0.35 - alto * v
            r = 0.18 * (1 - 0.4 * v)
            g, h = icone(T, poe(CHAMA, 0.45 + r * math.cos(a), y, 0.08 * (1 - 0.3 * v)), k * 1.0, 0.6)
            G, H = G + g, H + h * 1.3
        G += T.gauss(0.45, 0.35 - alto * 0.5, 0.12, 0.45 * sobe + 0.01) * k * 0.6
        P, nos = _punho(T, 0.45, 0.35 - alto, 2.0, -math.pi / 2)
        G += P * 0.9 * k
        H += nos * 0.4 * k
    g2, h2 = clarao(T, t, 0.12, 0.35, 0.45, 0.0, 1.3, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.05, 0.5, 0.6, 0.35, 1.3)
    G += particulas(T, t, 0.3, 1.0, 22, 6, 0.45, -0.2, 0.25, 0.8, 0.012)
    return G * env, H * env


REGISTRO = [
    ("santen_kesshun", santen_kesshun, GRANDE, "Orihime · as três fadas e o escudo em triângulo", False),
    ("souten_kisshun", souten_kisshun, GRANDE, "Orihime · a cúpula oval que cura", False),
    ("orihime_preparo", orihime_preparo, MEDIA, "Orihime · os grampos de flor brilhando (Preparo, laço)", True),
    ("rejeicao_total", rejeicao_total, GRANDE, "Orihime · a cúpula girando ao contrário", False),
    ("cura_de_aerith", cura_de_aerith, GRANDE, "Aerith · a matéria verde e as flores de luz", False),
    ("esna", esna, GRANDE, "Aerith · os anéis de luz e a fita", False),
    ("aerith_preparo", aerith_preparo, MEDIA, "Aerith · a prece e a matéria branca (Preparo, laço)", True),
    ("grande_bencao", grande_bencao, GRANDE, "Aerith · a chuva de penas e o pilar sagrado", False),
    ("chicote_de_agua_katara", chicote_de_agua_katara, GRANDE, "Katara · o chicote de água", False),
    ("cura_com_agua", cura_com_agua, GRANDE, "Katara · a luva de água curando", False),
    ("katara_preparo", katara_preparo, MEDIA, "Katara · a água subindo em espiral (Preparo, laço)", True),
    ("prisao_de_gelo_katara", prisao_de_gelo_katara, GRANDE, "Katara · a água virando gelo no rival", False),
    ("nevoa_de_bolhas", nevoa_de_bolhas, GRANDE, "Sailor Mercury · a névoa de bolhas", False),
    ("spray_de_bolhas", spray_de_bolhas, GRANDE, "Sailor Mercury · o jato de bolhas", False),
    ("mercury_preparo", mercury_preparo, MEDIA, "Sailor Mercury · o símbolo e o anel de água (Preparo, laço)", True),
    ("rapsodia_aquatica", rapsodia_aquatica, GRANDE, "Sailor Mercury · a harpa e a onda que congela", False),
    ("chicote_de_rosas", chicote_de_rosas, GRANDE, "Kurama · o chicote de espinhos e as pétalas", False),
    ("planta_comedora", planta_comedora, GRANDE, "Kurama · a planta carnívora mordendo", False),
    ("kurama_preparo", kurama_preparo, MEDIA, "Kurama · a rosa girando e as pétalas (Preparo, laço)", True),
    ("arvore_da_ilusao", arvore_da_ilusao, GRANDE, "Kurama · a árvore de galhos e as espirais", False),
    ("hadouken_ken", hadouken_ken, GRANDE, "Ken · as mãos juntas e a bola de energia", False),
    ("tatsumaki_ken", tatsumaki_ken, GRANDE, "Ken · o chute giratório de fogo", False),
    ("ken_preparo", ken_preparo, MEDIA, "Ken · o punho pegando fogo (Preparo, laço)", True),
    ("shinryuken", shinryuken, GRANDE, "Ken · o gancho em espiral de fogo", False),
]
