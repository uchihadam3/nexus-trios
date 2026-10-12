"""As Mecânicas únicas ativando como uma habilidade (pedido do jogador: "a mecânica única a gente tem que tratar
como se fosse realmente uma habilidade… mostra o nome, para, ele ativa… um efeito único pra cada uma").

- unica_ativa: a ativação de quem ainda não tem efeito próprio — o círculo roxo de runas se abre em volta, as
  runas giram e acendem, e a luz sobe.
- cell_contagem: o "Vai explodir!" do Cell — o corpo incha de luz, as rachaduras brilham e os anéis da contagem
  fecham em volta.
- cell_autodestruicao: a Autodestruição — o clarão branco, a cúpula de energia enorme que engole tudo e a onda.
- pontos_de_chakra: os Pontos de chakra da Hinata — o Byakugan acende, o círculo dos oito trigramas aparece no
  chão e os pontos de chakra acendem um a um, com as duas cabeças de leão das palmas.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .rodada13 import _borda, _gira


def _runa(cx, cy, s, k):
    """Uma runa simples (seis desenhos diferentes) feita de traços."""
    w = 0.035 * s
    formas = [
        [(-w, -w, w, w), (-w, w, w, -w)],
        [(0, -w, 0, w), (-w, 0, w, 0)],
        [(-w, w, 0, -w), (0, -w, w, w)],
        [(-w, -w, w, -w), (0, -w, 0, w), (-w, w, w, w)],
        [(-w, 0, 0, -w), (0, -w, w, 0), (w, 0, 0, w), (0, w, -w, 0)],
        [(-w, -w, -w, w), (-w, 0, w, -w), (-w, 0, w, w)],
    ][k % 6]
    return [(cx + a, cy + b, cx + c, cy + d, 1.0) for a, b, c, d in formas]


def unica_ativa(T, t, rng):
    """A ativação: o círculo roxo de runas se abre em volta, as runas giram e acendem uma a uma, e a luz sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 3)
    if abre > 0:
        r = 0.46 * abre
        G += T.ring(r, 0.022, 0, 0.05) * 1.2 + T.ring(r * 0.78, 0.01, 0, 0.05) * 0.8
        segs = []
        for k in range(8):
            a = TAU * k / 8 + t * 2.2
            acesa = 1.0 if rel(t, 0.15 + 0.04 * k, 0.2 + 0.04 * k) >= 1 else 0.3
            segs += [(x1, y1, x2, y2, acesa) for x1, y1, x2, y2, _ in _runa(r * 0.89 * math.cos(a), 0.05 + r * 0.89 * math.sin(a), 1.0, k)]
        G += T.lines(segs, 0.01) * 1.1
    sobe = rel(t, 0.3, 0.9)
    if 0 < sobe < 1:
        q = np.random.default_rng(3)
        pts = [(q.uniform(-0.35, 0.35), 0.3 - 0.8 * ((sobe + q.uniform(0, 1)) % 1), q.uniform(0.5, 1)) for _ in range(18)]
        H += T.splats(pts, 0.014) * (1 - sobe) * 1.2
        G += T.gauss(0, -0.1, 0.15, 0.45) * pulso(t, 0.3, 0.8) * 0.35
    clarao = pulso(t, 0.3, 0.55)
    H += T.gauss(0, 0.05, 0.08) * clarao * 1.5
    return G * env, H * env


def cell_contagem(T, t, rng):
    """O "Vai explodir!": o corpo do Cell incha de luz, as rachaduras brilham e os três anéis da contagem fecham
    em volta, piscando cada vez mais rápido."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    incha = ease_in(rel(t, 0.0, 0.9), 1.5)
    G += T.gauss(0, 0, 0.15 + 0.2 * incha) * (0.4 + 0.6 * incha)
    H += T.gauss(0, 0, 0.06 + 0.08 * incha) * (0.5 + 0.8 * incha) * (0.7 + 0.3 * math.sin(t * (20 + 40 * t)))
    q = np.random.default_rng(21)
    for k in range(7):
        a = TAU * k / 7 + q.uniform(-0.3, 0.3)
        fim = 0.1 + 0.3 * incha
        G += T.polyline(jagged(q, 0, 0, fim * math.cos(a), fim * math.sin(a), 3, 0.3), 0.01) * incha * 1.3
    for k in range(3):
        u = rel(t, 0.1 + 0.2 * k, 0.4 + 0.2 * k)
        if u > 0:
            r = 0.55 - 0.3 * ease_out(u, 2)
            pisca = 1.0 if int(t * (6 + 8 * k)) % 2 == 0 else 0.4
            G += T.ring(r, 0.015, 0, 0) * (1 - 0.5 * u) * pisca
    return G * env, H * env


def cell_autodestruicao(T, t, rng):
    """A Autodestruição: o clarão branco, a cúpula de energia enorme que cresce e engole tudo, e a onda de choque
    no chão."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    H += T.gauss(0, 0, 0.2) * pulso(t, 0.0, 0.2) * 2.5
    cresce = ease_out(rel(t, 0.05, 0.6), 2.2)
    if cresce > 0:
        r = 0.12 + 0.52 * cresce
        b = 1 - rel(t, 0.55, 0.9)
        G += T.gauss(0, 0, r * 0.5) * b * 1.4 + T.ring(r, 0.04, 0, 0) * b * 1.3
        H += T.gauss(0, 0, r * 0.28) * b * 1.2
        q = np.random.default_rng(int(t * 25) % 7)
        for k in range(6):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0, 0, r * math.cos(a), r * math.sin(a), 3, 0.3), 0.012) * b
    onda = rel(t, 0.3, 0.9)
    if 0 < onda < 1:
        G += T.ring(0.25 + 0.55 * ease_out(onda, 2), 0.035, 0, 0.35, 3.0) * (1 - onda) * 1.4
    return G * env, H * env


def _trigrama(cx, cy, s, k, ang):
    """Um dos oito trigramas: três barras, inteiras ou partidas."""
    segs = []
    for j in range(3):
        partida = (k >> j) & 1
        y = (j - 1) * 0.025 * s
        if partida:
            segs += [(-0.04 * s, y, -0.01 * s, y), (0.01 * s, y, 0.04 * s, y)]
        else:
            segs += [(-0.04 * s, y, 0.04 * s, y)]
    out = []
    for x1, y1, x2, y2 in segs:
        (a, b), (c, d) = _gira([(x1, y1), (x2, y2)], ang, cx, cy)
        out.append((a, b, c, d, 1.0))
    return out


def pontos_de_chakra(T, t, rng):
    """Os Pontos de chakra: o círculo dos oito trigramas aparece no chão, os pontos de chakra acendem um a um e as
    duas cabeças de leão das palmas surgem dos lados."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 3)
    if abre > 0:
        r = 0.5 * abre
        G += T.ring(r, 0.015, 0, 0.1, 1.6) * 1.1 + T.ring(r * 0.55, 0.01, 0, 0.1, 1.6) * 0.8
        segs = []
        for k in range(8):
            a = TAU * k / 8 + 0.3 * t
            segs += _trigrama(r * 0.78 * math.cos(a), 0.1 + r * 0.78 * math.sin(a) / 1.6, 1.0, k, a + math.pi / 2)
        G += T.lines(segs, 0.008) * 1.1
    pontos = [(-0.12, -0.25), (0.12, -0.25), (0.0, -0.12), (-0.15, 0.0), (0.15, 0.0), (0.0, 0.1), (-0.08, 0.22), (0.08, 0.22)]
    for k, (x, y) in enumerate(pontos):
        u = rel(t, 0.25 + 0.05 * k, 0.32 + 0.05 * k)
        if u > 0:
            H += T.gauss(x, y, 0.018) * u * 1.6
            G += T.gauss(x, y, 0.045) * u * 0.8
    leao = pulso(t, 0.45, 0.95)
    if leao > 0:
        for lado in (-1, 1):
            cx = lado * 0.42
            cabeca = [(cx, -0.12), (cx + lado * 0.1, -0.06), (cx + lado * 0.12, 0.06), (cx, 0.12), (cx - lado * 0.06, 0.0)]
            P = T.polys([(cabeca, 1.0)])
            G += (P * 0.3 + _borda(T, P, 0.007) * 1.2) * leao
            for j in range(5):
                a = -math.pi / 2 + j * math.pi / 4
                G += T.tapered([(cx, 0, cx + lado * 0.16 * math.cos(a) * 0.9, 0.16 * math.sin(a), 1.0)], 0.02) * leao * 0.7
    return G * env, H * env


REGISTRO = [
    ("unica_ativa", unica_ativa, GRANDE, "Mecânica única · o círculo de runas abrindo (ativação)", False),
    ("cell_contagem", cell_contagem, GRANDE, "Cell · o corpo inchando de luz e a contagem", False),
    ("cell_autodestruicao", cell_autodestruicao, GRANDE, "Cell · o clarão e a cúpula da Autodestruição", False),
    ("pontos_de_chakra", pontos_de_chakra, GRANDE, "Hinata · os oito trigramas e os pontos de chakra", False),
]
