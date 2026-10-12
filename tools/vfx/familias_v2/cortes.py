"""Cortes: lâminas com caráter (vertical, saque rápido, mil cortes, foice, espadão, lâminas elementais)."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, _subindo, apaga, ease_out, faiscas, jagged, janela, lamina, pulso, rel,
                   smooth, some, vazio)


def _rasgo(T, x1, y1, x2, y2, larg, p, fim):
    """Corpo e fio de um corte reto que aparece em `p` e se desfaz a partir de `fim`."""
    corpo = T.polys([(lamina(x1, y1, x2, y2, larg, p, inicio=fim), 1)], 0.004)
    fio = T.polys([(lamina(x1, y1, x2, y2, larg * 0.3, p, inicio=fim), 1)], 0.002)
    return corpo, fio


def espadao(T, t, rng):
    """Espadão: arco largo e pesado, o chão racha embaixo e blocos voam."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.25), 2.2)
    env = apaga(t, 0.4, 0.85)
    arco = T.arc_band(0.66, 0.2, -2.7, -2.7 + 2.9 * p + 0.01, squash=0.85, crescente=True) * env
    fio = T.arc_band(0.74, 0.03, -2.7, -2.7 + 2.9 * p + 0.01, squash=0.85) * env
    tt = rel(t, 0.22, 1)
    sub = np.random.default_rng(15)
    rach = T.zero()
    for k in range(5):
        pts = jagged(sub, 0.2, 0.55, 0.2 + sub.uniform(-0.8, 0.8), 0.55 + sub.uniform(-0.15, 0.2), 4, 0.25)
        rach += T.polyline(pts, 0.012, 1) * janela(t, 0.22, 0.32)
    blocos = []
    for _ in range(10):
        a = rng.uniform(-math.pi + 0.3, -0.3)
        d = rng.uniform(0.2, 0.7) * ease_out(tt, 2)
        x, y = 0.2 + math.cos(a) * d, 0.5 + math.sin(a) * d + 0.9 * tt * tt
        s = rng.uniform(0.03, 0.06)
        blocos.append(([(x - s, y - s), (x + s, y - s * 0.6), (x + s * 0.7, y + s), (x - s, y + s * 0.7)], (1 - tt) * (t > 0.22)))
    b = T.polys(blocos, 0.003)
    impacto = T.gauss(0.2, 0.5, 0.2, 0.1) * some(t, 0.22, 0.55) * 2.6
    G += T.glow(arco, 1, 1.2, 0.03) + fio * 1.5 + rach * apaga(t, 0.6, 1) + b * 1.2 + impacto
    H += fio * 1.5 + arco * 0.3 + rach * 0.6 * apaga(t, 0.6, 1) + impacto
    return G, H


def _arco_corte(T, t, a0=-2.4, span=2.6, raio=0.62, larg=0.12, dur=0.25):
    p = ease_out(rel(t, 0, dur), 2.2)
    return T.arc_band(raio, larg, a0, a0 + span * p + 0.01, squash=0.75, crescente=True), p


def lamina_eletrica(T, t, rng):
    """Lâmina elétrica: o corte corre com raios pulando ao longo do fio."""
    G, H = vazio(T)
    arco, p = _arco_corte(T, t, larg=0.09)
    env = apaga(t, 0.5, 1)
    sub = np.random.default_rng(int(t * 997) + 3)
    lin = T.zero()
    for k in range(5):
        a1 = -2.4 + 2.6 * p * sub.uniform(0, 0.8)
        a2 = a1 + sub.uniform(0.3, 0.7)
        x1, y1 = math.cos(a1) * 0.62, math.sin(a1) * 0.62 * 0.75
        x2, y2 = math.cos(a2) * 0.62, math.sin(a2) * 0.62 * 0.75
        lin += T.polyline(jagged(sub, x1, y1, x2, y2, 4, 0.35), 0.012, 1)
    clarao = T.gauss(0, -0.25, 0.14) * (0.4 + 0.6 * sub.uniform()) * pulso(t, 0.1, 0.5) * 1.3
    G += (T.glow(arco, 1, 1.1, 0.02) + T.glow(lin, 1.4, 1.6, 0.02)) * env + clarao
    H += (arco * 0.7 + lin * 1.4) * env + clarao * 0.6
    return G, H


def lamina_sombria(T, t, rng):
    """Lâmina sombria: meia-lua escura com bordas que se desfazem em fumaça e fiapos subindo."""
    G, H = vazio(T)
    arco, p = _arco_corte(T, t, larg=0.16)
    env = apaga(t, 0.5, 1)
    n = T.noise(np.random.default_rng(121), 0.04, 3)
    franja = T.warp(arco, n * 0.04, n * 0.04 - 0.08 * rel(t, 0.2, 1))
    fio = T.arc_band(0.66, 0.02, -2.4, -2.4 + 2.6 * p + 0.01, squash=0.75)
    fiapos = []
    for _ in range(18):
        f = (rng.uniform(0, 1) + t) % 1
        fiapos.append((rng.uniform(-0.6, 0.6), 0.1 - f * 0.7, math.sin(math.pi * f) * rng.uniform(0.3, 0.9)))
    G += (arco * 0.9 + franja * 0.8 * np.clip(0.6 + 0.4 * n, 0, 1) + fio * 1.4) * env + T.splats(fiapos, 0.02) * 0.9 * janela(t, 0.2, 0.4)
    H += fio * 1.1 * env
    return G, H


def motosserra(T, t, rng):
    """Motosserra: anel de dentes girando rápido, faíscas jorrando na tangente e clarão tremido."""
    G, H = vazio(T)
    env = janela(t, 0, 0.1) * apaga(t, 0.65, 1)
    giro = t * TAU * 4
    dentes = []
    for k in range(18):
        a = TAU * k / 18 + giro
        r0, r1 = 0.36, 0.5
        dentes.append(([(math.cos(a) * r0, math.sin(a) * r0), (math.cos(a + 0.22) * r1, math.sin(a + 0.22) * r1), (math.cos(a + 0.3) * r0, math.sin(a + 0.3) * r0)], 1))
    d = T.polys(dentes, 0.003)
    aro = T.ring(0.36, 0.02)
    sub = np.random.default_rng(int(t * 997) + 5)
    jorro = faiscas(T, sub, 0.5, 18, 0.7, 0.03, cone=(0.2, 1.2), cx=0.3, cy=-0.3, gravidade=0.3)
    tremido = T.gauss(sub.uniform(-0.03, 0.03), sub.uniform(-0.03, 0.03), 0.18) * (0.6 + 0.4 * sub.uniform()) * 1.6
    G += (T.glow(d + aro, 1.1, 1, 0.015) + T.glow(jorro, 1, 1.2, 0.02) + tremido) * env
    H += (d * 0.6 + jorro * 0.9 + tremido) * env
    return G, H


def lamina_de_agua(T, t, rng):
    """Lâmina de água: uma fita ondulada que gira em espiral com crista de espuma e gotas."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.35), 2)
    env = apaga(t, 0.55, 1)
    pts, crista = [], []
    for k in range(80):
        u = k / 79 * p
        a = -2.8 + u * 6.0
        r = 0.78 - 0.5 * u + 0.04 * math.sin(u * 18 - t * 8)
        pts.append((math.cos(a) * r, math.sin(a) * r * 0.8))
        crista.append((math.cos(a) * (r + 0.06), math.sin(a) * (r + 0.06) * 0.8))
    fita = T.polyline(pts, 0.05, 1) + T.polyline([(x * 0.86, y * 0.86) for x, y in pts], 0.02, 0.6)
    esp = T.polyline(crista, 0.018, 1)
    gotas = []
    tt = rel(t, 0.15, 1)
    for _ in range(26):
        k = int(rng.uniform(0, 79) * p)
        x, y = pts[k]
        gotas.append((x * (1 + 0.3 * tt), y * (1 + 0.3 * tt) + 0.4 * tt * tt, (1 - tt) * rng.uniform(0.4, 1)))
    G += (T.glow(fita, 0.7, 1, 0.03) + esp * 1.5) * env + T.splats(gotas, 0.012) * 1.2
    H += (esp * 1.2 + fita * 0.2) * env + T.splats(gotas, 0.01) * 0.7
    return G, H


def florete(T, t, rng):
    """Florete: cinco estocadas finas e rápidas em ângulos diferentes, cada uma com um ponto de luz."""
    G, H = vazio(T)
    acc, pontos = T.zero(), T.zero()
    for k in range(5):
        a0 = k * 0.11
        ang = (k - 2) * 0.14
        p = ease_out(rel(t, a0, a0 + 0.08), 2)
        if p <= 0:
            continue
        tx, ty = 0.15 * math.cos(ang) + (k - 2) * 0.02, 0.15 * math.sin(ang) + (k - 2) * 0.12
        x1, y1 = tx - math.cos(ang) * 1.0, ty - math.sin(ang) * 1.0
        segs = [(x1, y1, x1 + (tx - x1) * p, y1 + (ty - y1) * p, apaga(t, a0 + 0.1, a0 + 0.3))]
        acc += T.tapered(segs, 0.04)
        pontos += (T.gauss(tx, ty, 0.05) * 2 + T.flare(tx, ty, 0.6, 0.6)) * pulso(t, a0 + 0.06, a0 + 0.3)
    G += T.glow(acc, 1.2, 1, 0.015) + pontos * 1.4
    H += acc * 0.9 + pontos
    return G, H


REGISTRO = [
    ("espadao", espadao, GRANDE, "espadão que racha o chão", False),
    ("lamina_eletrica", lamina_eletrica, GRANDE, "lâmina elétrica", False),
    ("lamina_sombria", lamina_sombria, GRANDE, "lâmina sombria", False),
    ("motosserra", motosserra, GRANDE, "dentes de serra girando", False),
    ("lamina_de_agua", lamina_de_agua, GRANDE, "fita de água em espiral", False),
    ("florete", florete, GRANDE, "estocadas finas em sequência", False),
]
