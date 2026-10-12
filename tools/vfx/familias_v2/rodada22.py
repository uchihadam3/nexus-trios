"""Rodada 22 das habilidades próprias: Bowser, Ryu, Chun-Li, Akuma, Scorpion e Sub-Zero.

Bowser
- investida_de_casco: o casco de espinhos girando em direção ao rival e o tranco que prende (Preso).
- sopro_flamejante: o rugido e o sopro de fogo largo; o casco brilha (Escudo, Fortalecido e Provocado).
- bowser_preparo: o Preparo do Tremor do rei — Bowser no ar, a sombra crescendo no chão (laço).
- tremor_do_rei: a queda do Bowser: o chão racha, as pedras pulam e todos ficam tontos (Paralisado).

Ryu
- hadouken_ryu: as mãos juntas e a bola azul do Hadouken voando, com as chamas (Queimando).
- ryu_preparo: o Preparo do Shinku Hadouken — a energia azul crescendo entre as mãos (laço).
- shinku_hadouken: o feixe enorme do Shinku Hadouken atravessando com os anéis.

Chun-Li
- spinning_bird_kick: as pernas girando de cabeça para baixo como hélice, avançando.
- kikosho: a bola de energia azul que explode em volta dela e paralisa.

Akuma
- gou_hadouken: o Hadouken roxo-escuro do Satsui no Hado (Enfraquecido).
- ashura_senku: o deslizar fantasma (as imagens que somem) e o golpe (Exposto).

Scorpion
- teleporte_infernal: o fogo do inferno some e reaparece atrás do rival, com o golpe (Queimando).
- scorpion_preparo: o Preparo do Toasty — a máscara caindo e a caveira em chamas (laço).
- toasty: a caveira cospe o fogo do inferno no rival (Exposto).

Sub-Zero
- lanca_de_gelo: a lança de gelo voando e o rival ficando azul (Lento).
- clone_congelado: o clone de gelo do Sub-Zero se forma e o rival bate nele e congela (Congelado).
- subzero_preparo: o Preparo do Inverno absoluto — o frio juntando nas mãos (laço).
- inverno_absoluto: o raio congelante e os cristais enormes prendendo o rival (Preso).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao, particulas, poe, raios,
                         surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _cranio(cx, cy, s):
    return [(cx + 0.17 * s * math.cos(a), cy + 0.2 * s * math.sin(a)) for a in np.linspace(math.pi * 0.85, math.pi * 2.15, 16)] + \
        [(cx + 0.1 * s, cy + 0.17 * s), (cx - 0.1 * s, cy + 0.17 * s)]


def _cristal(cx, cy, s, ang):
    return poe([(0, -1), (0.3, -0.3), (0.2, 0.6), (-0.2, 0.6), (-0.3, -0.3)], cx, cy, s, ang)


# ------------------------------------------------------------------ Bowser

def _casco(T, cx, cy, s, giro):
    G, H = vazio(T)
    g, h = icone(T, poe(_circ(24), cx, cy, 0.18 * s), 1.1, 0.55)
    G, H = G + g, H + h
    for j in range(6):
        a = giro + TAU * j / 6
        g2, h2 = cheio(T, poe([(0, -1), (0.35, 0), (-0.35, 0)], cx + 0.17 * s * math.cos(a), cy + 0.17 * s * math.sin(a), 0.08 * s, a + math.pi / 2), 1.3)
        G, H = G + g2, H + h2
    return G, H


def investida_de_casco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.45)
    if u < 1:
        x = -0.75 + 1.3 * ease_in(u, 1.5)
        g, h = _casco(T, x, 0.1, 1.2, t * 30)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.6, 0.1, x - 0.15, 0.1, 0.5)], 0.08) * 0.8
    g2, h2 = clarao(T, t, 0.42, 0.6, 0.55, 0.1, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.42, 0.8, 14, 4, 0.55, 0.1, 0.55, 0.015)
    G += anel(T, t, 0.42, 0.9, 0.08, 0.5, 0.04, 0.1)
    return G * env, H * env


def sopro_flamejante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(4)
    u = rel(t, 0.1, 0.85)
    if 0 < u < 1:
        for j in range(30):
            v = (u * 1.3 + j / 30) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            x = -0.5 + 1.3 * v
            y = q.normal(0, 0.12) * v
            g, h = icone(T, poe(CHAMA, x, y, 0.06 + 0.16 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.2, 1.0, 0.4, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


def bowser_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 6)
    G += T.gauss(0, 0.4, 0.35 * (0.6 + 0.4 * p), 0.06 * (0.6 + 0.4 * p)) * 0.8
    g, h = _casco(T, 0, -0.4 - 0.05 * p, 0.8, t * 4)
    return G + g, H + h


def tremor_do_rei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    cai = ease_in(rel(t, 0.0, 0.2), 2)
    if t < 0.25:
        g, h = _casco(T, 0, -0.7 + 0.95 * cai, 1.4, 0)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.2, 0.4, 0, 0.3, 1.2, 1.4)
    G, H = G + g2, H + h2
    r = ease_out(rel(t, 0.2, 0.6), 2)
    if r > 0:
        q = np.random.default_rng(7)
        for j in range(7):
            a = math.pi * j / 6
            pts = [(0, 0.3)]
            for k in range(1, 5):
                d = 0.9 * r * k / 4
                pts.append((d * math.cos(a) + q.normal(0, 0.03), 0.3 + 0.25 * d * math.sin(a) * 0.5 + q.normal(0, 0.01)))
            G += T.polyline(pts, 0.015) * (1 - rel(t, 0.85, 1)) * 1.4
    q2 = np.random.default_rng(9)
    for j in range(10):
        u = rel(t, 0.22, 0.75)
        if 0 < u < 1:
            x = q2.uniform(-0.8, 0.8)
            y = 0.3 - 0.6 * math.sin(math.pi * u) * q2.uniform(0.4, 1)
            g3, h3 = cheio(T, poe([(-1, -0.6), (1, -0.8), (0.8, 0.7), (-0.9, 0.6)], x, y, 0.04, u * 6 + j), 1.2)
            G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.2, 0.8, 1.0, 0.32, 1.8)
    return G * env, H * env


# ------------------------------------------------------------------ Ryu

def _bola(T, x, y, r, t, k=1.0):
    G = T.gauss(x, y, r) * 1.4 * k
    H = T.gauss(x, y, r * 0.45) * 2.0 * k
    G += T.ring(r * 1.2, r * 0.25, x, y) * 0.8 * k
    for j in range(3):
        a = t * 25 + TAU * j / 3
        G += T.tapered([(x - r * 2.5, y + r * 0.6 * math.sin(a), x - r * 0.6, y + r * 0.3 * math.sin(a), 0.6)], r * 0.5) * k
    return G, H


def hadouken_ryu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.3)
    if k > 0:
        for lado in (-1, 1):
            P, nos = _punho(T, -0.6, lado * 0.06, 1.3, 0)
            G += P * 0.7 * k
            H += nos * 0.3 * k
        G += T.gauss(-0.48, 0.0, 0.08 * k + 0.001) * 1.2
    u = rel(t, 0.2, 0.7)
    if 0 < u < 1:
        g, h = _bola(T, -0.45 + 1.2 * u, 0.0, 0.12, t)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.68, 0.85, 0.75, 0.0, 0.8)
    G, H = G + g2, H + h2
    for j in range(4):
        kk = pulso(t, 0.72 + 0.03 * j, 0.95)
        g3, h3 = icone(T, poe(CHAMA, 0.6 + 0.1 * j - 0.15, -0.05 - 0.1 * (j % 2), 0.08 * kk), kk, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def ryu_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 10)
    G += T.gauss(0, 0, 0.12 + 0.03 * p) * 1.2
    H += T.gauss(0, 0, 0.05) * (1.5 + p)
    G += converge(T, (t * 1.3) % 1, 0.0, 1.0, 14, 2, 0, 0, 0.5, 0.01) * 0.8
    for lado in (-1, 1):
        P, nos = _punho(T, lado * 0.25, 0, 1.2, 0 if lado < 0 else math.pi)
        G += P * 0.5
    return G, H


def shinku_hadouken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.3), 3)
    k = 1 - rel(t, 0.6, 0.9)
    if u > 0:
        x1 = -0.7 + 1.65 * u
        G += T.lines([(-0.7, 0.0, x1, 0.0, 1.0)], 0.16) * 0.8 * k
        H += T.lines([(-0.7, 0.0, x1, 0.0, 1.0)], 0.05) * 1.4 * k
        for j in range(4):
            xr = -0.5 + 0.35 * j
            if xr < x1:
                G += T.arc_band(0.22, 0.03, 0, TAU, 0.35, math.pi / 2, xr, 0.0, 1.0) * k * 1.2
    g, h = clarao(T, t, 0.0, 0.2, -0.7, 0.0, 0.8)
    g2, h2 = clarao(T, t, 0.3, 0.55, 0.85, 0.0, 1.2, 1.4)
    return (G + g + g2) * env, (H + h + h2) * env


# ------------------------------------------------------------------ Chun-Li

def spinning_bird_kick(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.7)
    if 0 < u < 1:
        x = -0.6 + 1.2 * u
        for j in range(2):
            a = t * 35 + j * math.pi
            G += T.tapered([(x, -0.05, x + 0.6 * math.cos(a), -0.05 + 0.2 * math.sin(a), 1.0)], 0.1) * 1.3
        for j in range(5):
            G += T.arc_band(0.6, 0.035, t * 35 + j * 1.2, t * 35 + j * 1.2 + 0.8, 0.35, 0, x, -0.05, 1.0) * (1 - u * 0.5) * 1.3
    g, h = clarao(T, t, 0.6, 0.8, 0.6, 0.0, 0.8)
    G, H = G + g, H + h
    G += estouro(T, t, 0.62, 0.95, 10, 2, 0.6, 0.0, 0.4, 0.014)
    return G * env, H * env


def kikosho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.1, 0.5), 2)
    k = 1 - rel(t, 0.6, 0.95)
    if s > 0:
        G += T.gauss(0, 0, 0.45 * s + 0.001) * 0.7 * k
        G += T.ring(0.45 * s, 0.05, 0, 0) * 1.3 * k
        H += T.ring(0.45 * s, 0.015, 0, 0) * k
    G += converge(T, t, 0.0, 0.3, 18, 5, 0, 0, 0.7, 0.012)
    g, h = clarao(T, t, 0.3, 0.55, 0, 0, 1.2)
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 25))
    kk = pulso(t, 0.5, 0.9)
    for _ in range(4):
        a = q.uniform(0, TAU)
        bolt = jagged(q, 0.45 * math.cos(a), 0.45 * math.sin(a), 0.75 * math.cos(a), 0.75 * math.sin(a), 3, 0.06)
        G += T.polyline(bolt, 0.012) * kk * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Akuma

def gou_hadouken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.15, 0.65)
    if 0 < u < 1:
        x = -0.5 + 1.2 * u
        g, h = _bola(T, x, 0.0, 0.13, t)
        G, H = G + g * 0.8, H + h * 0.6
        G += T.ring(0.2, 0.02, x, 0.0) * 1.2
        q = np.random.default_rng(int(t * 30))
        for _ in range(3):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, x, 0.0, x + 0.25 * math.cos(a), 0.25 * math.sin(a), 3, 0.05), 0.01) * 1.0
    g2, h2 = clarao(T, t, 0.62, 0.8, 0.7, 0.0, 0.8)
    G, H = G + g2, H + h2
    return G * env, H * env


def ashura_senku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        u = rel(t, 0.04 * j, 0.25 + 0.04 * j)
        k = (1 - rel(t, 0.15 + 0.06 * j, 0.5 + 0.06 * j))
        if u > 0 and k > 0:
            x = -0.7 + 0.3 * j
            G += T.gauss(x, 0.0, 0.08, 0.22) * 0.7 * k
            G += T.gauss(x, -0.25, 0.05) * 0.6 * k
    g, h = corte(T, t, 0.45, 0.7, 0.4, 1.3, 0.08, 0.6, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.48, 0.65, 0.6, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Scorpion

def teleporte_infernal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for cx, a, b in ((-0.6, 0.0, 0.35), (0.6, 0.3, 0.7)):
        k = pulso(t, a, b)
        if k > 0:
            for j in range(6):
                g, h = icone(T, poe(CHAMA, cx - 0.3 + 0.12 * j, 0.25 - 0.15 * abs(math.sin(j)), 0.2 * k * (1 + 0.2 * math.sin(t * 30 + j))), k, 0.6)
                G, H = G + g, H + h
    g2, h2 = corte(T, t, 0.55, 0.8, -0.6, 1.2, 0.08, 0.55, 0.0)
    G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.58, 0.75, 0.55, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


def scorpion_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.polyline(_cranio(0, 0.05, 2.2) + [_cranio(0, 0.05, 2.2)[0]], 0.03) * 1.3
    for lado in (-1, 1):
        H += T.gauss(lado * 0.13, 0.0, 0.045) * 1.8
    for j in range(5):
        k = 0.6 + 0.4 * math.sin(t * 12 + j)
        g, h = icone(T, poe(CHAMA, -0.3 + 0.15 * j, -0.45, 0.13 * k), k, 0.6)
        G, H = G + g, H + h
    return G, H


def toasty(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        cr = _cranio(-0.45, 0.0, 1.6 * s)
        G += T.polyline(cr + [cr[0]], 0.025) * 1.3
        for lado in (-1, 1):
            H += T.gauss(-0.45 + lado * 0.1 * s, -0.03, 0.035) * 2 * s
    q = np.random.default_rng(3)
    u = rel(t, 0.2, 0.9)
    if 0 < u < 1:
        for j in range(26):
            v = (u * 1.3 + j / 26) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            x = -0.3 + 1.2 * v
            y = 0.05 + q.normal(0, 0.08) * v
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.15 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Sub-Zero

def lanca_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.05, 0.45)
    if 0 < u < 1:
        x = -0.65 + 1.3 * ease_in(u, 1.3)
        g, h = icone(T, [(x, 0.0), (x - 0.2, -0.1), (x - 0.65, -0.03), (x - 0.65, 0.03), (x - 0.2, 0.1)], 1.3, 0.6)
        G, H = G + g, H + h * 1.5
        G += particulas(T, t, 0.05, 0.6, 14, 3, x - 0.4, 0.0, 0.2, 0.0, 0.01)
    g2, h2 = clarao(T, t, 0.43, 0.6, 0.65, 0.0, 0.7)
    G, H = G + g2, H + h2
    for j in range(6):
        k = pulso(t, 0.45 + 0.03 * j, 0.95)
        a = TAU * j / 6
        g3, h3 = icone(T, _cristal(0.65 + 0.22 * math.cos(a), 0.22 * math.sin(a), 0.12 * k, a + math.pi / 2), k * 1.1, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def clone_congelado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        corpo = [(-0.12, -0.45), (0.12, -0.45), (0.2, -0.25), (0.18, 0.4), (0.06, 0.4), (0.0, 0.1), (-0.06, 0.4), (-0.18, 0.4), (-0.2, -0.25)]
        g, h = icone(T, [(x * s - 0.2, y * s) for x, y in corpo], 0.9, 0.7)
        G, H = G + g, H + h * 1.5
    g2, h2 = clarao(T, t, 0.5, 0.7, -0.2, 0.0, 0.8)
    G, H = G + g2, H + h2
    q = np.random.default_rng(5)
    for j in range(12):
        u = rel(t, 0.7, 1.0)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.6 * ease_out(u) * q.uniform(0.4, 1)
            g3, h3 = icone(T, _cristal(-0.2 + d * math.cos(a), d * math.sin(a), 0.05, a), (1 - u) * 1.2, 0.6)
            G, H = G + g3, H + h3
    return G * env, H * env


def subzero_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(6):
        a = t * 4 + TAU * j / 6
        g, h = icone(T, _cristal(0.3 * math.cos(a), 0.2 * math.sin(a), 0.06, a + math.pi / 2), 1.1, 0.6)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.12) * (0.8 + 0.3 * math.sin(t * 8))
    H += T.gauss(0, 0, 0.04) * 1.5
    return G, H


def inverno_absoluto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.25), 3)
    k = 1 - rel(t, 0.45, 0.65)
    if u > 0:
        G += T.lines([(-0.7, 0.0, -0.7 + 1.35 * u, 0.0, 1.0)], 0.1) * 0.8 * k
        H += T.lines([(-0.7, 0.0, -0.7 + 1.35 * u, 0.0, 1.0)], 0.03) * 1.3 * k
    for j in range(7):
        c = ease_out(rel(t, 0.25 + 0.03 * j, 0.5 + 0.03 * j), 2) * (1 - rel(t, 0.88, 1))
        if c > 0:
            a = -math.pi / 2 + (j - 3) * 0.4
            g, h = icone(T, _cristal(0.6 + 0.15 * math.cos(a), 0.25 + 0.15 * math.sin(a) - 0.1, 0.22 * c, a + math.pi / 2), 1.1, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.2, 1.0, 30, 6, 0.6, 0.0, 0.5, 0.2, 0.012)
    return G * env, H * env


REGISTRO = [
    ("investida_de_casco", investida_de_casco, GRANDE, "Bowser · o casco girando e o tranco", False),
    ("sopro_flamejante", sopro_flamejante, GRANDE, "Bowser · o sopro de fogo", False),
    ("bowser_preparo", bowser_preparo, MEDIA, "Bowser · no ar, a sombra crescendo (Preparo, laço)", True),
    ("tremor_do_rei", tremor_do_rei, GRANDE, "Bowser · a queda e o chão rachando", False),
    ("hadouken_ryu", hadouken_ryu, GRANDE, "Ryu · o Hadouken", False),
    ("ryu_preparo", ryu_preparo, MEDIA, "Ryu · a energia entre as mãos (Preparo, laço)", True),
    ("shinku_hadouken", shinku_hadouken, GRANDE, "Ryu · o feixe do Shinku Hadouken", False),
    ("spinning_bird_kick", spinning_bird_kick, GRANDE, "Chun-Li · a hélice de pernas", False),
    ("kikosho", kikosho, GRANDE, "Chun-Li · a bola de energia que explode", False),
    ("gou_hadouken", gou_hadouken, GRANDE, "Akuma · o Hadouken sombrio", False),
    ("ashura_senku", ashura_senku, GRANDE, "Akuma · o deslizar fantasma", False),
    ("teleporte_infernal", teleporte_infernal, GRANDE, "Scorpion · o fogo que some e volta", False),
    ("scorpion_preparo", scorpion_preparo, MEDIA, "Scorpion · a caveira em chamas (Preparo, laço)", True),
    ("toasty", toasty, GRANDE, "Scorpion · o fogo do inferno da caveira", False),
    ("lanca_de_gelo", lanca_de_gelo, GRANDE, "Sub-Zero · a lança de gelo", False),
    ("clone_congelado", clone_congelado, GRANDE, "Sub-Zero · o clone de gelo", False),
    ("subzero_preparo", subzero_preparo, MEDIA, "Sub-Zero · o frio juntando (Preparo, laço)", True),
    ("inverno_absoluto", inverno_absoluto, GRANDE, "Sub-Zero · o raio e os cristais", False),
]
