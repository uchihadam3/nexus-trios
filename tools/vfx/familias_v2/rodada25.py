"""Rodada 25 das habilidades próprias: Ryu Hayabusa, Cabeça de Pirâmide, Kirby, Simon Belmont, Príncipe da Pérsia,
Alucard e Seiya.

Ryu Hayabusa
- lamina_do_dragao: o corte rápido da Espada do Dragão com o rastro azul e o dragão estilizado.
- arte_do_vento: os redemoinhos de vento ninja cortando todos (Lento).
- izuna_otoshi: o rival agarrado no ar, girado e jogado de cabeça no chão (Paralisado).

Cabeça de Pirâmide
- presenca_opressiva: o capacete triangular, a névoa e a sirene (Escudo, Fortalecido e Enfraquecido).
- pyramidhead_preparo: o Preparo da Sentença — a Grande Faca arrastada no chão com as faíscas (laço).
- sentenca: a Grande Faca desce de cima com o peso e o chão afunda (Silenciado).

Kirby
- inalar: a boca enorme do Kirby puxando o vento e o rival (Silenciado).
- copia_de_poder: a estrela da cópia e o chapéu do poder aparecendo (Fortalecido e cópia).
- super_inalacao: o redemoinho gigante sugando e a estrela cuspida de volta (Exposto).

Simon Belmont
- vampire_killer: o chicote de corrente estalando e enrolando (Preso e Lento).
- cruz_arremessada: a cruz dourada girando como bumerangue (Preparo interrompido).

Príncipe da Pérsia
- rebobinar: o tempo voltando: o relógio girando ao contrário e a areia subindo (Vida, Acelerado e Protegido).
- prince_preparo: o Preparo da Tempestade de areia — a areia girando em volta da Adaga (laço).
- tempestade_de_areia: a tempestade de areia varrendo todos os rivais.

Alucard
- forma_de_nevoa: o corpo vira névoa e morcegos e volta (Protegido, Acelerado e Vampirismo).
- alucard_preparo: o Preparo do Ataque da alma — as almas girando em volta dele (laço).
- ataque_da_alma: as almas uivando voam e explodem no rival (Fortalecido).

Seiya
- cosmo_ardente: o cosmo dourado queimando e a constelação de Pégaso (Acelerado e Fortalecido).
- seiya_preparo: o Preparo do Cometa de Pégaso — o cosmo virando uma esfera (laço).
- cometa_de_pegaso: o cometa de cosmo concentrado voando e explodindo (Exposto).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (AMPULHETA, CRUZ, ESPADA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _areia(T, t, cx, cy, r0, r1, n, seed, giro, k=1.0, sq=0.6):
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = q.uniform(0, TAU) + t * giro * q.uniform(0.7, 1.3)
        r = q.uniform(r0, r1)
        pts.append((cx + r * math.cos(a), cy + r * sq * math.sin(a), q.uniform(0.4, 1) * k))
    return T.splats(pts, 0.012) * 1.3


# ------------------------------------------------------------------ Hayabusa

def lamina_do_dragao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = corte(T, t, 0.05, 0.35, 0.35, 1.6, 0.1, 0.0, 0.0)
    G, H = G + g * 1.3, H + h
    u = rel(t, 0.15, 0.75)
    if 0 < u < 1:
        pts = [(-0.7 + 1.4 * v, -0.05 + 0.15 * math.sin(v * 8 - t * 10)) for v in np.linspace(0, ease_out(u), 30)]
        G += T.polyline(pts, 0.03) * (1 - u) * 1.3
        if pts:
            g2, h2 = cheio(T, poe([(0.15, 0), (-0.05, -0.07), (-0.1, 0), (-0.05, 0.07)], pts[-1][0], pts[-1][1], 1.0, 0), (1 - u) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


def arte_do_vento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.05 + 0.08 * j, 0.75 + 0.05 * j)
        if 0 < u < 1:
            for m in range(4):
                y = 0.3 - 0.18 * m
                r = 0.08 + 0.05 * m
                G += T.arc_band(r, 0.02, t * 25 + m, t * 25 + m + 4.5, 0.35, 0, x, y, 1.0) * (1 - u) * 1.4
    for j in range(5):
        g, h = corte(T, t, 0.3 + 0.05 * j, 0.5 + 0.05 * j, 0.8 * (-1) ** j, 0.5, 0.04, -0.55 + 0.27 * j, -0.05)
        G, H = G + g, H + h
    return G * env, H * env


def izuna_otoshi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = rel(t, 0.0, 0.3)
    gira = rel(t, 0.3, 0.55)
    cai = rel(t, 0.55, 0.7)
    if t < 0.7:
        y = 0.2 - 0.7 * ease_out(sobe) + 0.95 * ease_in(cai, 2)
        G += T.gauss(0, y, 0.1, 0.14) * 1.2
        if gira > 0:
            G += T.arc_band(0.25, 0.03, gira * TAU * 2, gira * TAU * 2 + 4, 1.0, 0, 0, y, 1.0) * 1.3
        G += T.tapered([(0, y - 0.35 * (1 if cai > 0 else -1), 0, y, 0.6)], 0.06) * (sobe if cai == 0 else 1)
    g, h = clarao(T, t, 0.68, 0.85, 0, 0.35, 1.2, 1.4)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.68, 0.98, 0.9, 0.35, 1.6)
    G += estouro(T, t, 0.68, 0.98, 14, 4, 0, 0.35, 0.5, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Cabeça de Pirâmide

def _piramide(cx, cy, s):
    return [(cx - 0.3 * s, cy + 0.2 * s), (cx + 0.3 * s, cy + 0.2 * s), (cx + 0.05 * s, cy - 0.45 * s), (cx - 0.05 * s, cy - 0.45 * s)]


def _faca(cx, cy, s, ang):
    return poe([(-0.08, -1.0), (0.12, -0.95), (0.15, 0.55), (-0.1, 0.55), (-0.12, -0.2)], cx, cy, s, ang)


def presenca_opressiva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    g, h = icone(T, _piramide(0, -0.15, 1.3 * s), 1.1, 0.5)
    G, H = G + g, H + h
    q = np.random.default_rng(3)
    nevoa = pulso(t, 0.0, 1.0)
    pts = [(q.uniform(-0.9, 0.9) + 0.1 * math.sin(t * 2 + j), q.uniform(-0.2, 0.5), nevoa * q.uniform(0.3, 0.8)) for j in range(25)]
    G += T.splats(pts, 0.12) * 0.5
    for j in range(3):
        G += anel(T, t, 0.1 + 0.15 * j, 0.6 + 0.12 * j, 0.1, 0.8, 0.025, -0.15, 1.0, 1.0)
    return G * env, H * env


def pyramidhead_preparo(T, t, rng):
    G, H = vazio(T)
    x = -0.4 + 0.3 * ((t * 0.6) % 1)
    g, h = icone(T, _faca(x, -0.05, 0.75, 1.3), 1.0, 0.5)
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 30))
    for _ in range(5):
        a = q.uniform(math.pi, TAU)
        G += T.lines([(x + 0.5, 0.35, x + 0.5 + 0.18 * math.cos(a), 0.35 + 0.18 * math.sin(a), 1.0)], 0.012) * 1.4
    H += T.gauss(x + 0.5, 0.35, 0.04) * 1.5
    return G, H


def sentenca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.55, 0.75)
    if k > 0:
        g, h = icone(T, _faca(0.1, -0.85 + 0.9 * desce, 0.75, 0.0), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.1, 0.35, 1.2, 1.5)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.28, 0.9, 1.0, 0.35, 1.8)
    q = np.random.default_rng(5)
    r = ease_out(rel(t, 0.3, 0.6), 2)
    for j in range(6):
        a = math.pi * j / 5
        pts = [(0.1, 0.35)] + [(0.1 + 0.8 * r * v * math.cos(a) + q.normal(0, 0.02), 0.35 + 0.12 * r * v * math.sin(a)) for v in (0.33, 0.66, 1.0)]
        G += T.polyline(pts, 0.015) * (1 - rel(t, 0.85, 1)) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Kirby

def _kirby(T, cx, cy, s, boca):
    G, H = vazio(T)
    g, h = icone(T, poe(_circ(30), cx, cy, 0.25 * s), 1.0, 0.45)
    G, H = G + g, H + h
    for lado in (-1, 1):
        G += T.gauss(cx + lado * 0.08 * s, cy - 0.06 * s, 0.02 * s + 0.001, 0.04 * s + 0.001) * -0.6
    G -= T.gauss(cx + 0.02, cy + 0.08 * s, 0.05 * boca * s + 0.001, 0.07 * boca * s + 0.001) * 0.8
    return np.maximum(G, 0), H


def inalar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.88, 1))
    boca = pulso(t, 0.1, 0.8)
    g, h = _kirby(T, -0.45, 0.0, 1.2 * s, 1.0 + boca)
    G, H = G + g, H + h
    for j in range(8):
        u = ((t * 2.5 + j / 8) % 1)
        y = -0.25 + 0.5 * (j / 7)
        x = 0.8 - 1.15 * u
        G += T.tapered([(x + 0.2, y * (1 - u), x, y * (1 - u) * 0.7, 0.8)], 0.025) * boca * 1.2
    u = ease_in(rel(t, 0.3, 0.75), 1.5)
    if 0 < u < 1:
        G += T.gauss(0.6 - 0.95 * u, 0.0, 0.08 * (1 - 0.6 * u)) * 1.2
    return G * env, H * env


def copia_de_poder(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    g, h = _kirby(T, 0, 0.1, 1.1 * s, 0.4)
    G, H = G + g, H + h
    c = surge(t, 0.35, 0.6) * (1 - rel(t, 0.88, 1))
    if c > 0:
        chapeu = [(-0.25, -0.12), (0.25, -0.12), (0.05, -0.5), (0.2, -0.6)]
        g2, h2 = icone(T, [(x * c, y + 0.0) for x, y in chapeu], 1.1, 0.5)
        G, H = G + g2, H + h2
        g3, h3 = cheio(T, poe(estrela_pts(5, 0.45), 0.2 * c, -0.6, 0.07 * c), 1.5)
        G, H = G + g3, H + h3 * 2
    g4, h4 = clarao(T, t, 0.3, 0.5, 0, -0.2, 0.8)
    G, H = G + g4, H + h4
    G += particulas(T, t, 0.35, 1.0, 26, 5, 0, 0, 0.5, 0.4, 0.013)
    return G * env, H * env


def super_inalacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    for j in range(3):
        pts = _espiral(-0.3, 0.0, 0.05, 0.8, 1.3, j * TAU / 3 - t * 15)
        G += T.polyline(pts, 0.02) * k * 1.2
    g, h = _kirby(T, -0.3, 0.0, 1.3 * surge(t, 0.0, 0.2) * (1 - rel(t, 0.88, 1)), 2.0 * k)
    G, H = G + g, H + h
    u = rel(t, 0.55, 0.85)
    if 0 < u < 1:
        x = -0.1 + 0.9 * ease_out(u)
        g2, h2 = cheio(T, poe(estrela_pts(5, 0.45), x, 0.0, 0.15, u * 8), 1.5)
        G, H = G + g2, H + h2 * 2
    g3, h3 = clarao(T, t, 0.82, 0.98, 0.8, 0.0, 0.9)
    return (G + g3) * env, (H + h3) * env


# ------------------------------------------------------------------ Simon Belmont

def vampire_killer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.7, 0.85)
    if u > 0:
        pts = []
        for v in np.linspace(0, 1, 26):
            x = -0.7 + 1.35 * v * u
            y = 0.1 - 0.25 * math.sin(math.pi * v) * (1 - u) + 0.03 * math.sin(v * 20)
            pts.append((x, y))
        for i in range(0, len(pts) - 1, 1):
            G += T.ring(0.018, 0.007, pts[i][0], pts[i][1], 0.7) * k * 1.3
        G += T.flare(pts[-1][0], pts[-1][1], 0.3 * pulso(t, 0.3, 0.45) + 0.01, 0.3, 0.02) * 1.3
    e = ease_out(rel(t, 0.4, 0.75), 2)
    if e > 0:
        G += T.arc_band(0.15, 0.015, 0, TAU * e, 0.5, 0, 0.6, 0.0, 1.0) * k * 1.3
        G += T.arc_band(0.15, 0.015, 0, TAU * e, 0.5, 0, 0.6, 0.12, 1.0) * k * 1.3
    return G * env, H * env


def cruz_arremessada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.05, 0.9)
    if 0 < u < 1:
        ida = math.sin(math.pi * u)
        x = -0.6 + 1.35 * ida
        y = -0.1 + 0.2 * (u - 0.5)
        g, h = icone(T, poe(CRUZ, x, y, 0.21, t * 30), 1.4, 0.6)
        G, H = G + g, H + h * 1.5
        for j in range(1, 4):
            uj = max(0.0, u - 0.03 * j)
            G += T.gauss(-0.6 + 1.35 * math.sin(math.pi * uj), -0.1 + 0.2 * (uj - 0.5), 0.08) * (0.4 - 0.1 * j)
    g2, h2 = clarao(T, t, 0.45, 0.6, 0.75, -0.1, 0.8)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Príncipe da Pérsia

def rebobinar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.35 * s, 0.03, 0, 0) * 1.2
        for j in range(12):
            a = TAU * j / 12
            G += T.lines([(0.3 * s * math.cos(a), 0.3 * s * math.sin(a), 0.35 * s * math.cos(a), 0.35 * s * math.sin(a), 1.0)], 0.01) * 1.2
        a = -math.pi / 2 - t * 18
        G += T.lines([(0, 0, 0.28 * s * math.cos(a), 0.28 * s * math.sin(a), 1.0)], 0.02) * 1.3
        a2 = -math.pi / 2 - t * 4
        G += T.lines([(0, 0, 0.18 * s * math.cos(a2), 0.18 * s * math.sin(a2), 1.0)], 0.025) * 1.3
    G += _areia(T, t, 0, 0, 0.4, 0.75, 120, 4, -4.0, pulso(t, 0.1, 0.95), 0.8)
    g, h = aura(T, t, 0.3, 1.0, 0.4, 0, 0.7)
    return (G + g) * env, (H + h) * env


def prince_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe([(0, -1), (0.12, -0.2), (0.25, -0.15), (0.12, 0.0), (0.06, 0.5), (-0.06, 0.5), (-0.12, 0.0), (-0.25, -0.15), (-0.12, -0.2)],
                        0, 0, 0.6, 0), 1.2, 0.5)
    G, H = G + g, H + h
    H += T.gauss(0, -0.15, 0.04) * (1.5 + 0.5 * math.sin(t * 8))
    G += _areia(T, t, 0, 0, 0.2, 0.45, 80, 9, 5.0, 1.0, 0.7)
    return G, H


def tempestade_de_areia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 1.0)
    q = np.random.default_rng(13)
    pts = []
    for _ in range(320):
        x0 = q.uniform(-1.4, 0.4)
        y = q.uniform(-0.6, 0.45)
        x = x0 + 1.6 * u * q.uniform(0.7, 1.2)
        pts.append((x, y + 0.05 * math.sin(x * 6 + t * 10), q.uniform(0.3, 1) * pulso(t, 0.0, 0.95)))
    G += T.splats(pts, 0.014) * 1.3
    for j in range(4):
        y = -0.4 + 0.25 * j
        G += T.tapered([(-0.9 + 1.6 * u - 0.6, y, -0.9 + 1.6 * u, y + 0.03, 0.6)], 0.03) * pulso(t, 0.0, 0.9) * 0.8
    return G * env, H * env


# ------------------------------------------------------------------ Alucard

def _morcego(x, y, s, bate):
    return [(x - 0.2 * s, y - 0.05 * s * bate), (x - 0.07 * s, y), (x, y - 0.06 * s), (x + 0.07 * s, y), (x + 0.2 * s, y - 0.05 * s * bate), (x, y + 0.08 * s)]


def forma_de_nevoa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.85)
    q = np.random.default_rng(6)
    pts = [(q.normal(0, 0.25) + 0.1 * math.sin(t * 3 + j), q.normal(0, 0.2), k * q.uniform(0.3, 0.8)) for j in range(40)]
    G += T.splats(pts, 0.08) * 0.6
    for j in range(6):
        u = rel(t, 0.2 + 0.05 * j, 0.7 + 0.04 * j)
        if 0 < u < 1:
            a = TAU * j / 6 + u * 2
            d = 0.15 + 0.5 * math.sin(math.pi * u)
            g, h = cheio(T, _morcego(d * math.cos(a), d * math.sin(a) * 0.7, 1.0, math.sin(t * 40 + j)), 1.3)
            G, H = G + g, H + h
    return G * env, H * env


def alucard_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(5):
        a = t * 4 + TAU * j / 5
        x, y = 0.4 * math.cos(a), 0.25 * math.sin(a)
        G += T.gauss(x, y, 0.05) * 1.2
        H += T.gauss(x, y, 0.02) * 1.4
        G += T.tapered([(x - 0.12 * math.cos(a + math.pi / 2), y - 0.08 * math.sin(a + math.pi / 2), x, y, 0.5)], 0.03)
    return G, H


def ataque_da_alma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        u = rel(t, 0.05 + 0.05 * j, 0.5 + 0.05 * j)
        if 0 < u < 1:
            y0 = -0.4 + 0.2 * j
            x = -0.6 + 1.3 * ease_in(u, 1.4)
            y = y0 * (1 - u) + 0.15 * math.sin(u * 8 + j)
            G += T.gauss(x, y, 0.06) * 1.3
            H += T.gauss(x, y, 0.025) * 1.5
            G += T.tapered([(x - 0.35, y - 0.05 * math.sin(u * 8 + j), x, y, 0.5)], 0.04) * 0.9
    g, h = clarao(T, t, 0.5, 0.75, 0.7, 0.0, 1.2, 1.4)
    G, H = G + g, H + h
    G += estouro(T, t, 0.5, 0.9, 14, 8, 0.7, 0.0, 0.45, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Seiya

def _pegaso(cx, cy, s):
    estrelas = [(-0.5, 0.1), (-0.2, -0.15), (0.1, -0.1), (0.35, -0.35), (0.5, -0.2), (0.15, 0.2), (-0.1, 0.35), (0.4, 0.3)]
    linhas = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (5, 7)]
    return [(cx + x * s, cy + y * s) for x, y in estrelas], linhas


def cosmo_ardente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = aura(T, t, 0.0, 1.0, 0.45, 0.0, 1.2)
    G, H = G + g, H + h
    s = surge(t, 0.2, 0.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        pts, linhas = _pegaso(0, -0.1, 0.9 * s)
        for i, j in linhas:
            G += T.lines([(pts[i][0], pts[i][1], pts[j][0], pts[j][1], 1.0)], 0.008) * 1.1
        for x, y in pts:
            g2, h2 = cheio(T, poe(estrela_pts(4, 0.3), x, y, 0.05), 1.4)
            G, H = G + g2, H + h2 * 2
    G += particulas(T, t, 0.1, 1.0, 40, 3, 0, 0.1, 0.6, 0.7, 0.012)
    return G * env, H * env


def seiya_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 9)
    G += T.gauss(0, 0, 0.14 + 0.03 * p) * 1.3
    H += T.gauss(0, 0, 0.06) * (1.5 + p)
    G += converge(T, (t * 1.2) % 1, 0.0, 1.0, 16, 7, 0, 0, 0.55, 0.01) * 0.9
    return G, H


def cometa_de_pegaso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.45)
    if 0 < u < 1:
        x = -0.65 + 1.35 * ease_in(u, 1.5)
        G += T.gauss(x, 0.0, 0.17) * 1.4
        H += T.gauss(x, 0.0, 0.08) * 2.0
        G += T.tapered([(x - 0.8, 0.0, x - 0.1, 0.0, 0.2)], 0.15) * 0.8
    g, h = clarao(T, t, 0.42, 0.65, 0.7, 0.0, 1.5, 1.6)
    G, H = G + g, H + h
    G += estouro(T, t, 0.42, 0.85, 20, 6, 0.7, 0.0, 0.6, 0.016)
    G += anel(T, t, 0.42, 0.95, 0.1, 0.6, 0.05, 0.0)
    return G * env, H * env


REGISTRO = [
    ("lamina_do_dragao", lamina_do_dragao, GRANDE, "Hayabusa · o corte e o dragão", False),
    ("arte_do_vento", arte_do_vento, GRANDE, "Hayabusa · os redemoinhos ninja", False),
    ("izuna_otoshi", izuna_otoshi, GRANDE, "Hayabusa · o rival girado e jogado no chão", False),
    ("presenca_opressiva", presenca_opressiva, GRANDE, "Cabeça de Pirâmide · o capacete e a névoa", False),
    ("pyramidhead_preparo", pyramidhead_preparo, MEDIA, "Cabeça de Pirâmide · a faca arrastada (Preparo, laço)", True),
    ("sentenca", sentenca, GRANDE, "Cabeça de Pirâmide · a Grande Faca descendo", False),
    ("inalar", inalar, GRANDE, "Kirby · a boca puxando", False),
    ("copia_de_poder", copia_de_poder, GRANDE, "Kirby · o chapéu do poder", False),
    ("super_inalacao", super_inalacao, GRANDE, "Kirby · o redemoinho e a estrela", False),
    ("vampire_killer", vampire_killer, GRANDE, "Simon · o chicote de corrente", False),
    ("cruz_arremessada", cruz_arremessada, GRANDE, "Simon · a cruz bumerangue", False),
    ("rebobinar", rebobinar, GRANDE, "Príncipe · o relógio ao contrário e a areia", False),
    ("prince_preparo", prince_preparo, MEDIA, "Príncipe · a Adaga e a areia (Preparo, laço)", True),
    ("tempestade_de_areia", tempestade_de_areia, GRANDE, "Príncipe · a tempestade de areia", False),
    ("forma_de_nevoa", forma_de_nevoa, GRANDE, "Alucard · a névoa e os morcegos", False),
    ("alucard_preparo", alucard_preparo, MEDIA, "Alucard · as almas girando (Preparo, laço)", True),
    ("ataque_da_alma", ataque_da_alma, GRANDE, "Alucard · as almas voando", False),
    ("cosmo_ardente", cosmo_ardente, GRANDE, "Seiya · o cosmo e a constelação", False),
    ("seiya_preparo", seiya_preparo, MEDIA, "Seiya · o cosmo virando esfera (Preparo, laço)", True),
    ("cometa_de_pegaso", cometa_de_pegaso, GRANDE, "Seiya · o Cometa de Pégaso", False),
]
