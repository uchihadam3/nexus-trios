"""Rodada 27 das habilidades próprias: Gaara, Cell, Broly, Beerus, Mewtwo e Garou.

Gaara
- defesa_absoluta: a parede de areia sobe na frente do aliado, com os espinhos de areia (Escudo e Espinhos).
- escudo_de_areia: a armadura de areia cobre o aliado em camadas (Protegido).
- gaara_preparo: o Preparo do Funeral do deserto — a cabaça abrindo e a areia girando (laço).
- funeral_do_deserto: a areia engole o rival, aperta e esmaga (Preso e Exposto).

Cell
- absorcao_cell: a cauda com o ferrão crava e suga a energia (Enfraquecido, Silenciado e Roubo de vida).
- regeneracao_celular: as células verdes se refazendo e a aura (Vida e Fortalecido).
- cell_preparo: o Preparo da Forma perfeita — as asas de inseto e a aura dourada pulsando (laço).
- forma_perfeita: o Kamehameha perfeito em leque sobre todos (Enfraquecido).

Broly
- eraser_cannon: a esfera verde pequena que explode enorme.
- furia_lendaria: a aura verde do Lendário explodindo e os músculos (Acelerado e Fortalecido).
- broly_preparo: o Preparo do Gigantic Roar — a esfera verde crescendo na mão (laço).
- gigantic_roar: o rugido verde em ondas enormes sobre todos (Exposto).

Beerus
- esfera_da_destruicao: a esfera roxa e laranja do Hakai pequena e densa (Exposto).
- beerus_preparo: o Preparo da Ira do deus — o sol de destruição sobre o dedo (laço).
- ira_do_deus: o sol de destruição cai e apaga tudo (Silenciado).

Mewtwo
- psiquico_mewtwo: a onda psíquica azul em anéis e o rival flutuando (Confuso e Marcado).
- barreira_mewtwo: a barreira de hexágonos psíquicos sobre o trio (Escudo, Protegido e Refletir).
- mewtwo_preparo: o Preparo da Tempestade mental — os olhos brilhando e a energia girando (laço).
- tempestade_mental: a tempestade psíquica em espirais sobre todos (Confuso e Silenciado).

Garou
- contra_fluxo: o desvio em água fluindo e o contra-ataque que paralisa.
- cacador_de_herois: as garras do monstro rasgando em X (Enfraquecido e Fortalecido).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (ASA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao, particulas, poe, raios,
                         surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _graos(T, pts, sigma=0.012, k=1.3):
    return T.splats(pts, sigma) * k


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * j / 6), cy + r * math.sin(ang + TAU * j / 6)) for j in range(6)]


# ------------------------------------------------------------------ Gaara

def defesa_absoluta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.85, 1)
    q = np.random.default_rng(3)
    pts = []
    for _ in range(300):
        x = q.uniform(-0.5, 0.5)
        y = 0.4 - q.uniform(0, 0.9) * sobe
        pts.append((x + 0.02 * math.sin(y * 20 + t * 8), y, q.uniform(0.4, 1) * k))
    G += _graos(T, pts)
    for j in range(5):
        e = surge(t, 0.4 + 0.05 * j, 0.6 + 0.05 * j) * k
        if e > 0:
            x = -0.4 + 0.2 * j
            G += T.polys([([(x - 0.04, -0.45 * sobe + 0.4), (x + 0.04, -0.45 * sobe + 0.4), (x, -0.45 * sobe + 0.4 - 0.2 * e)], 1.0)]) * 1.2
    return G * env, H * env


def escudo_de_areia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(3):
        u = ease_out(rel(t, 0.1 * j, 0.4 + 0.1 * j), 2)
        if u > 0:
            r = 0.45 - 0.08 * j
            pts = [(r * math.cos(a), 0.0 + r * 1.1 * math.sin(a)) for a in np.linspace(-math.pi / 2, -math.pi / 2 + TAU * u, 40)]
            G += T.polyline(pts, 0.03) * k * 1.1
            q = np.random.default_rng(j)
            G += _graos(T, [(x + q.normal(0, 0.02), y + q.normal(0, 0.02), 0.8 * k) for x, y in pts], 0.01, 1.0)
    g, h = aura(T, t, 0.35, 1.0, 0.4, 0.0, 0.6)
    return (G + g) * env, (H + h) * env


def gaara_preparo(T, t, rng):
    G, H = vazio(T)
    cabaca = [(0.12 * math.cos(a), 0.15 + 0.16 * math.sin(a)) for a in np.linspace(0, TAU, 24, endpoint=False)]
    g, h = icone(T, cabaca, 1.0, 0.45)
    G, H = G + g, H + h
    g2, h2 = icone(T, [(0.07 * math.cos(a), -0.08 + 0.09 * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)], 1.0, 0.45)
    G, H = G + g2, H + h2
    q = np.random.default_rng(9)
    pts = []
    for _ in range(140):
        a = q.uniform(0, TAU) + t * 4 * q.uniform(0.7, 1.3)
        r = q.uniform(0.2, 0.5)
        pts.append((r * math.cos(a), 0.05 + r * 0.6 * math.sin(a), q.uniform(0.4, 1)))
    return G + _graos(T, pts), H


def funeral_do_deserto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(7)
    envolve = ease_out(rel(t, 0.0, 0.45), 2)
    aperta = ease_in(rel(t, 0.45, 0.65), 2)
    pts = []
    for _ in range(350):
        a = q.uniform(0, TAU) + t * 6
        r0 = q.uniform(0.2, 0.9)
        r = r0 * (1 - envolve) + 0.28 * envolve * (1 - 0.5 * aperta)
        pts.append((0.3 + r * math.cos(a), r * 1.2 * math.sin(a), q.uniform(0.4, 1) * (1 - rel(t, 0.8, 0.95))))
    G += _graos(T, pts)
    g, h = clarao(T, t, 0.6, 0.8, 0.3, 0.0, 1.0)
    G, H = G + g, H + h
    G += estouro(T, t, 0.6, 0.95, 18, 4, 0.3, 0.0, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Cell

def absorcao_cell(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.75, 0.9)
    if u > 0:
        pts = [(-0.6 + 1.2 * v * u, -0.25 * math.sin(math.pi * v) + 0.05 * math.sin(v * 12)) for v in np.linspace(0, 1, 30)]
        for i in range(len(pts) - 1):
            G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.05 * (1 - 0.6 * i / 30)) * k * 1.1
        tx, ty = pts[-1]
        G += T.polys([([(tx + 0.12, ty), (tx - 0.02, ty - 0.06), (tx - 0.02, ty + 0.06)], 1.0)]) * k * 1.3
    suga = rel(t, 0.35, 0.8)
    if 0 < suga < 1:
        for j in range(6):
            v = (suga * 1.5 + j / 6) % 1
            x = 0.6 - 1.2 * v
            y = -0.25 * math.sin(math.pi * (1 - v))
            G += T.gauss(x, y, 0.035) * 1.3
            H += T.gauss(x, y, 0.015) * 1.4
    return G * env, H * env


def regeneracao_celular(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(4)
    for j in range(14):
        a = q.uniform(0, TAU)
        r = q.uniform(0.1, 0.45)
        cresce = surge(t, 0.03 * j, 0.3 + 0.03 * j) * (1 - rel(t, 0.85, 1))
        if cresce > 0:
            G += T.ring(0.05 * cresce, 0.012, r * math.cos(a), r * math.sin(a)) * 1.2
            G += T.gauss(r * math.cos(a), r * math.sin(a), 0.02 * cresce + 0.001) * 0.8
    g, h = aura(T, t, 0.2, 1.0, 0.42, 0.0, 1.0)
    G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 30, 3, 0, 0, 0.5, 0.5, 0.012)
    return G * env, H * env


def cell_preparo(T, t, rng):
    G, H = vazio(T)
    bate = 0.15 * math.sin(t * 25)
    for lado in (-1, 1):
        asa = [(lado * x * 0.5, -0.1 + y * 0.45 + bate * x) for x, y in ASA]
        g, h = icone(T, asa, 0.6, 0.5)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.3, 0.4) * (0.5 + 0.2 * math.sin(t * 8))
    H += T.gauss(0, 0, 0.08) * 1.2
    return G, H


def forma_perfeita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.25, 16, 6, -0.6, 0.0, 0.35, 0.012)
    G += T.gauss(-0.6, 0.0, 0.1) * pulso(t, 0.0, 0.35) * 1.4
    u = ease_out(rel(t, 0.25, 0.45), 3)
    k = 1 - rel(t, 0.65, 0.85)
    if u > 0:
        for ang in (-0.35, 0.0, 0.35):
            x1, y1 = -0.6 + 1.6 * u * math.cos(ang), 1.6 * u * math.sin(ang) * 0.6
            G += T.lines([(-0.6, 0.0, x1, y1, 1.0)], 0.07) * 0.8 * k
            H += T.lines([(-0.6, 0.0, x1, y1, 1.0)], 0.02) * 1.3 * k
    for x, y in ((0.6, -0.25), (0.7, 0.0), (0.6, 0.25)):
        g, h = clarao(T, t, 0.4, 0.6, x, y, 0.6)
        G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Broly

def eraser_cannon(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.4)
    if 0 < u < 1:
        x = -0.6 + 1.2 * u
        G += T.gauss(x, 0.0, 0.06) * 1.5
        H += T.gauss(x, 0.0, 0.025) * 2.0
        G += T.tapered([(x - 0.3, 0.0, x, 0.0, 0.4)], 0.04)
    s = ease_out(rel(t, 0.38, 0.75), 2)
    k = 1 - rel(t, 0.7, 0.95)
    if s > 0:
        G += T.gauss(0.6, 0.0, 0.5 * s + 0.001) * 0.9 * k
        G += T.ring(0.5 * s, 0.05, 0.6, 0.0) * 1.2 * k
        H += T.gauss(0.6, 0.0, 0.2 * s + 0.001) * 1.2 * k
    G += estouro(T, t, 0.38, 0.9, 20, 3, 0.6, 0.0, 0.8, 0.016)
    return G * env, H * env


def furia_lendaria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.3, 0, 0, 1.2, 1.4)
    G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.1, 1.0, 0.5, -0.05, 1.4)
    G, H = G + g2, H + h2
    q = np.random.default_rng(int(t * 25))
    k = pulso(t, 0.15, 0.95)
    for _ in range(4):
        a = q.uniform(0, TAU)
        G += T.polyline(jagged(q, 0.2 * math.cos(a), 0.3 * math.sin(a), 0.5 * math.cos(a), 0.6 * math.sin(a), 3, 0.08), 0.015) * k * 1.2
    for j in range(8):
        a = -math.pi / 2 + (j - 3.5) * 0.25
        u = rel(t, 0.1, 0.9)
        G += T.tapered([(0.3 * math.cos(a), 0.3 * math.sin(a), (0.3 + 0.5 * u) * math.cos(a), (0.3 + 0.5 * u) * math.sin(a) - 0.2 * u, 1.0)], 0.03) * (1 - u) * 1.2
    return G * env, H * env


def broly_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 10)
    r = 0.12 + 0.05 * p
    G += T.gauss(0.15, -0.15, r) * 1.4
    H += T.gauss(0.15, -0.15, r * 0.4) * 2.0
    G += T.ring(r * 1.3, 0.015, 0.15, -0.15) * 1.2
    G += converge(T, (t * 1.3) % 1, 0.0, 1.0, 14, 5, 0.15, -0.15, 0.5, 0.01) * 0.8
    return G, H


def gigantic_roar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        a0 = 0.05 + 0.1 * j
        u = rel(t, a0, a0 + 0.55)
        if 0 < u < 1:
            r = 0.15 + 0.9 * ease_out(u)
            G += T.arc_band(r, 0.06 * (1 - 0.5 * u), -1.0, 1.0, 0.8, 0, -0.5, 0.0, 1.0) * (1 - u) * 1.6
    g, h = clarao(T, t, 0.05, 0.3, -0.5, 0.0, 0.9)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.2, 0.9, 1.0, 0.35, 1.5)
    return G * env, H * env


# ------------------------------------------------------------------ Beerus

def esfera_da_destruicao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25)
    u = rel(t, 0.25, 0.6)
    x = -0.4 + 1.0 * ease_in(u, 1.5) if u > 0 else -0.4
    k = 1 - rel(t, 0.6, 0.65)
    if k > 0:
        G += T.gauss(x, -0.1, 0.12 * s + 0.001) * 1.3 * k
        G += T.ring(0.14 * s, 0.03, x, -0.1) * 1.2 * k
        H += T.gauss(x, -0.1, 0.05 * s + 0.001) * 1.8 * k
        for j in range(3):
            a = t * 20 + j * TAU / 3
            G += T.gauss(x + 0.16 * math.cos(a), -0.1 + 0.16 * math.sin(a), 0.025) * k
    g, h = clarao(T, t, 0.58, 0.8, 0.6, -0.1, 1.2, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.58, 0.95, 16, 2, 0.6, -0.1, 0.5, 0.014)
    return G * env, H * env


def beerus_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 6)
    G += T.lines([(0.0, 0.4, 0.0, 0.05, 1.0)], 0.03) * 0.8
    G += T.gauss(0, -0.25, 0.22 + 0.04 * p) * 1.3
    G += T.ring(0.3 + 0.04 * p, 0.02, 0, -0.25) * 1.2
    H += T.gauss(0, -0.25, 0.08) * 1.8
    return G, H


def ira_do_deus(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    cai = ease_in(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.35, 0.45)
    if k > 0:
        y = -0.9 + 0.9 * cai
        G += T.gauss(0.2, y, 0.35) * 1.3 * k
        H += T.gauss(0.2, y, 0.15) * 1.6 * k
        G += T.ring(0.42, 0.04, 0.2, y) * 1.2 * k
    g, h = clarao(T, t, 0.33, 0.6, 0.2, 0.0, 1.6, 1.8)
    G, H = G + g, H + h
    apaga_tudo = pulso(t, 0.4, 0.95)
    G += T.gauss(0.2, 0.0, 0.9, 0.7) * apaga_tudo * 0.5
    G += anel(T, t, 0.35, 0.95, 0.1, 1.0, 0.06, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Mewtwo

def psiquico_mewtwo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        u = rel(t, 0.05 * j, 0.5 + 0.05 * j)
        if 0 < u < 1:
            x = -0.5 + 1.1 * ease_out(u)
            G += T.ring(0.15 + 0.25 * u, 0.035, x, 0.0, 1.4) * (1 - u) * 1.5
    sobe = ease_out(rel(t, 0.4, 0.8), 2)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        G += T.gauss(0.6, -0.2 * sobe, 0.18, 0.24) * 0.9 * k
        G += T.ring(0.3, 0.025, 0.6, -0.2 * sobe, 1.3) * k * 1.3
        H += T.ring(0.2, 0.005, 0.6, -0.2 * sobe, 1.3) * k
    return G * env, H * env


def barreira_mewtwo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.88, 1))
    for i in range(-3, 4):
        for j in range(-2, 3):
            cx = i * 0.14 + (0.07 if j % 2 else 0)
            cy = j * 0.12
            if cx * cx + cy * cy < (0.5 * s) ** 2:
                acesa = pulso(t, 0.1 + 0.03 * abs(i + j), 0.7 + 0.03 * abs(i - j))
                G += T.polyline(_hexagono(cx, cy, 0.07) + [_hexagono(cx, cy, 0.07)[0]], 0.008) * (0.6 + 0.6 * acesa)
    G += T.ring(0.55 * s, 0.03, 0, 0) * 1.2
    G += anel(T, t, 0.4, 0.9, 0.5, 0.75, 0.03, 0.0)
    return G * env, H * env


def mewtwo_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.08, -0.15, 0.03) * (1.5 + 0.5 * math.sin(t * 10))
        G += T.gauss(lado * 0.08, -0.15, 0.07) * 0.9
    for j in range(3):
        pts = _espiral(0, 0.05, 0.1, 0.45, 0.6, t * 5 + j * TAU / 3)
        G += T.polyline(pts, 0.012) * 1.1
    return G, H


def tempestade_mental(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.1, 0.95)
        for j in range(2):
            pts = _espiral(x, -0.05, 0.02, 0.22, 1.5, t * 8 + j * math.pi)
            G += T.polyline([(px, -0.05 + (py + 0.05) * 0.6) for px, py in pts], 0.014) * k * 1.3
    q = np.random.default_rng(int(t * 20))
    kk = pulso(t, 0.3, 0.85)
    for _ in range(3):
        x = q.uniform(-0.7, 0.7)
        G += T.polyline(jagged(q, x, -0.8, x + q.uniform(-0.2, 0.2), -0.1, 4, 0.08), 0.012) * kk * 1.1
    g, h = clarao(T, t, 0.0, 0.25, 0, -0.5, 0.6)
    G += T.gauss(0, -0.6, 0.9, 0.25) * 0.4 * pulso(t, 0.0, 0.9)
    return (G + g) * env, (H + h) * env


# ------------------------------------------------------------------ Garou

def contra_fluxo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        for j in range(3):
            a0 = math.pi + u * 3 + j * 0.4
            G += T.arc_band(0.35 + 0.1 * j, 0.045, a0, a0 + 2.0, 0.6, 0, -0.2, 0.0, 1.0) * (1 - u) * 1.5
    g, h = corte(T, t, 0.4, 0.6, 0.5, 1.0, 0.07, 0.45, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.45, 0.65, 0.5, 0.0, 0.9)
    G, H = G + g2, H + h2
    q = np.random.default_rng(int(t * 25))
    k = pulso(t, 0.5, 0.95)
    for _ in range(3):
        a = q.uniform(0, TAU)
        G += T.polyline(jagged(q, 0.5, 0.0, 0.5 + 0.3 * math.cos(a), 0.3 * math.sin(a), 3, 0.05), 0.01) * k * 1.1
    return G * env, H * env


def cacador_de_herois(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (a, t0) in enumerate(((0.7, 0.05), (-0.7, 0.2))):
        for m in range(3):
            g, h = corte(T, t, t0 + 0.02 * m, t0 + 0.35 + 0.02 * m, a, 1.4, 0.06, 0.1 + 0.08 * m * math.sin(a), 0.08 * m * math.cos(a))
            G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.25, 0.5, 0.1, 0.0, 1.1)
    G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.4, 1.0, 0.4, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


REGISTRO = [
    ("defesa_absoluta", defesa_absoluta, GRANDE, "Gaara · a parede de areia", False),
    ("escudo_de_areia", escudo_de_areia, GRANDE, "Gaara · a armadura de areia", False),
    ("gaara_preparo", gaara_preparo, MEDIA, "Gaara · a cabaça e a areia (Preparo, laço)", True),
    ("funeral_do_deserto", funeral_do_deserto, GRANDE, "Gaara · o funeral do deserto", False),
    ("absorcao_cell", absorcao_cell, GRANDE, "Cell · a cauda sugando", False),
    ("regeneracao_celular", regeneracao_celular, GRANDE, "Cell · as células se refazendo", False),
    ("cell_preparo", cell_preparo, MEDIA, "Cell · as asas e a aura (Preparo, laço)", True),
    ("forma_perfeita", forma_perfeita, GRANDE, "Cell · o Kamehameha em leque", False),
    ("eraser_cannon", eraser_cannon, GRANDE, "Broly · a esfera que explode enorme", False),
    ("furia_lendaria", furia_lendaria, GRANDE, "Broly · a aura do Lendário", False),
    ("broly_preparo", broly_preparo, MEDIA, "Broly · a esfera crescendo (Preparo, laço)", True),
    ("gigantic_roar", gigantic_roar, GRANDE, "Broly · o rugido em ondas", False),
    ("esfera_da_destruicao", esfera_da_destruicao, GRANDE, "Beerus · a esfera da destruição", False),
    ("beerus_preparo", beerus_preparo, MEDIA, "Beerus · o sol sobre o dedo (Preparo, laço)", True),
    ("ira_do_deus", ira_do_deus, GRANDE, "Beerus · o sol de destruição caindo", False),
    ("psiquico_mewtwo", psiquico_mewtwo, GRANDE, "Mewtwo · a onda psíquica", False),
    ("barreira_mewtwo", barreira_mewtwo, GRANDE, "Mewtwo · a barreira de hexágonos", False),
    ("mewtwo_preparo", mewtwo_preparo, MEDIA, "Mewtwo · os olhos e a energia (Preparo, laço)", True),
    ("tempestade_mental", tempestade_mental, GRANDE, "Mewtwo · a tempestade psíquica", False),
    ("contra_fluxo", contra_fluxo, GRANDE, "Garou · o desvio e o contra-ataque", False),
    ("cacador_de_herois", cacador_de_herois, GRANDE, "Garou · as garras em X", False),
]
