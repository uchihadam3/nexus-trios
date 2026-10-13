"""Mecânicas únicas refeitas, lote f: o impacto conta o nome da mecânica.

- mu_suspeita (L): a lupa passando e o medidor de Suspeita enchendo;
- mu_leque (Kitana): o leque de lâminas abrindo e a rajada levantando;
- mu_esconderijo (Patrick): a pedra descendo por cima e o esconderijo;
- mu_disfarce (Viúva Negra): a silhueta disfarçada sumindo e a ampulheta vermelha;
- mu_ladra (Mulher-Gato): o chicote estalando e a joia sendo puxada;
- mu_desequilibrio (Asa Noturna): o balanço de trapézio e o ponteiro atrasando;
- mu_stars (Nemesis): a mira de caça travando e o tentáculo chicoteando;
- mu_cria (Xenomorfo): o ovo abrindo em pétalas e as patas saindo;
- mu_nova_esperanca (Luke): o sabre verde acendendo e o brilho da esperança;
- mu_mais_smith (Agente Smith): os óculos se multiplicando entre linhas de código;
- mu_recarregou (John Wick): o pente subindo, as cápsulas voando e o clarão;
- mu_corpo_metal (RoboCop): as placas de metal e a linha do visor varrendo;
- mu_exercito (Rambo): a rajada de clarões e as cápsulas, a faixa na cabeça;
- mu_radiacao (Godzilla): o símbolo de radiação girando e os anéis pulsando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio
from .unicas_refeitas_d import _contorno, _gira, _maior, _oval


def suspeita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    passa = rel(t, 0.0, 0.5)
    cx, cy = -0.3 + 0.5 * ease_out(passa, 2), -0.1 + 0.08 * math.sin(passa * 6)
    G += T.ring(0.12, 0.02, cx=cx, cy=cy) * (1 - rel(t, 0.5, 0.6)) * 1.2
    G += T.lines([(cx + 0.085, cy + 0.085, cx + 0.2, cy + 0.2, 1)], 0.03) * (1 - rel(t, 0.5, 0.6))
    H += T.gauss(cx, cy, 0.06) * (1 - rel(t, 0.5, 0.6)) * 0.8
    enche = ease_out(rel(t, 0.4, 0.85), 2)
    if enche > 0:
        G += T.arc_band(0.32, 0.03, math.pi, math.pi + math.pi * enche, taper=0.0) * 1.2
        G += T.arc_band(0.32, 0.01, math.pi, 2 * math.pi, taper=0.0) * 0.35
        a = math.pi + math.pi * enche
        G += T.lines([(0, 0.05, 0.28 * math.cos(a), 0.05 + 0.28 * math.sin(a), 1)], 0.02) * 1.1
        H += T.gauss(0.32 * math.cos(a), 0.32 * math.sin(a), 0.04) * 1.2
    return G * env, H * env


def leque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2)
    n = 9
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * 0.16 * abre
        G += T.tapered([(0, 0.2, 0.42 * math.cos(a), 0.2 + 0.42 * math.sin(a), 1)], 0.035) * 1.0
    G += T.arc_band(0.42, 0.02, -math.pi / 2 - 0.65 * abre, -math.pi / 2 + 0.65 * abre, cy=0.2, taper=0.0) * 0.9 if abre > 0.05 else T.zero()
    sobe = rel(t, 0.4, 0.95)
    if sobe > 0:
        for k in range(5):
            x = -0.3 + 0.15 * k
            y = 0.1 - 0.6 * ease_out(sobe, 2) - 0.05 * (k % 2)
            G += T.polyline([(x + 0.04 * math.sin(u * 8 + k), y + 0.25 * u) for u in np.linspace(0, 1, 10)], 0.014) * (1 - sobe) * 1.1
        H += T.gauss(0, -0.1, 0.12) * pulso(t, 0.4, 0.8) * 1.0
    return G * env, H * env


def esconderijo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_in(rel(t, 0.0, 0.4), 2)
    y = -0.6 + 0.6 * desce
    pedra = [(0.4 * math.cos(u), 0.25 + y - 0.32 * math.sin(u) * (1 + 0.1 * math.sin(u * 7))) for u in np.linspace(0, math.pi, 20)]
    G += T.polys([(pedra, 1.0)], 0.005) * 0.55 + T.polyline(pedra, 0.022) * 1.1
    for k in range(3):
        G += T.lines([(-0.2 + 0.18 * k, 0.1 + y, -0.14 + 0.18 * k, 0.04 + y, 1)], 0.01) * 0.8
    poeira = rel(t, 0.38, 0.8)
    if poeira > 0:
        for s in (-1, 1):
            G += T.splats([(s * (0.42 + 0.2 * poeira + 0.05 * k), 0.25 - 0.05 * k, 1.0) for k in range(4)], 0.035) * (1 - poeira) * 0.9
        H += T.gauss(0, 0.25, 0.1) * pulso(t, 0.38, 0.6) * 1.2
    return G * env, H * env


def disfarce(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    some = rel(t, 0.0, 0.5)
    cabeca = _oval(0, -0.18, 0.11, 0.13)
    ombros = [(-0.3, 0.32), (-0.25, 0.08), (0, 0.0), (0.25, 0.08), (0.3, 0.32)]
    vis = (1 - some) * (0.6 + 0.4 * math.sin(t * 40) ** 2)
    G += (_contorno(T, cabeca, 0.014) + T.polyline(ombros, 0.016)) * vis
    amp = ease_out(rel(t, 0.4, 0.7), 2)
    if amp > 0:
        s = 0.18 * amp
        G += T.polys([([(-s, -s), (s, -s), (0, 0)], 1.0), ([(-s, s), (s, s), (0, 0)], 1.0)], 0.004) * (1 - rel(t, 0.85, 0.97)) * 1.4
        H += T.gauss(0, 0, 0.08) * amp * 1.4
    return G * env, H * env


def ladra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    estala = ease_out(rel(t, 0.0, 0.35), 2)
    pts = [(-0.45 + 0.85 * u * estala, -0.1 - 0.18 * math.sin(math.pi * u) * (1 - 0.5 * estala) + 0.05 * math.sin(u * 9)) for u in np.linspace(0, 1, 24)]
    G += T.polyline(pts, 0.016) * (1 - rel(t, 0.55, 0.7)) * 1.2
    G += T.polys([(estrela(*pts[-1], 0.08 * pulso(t, 0.25, 0.45) + 0.005, 0.3, 6), 1.0)]) * pulso(t, 0.25, 0.45) * 1.3
    puxa = ease_in(rel(t, 0.35, 0.85), 2)
    jx, jy = 0.4 - 0.75 * puxa, -0.1 + 0.05 * math.sin(puxa * math.pi)
    joia = [(jx, jy - 0.1), (jx + 0.08, jy - 0.03), (jx, jy + 0.1), (jx - 0.08, jy - 0.03)]
    G += T.polys([(joia, 1.0)], 0.003) * 0.8 + _contorno(T, joia, 0.012)
    G += T.lines([(jx - 0.08, jy - 0.03, jx + 0.08, jy - 0.03, 1)], 0.008)
    H += T.gauss(jx, jy, 0.05) * (0.6 + 0.6 * math.sin(t * 30) ** 2) * (1 - rel(t, 0.85, 0.97))
    return G * env, H * env


def desequilibrio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    balanco = math.sin(rel(t, 0.0, 0.7) * math.pi * 2) * 0.9 * (1 - rel(t, 0.5, 0.8))
    px, py = 0.42 * math.sin(balanco), -0.4 + 0.42 * math.cos(balanco)
    G += T.lines([(0, -0.4, px, py, 1)], 0.012) * 1.0
    G += T.lines([(px - 0.1, py, px + 0.1, py, 1)], 0.03) * 1.1
    G += T.arc_band(0.42, 0.008, math.pi / 2 - 0.9, math.pi / 2 + 0.9, cy=-0.4, taper=0.0) * 0.4
    relogio = rel(t, 0.45, 0.95)
    if relogio > 0:
        G += T.ring(0.15, 0.015, cy=0.25) * 1.0
        a = -math.pi / 2 - 1.5 * ease_out(relogio, 2)
        G += T.lines([(0, 0.25, 0.12 * math.cos(a), 0.25 + 0.12 * math.sin(a), 1)], 0.02) * 1.2
        H += T.gauss(0, 0.25, 0.05) * pulso(t, 0.45, 0.9) * 1.2
    return G * env, H * env


def stars(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    trava = ease_out(rel(t, 0.0, 0.45), 3)
    r = 0.45 - 0.25 * trava
    G += T.ring(r, 0.016) * 1.1
    for k in range(4):
        a = TAU * k / 4 + (1 - trava) * 1.5
        G += T.lines([(r * 0.7 * math.cos(a), r * 0.7 * math.sin(a), r * 1.25 * math.cos(a), r * 1.25 * math.sin(a), 1)], 0.02) * 1.1
    H += T.gauss(0, 0, 0.03) * trava * 1.6
    chicote = rel(t, 0.45, 0.85)
    if chicote > 0:
        pts = [(-0.5 + 0.55 * u, 0.35 - 0.35 * u + 0.12 * math.sin(u * 7 - chicote * 10)) for u in np.linspace(0, ease_out(chicote, 2), 20)]
        if len(pts) > 1:
            G += T.polyline(pts, 0.04) * (1 - rel(t, 0.8, 0.95)) * 1.1
        G += T.polys([(estrela(0, 0, 0.2 * pulso(t, 0.7, 0.9) + 0.005, 0.0, 7), 1.0)]) * pulso(t, 0.7, 0.9) * 1.3
    return G * env, H * env


def cria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.15, 0.55), 2)
    G += _contorno(T, _oval(0, 0.1, 0.18, 0.24), 0.018) * (1 - abre * 0.6)
    for k in range(4):
        a = -math.pi / 2 + (k - 1.5) * (0.35 + 0.35 * abre)
        p = [(0, -0.05), (0.2 * math.cos(a - 0.2), -0.05 + 0.2 * math.sin(a - 0.2) - 0.05 * abre), (0.26 * math.cos(a), -0.05 + 0.26 * math.sin(a) - 0.1 * abre), (0.2 * math.cos(a + 0.2), -0.05 + 0.2 * math.sin(a + 0.2) - 0.05 * abre)]
        G += T.polys([(p, 1.0)], 0.004) * abre * 0.8
    sai = rel(t, 0.5, 0.95)
    if sai > 0:
        cy = -0.05 - 0.3 * ease_out(sai, 2)
        G += T.gauss(0, cy, 0.05) * 1.2
        for k in range(8):
            a = TAU * k / 8
            pts = [(0.05 * math.cos(a), cy + 0.05 * math.sin(a)), (0.18 * math.cos(a), cy + 0.14 * math.sin(a) - 0.04), (0.25 * math.cos(a), cy + 0.2 * math.sin(a) + 0.03)]
            G += T.polyline(pts, 0.014) * (1 - rel(t, 0.85, 0.97)) * 1.1
        H += T.gauss(0, cy, 0.06) * 1.0
    return G * env, H * env


def nova_esperanca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += T.polys([([(-0.035, 0.18), (0.035, 0.18), (0.035, 0.38), (-0.035, 0.38)], 1.0)], 0.003) * 0.7
    acende = ease_out(rel(t, 0.1, 0.4), 2)
    topo = 0.18 - 0.6 * acende
    G += T.lines([(0, 0.18, 0, topo, 1)], 0.05) * 0.7 + T.lines([(0, 0.18, 0, topo, 1)], 0.02) * 1.3
    H += T.lines([(0, 0.18, 0, topo, 1)], 0.012) * 1.6
    brilho = pulso(t, 0.35, 0.95)
    G += T.polys([(estrela(0, -0.15, 0.3 * brilho + 0.005, 0.0, 4, 0.22), 1.0)]) * brilho * 1.0
    G += T.ring(0.15 + 0.3 * rel(t, 0.4, 0.95), 0.02, cy=-0.1) * (1 - rel(t, 0.4, 0.95)) * 1.1
    return G * env, H * env


def _oculos(cx, cy, s):
    return [[(cx - 0.17 * s, cy - 0.04 * s), (cx - 0.02 * s, cy - 0.04 * s), (cx - 0.04 * s, cy + 0.06 * s), (cx - 0.15 * s, cy + 0.06 * s)],
            [(cx + 0.02 * s, cy - 0.04 * s), (cx + 0.17 * s, cy - 0.04 * s), (cx + 0.15 * s, cy + 0.06 * s), (cx + 0.04 * s, cy + 0.06 * s)]]


def mais_smith(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(9):
        x = -0.45 + 0.11 * k
        f = (t * 1.3 + k * 0.17) % 1
        G += T.lines([(x, -0.5 + f * 0.8, x, -0.38 + f * 0.8, 1)], 0.01) * 0.45 * (1 - rel(t, 0.85, 0.97))
    for k, (cx, cy) in enumerate(((0.0, -0.05), (-0.28, 0.15), (0.28, 0.15))):
        f = ease_out(rel(t, 0.1 + 0.18 * k, 0.4 + 0.18 * k), 2)
        if f <= 0:
            continue
        lentes = _oculos(cx, cy, 0.9 + 0.3 * f)
        G += T.polys([(p, 1.0) for p in lentes], 0.004) * f * 1.2
        G += T.lines([(cx - 0.02, cy - 0.03, cx + 0.02, cy - 0.03, 1)], 0.008) * f
        H += T.gauss(cx - 0.09, cy - 0.02, 0.015) * pulso(t, 0.2 + 0.18 * k, 0.6 + 0.18 * k) * 1.8
    return G * env, H * env


def recarregou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2)
    y = 0.45 - 0.35 * sobe
    pente = [(-0.06, y - 0.2), (0.06, y - 0.2), (0.08, y + 0.1), (-0.04, y + 0.1)]
    G += T.polys([(pente, 1.0)], 0.003) * 0.6 + _contorno(T, pente, 0.012)
    G += T.lines([(-0.12, 0.05, 0.12, 0.05, 1)], 0.014) * 0.8
    trava = pulso(t, 0.3, 0.45)
    H += T.gauss(0, 0.05, 0.05) * trava * 2.0
    voa = rel(t, 0.4, 0.95)
    if voa > 0:
        for k in range(4):
            f = rel(voa, 0.15 * k, 0.15 * k + 0.6)
            if f <= 0:
                continue
            cx, cy = 0.1 + 0.4 * f, -0.05 - 0.35 * math.sin(math.pi * f) + 0.1 * f
            G += T.polys([(_gira([(-0.03, -0.012), (0.03, -0.012), (0.03, 0.012), (-0.03, 0.012)], f * 9, cx, cy), 1.0)]) * (1 - f) * 1.3
        G += T.polys([(estrela(-0.3, -0.05, 0.12 * pulso(t, 0.45, 0.6) + 0.005, 0.0, 8), 1.0)]) * pulso(t, 0.45, 0.6) * 1.4
    return G * env, H * env


def corpo_metal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    monta = ease_out(rel(t, 0.0, 0.45), 2)
    for lin in range(3):
        for col in range(3):
            if monta < (lin * 3 + col) / 9:
                continue
            x, y = -0.24 + 0.24 * col, -0.24 + 0.24 * lin
            placa = [(x - 0.1, y - 0.1), (x + 0.1, y - 0.1), (x + 0.1, y + 0.1), (x - 0.1, y + 0.1)]
            G += T.polys([(placa, 1.0)], 0.003) * 0.3 + _contorno(T, placa, 0.01) * 0.9
            G += T.gauss(x + 0.07, y - 0.07, 0.01) * 0.8
    varre = rel(t, 0.4, 0.9)
    if varre > 0:
        y = -0.35 + 0.7 * varre
        G += T.lines([(-0.38, y, 0.38, y, 1)], 0.02) * 1.3
        H += T.lines([(-0.38, y, 0.38, y, 1)], 0.006) * 1.5
    return G * env, H * env


def exercito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(6):
        f = pulso(t, 0.05 + 0.1 * k, 0.25 + 0.1 * k)
        x = -0.35 + 0.14 * k
        y = -0.05 + 0.06 * math.sin(k * 2.1)
        G += T.polys([(estrela(x, y, 0.2 * f + 0.003, k * 0.4, 6, 0.4), 1.0)]) * f * 1.4
        H += T.gauss(x, y, 0.04) * f * 1.6
    voa = rel(t, 0.15, 0.95)
    if voa > 0:
        q = np.random.default_rng(12)
        caps = []
        for k in range(10):
            f = (voa * 1.3 - k * 0.07)
            if 0 < f < 1:
                caps.append((-0.3 + 0.07 * k + 0.1 * f, 0.05 + 0.4 * f * f - 0.2 * f, 1.0))
        G += T.splats(caps, 0.018) * 1.1
    G += T.polyline([(-0.4, -0.35), (0.0, -0.3), (0.4, -0.35)], 0.03) * pulso(t, 0.0, 0.9) * 0.9
    G += T.lines([(0.38, -0.34, 0.48, -0.2, 1), (0.36, -0.33, 0.42, -0.18, 1)], 0.02) * pulso(t, 0.0, 0.9) * 0.9
    return G * env, H * env


def radiacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    gira = t * 2.5
    for k in range(3):
        a = gira + TAU * k / 3
        G += T.arc_band(0.24 * surge + 0.02, 0.1 * surge + 0.005, a - 0.5, a + 0.5, taper=0.0) * 1.1
    G += T.gauss(0, 0, 0.05 * surge + 0.005) * 1.5
    for k in range(3):
        r = ((t * 1.4 + k / 3) % 1)
        G += T.ring(0.15 + 0.4 * r, 0.02) * (1 - r) * pulso(t, 0.1, 0.95) * 0.9
    H += T.gauss(0, 0, 0.12) * pulso(t, 0.05, 0.9) * 1.3
    return G * env, H * env


REGISTRO = [
    ("mu_suspeita", lambda T, t, r: _maior(suspeita, T, t, r, 1.25), GRANDE, "L · a lupa passando e o medidor de Suspeita enchendo", False),
    ("mu_leque", lambda T, t, r: _maior(leque, T, t, r, 1.2), GRANDE, "Kitana · o leque abrindo e a rajada levantando", False),
    ("mu_esconderijo", lambda T, t, r: _maior(esconderijo, T, t, r, 1.2), GRANDE, "Patrick · a pedra descendo por cima", False),
    ("mu_disfarce", lambda T, t, r: _maior(disfarce, T, t, r, 1.3), GRANDE, "Viúva Negra · a silhueta sumindo e a ampulheta", False),
    ("mu_ladra", lambda T, t, r: _maior(ladra, T, t, r, 1.2), GRANDE, "Mulher-Gato · o chicote e a joia sendo puxada", False),
    ("mu_desequilibrio", lambda T, t, r: _maior(desequilibrio, T, t, r, 1.2), GRANDE, "Asa Noturna · o trapézio e o ponteiro atrasando", False),
    ("mu_stars", lambda T, t, r: _maior(stars, T, t, r, 1.15), GRANDE, "Nemesis · a mira de caça e o tentáculo", False),
    ("mu_cria", lambda T, t, r: _maior(cria, T, t, r, 1.3), GRANDE, "Xenomorfo · o ovo abrindo e a cria saindo", False),
    ("mu_nova_esperanca", lambda T, t, r: _maior(nova_esperanca, T, t, r, 1.2), GRANDE, "Luke · o sabre verde acendendo", False),
    ("mu_mais_smith", lambda T, t, r: _maior(mais_smith, T, t, r, 1.3), GRANDE, "Agente Smith · os óculos se multiplicando no código", False),
    ("mu_recarregou", lambda T, t, r: _maior(recarregou, T, t, r, 1.75), GRANDE, "John Wick · o pente subindo e as cápsulas voando", False),
    ("mu_corpo_metal", lambda T, t, r: _maior(corpo_metal, T, t, r, 1.25), GRANDE, "RoboCop · as placas de metal e o visor varrendo", False),
    ("mu_exercito", lambda T, t, r: _maior(exercito, T, t, r, 1.4), GRANDE, "Rambo · a rajada de clarões e as cápsulas", False),
    ("mu_radiacao", lambda T, t, r: _maior(radiacao, T, t, r, 1.25), GRANDE, "Godzilla · o símbolo de radiação girando", False),
]
