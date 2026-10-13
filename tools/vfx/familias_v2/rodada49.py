"""Rodada 49 das habilidades próprias: Anúbis, Rá, Set, Ísis, Hórus e Sekhmet.

Anúbis
- cajado_do_juizo: o cajado com a cabeça de chacal e o selo da maldição no rival (Amaldiçoado).
- guia_das_almas: a alma subindo pelo portal do Duat e voltando para o corpo do aliado caído (Levantar).
- anubis_preparo: o Preparo do Juízo — a balança das almas pendendo e os olhos de chacal acesos (laço).
- julgamento_de_anubis: a balança — a pena de um lado, o coração do outro — pesando e caindo no rival (Enfraquecido).

- raio_solar_ra: o disco solar acima da cabeça de falcão e o feixe de sol que queima (Queimando).
- clarao_de_ra: o sol abrindo os olhos e o clarão branco em todos os rivais (Cego).
- ra_preparo: o Preparo da Fúria de Rá — o disco solar crescendo com a serpente em volta (laço).
- furia_de_ra: o sol enorme e os raios descendo em leque sobre todos os rivais, as chamas (Queimando).

Set
- tempestade_de_areia_set: o redemoinho de areia cobrindo os rivais e os grãos voando (Cego e Confuso).
- cetro_do_caos: o cetro com a cabeça da besta de Set batendo e a rachadura vermelha (Exposto).
- set_preparo: o Preparo da Traição — a adaga escondida nas costas e os olhos vermelhos (laço).
- traicao_de_set: o vulto surgindo atrás do rival e a facada pelas costas.

Ísis
- bencao_de_isis: as asas abertas de Ísis em cima do aliado e a luz turquesa da cura (Vida).
- purificacao_de_isis: o ankh brilhando sobre o trio e os debuffs se dissolvendo (Purificar, Protegido e Regeneração).
- isis_preparo: o Preparo da Ressurreição — as asas fechando e abrindo em volta do ankh (laço).
- ressurreicao_de_isis: o ankh gigante acendendo e a luz levantando o aliado caído (Vida e Levantar).

Hórus
- garras_do_falcao: o falcão mergulhando e as garras rasgando em X.
- olho_de_horus: o Olho de Hórus abrindo em cima do rival e a mira (Marcado e Exposto).
- horus_preparo: o Preparo do Voo do falcão — as asas abertas e o olho brilhando (laço).
- voo_do_falcao: o falcão de luz mergulhando do alto e atravessando o rival.

Sekhmet
- garras_da_leoa: as patas de leoa rasgando e o sangue (Sangrando).
- rugido_de_sekhmet: a cabeça de leoa rugindo e as ondas vermelhas nos rivais (Enfraquecido).
- sekhmet_preparo: o Preparo da Fúria da leoa — a juba em chamas e o sol vermelho atrás (laço).
- furia_da_leoa: o salto da leoa, as garras e a vida voltando para ela (Roubo de vida).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (ASA, CHAMA, CORACAO, GOTA, PENA, anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao,
                         particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _sol(T, cx, cy, r, gira, k, n=12):
    G = T.gauss(cx, cy, r * 0.9) * k * 1.2
    G += T.ring(r, r * 0.12, cx, cy) * k * 1.2
    segs = []
    for j in range(n):
        a = gira + TAU * j / n
        r2 = r * (1.6 if j % 2 else 1.35)
        segs.append((cx + r * 1.15 * math.cos(a), cy + r * 1.15 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a), 1.0))
    G += T.tapered(segs, r * 0.12) * k * 1.2
    return G, T.gauss(cx, cy, r * 0.4) * k * 1.4


def _ankh(T, cx, cy, s, k):
    G = T.ring(s * 0.28, s * 0.09, cx, cy - s * 0.55, 0.8) * k * 1.3
    G += T.lines([(cx, cy - s * 0.25, cx, cy + s * 0.9, 1.0), (cx - s * 0.4, cy - s * 0.15, cx + s * 0.4, cy - s * 0.15, 1.0)], s * 0.14) * k * 1.3
    return G, T.gauss(cx, cy - s * 0.15, s * 0.12) * k * 1.2


def _olho_horus(T, cx, cy, s, k, abre=1.0):
    G = 0.0
    topo = [(cx - s, cy), (cx - s * 0.4, cy - s * 0.4 * abre), (cx + s * 0.4, cy - s * 0.4 * abre), (cx + s, cy)]
    base = [(cx - s, cy), (cx - s * 0.4, cy + s * 0.35 * abre), (cx + s * 0.4, cy + s * 0.35 * abre), (cx + s, cy)]
    G += T.polyline(topo, s * 0.08) * k * 1.3 + T.polyline(base, s * 0.08) * k * 1.3
    G += T.gauss(cx, cy, s * 0.25 * abre + 0.001) * k * 1.4
    G += T.polyline([(cx - s * 0.1, cy + s * 0.35), (cx - s * 0.15, cy + s * 0.9), (cx - s * 0.3, cy + s * 1.05)], s * 0.07) * k * 1.2
    G += T.polyline([(cx + s * 0.3, cy + s * 0.3), (cx + s * 0.6, cy + s * 0.8), (cx + s * 0.85, cy + s * 0.7), (cx + s * 0.8, cy + s * 0.55)], s * 0.07) * k * 1.2
    G += T.polyline([(cx - s * 1.1, cy - s * 0.65), (cx + s * 0.9, cy - s * 0.65)], s * 0.07) * k * 1.1
    return G, T.gauss(cx, cy, s * 0.1) * k * 1.5 * abre


def _balanca(T, cx, cy, s, inclina, k):
    G = T.lines([(cx, cy - s * 0.9, cx, cy + s * 0.9, 1.0)], s * 0.05) * k * 1.2
    c, sn = math.cos(inclina), math.sin(inclina)
    x1, y1, x2, y2 = cx - s * c, cy - s * 0.8 - s * sn, cx + s * c, cy - s * 0.8 + s * sn
    G += T.lines([(x1, y1, x2, y2, 1.0)], s * 0.05) * k * 1.2
    for x, y in ((x1, y1), (x2, y2)):
        G += T.lines([(x, y, x - s * 0.2, y + s * 0.5, 1.0), (x, y, x + s * 0.2, y + s * 0.5, 1.0)], s * 0.02) * k * 1.0
        G += T.arc_band(s * 0.22, s * 0.05, 0.0, math.pi, 1.0, 0, x, y + s * 0.5, 0.0) * k * 1.2
    return G, (x1, y1 + s * 0.45), (x2, y2 + s * 0.45)


# ------------------------------------------------------------------ Anúbis

_CHACAL = [(-0.5, 0.6), (-0.45, -0.1), (-0.6, -0.95), (-0.25, -0.4), (0.1, -0.35), (0.3, -0.95), (0.35, -0.3), (0.95, 0.05), (0.9, 0.2),
           (0.4, 0.25), (0.3, 0.6)]


def cajado_do_juizo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.8)
    k = 1 - rel(t, 0.45, 0.57)
    if k > 0:
        ang = -2.2 + 1.9 * u
        hx, hy = -0.05 + 0.6 * math.cos(ang), 0.35 + 0.6 * math.sin(ang)
        G += T.lines([(-0.05, 0.35, hx, hy, 1.0)], 0.022) * k * 1.2
        g, h = icone(T, poe(_CHACAL, hx, hy, 0.16, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.1, 1.2)
    G, H = G + g2, H + h2
    s = surge(t, 0.4, 0.62) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.2 * s, 0.015, 0.45, 0.0) * 1.2
        for j in range(6):
            a = t * 2 + TAU * j / 6
            G += T.lines([(0.45 + 0.13 * s * math.cos(a), 0.13 * s * math.sin(a), 0.45 + 0.2 * s * math.cos(a), 0.2 * s * math.sin(a), 1.0)], 0.01) * 1.2
        g3, h3 = icone(T, poe(_CHACAL, 0.45, 0.0, 0.08 * s), 1.0, 0.4)
        G, H = G + g3, H + h3
    G += particulas(T, t, 0.35, 1.0, 12, 77, 0.45, 0.0, 0.15, -0.3, 0.012)
    return G * env, H * env


def guia_das_almas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    p = ease_out(rel(t, 0.0, 0.25), 2)
    if p > 0 and k > 0:
        G += T.ring(0.25 * p, 0.03, 0.0, -0.5, 2.5) * k * 1.3
        G += T.ring(0.17 * p, 0.012, 0.0, -0.5, 2.5) * k * 1.0
        G += T.gauss(0.0, -0.5, 0.2 * p, 0.07) * k * 0.6
    u = rel(t, 0.2, 0.7)
    if 0 < u < 1:
        y = -0.5 + 0.75 * ease_in(u, 1.3)
        alma = [(0, -1), (0.5, -0.4), (0.4, 0.4), (0.15, 0.9), (0, 0.6), (-0.15, 0.9), (-0.4, 0.4), (-0.5, -0.4)]
        g, h = icone(T, poe(alma, 0.06 * math.sin(u * 10), y, 0.1), 1.3, 0.5)
        G, H = G + g, H + h
        G += T.tapered([(0.0, -0.5, 0.06 * math.sin(u * 10), y - 0.05, 0.8)], 0.04) * 0.7
    w = rel(t, 0.65, 0.9)
    if w > 0 and k > 0:
        G += T.gauss(0.0, 0.25, 0.25, 0.3) * pulso(t, 0.65, 1.0) * 0.6
        G += anel(T, t, 0.68, 0.95, 0.05, 0.5, 0.03, 0.25, 2.0)
        H += T.flare(0.0, 0.2, 0.4 * pulso(t, 0.65, 0.9) + 0.01, 0.0, 0.01) * 1.5 * pulso(t, 0.65, 0.9)
    return G * env, H * env


def anubis_preparo(T, t, rng):
    G, H = vazio(T)
    g, p1, p2 = _balanca(T, 0.0, 0.15, 0.42, 0.25 * math.sin(t * TAU), 1.0)
    G += g
    g2, h2 = icone(T, poe(PENA, p1[0], p1[1] - 0.06, 0.06), 1.1, 0.5)
    G, H = G + g2, H + h2
    g3, h3 = cheio(T, poe(CORACAO, p2[0], p2[1] - 0.04, 0.045), 1.1)
    G, H = G + g3, H + h3
    b = 0.6 + 0.4 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, -0.4, 0.015) * b * 2.0
    return G, H


def julgamento_de_anubis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.65))
    inclina = 0.05 * math.sin(t * 20) * (1 - rel(t, 0.2, 0.35)) + 0.5 * ease_in(rel(t, 0.3, 0.45), 2)
    if s > 0:
        g, p1, p2 = _balanca(T, 0.45, -0.3, 0.38 * s, inclina, 1.0)
        G += g
        g2, h2 = icone(T, poe(PENA, p1[0], p1[1] - 0.06, 0.05 * s), 1.1, 0.5)
        G, H = G + g2, H + h2
        g3, h3 = cheio(T, poe(CORACAO, p2[0], p2[1] - 0.04, 0.045 * s), 1.1)
        G, H = G + g3, H + h3
    g4, h4 = clarao(T, t, 0.45, 0.7, 0.45, 0.05, 1.6, 1.5)
    G, H = G + g4, H + h4
    G += anel(T, t, 0.47, 0.9, 0.05, 0.6, 0.04, 0.05)
    G += onda_no_chao(T, t, 0.47, 0.95, 0.8, 0.38, 1.3)
    m = surge(t, 0.62, 0.8) * (1 - rel(t, 0.9, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.25 + 0.1 * j + 0.1 * rel(t, 0.62, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.07 * m), (0.52, y0)], 0.014) * m * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Rá

def raio_solar_ra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        g, h = _sol(T, -0.55, -0.35, 0.09 * s, t * 3, 1.0)
        G, H = G + g, H + h
    u = rel(t, 0.2, 0.4)
    k = 1 - rel(t, 0.6, 0.72)
    if u > 0 and k > 0:
        e = min(1.0, ease_in(u) * 1.2)
        x2, y2 = -0.55 + 1.0 * e, -0.35 + 0.35 * e
        G += T.tapered([(-0.55, -0.35, x2, y2, 1.0)], 0.12) * k * 0.8
        G += T.lines([(-0.55, -0.35, x2, y2, 1.0)], 0.022) * k * 1.4
        H += T.lines([(-0.55, -0.35, x2, y2, 1.0)], 0.008) * k
    g2, h2 = clarao(T, t, 0.35, 0.6, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    kk = pulso(t, 0.45, 1.0)
    if kk > 0:
        for m in range(3):
            g3, h3 = icone(T, poe(CHAMA, 0.37 + 0.08 * m, 0.08 - 0.02 * math.sin(t * 25 + m), 0.05 + 0.01 * math.sin(t * 18 + m)), kk * 1.1, 0.7)
            G, H = G + g3, H + h3
    return G * env, H * env


def clarao_de_ra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3)
    abre = ease_out(rel(t, 0.2, 0.4), 2)
    k = 1 - rel(t, 0.75, 0.9)
    if s > 0 and k > 0:
        g, h = _sol(T, 0.0, -0.5, 0.12 * s, t * 2, k)
        G, H = G + g, H + h
        g2, h2 = _olho_horus(T, 0.0, -0.5, 0.07, k * 1.2, abre)
        G, H = G + g2 * 0.8, H + h2
    f = pulso(t, 0.35, 0.75)
    if f > 0:
        G += T.gauss(0.0, -0.2, 0.55, 0.35) * f * 0.3
        H += T.flare(0.0, -0.5, 1.2 * f, 0.0, 0.015) * 1.5 + T.flare(0.0, -0.5, 0.8 * f, math.pi / 2, 0.012) * 1.5
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = pulso(t, 0.5 + 0.05 * i, 1.0)
        if m > 0:
            for lado in (-1, 1):
                G += T.lines([(cx + lado * 0.06 - 0.03, -0.12, cx + lado * 0.06 + 0.03, -0.06, 1.0),
                              (cx + lado * 0.06 + 0.03, -0.12, cx + lado * 0.06 - 0.03, -0.06, 1.0)], 0.01) * m * 1.3
    return G * env, H * env


def ra_preparo(T, t, rng):
    G, H = vazio(T)
    r = 0.13 + 0.02 * math.sin(t * TAU * 2)
    g, h = _sol(T, 0.0, -0.05, r, t * TAU * 0.4, 1.0, 16)
    G, H = G + g, H + h
    pts = [(0.25 * math.cos(a), -0.05 + 0.25 * math.sin(a) * 0.9) for a in np.linspace(t * TAU, t * TAU + TAU * 0.8, 30)]
    G += T.polyline(pts, 0.016) * 1.2
    G += T.gauss(pts[-1][0], pts[-1][1], 0.025) * 1.3
    return G, H


def furia_de_ra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.78, 0.9))
    if s > 0:
        g, h = _sol(T, 0.0, -0.65, 0.17 * s, t * 2, 1.0, 16)
        G, H = G + g, H + h
    G += converge(T, t, 0.05, 0.3, 14, 78, 0.0, -0.65, 0.45, 0.008)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.28 + 0.05 * i, 0.45 + 0.05 * i)
        k = 1 - rel(t, 0.65 + 0.05 * i, 0.78 + 0.05 * i)
        if u > 0 and k > 0:
            e = min(1.0, ease_in(u) * 1.2)
            G += T.tapered([(0.0, -0.6, cx * e, -0.6 + 0.6 * e, 1.0)], 0.13) * k * 0.8
            G += T.lines([(0.0, -0.6, cx * e, -0.6 + 0.6 * e, 1.0)], 0.022) * k * 1.3
            H += T.lines([(0.0, -0.6, cx * e, -0.6 + 0.6 * e, 1.0)], 0.008) * k
        g2, h2 = clarao(T, t, 0.42 + 0.05 * i, 0.65 + 0.05 * i, cx, 0.0, 0.6, 1.1)
        G, H = G + g2, H + h2
        kk = pulso(t, 0.5 + 0.05 * i, 1.0)
        if kk > 0:
            for m in range(3):
                g3, h3 = icone(T, poe(CHAMA, cx - 0.08 + 0.08 * m, 0.12 - 0.02 * math.sin(t * 25 + m + i), 0.05 + 0.012 * math.sin(t * 18 + m)), kk * 1.1, 0.7)
                G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.35, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ Set

def _areia(T, t, cx, cy, r, k, seed):
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(40):
        a0, rr, v = q.uniform(0, TAU), q.uniform(0.2, 1.0) * r, q.uniform(6, 12)
        a = a0 + t * v
        pts.append((cx + rr * math.cos(a), cy + rr * 0.45 * math.sin(a) - 0.3 * r * (rr / r), q.uniform(0.5, 1.0) * k))
    return T.splats(pts, 0.009) * 1.3


def tempestade_de_areia_set(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for m in range(4):
        u = rel(t, 0.04 * m, 0.45 + 0.04 * m)
        if 0 < u < 1:
            x = -1.0 + 2.0 * ease_out(u, 1.3)
            G += T.gauss(x, 0.05 + 0.06 * (m - 1.5), 0.35, 0.1) * (1 - rel(u, 0.7, 1)) * 0.35
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = ease_out(rel(t, 0.25 + 0.06 * i, 0.45 + 0.06 * i), 2) * (1 - rel(t, 0.85, 0.97))
        if k > 0:
            G += _areia(T, t, cx, 0.1, 0.22, k, 79 + i)
            for m in range(3):
                a = -t * 10 + m * 2.1
                G += T.arc_band(0.1 + 0.05 * m, 0.016, a, a + 2.2, 0.4, 0, cx, 0.25 - 0.1 * m, 1.0) * k * 1.1
            G += T.gauss(cx, 0.05, 0.16, 0.2) * k * 0.3
    return G * env, H * env


_BESTA = [(-0.5, 0.5), (-0.4, -0.1), (-0.5, -0.9), (-0.25, -0.35), (0.05, -0.35), (0.1, -0.9), (0.25, -0.25), (0.95, 0.15), (0.9, 0.3),
          (0.3, 0.3), (0.25, 0.5)]


def cetro_do_caos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.57)
    if k > 0:
        ang = -2.2 + 1.85 * u
        hx, hy = -0.05 + 0.6 * math.cos(ang), 0.35 + 0.6 * math.sin(ang)
        G += T.lines([(-0.05, 0.35, hx, hy, 1.0)], 0.022) * k * 1.2
        g, h = icone(T, poe(_BESTA, hx, hy, 0.16, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.45, 0.05, 1.2, 1.3)
    G, H = G + g2, H + h2
    racha = ease_out(rel(t, 0.3, 0.5), 2)
    if racha > 0:
        kk = 1 - rel(t, 0.85, 0.97)
        for j in range(4):
            a = -0.6 + 0.4 * j
            G += _zap(T, 85 + j, 0.45, 0.05, 0.45 + 0.3 * racha * math.cos(a), 0.05 + 0.3 * racha * math.sin(a), 0.01, 3, 0.25) * kk * 1.3
    m = surge(t, 0.5, 0.72) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.11 * m, 0.012, 0.45, -0.05) * 1.3
        G += T.lines([(0.45 - 0.17 * m, -0.05, 0.45 - 0.06 * m, -0.05, 1.0), (0.45 + 0.06 * m, -0.05, 0.45 + 0.17 * m, -0.05, 1.0),
                      (0.45, -0.05 - 0.17 * m, 0.45, -0.05 - 0.06 * m, 1.0), (0.45, -0.05 + 0.06 * m, 0.45, -0.05 + 0.17 * m, 1.0)], 0.01) * 1.3
    return G * env, H * env


_ADAGA = [(0, -1), (0.12, -0.7), (0.1, 0.25), (0.3, 0.3), (0.3, 0.4), (0.07, 0.4), (0.07, 0.9), (-0.07, 0.9), (-0.07, 0.4),
          (-0.3, 0.4), (-0.3, 0.3), (-0.1, 0.25), (-0.12, -0.7)]


def set_preparo(T, t, rng):
    G, H = vazio(T)
    sombra = [(-0.22, 0.4), (-0.28, -0.05), (-0.18, -0.3), (-0.08, -0.38), (0.08, -0.38), (0.18, -0.3), (0.28, -0.05), (0.22, 0.4)]
    g, h = icone(T, sombra, 0.5, 0.2)
    G, H = G + g, H + h
    b = 0.6 + 0.4 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, -0.25, 0.015) * b * 2.0
        G += T.gauss(lado * 0.07, -0.25, 0.035) * b * 0.8
    brilho = (t * 1.5) % 1
    g2, h2 = icone(T, poe(_ADAGA, 0.32, 0.15, 0.16, 2.6), 1.0, 0.5)
    G, H = G + g2, H + h2
    H += T.gauss(0.32 + 0.12 * (brilho - 0.5), 0.15 + 0.1 * (brilho - 0.5), 0.015) * 1.5
    return G, H


def traicao_de_set(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        sombra = [(0.73, 0.4), (0.67, -0.05), (0.77, -0.3), (0.87, -0.38), (1.0, -0.36), (1.03, -0.05), (0.97, 0.4)]
        g, h = icone(T, poe(sombra, -0.05, 0.0, 1.0), s * 0.6, 0.25)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(0.82 + lado * 0.05, -0.27, 0.012) * s * 2.0
    u = ease_in(rel(t, 0.25, 0.4), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if u > 0 and k > 0:
        g2, h2 = icone(T, poe(_ADAGA, 0.75 - 0.3 * u, 0.0, 0.14, -math.pi / 2), k * 1.3, 0.5)
        G, H = G + g2, H + h2
    g3, h3 = corte(T, t, 0.36, 0.55, 2.6, 0.9, 0.08, 0.45, 0.0)
    G, H = G + g3 * 1.2, H + h3
    g4, h4 = clarao(T, t, 0.38, 0.6, 0.45, 0.0, 1.5, 1.5)
    G, H = G + g4, H + h4
    G += estouro(T, t, 0.4, 0.85, 14, 86, 0.45, 0.0, 0.5, 0.013)
    q = np.random.default_rng(87)
    for j in range(8):
        w = rel(t, 0.42 + 0.02 * j, 0.9)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.45, -0.1), q.uniform(-0.4, -0.1)
            g5, h5 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.8 * w * w, 0.03), (1 - w) * 1.1)
            G, H = G + g5, H + h5
    return G * env, H * env


# ------------------------------------------------------------------ Ísis

def _asas_isis(T, cx, cy, s, abre, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        for m in range(3):
            pts = [(cx, cy), (cx + lado * s * (0.4 + 0.6 * abre), cy - s * (0.3 + 0.2 * m) * abre),
                   (cx + lado * s * (0.5 + 0.55 * abre), cy - s * (0.1 + 0.12 * m)), (cx + lado * s * 0.3, cy + s * 0.05 * m)]
            g, h = icone(T, pts, k * (1.0 - 0.15 * m), 0.3)
            G, H = G + g, H + h
    return G, H


def bencao_de_isis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.8, 0.95)
    if k > 0:
        g, h = _asas_isis(T, 0.0, -0.3, 0.55, abre, k * 1.1)
        G, H = G + g, H + h
    kk = pulso(t, 0.25, 0.95)
    if kk > 0:
        G += T.gauss(0.0, 0.0, 0.25, 0.35) * kk * 0.5
        G += T.ring(0.25, 0.015, 0.0, 0.3, 3.0) * kk * 1.2
        H += T.flare(0.0, 0.0, 0.3 * kk + 0.01, 0.0, 0.01) * 1.3
    for j in range(8):
        u = rel(t, 0.3 + 0.05 * j, 0.8 + 0.05 * j)
        if 0 < u < 1:
            x = -0.2 + 0.4 * ((j * 0.37) % 1)
            G += T.lines([(x - 0.025, 0.2 - 0.4 * u, x + 0.025, 0.2 - 0.4 * u, 1.0), (x, 0.175 - 0.4 * u, x, 0.225 - 0.4 * u, 1.0)], 0.008) * (1 - u) * 1.4
    return G * env, H * env


def purificacao_de_isis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _ankh(T, 0.0, -0.45, 0.22 * s, 1.0)
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.45, 0.25 * s) * 0.3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.25 + 0.05 * i, 0.45 + 0.05 * i)
        if 0 < u < 1:
            G += T.tapered([(0.0, -0.4, cx * u, -0.4 + 0.5 * u, 1.0)], 0.02) * (1 - u) * 1.2
        k = pulso(t, 0.4 + 0.05 * i, 1.0)
        if k > 0:
            G += T.ring(0.18, 0.015, cx, 0.1) * k * 1.0
            G += T.gauss(cx, 0.1, 0.13) * k * 0.35
        q = np.random.default_rng(88 + i)
        for _ in range(6):
            w = rel(t, 0.45 + 0.05 * i, 0.85 + 0.05 * i)
            if 0 < w < 1:
                x, y = cx + q.uniform(-0.12, 0.12), 0.1 + q.uniform(-0.12, 0.12)
                G += T.gauss(x, y - 0.2 * w, 0.015 * (1 - w)) * (1 - w) * 0.8
    G += anel(T, t, 0.45, 0.9, 0.1, 1.0, 0.03, 0.25, 3.0)
    return G * env, H * env


def isis_preparo(T, t, rng):
    G, H = vazio(T)
    abre = 0.5 + 0.5 * math.sin(t * TAU)
    g, h = _asas_isis(T, 0.0, 0.0, 0.4, 0.4 + 0.6 * abre, 1.0)
    G, H = G + g, H + h
    g2, h2 = _ankh(T, 0.0, 0.05, 0.16, 1.2)
    G, H = G + g2, H + h2
    return G, H


def ressurreicao_de_isis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _ankh(T, 0.0, -0.3, 0.38 * s, 1.0)
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.3, 0.4 * s) * 0.3
    k = pulso(t, 0.35, 1.0)
    if k > 0:
        G += T.gauss(0.0, 0.1, 0.12, 0.45) * k * 0.6
        H += T.gauss(0.0, 0.1, 0.03, 0.4) * k * 0.6
    G += anel(T, t, 0.45, 0.9, 0.05, 0.7, 0.04, 0.3, 2.5)
    G += particulas(T, t, 0.4, 1.0, 22, 89, 0.0, 0.25, 0.3, 0.8, 0.011)
    g3, h3 = clarao(T, t, 0.55, 0.85, 0.0, 0.1, 1.3, 1.3)
    return (G + g3) * env, (H + h3) * env


# ------------------------------------------------------------------ Hórus

def _falcao(T, cx, cy, s, ang, k, bate=0.0):
    G, H = 0.0, 0.0
    corpo = [(1.0, 0.0), (0.6, -0.12), (-0.5, -0.1), (-0.9, -0.25), (-0.85, 0.0), (-0.9, 0.25), (-0.5, 0.1), (0.6, 0.12)]
    g, h = icone(T, poe(corpo, cx, cy, s, ang), k, 0.45)
    G, H = G + g, H + h
    for lado in (-1, 1):
        g2, h2 = icone(T, poe(ASA, cx, cy, s * 0.9, ang + lado * (math.pi / 2 + 0.4 * bate) + (math.pi if lado < 0 else 0)), k, 0.35)
        G, H = G + g2, H + h2
    return G, H


def garras_do_falcao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.28), 1.5)
    if 0 < u < 1:
        x, y = -0.6 + 1.0 * u, -0.6 + 0.55 * u
        g, h = _falcao(T, x, y, 0.22, math.atan2(0.55, 1.0), 1.1, math.sin(t * 30))
        G, H = G + g, H + h
    for j, ang in enumerate((0.8, -0.8)):
        for m in (-1, 0, 1):
            dx, dy = -math.sin(ang) * 0.07 * m, math.cos(ang) * 0.07 * m
            g2, h2 = corte(T, t, 0.25 + 0.12 * j + 0.015 * (m + 1), 0.48 + 0.12 * j + 0.015 * (m + 1), ang, 0.6, 0.04, 0.45 + dx, dy)
            G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.27, 0.55, 0.45, 0.0, 1.1)
    G, H = G + g3, H + h3
    q = np.random.default_rng(90)
    for j in range(6):
        w = rel(t, 0.35, 0.95)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0)
            d = 0.1 + 0.4 * ease_out(w)
            g4, h4 = icone(T, poe(PENA, 0.45 + d * math.cos(a), d * math.sin(a) + 0.4 * w * w, 0.035, a + w * 5), (1 - w) * 1.1, 0.5)
            G, H = G + g4, H + h4
    return G * env, H * env


def olho_de_horus(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.1, 0.35), 2)
    k = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        g, h = _olho_horus(T, 0.45, -0.4, 0.12, k * 1.2, abre)
        G, H = G + g, H + h
        G += T.gauss(0.45, -0.4, 0.2) * k * 0.3
    u = rel(t, 0.35, 0.55)
    if u > 0 and k > 0:
        G += T.tapered([(0.45, -0.35, 0.45, -0.35 + 0.33 * min(1.0, u * 1.3), 1.0)], 0.05) * k * 0.9
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.05) * 1.2
        G += T.ring(0.12 * m, 0.01, 0.45, 0.05) * 1.0
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.15 * m * math.cos(a), 0.05 + 0.15 * m * math.sin(a), 0.45 + 0.26 * m * math.cos(a), 0.05 + 0.26 * m * math.sin(a), 1.0)], 0.01) * 1.3
    return G * env, H * env


def horus_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _falcao(T, 0.0, 0.12, 0.32, -math.pi / 2, 1.0, 0.3 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    g2, h2 = _olho_horus(T, 0.0, -0.3, 0.07, 1.0 + 0.3 * math.sin(t * TAU * 2))
    return G + g2, H + h2


def voo_do_falcao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.42), 1.6)
    k = 1 - rel(t, 0.5, 0.6)
    if u > 0 and k > 0:
        x, y = -0.7 + 1.15 * u, -0.85 + 0.85 * u
        ang = math.atan2(0.85, 1.15)
        g, h = _falcao(T, x, y, 0.22, ang, k * 1.2, 0.0)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.8 * math.cos(ang), y - 0.8 * math.sin(ang), x, y, 1.0)], 0.12) * k * 0.6
        H += T.gauss(x, y, 0.04) * k * 1.4
    g2, h2 = clarao(T, t, 0.38, 0.65, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.42, 0.85, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.42, 0.9, 16, 91, 0.45, 0.0, 0.6, 0.014)
    q = np.random.default_rng(92)
    for j in range(10):
        w = rel(t, 0.45, 1.0)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            d = 0.1 + 0.5 * ease_out(w)
            g3, h3 = icone(T, poe(PENA, 0.45 + d * math.cos(a), d * math.sin(a) + 0.3 * w * w, 0.035, a + w * 5), (1 - w) * 1.1, 0.5)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Sekhmet

def _pata(T, t, a, b, cx, cy, ang):
    G, H = 0.0, 0.0
    for m in (-1.5, -0.5, 0.5, 1.5):
        dx, dy = -math.sin(ang) * 0.065 * m, math.cos(ang) * 0.065 * m
        g, h = corte(T, t, a, b, ang, 0.65, 0.045, cx + dx, cy + dy, 0.06)
        G, H = G + g, H + h
    return G, H


def garras_da_leoa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = _pata(T, t, 0.05, 0.3, 0.45, 0.0, 1.0)
    G, H = G + g * 1.2, H + h
    g, h = _pata(T, t, 0.22, 0.47, 0.45, 0.0, -1.0)
    G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.2, 0.45, 0.45, 0.0, 1.0)
    G, H = G + g2, H + h2
    q = np.random.default_rng(93)
    for j in range(12):
        w = rel(t, 0.3 + 0.02 * j, 0.85)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.45), q.uniform(-0.5, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.033), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


_LEOA = [(-0.75, 0.0), (-0.85, -0.45), (-0.55, -0.85), (-0.1, -0.95), (0.35, -0.8), (0.65, -0.45), (0.95, -0.2), (0.95, 0.15), (0.6, 0.3),
         (0.5, 0.65), (0.0, 0.75), (-0.5, 0.55)]


def rugido_de_sekhmet(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = icone(T, poe(_LEOA, -0.55, -0.15, 0.24 * s), 1.1, 0.35)
        G, H = G + g, H + h
        boca = pulso(t, 0.1, 0.7)
        G += T.polys([([(-0.4, -0.12), (-0.38 + 0.05 * boca, -0.08), (-0.38 + 0.05 * boca, -0.02 + 0.06 * boca), (-0.42, -0.04)], 1.0)], 0.004) * s * 1.2
        H += T.gauss(-0.52, -0.22, 0.012) * s * 2.0
        g2, h2 = _sol(T, -0.6, -0.42, 0.06 * s, t * 2, 0.8, 10)
        G, H = G + g2, H + h2
    for j in range(4):
        u = rel(t, 0.12 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.1 * u, 0.045 * (1 - 0.5 * u), -0.55, 0.55, 0.7, 0, -0.45, -0.08, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = surge(t, 0.5 + 0.06 * i, 0.68 + 0.06 * i) * (1 - rel(t, 0.88, 1))
        if m > 0 and i > 0:
            for k2 in range(2):
                y0 = -0.3 + 0.1 * k2 + 0.1 * rel(t, 0.5, 0.95)
                G += T.polyline([(cx - 0.07, y0), (cx, y0 + 0.07 * m), (cx + 0.07, y0)], 0.014) * m * 1.2
    return G * env, H * env


def sekhmet_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _sol(T, 0.0, -0.1, 0.22, t * TAU * 0.3, 0.6, 14)
    G, H = G + g, H + h
    for j in range(9):
        a = math.pi + math.pi * (j + 0.5) / 9 + 0.0
        x, y = 0.17 * math.cos(a), 0.05 + 0.17 * math.sin(a)
        g2, h2 = icone(T, poe(CHAMA, x, y, 0.05 + 0.012 * math.sin(t * 20 + j), a + math.pi / 2), 1.1, 0.7)
        G, H = G + g2, H + h2
    g3, h3 = icone(T, poe(_LEOA, 0.0, 0.1, 0.12), 1.0, 0.4)
    return G + g3, H + h3


def furia_da_leoa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        x = -0.6 + 0.9 * ease_in(u, 1.3)
        y = -0.3 * math.sin(math.pi * u)
        g, h = icone(T, poe(_LEOA, x, y, 0.2), 1.1, 0.4)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.5, y + 0.1, x - 0.1, y, 0.8)], 0.06) * 0.8
    g, h = _pata(T, t, 0.25, 0.48, 0.45, 0.0, 1.1)
    G, H = G + g * 1.3, H + h
    g, h = _pata(T, t, 0.32, 0.55, 0.45, 0.0, -1.1)
    G, H = G + g * 1.3, H + h
    g2, h2 = clarao(T, t, 0.3, 0.58, 0.45, 0.0, 1.5, 1.5)
    G, H = G + g2, H + h2
    for j in range(6):
        w = rel(t, 0.5 + 0.04 * j, 0.95)
        if 0 < w < 1:
            x = 0.45 - 1.0 * ease_in(w)
            y = -0.05 * (j - 2.5) * (1 - w) - 0.15 * math.sin(math.pi * w)
            G += T.gauss(x, y, 0.02) * (1 - rel(w, 0.8, 1)) * 1.3
            H += T.gauss(x, y, 0.01) * (1 - rel(w, 0.8, 1)) * 1.2
    kk = pulso(t, 0.8, 1.0)
    G += T.gauss(-0.55, 0.0, 0.15) * kk * 0.6
    G += anel(T, t, 0.8, 1.0, 0.05, 0.3, 0.02, 0.0)
    return G * env, H * env


REGISTRO = [
    ("cajado_do_juizo", cajado_do_juizo, GRANDE, "Anúbis · o cajado de chacal e o selo", False),
    ("guia_das_almas", guia_das_almas, GRANDE, "Anúbis · a alma voltando pelo portal", False),
    ("anubis_preparo", anubis_preparo, MEDIA, "Anúbis · a balança das almas (Preparo, laço)", True),
    ("julgamento_de_anubis", julgamento_de_anubis, GRANDE, "Anúbis · a balança pesando no rival", False),
    ("raio_solar_ra", raio_solar_ra, GRANDE, "Rá · o feixe do disco solar", False),
    ("clarao_de_ra", clarao_de_ra, GRANDE, "Rá · o olho do sol e o clarão", False),
    ("ra_preparo", ra_preparo, MEDIA, "Rá · o disco solar e a serpente (Preparo, laço)", True),
    ("furia_de_ra", furia_de_ra, GRANDE, "Rá · os raios de sol em leque", False),
    ("tempestade_de_areia_set", tempestade_de_areia_set, GRANDE, "Set · os redemoinhos de areia", False),
    ("cetro_do_caos", cetro_do_caos, GRANDE, "Set · o cetro da besta e a rachadura", False),
    ("set_preparo", set_preparo, MEDIA, "Set · a adaga escondida (Preparo, laço)", True),
    ("traicao_de_set", traicao_de_set, GRANDE, "Set · a facada pelas costas", False),
    ("bencao_de_isis", bencao_de_isis, GRANDE, "Ísis · as asas e a luz turquesa", False),
    ("purificacao_de_isis", purificacao_de_isis, GRANDE, "Ísis · o ankh sobre o trio", False),
    ("isis_preparo", isis_preparo, MEDIA, "Ísis · as asas em volta do ankh (Preparo, laço)", True),
    ("ressurreicao_de_isis", ressurreicao_de_isis, GRANDE, "Ísis · o ankh gigante levantando o aliado", False),
    ("garras_do_falcao", garras_do_falcao, GRANDE, "Hórus · o mergulho e as garras", False),
    ("olho_de_horus", olho_de_horus, GRANDE, "Hórus · o Olho de Hórus e a mira", False),
    ("horus_preparo", horus_preparo, MEDIA, "Hórus · o falcão e o olho (Preparo, laço)", True),
    ("voo_do_falcao", voo_do_falcao, GRANDE, "Hórus · o falcão de luz mergulhando", False),
    ("garras_da_leoa", garras_da_leoa, GRANDE, "Sekhmet · as patas rasgando", False),
    ("rugido_de_sekhmet", rugido_de_sekhmet, GRANDE, "Sekhmet · a leoa rugindo", False),
    ("sekhmet_preparo", sekhmet_preparo, MEDIA, "Sekhmet · a juba em chamas (Preparo, laço)", True),
    ("furia_da_leoa", furia_da_leoa, GRANDE, "Sekhmet · o salto e a vida voltando", False),
]
