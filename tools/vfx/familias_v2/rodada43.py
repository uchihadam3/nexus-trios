"""Rodada 43 das habilidades próprias: Morty, Tails, Knuckles, Velma, Fred e Leorio.

Morty Smith
- arma_de_laser_morty: a arma de laser tremendo na mão e o tiro verde em zigue-zague.
- grito_de_panico: o grito "Ai, caramba!" em ondas tremidas e as gotas de suor (Confuso).
- morty_preparo: o Preparo do Morty mau — o tapa-olho e o brilho frio do olho (laço).
- morty_mau: o espiral escuro e o feixe frio do Morty mau (Enfraquecido).

Tails
- giro_de_cauda: as duas caudas girando como hélice e acertando o rival.
- voo_de_resgate: o Tails voando com as caudas-hélice e os anéis de velocidade no trio (Adianta e Acelerado).
- tails_preparo: o Preparo do Canhão de energia — a engrenagem girando e a carga juntando (laço).
- canhao_de_energia_tails: o tiro de energia do canhão no rival (Eletrificado).

Knuckles
- soco_espinhoso: a luva com os dois espinhos acertando o rival (Exposto).
- escavar: a terra subindo em volta, o Knuckles entrando no chão (Protegido e Escudo).
- knuckles_preparo: o Preparo do Soco do terremoto — o punho erguido e as pedras flutuando (laço).
- soco_do_terremoto: o soco no chão, as rachaduras e as pedras voando em todos (Preso).

Velma
- lupa_da_velma: a lupa e o ponto de exclamação da pista no rival (Marcado e Enfraquecido).
- cade_meus_oculos: os óculos caindo, a vista embaçada e a Velma tateando (Esquiva).
- velma_preparo: o Preparo do Tirar a máscara — o dedo apontando e o "Jinkies!" brilhando (laço).
- tirar_a_mascara: a máscara arrancada voando e os bônus do rival se desfazendo (Dissipar).

Fred
- rede_do_fred: a rede jogada abrindo e caindo no rival (Preso e Lento).
- vamos_nos_separar: as três setas se separando para os lados e o trio acelerando (Acelerado e Adianta).
- armadilha_perfeita: a gaiola caindo do alto em cima do rival em Preparo (Paralisado).

Leorio
- soco_teletransportado: o portal ao lado dele e o punho saindo do outro portal no rival.
- primeiros_socorros: a maleta, as faixas enrolando e a cruz de cura (Vida e Regeneração).
- leorio_preparo: o Preparo do Bisturi de Nen — o bisturi brilhando com a aura (laço).
- bisturi_de_nen: o corte fino e preciso do bisturi de Nen.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CRUZ, GOTA, SETA, anel, aura, cheio, circulo, clarao, converge, corte, engrenagem, estouro, estrela_pts, icone,
                         onda_no_chao, particulas, poe, raios, surge)


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


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


def _pedra(cx, cy, r, giro):
    q = np.random.default_rng(17)
    rr = [q.uniform(0.75, 1.0) for _ in range(8)]
    return [(cx + math.cos(giro + TAU * j / 8) * r * rr[j], cy + math.sin(giro + TAU * j / 8) * r * rr[j] * 0.85) for j in range(8)]


def _portal(T, cx, cy, s, t, k):
    G = 0.0
    for j in range(3):
        a = t * 10 + TAU * j / 3
        G = G + T.arc_band(s * (1 - 0.2 * j), s * 0.12, a, a + 3.5, 0.5, 0, cx, cy, 1.0) * k * 1.2
    return G + T.gauss(cx, cy, s * 0.5, s * 0.8) * k * 0.6


# ------------------------------------------------------------------ Morty

def arma_de_laser_morty(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.7, 0.85))
    treme = 0.015 * math.sin(t * 60)
    if s > 0:
        g, h = icone(T, [(-0.75, -0.05 + treme), (-0.45, -0.05 + treme), (-0.45, 0.04 + treme), (-0.62, 0.04 + treme), (-0.65, 0.15 + treme),
                         (-0.72, 0.15 + treme), (-0.72, 0.04 + treme), (-0.75, 0.04 + treme)], s * 1.1, 0.5)
        G, H = G + g, H + h
    k = pulso(t, 0.2, 0.55)
    if k > 0:
        q = np.random.default_rng(int(t * 40))
        pts = [(-0.45 + 1.0 * v, q.normal(0, 0.04) * math.sin(math.pi * v)) for v in np.linspace(0, 1, 14)]
        G += T.polyline(pts, 0.03) * k * 1.3
        H += T.polyline(pts, 0.008) * k * 1.4
    g2, h2 = clarao(T, t, 0.25, 0.5, 0.55, 0.0, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.28, 0.75, 12, 4, 0.55, 0.0, 0.4, 0.012)
    return G * env, H * env


def grito_de_panico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(int(t * 25))
    for j in range(4):
        u = rel(t, 0.05 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            r = 0.15 + 0.9 * u
            pts = [(-0.6 + r * math.cos(a) + q.normal(0, 0.008), r * 0.6 * math.sin(a) + q.normal(0, 0.008)) for a in np.linspace(-0.6, 0.6, 16)]
            G += T.polyline(pts, 0.032) * (1 - u) * 1.3
    for j in range(4):
        u = ((t * 3) + j / 4) % 1
        g, h = cheio(T, poe(GOTA, -0.7 + 0.1 * j, -0.35 + 0.25 * u, 0.035), pulso(t, 0.0, 0.7) * (1 - u) * 1.3)
        G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = _tontas(T, t, 0.5, 1.0, x + 0.1, -0.25, 3, 0.1, 0.03)
        G, H = G + g2, H + h2
    return G * env, H * env


def morty_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0, 0.0, 0.18) * 0.4
    tapa = [(-0.24, -0.12), (-0.03, -0.12), (-0.03, 0.06), (-0.24, 0.06)]
    g, h = cheio(T, tapa, 1.1)
    G, H = G + g, H + h
    G += T.lines([(-0.2, -0.12, 0.2, -0.16, 1.0)], 0.01) * 1.0
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    H += T.gauss(0.09, -0.02, 0.015) * (1.5 + b)
    G += T.gauss(0.09, -0.02, 0.04) * (0.8 + 0.5 * b)
    return G, H


def morty_mau(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.45, 0.55))
    if s > 0:
        pts = [(-0.55 + 0.03 * (a / 12) * 6 * math.cos(a + t * 8) * s, 0.03 * (a / 12) * 6 * math.sin(a + t * 8) * s) for a in np.linspace(0.3, 12, 50)]
        G += T.polyline(pts, 0.014) * 1.3
    k = pulso(t, 0.3, 0.75)
    if k > 0:
        G += T.tapered([(-0.55, 0.0, 0.55, 0.0, 1.0)], 0.08 * k + 0.01) * 1.2
        H += T.lines([(-0.55, 0.0, 0.55, 0.0, 1.0)], 0.01) * k * 1.4
        for j in range(5):
            v = ((t * 3) + j / 5) % 1
            G += T.ring(0.05, 0.01, -0.55 + 1.1 * v, 0.0, 0.5) * k * 1.0
    g, h = clarao(T, t, 0.35, 0.65, 0.55, 0.0, 1.3, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.4, 0.9, 14, 5, 0.55, 0.0, 0.5, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Tails

def _caudas(T, cx, cy, s, a, k):
    G = 0.0
    for j in range(2):
        b = a + math.pi * j
        pts = [(cx + s * v * math.cos(b + 0.6 * v), cy + s * v * math.sin(b + 0.6 * v) * 0.5) for v in np.linspace(0, 1, 10)]
        G = G + T.polyline(pts, s * 0.4) * k * 1.1
        G = G + T.gauss(pts[-1][0], pts[-1][1], s * 0.2) * k * 1.0
    return G


def giro_de_cauda(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.65, 0.8)
    x = -0.5 + 0.85 * u
    G += _caudas(T, x, 0.0, 0.25, t * 35, k)
    G += T.ring(0.25, 0.03, x, 0.0, 0.5) * k * 0.6
    for j in range(3):
        g, h = clarao(T, t, 0.3 + 0.1 * j, 0.4 + 0.1 * j, 0.45, -0.05 + 0.05 * j, 0.5)
        G, H = G + g, H + h
    G += estouro(T, t, 0.35, 0.85, 12, 4, 0.45, 0.0, 0.4, 0.012)
    return G * env, H * env


def voo_de_resgate(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.7)
    k = 1 - rel(t, 0.85, 1)
    if 0 < u < 1:
        x = -0.8 + 1.6 * u
        G += _caudas(T, x, -0.55, 0.15, t * 40, 1.0)
        G += T.tapered([(x - 0.4, -0.5, x - 0.1, -0.55, 1.0)], 0.04) * 0.7
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        m = surge(t, 0.2 + 0.1 * j, 0.4 + 0.1 * j) * k
        if m > 0:
            G += T.ring(0.13 * m, 0.02, x, -0.05, 2.0) * 1.2
            G += T.ring(0.09 * m, 0.012, x, 0.08, 2.0) * 1.0
            G += T.gauss(x, 0.05, 0.12, 0.2) * m * 0.4
    G += particulas(T, t, 0.2, 1.0, 16, 5, 0, 0.0, 0.8, 0.4, 0.011)
    return G * env, H * env


def tails_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(engrenagem(8, 1.0, 0.75), -0.15, 0.05, 0.12, t * TAU), 1.1, 0.45)
    G, H = G + g, H + h
    G += T.lines([(-0.05, 0.0, 0.3, 0.0, 1.0)], 0.06) * 0.9
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    H += T.gauss(0.32, 0.0, 0.03 + 0.01 * b) * (1.5 + b)
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 8, int(t * 2), 0.32, 0.0, 0.25)
    return G, H


def canhao_de_energia_tails(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.gauss(-0.65, 0.0, 0.06) * pulso(t, 0.0, 0.3) * 1.4
    k = pulso(t, 0.15, 0.6)
    if k > 0:
        G += T.tapered([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.11 * k + 0.01) * 1.3
        H += T.lines([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.018) * k * 1.6
        for j in range(2):
            g, h = _raio(T, t, -0.6, 0.0, 0.55, 0.0, k * 0.6, 0.008, j, 0.15)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.25, 0.6, 0.55, 0.0, 1.3, 1.3)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.3, 0.85, 6, 8, 0.55, 0.0, 0.35, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Knuckles

def _luva_espinhos(T, cx, cy, s, k):
    P, nos = _punho(T, cx, cy, s * 10, 0)
    G = P * 0.95 * k
    for dy in (-0.25, 0.25):
        G = G + T.polys([([(cx + s * 0.9, cy + s * dy * 4 - s * 0.4), (cx + s * 2.2, cy + s * dy * 4), (cx + s * 0.9, cy + s * dy * 4 + s * 0.4)], 1.0)],
                        0.004) * k * 1.3
    return G, nos * 0.45 * k


def soco_espinhoso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.28), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        g, h = _luva_espinhos(T, -0.55 + 0.9 * u, 0.0, 0.26, k)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.25, 0.48, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.27, 0.8, 14, 4, 0.45, 0.0, 0.5, 0.013)
    return G * env, H * env


def escavar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(6)
    for j in range(14):
        a = math.pi + q.uniform(0.1, math.pi - 0.1)
        u = rel(t, 0.03 * j, 0.5 + 0.03 * j)
        if 0 < u < 1:
            r = 0.1 + 0.4 * u
            x, y = r * math.cos(a), 0.3 + r * math.sin(a) * 1.2 + 0.6 * u * u
            g, h = icone(T, _pedra(x, y, 0.035, u * 6 + j), (1 - rel(u, 0.8, 1)) * 1.1, 0.6)
            G, H = G + g, H + h
    s = ease_out(rel(t, 0.3, 0.6), 2) * (1 - rel(t, 0.88, 1))
    if s > 0:
        monte = [(-0.35 * s, 0.35), (-0.2 * s, 0.35 - 0.2 * s), (0.0, 0.35 - 0.26 * s), (0.2 * s, 0.35 - 0.2 * s), (0.35 * s, 0.35)]
        g2, h2 = icone(T, monte, 1.0, 0.5)
        G, H = G + g2, H + h2
        G += T.arc_band(0.38 * s, 0.025, math.pi, TAU, 0.8, 0, 0.0, 0.35, 0.0) * 1.1
    G += onda_no_chao(T, t, 0.0, 0.5, 0.5, 0.35, 1.2)
    return G * env, H * env


def knuckles_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _luva_espinhos(T, 0.0, -0.05, 0.18, 1.0)
    G, H = G + g, H + h
    for j in range(5):
        a = t * TAU * 0.8 + TAU * j / 5
        g2, h2 = icone(T, _pedra(0.3 * math.cos(a), 0.15 + 0.12 * math.sin(a), 0.035, a), 1.0, 0.6)
        G, H = G + g2, H + h2
    return G, H


def soco_do_terremoto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.3), 2.3)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        P, nos = _punho(T, -0.2, -0.6 + 0.85 * desce, 2.8, math.pi / 2)
        G += P * 0.95 * k
        H += nos * 0.45 * k
    g, h = clarao(T, t, 0.28, 0.5, -0.2, 0.3, 1.4, 1.4)
    G, H = G + g, H + h
    r = ease_out(rel(t, 0.3, 0.6), 2)
    q = np.random.default_rng(3)
    for j in range(8):
        a = math.pi * j / 7
        pts = [(-0.2, 0.35)] + [(-0.2 + 1.0 * r * v * math.cos(a) + q.normal(0, 0.02), 0.35 + 0.08 * r * v * math.sin(a)) for v in (0.33, 0.66, 1.0)]
        G += T.polyline(pts, 0.014) * (1 - rel(t, 0.85, 1)) * 1.2
    for j in range(10):
        u = rel(t, 0.35 + 0.02 * j, 0.85)
        if 0 < u < 1:
            x = -0.85 + 0.17 * j
            g2, h2 = icone(T, _pedra(x, 0.3 - 0.5 * math.sin(math.pi * u), 0.035, u * 5), (1 - rel(u, 0.8, 1)) * 1.1, 0.6)
            G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.3, 0.95, 1.0, 0.35, 1.7)
    return G * env, H * env


# ------------------------------------------------------------------ Velma

def _oculos(T, cx, cy, s, k, ang=0.0):
    G = 0.0
    c, sn = math.cos(ang), math.sin(ang)
    for lado in (-1, 1):
        ox, oy = cx + lado * s * c, cy + lado * s * sn
        G = G + T.ring(s * 0.7, s * 0.15, ox, oy, 0.75) * k * 1.3
    G = G + T.lines([(cx - s * 0.3 * c, cy - s * 0.3 * sn, cx + s * 0.3 * c, cy + s * 0.3 * sn, 1.0)], s * 0.12) * k * 1.2
    return G


def lupa_da_velma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.45), 1.5)
    k = 1 - rel(t, 0.75, 0.9)
    cx = -0.4 + 0.85 * u
    G += T.ring(0.18, 0.025, cx, -0.1) * k * 1.3
    G += T.lines([(cx + 0.13, 0.03, cx + 0.3, 0.2, 1.0)], 0.04) * k * 1.2
    G += T.gauss(cx, -0.1, 0.13) * k * 0.3
    H += T.gauss(cx - 0.06, -0.16, 0.025) * k * 1.6
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(0.45, -0.55, 0.45, -0.4 * s - 0.15 - 0.1, 1.0)], 0.03) * 1.4
        G += T.gauss(0.45, -0.18, 0.025) * s * 1.6
    return G * env, H * env


def cade_meus_oculos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        G += _oculos(T, 0.1 * u, -0.25 + 0.6 * ease_in(u, 2), 0.13, 1.0, u * 3)
    k = pulso(t, 0.3, 0.95)
    if k > 0:
        for j in range(3):
            G += T.gauss(-0.15 + 0.15 * j + 0.04 * math.sin(t * 8 + j), -0.05, 0.12, 0.18) * k * 0.3
        for lado in (-1, 1):
            x = lado * (0.2 + 0.08 * math.sin(t * 6))
            G += T.gauss(x, 0.05, 0.04) * k * 0.9
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        for j in range(3):
            G += T.lines([(-0.45 + 0.05 * j, -0.4 - 0.05 * j, -0.6 + 0.05 * j, -0.35 - 0.05 * j, 1.0)], 0.008) * s * 1.2
    return G * env, H * env


def velma_preparo(T, t, rng):
    G, H = vazio(T)
    G += _oculos(T, 0.0, -0.1, 0.11, 1.0)
    G += T.lines([(0.1, 0.15, 0.3, -0.1, 1.0)], 0.02) * 1.1
    b = 0.5 + 0.5 * math.sin(t * TAU * 3)
    g, h = cheio(T, poe(estrela_pts(4, 0.3), 0.33, -0.15, 0.04 + 0.02 * b), 1.3)
    G, H = G + g, H + h
    return G, H


_MASCARA = [(-0.7, -0.4), (0.0, -0.8), (0.7, -0.4), (0.6, 0.4), (0.0, 0.85), (-0.6, 0.4)]


def tirar_a_mascara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.25, 0.65), 1.4)
    k = 1 - rel(t, 0.7, 0.8)
    if k > 0:
        x = 0.45 + 0.5 * u
        y = -0.15 - 0.5 * math.sin(math.pi * u * 0.8)
        g, h = icone(T, poe(_MASCARA, x, y, 0.15, u * 5), k * 1.2, 0.45)
        G, H = G + g, H + h
    pux = pulso(t, 0.0, 0.35)
    if pux > 0:
        G += T.lines([(-0.4, 0.0, 0.4, -0.15, 1.0)], 0.02) * pux * 1.0
    g2, h2 = clarao(T, t, 0.25, 0.45, 0.45, -0.15, 1.0)
    G, H = G + g2, H + h2
    q = np.random.default_rng(3)
    for j in range(8):
        a = q.uniform(0, TAU)
        w = rel(t, 0.35, 0.9)
        if 0 < w < 1:
            r = 0.1 + 0.4 * w
            g3, h3 = cheio(T, poe(estrela_pts(4, 0.3), 0.45 + r * math.cos(a), r * math.sin(a), 0.03), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Fred

def _rede(T, cx, cy, s, k):
    linhas = []
    for m in range(6):
        v = -1 + 2 * m / 5
        linhas.append((cx + v * s, cy - s * (1 - 0.3 * v * v), cx + v * s * 0.8, cy + s, 1.0))
        linhas.append((cx - s, cy + v * s * 0.8, cx + s, cy + v * s * 0.8, 1.0))
    return T.lines(linhas, max(0.004, s * 0.035)) * k * 1.3


def rede_do_fred(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        x = -0.6 + 1.05 * ease_out(u, 1.5)
        y = -0.1 - 0.35 * math.sin(math.pi * u)
        G += _rede(T, x, y, 0.06 + 0.16 * u, 1.0)
    s = rel(t, 0.45, 0.6)
    k = 1 - rel(t, 0.88, 1)
    if s > 0:
        G += _rede(T, 0.45, 0.05, 0.22, k)
        for j in range(4):
            G += T.gauss(0.45 + 0.2 * (-1 if j % 2 else 1), -0.15 + 0.4 * (j // 2), 0.025) * k * 1.2
    g, h = clarao(T, t, 0.42, 0.6, 0.45, 0.05, 0.7)
    return (G + g) * env, (H + h) * env


def vamos_nos_separar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.5), 2)
    k = 1 - rel(t, 0.8, 0.95)
    for j, a in enumerate((-0.9, -math.pi / 2, math.pi + 0.9)):
        r = 0.1 + 0.45 * u
        g, h = icone(T, poe(SETA, r * math.cos(a), -0.1 + r * math.sin(a), 0.1, a), k * 1.2, 0.5)
        G, H = G + g, H + h
        G += T.lines([(0.0, -0.1, r * 0.7 * math.cos(a), -0.1 + r * 0.7 * math.sin(a), 1.0)], 0.008) * k * 1.0
    for x in (-0.55, 0.0, 0.55):
        m = pulso(t, 0.45, 1.0)
        G += T.gauss(x, 0.1, 0.13, 0.2) * m * 0.45
        G += particulas(T, t, 0.45, 1.0, 5, int(x * 10) + 50, x, 0.3, 0.1, 0.4, 0.011)
    return G * env, H * env


def armadilha_perfeita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.1, 0.4), 2.3)
    k = 1 - rel(t, 0.88, 1)
    if u > 0 and k > 0:
        y = -0.95 + 0.95 * u
        topo = y - 0.3
        G += T.lines([(0.45, -1.0, 0.45, topo, 1.0)], 0.008) * k * 1.0
        barras = [(0.25 + 0.1 * m, topo, 0.25 + 0.1 * m, y + 0.3, 1.0) for m in range(5)]
        barras += [(0.23, topo, 0.67, topo, 1.0), (0.23, y + 0.3, 0.67, y + 0.3, 1.0)]
        G += T.lines(barras, 0.016) * k * 1.3
    g, h = clarao(T, t, 0.38, 0.58, 0.45, 0.3, 1.1, 1.2)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.38, 0.8, 0.6, 0.35, 1.3)
    g2, h2 = _tontas(T, t, 0.45, 1.0, 0.45, -0.1, 3, 0.1, 0.03)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Leorio

def soco_teletransportado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        G += _portal(T, -0.5, 0.0, 0.14 * s, t, 1.0)
        G += _portal(T, 0.2, 0.0, 0.14 * s, -t, 1.0)
    u = ease_in(rel(t, 0.25, 0.45), 2)
    k = 1 - rel(t, 0.55, 0.7)
    if u > 0 and k > 0:
        P, nos = _punho(T, 0.2 + 0.2 * u, 0.0, 2.2, 0)
        G += P * 0.95 * k
        H += nos * 0.4 * k
        P2, _ = _punho(T, -0.55 + 0.05 * u, 0.0, 1.8, 0)
        G += P2 * 0.5 * (1 - u)
    g, h = clarao(T, t, 0.4, 0.6, 0.5, 0.0, 1.1, 1.2)
    G, H = G + g, H + h
    G += estouro(T, t, 0.42, 0.85, 12, 4, 0.5, 0.0, 0.45, 0.012)
    return G * env, H * env


def primeiros_socorros(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = icone(T, [(-0.65, -0.1), (-0.3, -0.1), (-0.3, 0.12), (-0.65, 0.12)], s * 1.1, 0.45)
        G, H = G + g, H + h
        G += T.arc_band(0.07, 0.015, math.pi, TAU, 1.0, 0, -0.475, -0.1, 0.0) * s * 1.2
    u = rel(t, 0.25, 0.75)
    if 0 < u < 1:
        pts = [(0.3 + 0.14 * math.cos(a), 0.0 + 0.3 * a / (TAU * 2.5) - 0.15) for a in np.linspace(0, TAU * 2.5 * u, 40)]
        if len(pts) > 1:
            G += T.polyline(pts, 0.025) * 1.1
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g2, h2 = icone(T, poe(CRUZ, 0.3, -0.35, 0.09 * m), 1.3, 0.5)
        G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.45, 1.0, 0.3, 0.0, 0.7)
    G += particulas(T, t, 0.5, 1.0, 12, 6, 0.3, 0.2, 0.15, 0.5, 0.012)
    return (G + g3) * env, (H + h3) * env


_BISTURI = [(-1.0, -0.06), (0.35, -0.06), (0.6, -0.2), (1.0, 0.0), (0.6, 0.08), (0.35, 0.06), (-1.0, 0.06)]


def leorio_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(_BISTURI, 0, 0, 0.3, -0.5), 1.2, 0.5)
    G, H = G + g, H + h
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    G += T.gauss(0, 0, 0.2, 0.12) * (0.4 + 0.3 * b)
    u = (t * 2) % 1
    H += T.gauss(-0.25 + 0.5 * u, 0.14 - 0.28 * u, 0.02) * 1.8
    return G, H


def bisturi_de_nen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.38))
    if s > 0:
        g, h = icone(T, poe(_BISTURI, -0.4, -0.05, 0.25 * s, -0.2), 1.2, 0.5)
        G, H = G + g, H + h
    k = pulso(t, 0.25, 0.6)
    if k > 0:
        G += T.lines([(-0.2, -0.15, 0.9, 0.12, 1.0)], 0.006) * k * 1.8
        H += T.lines([(-0.2, -0.15, 0.9, 0.12, 1.0)], 0.003) * k * 2.0
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.45, 0.0, 1.1, 1.3)
    G, H = G + g2, H + h2
    w = rel(t, 0.4, 0.85)
    if 0 < w < 1:
        G += T.lines([(0.45 - 0.25, -0.06 - 0.03 * w, 0.45 + 0.25, 0.06 - 0.03 * w, 1.0)], 0.012) * (1 - w) * 1.2
    G += particulas(T, t, 0.35, 0.9, 12, 4, 0.45, 0.0, 0.2, 0.3, 0.01)
    return G * env, H * env


REGISTRO = [
    ("arma_de_laser_morty", arma_de_laser_morty, GRANDE, "Morty · a arma tremendo e o tiro verde", False),
    ("grito_de_panico", grito_de_panico, GRANDE, "Morty · o grito em ondas e o suor", False),
    ("morty_preparo", morty_preparo, MEDIA, "Morty · o tapa-olho e o olho frio (Preparo, laço)", True),
    ("morty_mau", morty_mau, GRANDE, "Morty · o espiral e o feixe do Morty mau", False),
    ("giro_de_cauda", giro_de_cauda, GRANDE, "Tails · as duas caudas girando", False),
    ("voo_de_resgate", voo_de_resgate, GRANDE, "Tails · o voo e os anéis no trio", False),
    ("tails_preparo", tails_preparo, MEDIA, "Tails · a engrenagem e a carga (Preparo, laço)", True),
    ("canhao_de_energia_tails", canhao_de_energia_tails, GRANDE, "Tails · o tiro de energia", False),
    ("soco_espinhoso", soco_espinhoso, GRANDE, "Knuckles · a luva com espinhos", False),
    ("escavar", escavar, GRANDE, "Knuckles · a terra subindo e o monte", False),
    ("knuckles_preparo", knuckles_preparo, MEDIA, "Knuckles · o punho e as pedras (Preparo, laço)", True),
    ("soco_do_terremoto", soco_do_terremoto, GRANDE, "Knuckles · o soco no chão e as rachaduras", False),
    ("lupa_da_velma", lupa_da_velma, GRANDE, "Velma · a lupa e a exclamação", False),
    ("cade_meus_oculos", cade_meus_oculos, GRANDE, "Velma · os óculos caindo e a vista embaçada", False),
    ("velma_preparo", velma_preparo, MEDIA, "Velma · o dedo apontando (Preparo, laço)", True),
    ("tirar_a_mascara", tirar_a_mascara, GRANDE, "Velma · a máscara voando", False),
    ("rede_do_fred", rede_do_fred, GRANDE, "Fred · a rede caindo no rival", False),
    ("vamos_nos_separar", vamos_nos_separar, GRANDE, "Fred · as setas se separando", False),
    ("armadilha_perfeita", armadilha_perfeita, GRANDE, "Fred · a gaiola caindo", False),
    ("soco_teletransportado", soco_teletransportado, GRANDE, "Leorio · os portais e o punho", False),
    ("primeiros_socorros", primeiros_socorros, GRANDE, "Leorio · a maleta, a faixa e a cruz", False),
    ("leorio_preparo", leorio_preparo, MEDIA, "Leorio · o bisturi brilhando (Preparo, laço)", True),
    ("bisturi_de_nen", bisturi_de_nen, GRANDE, "Leorio · o corte fino do bisturi", False),
]
