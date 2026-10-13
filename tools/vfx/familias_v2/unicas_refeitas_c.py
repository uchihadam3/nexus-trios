"""Mecânicas únicas refeitas, lote c: o impacto conta o nome da mecânica.

- mu_interrogatorio (Justiceiro): a caveira na cara do alvo, o soco e a Carga caindo em pedaços;
- mu_corpo_novo (Ultron): as placas de metal voltando e montando o rosto, os olhos acendendo;
- mu_doze_por_cento (Senhor das Estrelas): a roleta girando e parando na fatia de 12%;
- mu_mina (Rocket): a mina piscando e explodindo com estilhaços;
- mu_sem_esperanca (Darkseid): o Ômega vermelho e as cruzes de cura quebrando;
- mu_hahaha (Coringa): os sorrisos gargalhando em volta, confete e espirais;
- mu_kakuja (Kaneki): os quatro tentáculos do kagune e o sangue voltando para ele.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio


def _oval(cx, cy, rx, ry, n=24):
    return [(cx + rx * math.cos(TAU * k / n), cy + ry * math.sin(TAU * k / n)) for k in range(n)]


def _contorno(T, pts, larg):
    return T.lines([(*a, *b, 1) for a, b in zip(pts, pts[1:] + pts[:1])], larg)


def interrogatorio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.25), 2)
    s = 0.4 + 0.6 * surge
    cranio = _oval(0, -0.08 * s, 0.28 * s, 0.26 * s)
    G += T.polys([(cranio, 1.0)], 0.004) * 0.45 * (1 - rel(t, 0.7, 0.9))
    G += _contorno(T, cranio, 0.014) * (1 - rel(t, 0.7, 0.9))
    for x in (-0.1, 0.1):
        G += T.polys([(_oval(x * s, -0.06 * s, 0.07 * s, 0.09 * s, 12), 1.0)]) * -0.5
    dentes = [(x * s, 0.12 * s, x * s, 0.36 * s, 1) for x in (-0.12, -0.04, 0.04, 0.12)]
    G += T.lines(dentes, 0.025) * (1 - rel(t, 0.7, 0.9))
    soco = pulso(t, 0.25, 0.5)
    G += T.ring(0.15 + 0.5 * rel(t, 0.25, 0.55), 0.04) * soco * 1.3
    H += T.gauss(0, 0, 0.06) * soco * 2.0
    cai = rel(t, 0.45, 0.95)
    if cai > 0:
        for k in range(5):
            x = -0.4 + 0.2 * k
            y = 0.5 + 0.4 * ease_in(cai, 2) * (0.6 + 0.1 * k)
            G += T.polys([([(x - 0.07, y - 0.025), (x + 0.07, y - 0.025), (x + 0.07, y + 0.025), (x - 0.07, y + 0.025)], 1.0)]) * (1 - cai) * 1.1
    return np.clip(G, 0, None) * env, H * env


def corpo_novo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    monta = ease_out(rel(t, 0.0, 0.55), 2)
    q = np.random.default_rng(14)
    rosto = [(-0.22, -0.3), (0.22, -0.3), (0.26, 0.05), (0.12, 0.35), (-0.12, 0.35), (-0.26, 0.05)]
    for k in range(10):
        a = q.uniform(0, TAU)
        d = 0.9 * (1 - monta)
        alvo = rosto[k % 6]
        cx = alvo[0] * 0.6 + d * math.cos(a)
        cy = alvo[1] * 0.6 + d * math.sin(a)
        placa = [(cx - 0.07, cy - 0.04), (cx + 0.07, cy - 0.05), (cx + 0.06, cy + 0.04), (cx - 0.06, cy + 0.05)]
        G += T.polys([(placa, 1.0)], 0.003) * 0.8 * (1 - rel(t, 0.55, 0.65))
    pronto = rel(t, 0.5, 0.7)
    G += (T.polys([(rosto, 1.0)], 0.004) * 0.35 + _contorno(T, rosto, 0.016)) * pronto * (1 - rel(t, 0.85, 0.97))
    olhos = pulso(t, 0.55, 0.95)
    for s in (-1, 1):
        olho = [(s * 0.04, -0.1), (s * 0.18, -0.13), (s * 0.15, -0.05)]
        G += T.polys([(olho, 1.0)], 0.004) * olhos * 1.6
        H += T.gauss(s * 0.11, -0.09, 0.03) * olhos * 1.8
    G += T.lines([(-0.1, 0.18, 0.1, 0.18, 1)], 0.012) * pronto
    return G * env, H * env


def doze_por_cento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 2)
    r = 0.42 * abre + 0.01
    G += T.ring(r, 0.025) * 1.1
    fatia = T.arc_band(r * 0.6, r * 0.75, -0.38, 0.38) if r > 0.05 else T.zero()
    G += fatia * 0.9
    for k in range(8):
        a = TAU * k / 8
        G += T.lines([(0, 0, r * math.cos(a), r * math.sin(a), 1)], 0.006) * 0.5
    gira = ease_out(rel(t, 0.1, 0.65), 3)
    ang = TAU * 3 * gira + 0.0
    G += T.tapered([(0, 0, 0.36 * abre * math.cos(ang), 0.36 * abre * math.sin(ang), 1)], 0.03) * 1.3
    acerta = pulso(t, 0.62, 0.92)
    G += T.polys([(estrela(r * 0.7, 0, 0.3 * acerta + 0.01, 0.0, 8, 0.3), 1.0)], 0.008) * acerta * 1.4
    H += T.gauss(r * 0.7, 0, 0.06) * acerta * 2.0
    return G * env, H * env


def mina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    antes = 1 - rel(t, 0.3, 0.34)
    disco = _oval(0, 0.25, 0.22, 0.07)
    G += (T.polys([(disco, 1.0)], 0.004) * 0.5 + _contorno(T, disco, 0.012)) * antes
    pisca = 1.0 if int(t * 24) % 2 == 0 else 0.2
    G += T.gauss(0, 0.2, 0.03) * pisca * antes * 1.6
    explode = rel(t, 0.3, 0.8)
    if explode > 0:
        G += T.gauss(0, 0.05, 0.12 + 0.35 * explode) * (1 - explode) * 1.4
        G += T.ring(0.1 + 0.7 * ease_out(explode, 2), 0.05 * (1 - explode) + 0.01, 0, 0.1) * (1 - explode) * 1.2
        H += T.gauss(0, 0.05, 0.1) * pulso(t, 0.3, 0.5) * 2.2
        q = np.random.default_rng(9)
        for k in range(14):
            a = q.uniform(-math.pi, 0.3)
            d = 0.9 * ease_out(explode, 1.5) * q.uniform(0.5, 1.0)
            G += T.gauss(d * math.cos(a), 0.1 + d * math.sin(a) + 0.4 * explode ** 2, 0.025) * (1 - explode) * 1.2
    return G * env, H * env


def sem_esperanca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.35), 2)
    s = 0.5 + 0.5 * surge
    G += T.arc_band(0.24 * s, 0.05, 0.75, TAU - 0.75 + 0.0, cx=0, cy=-0.08, rot=math.pi / 2) * surge * 1.2
    G += T.lines([(-0.24 * s, 0.17, -0.1 * s, 0.17, 1), (0.1 * s, 0.17, 0.24 * s, 0.17, 1)], 0.05) * surge * 1.2
    H += T.gauss(0, -0.08, 0.1) * pulso(t, 0.1, 0.5) * 1.0
    quebra = rel(t, 0.35, 0.9)
    for k, (cx, cy) in enumerate([(-0.55, -0.4), (0.55, -0.35), (-0.5, 0.45), (0.55, 0.45)]):
        d = 0.2 * ease_out(quebra, 2)
        for parte, (dx, dy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
            x, y = cx + dx * d * 0.5, cy + dy * d * 0.5
            G += T.polys([([(x - 0.035, y - 0.012), (x + 0.035, y - 0.012), (x + 0.035, y + 0.012), (x - 0.035, y + 0.012)], 1.0)]) * (1 - quebra) * 0.9
            G += T.polys([([(x - 0.012, y - 0.035), (x + 0.012, y - 0.035), (x + 0.012, y + 0.035), (x - 0.012, y + 0.035)], 1.0)]) * (1 - quebra) * 0.9
    return G * env, H * env


def hahaha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(5):
        surge = ease_out(rel(t, 0.05 * k, 0.3 + 0.05 * k), 2)
        if surge <= 0:
            continue
        a = TAU * k / 5 + 0.5
        d = 0.15 + 0.45 * surge
        cx, cy = d * math.cos(a), d * math.sin(a) * 0.8
        sacode = 0.02 * math.sin(TAU * (t * 8 + k * 0.3))
        larg = 0.16 * surge
        G += T.arc_band(larg, 0.022, 0.3, math.pi - 0.3, cx=cx, cy=cy - 0.04 + sacode) * 1.2
        G += T.lines([(cx - larg * 0.8 + 0.06 * j, cy + 0.03 + sacode, cx - larg * 0.8 + 0.06 * j, cy + 0.08 + sacode, 1) for j in range(int(larg * 26))], 0.008) * 0.7
        G += T.gauss(cx - 0.05, cy - 0.06 + sacode, 0.015) * 1.2 + T.gauss(cx + 0.05, cy - 0.06 + sacode, 0.015) * 1.2
    q = np.random.default_rng(3)
    confete = [(q.uniform(-0.8, 0.8), -0.8 + 1.6 * ((t * 0.9 + q.uniform(0, 1)) % 1), 1.0) for _ in range(22)]
    G += T.splats(confete, 0.016) * (1 - rel(t, 0.75, 0.95))
    G += T.arc_band(0.08 + 0.3 * t, 0.015, t * 9, t * 9 + 4, cx=0, cy=0) * 0.7 * (1 - rel(t, 0.7, 0.9))
    return G * env, H * env


def kakuja(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cresce = ease_out(rel(t, 0.0, 0.45), 2)
    for k, base in enumerate((-2.6, -2.1, -1.0, -0.5)):
        pts = []
        for i in range(14):
            f = i / 13 * cresce
            ang = base + 0.9 * f * (1 if k < 2 else -1) + 0.15 * math.sin(TAU * (t * 1.5 + i * 0.07))
            r = 0.1 + 0.85 * f
            pts.append((r * math.cos(ang) * (1.0 if k < 2 else 1.0), 0.2 + r * math.sin(ang)))
        G += T.polyline(pts, 0.05 * (1 - 0.3 * cresce) + 0.015) * 1.0
        H += T.polyline(pts, 0.012) * 0.4
    volta = rel(t, 0.35, 0.9)
    if volta > 0:
        q = np.random.default_rng(2)
        gotas = []
        for _ in range(16):
            a = q.uniform(0, TAU)
            d = 0.8 * (1 - ease_in(((volta + q.uniform(0, 0.5)) % 1), 1.5))
            gotas.append((d * math.cos(a), 0.2 + d * math.sin(a), 1.0))
        G += T.splats(gotas, 0.02) * 1.1 * (1 - rel(t, 0.8, 0.95))
        G += T.gauss(0, 0.2, 0.12) * pulso(t, 0.6, 0.95) * 0.9
    return G * env, H * env


REGISTRO = [
    ("mu_interrogatorio", interrogatorio, GRANDE, "Justiceiro · a caveira, o soco e a Carga caindo", False),
    ("mu_corpo_novo", corpo_novo, GRANDE, "Ultron · as placas montando o rosto e os olhos acendendo", False),
    ("mu_doze_por_cento", doze_por_cento, GRANDE, "Senhor das Estrelas · a roleta parando nos 12%", False),
    ("mu_mina", mina, GRANDE, "Rocket · a mina piscando e explodindo", False),
    ("mu_sem_esperanca", sem_esperanca, GRANDE, "Darkseid · o Ômega e as cruzes de cura quebrando", False),
    ("mu_hahaha", hahaha, GRANDE, "Coringa · os sorrisos gargalhando, confete e espirais", False),
    ("mu_kakuja", kakuja, GRANDE, "Kaneki · os tentáculos do kagune e o sangue voltando", False),
]
