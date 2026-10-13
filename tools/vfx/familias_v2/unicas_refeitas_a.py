"""Mecânicas únicas refeitas, lote a: o impacto conta o nome da mecânica (pedido do jogador: "as animações têm que
ser de acordo com o nome… o mesmo nível de cuidado das habilidades").

Registradas por último: substituem as folhas antigas de mesmo nome.

- mu_pagina_no_relogio (Light): o relógio abre, a página sai, o nome é escrito e o coração para (linha do monitor);
- mu_modo_serio (Saitama): os olhos sérios, a aura subindo e a onda de choque;
- mu_batarangue (Batman): o batarangue cravando girando e as faíscas (o voo já vem antes, pela entrega);
- mu_gancho (Batman): o cabo do gancho descendo e o escudo com o morcego;
- mu_bomba_de_fumaca (Batman): a fumaça densa se espalhando em nuvens;
- mu_doenca_terminal (Itachi): a tosse de sangue, os corvos se espalhando e o tomoe;
- mu_juntas (Inosuke): as correntes arrebentando elo por elo;
- mu_endurecer (Eren): as placas de cristal hexagonais fechando em volta;
- mu_agora_e_meu (Makima): o olho de anéis e a corrente que prende.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio
from .unicas_b import _morcego


def _ret(cx, cy, w, h, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in ((-w, -h), (w, -h), (w, h), (-w, h))]


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def pagina_no_relogio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 2)
    rel_x, rel_y = -0.45, -0.35
    some_relogio = 1 - rel(t, 0.35, 0.5)
    G += (T.ring(0.16 * abre + 0.01, 0.025, rel_x, rel_y) + T.lines([(rel_x, rel_y, rel_x, rel_y - 0.1 * abre, 1), (rel_x, rel_y, rel_x + 0.07 * abre, rel_y, 1)], 0.015)) * some_relogio
    sai = ease_out(rel(t, 0.12, 0.38), 2)
    px, py = rel_x + (0.45 - rel_x) * sai * 0.95, rel_y + (0.0 - rel_y) * sai
    ang = -0.5 * (1 - sai)
    pagina = T.polys([(_ret(px, py, 0.3 * (0.4 + 0.6 * sai), 0.38 * (0.4 + 0.6 * sai), ang), 1.0)], 0.004)
    borda = T.lines([(*a, *b, 1) for a, b in zip(_ret(px, py, 0.3 * (0.4 + 0.6 * sai), 0.38 * (0.4 + 0.6 * sai), ang), _ret(px, py, 0.3 * (0.4 + 0.6 * sai), 0.38 * (0.4 + 0.6 * sai), ang)[1:] + _ret(px, py, 0.3 * (0.4 + 0.6 * sai), 0.38 * (0.4 + 0.6 * sai), ang)[:1])], 0.012)
    G += pagina * 0.35 * sai + borda * 0.9 * sai
    escreve = rel(t, 0.32, 0.62)
    for k in range(5):
        p = np.clip(escreve * 5 - k, 0, 1)
        if p <= 0:
            continue
        y = -0.24 + 0.11 * k
        x0, x1 = -0.2, -0.2 + 0.38 * p
        traco = [(x0 + (x1 - x0) * i / 10, y + 0.012 * math.sin(i * 2.3 + k)) for i in range(11)]
        G += T.polyline(traco, 0.012) * 1.1
        H += T.polyline(traco, 0.006) * 0.6
    para = rel(t, 0.6, 0.86)
    if para > 0:
        alc = -0.95 + 1.9 * ease_out(para, 2)
        xs = np.linspace(-0.95, alc, 40)
        pts = []
        for x in xs:
            pico = 0.0
            if -0.35 < x < -0.05:
                fase = (x + 0.35) / 0.3
                pico = 0.35 * math.sin(TAU * fase * 2) * math.exp(-((fase - 0.4) / 0.25) ** 2)
            pts.append((x, 0.55 - pico))
        G += T.polyline(pts, 0.018) * 1.4
        H += T.polyline(pts, 0.008) * 0.8
        G += T.gauss(0, 0, 0.5) * pulso(t, 0.7, 0.95) * 0.9
    return G * env, H * env


def modo_serio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    olhos = rel(t, 0.0, 0.18)
    for s in (-1, 1):
        G += T.tapered([(s * 0.06, -0.18, s * 0.26, -0.2 - 0.03 * olhos, 1.0)], 0.03 * olhos) * (1 - rel(t, 0.7, 0.9)) * 1.4
    sobe = rel(t, 0.1, 0.8)
    if sobe > 0:
        q = np.random.default_rng(3)
        segs = []
        for k in range(18):
            x = q.uniform(-0.55, 0.55)
            y0 = 0.6 - 1.4 * ((sobe * 1.3 + q.uniform(0, 1)) % 1)
            segs.append((x, y0 + 0.25, x * 1.05, y0, 1.0))
        G += T.lines(segs, 0.014, 0.004) * 0.9 * (1 - rel(t, 0.75, 0.95))
    onda = rel(t, 0.22, 0.7)
    if onda > 0:
        G += T.ring(0.1 + 0.85 * ease_out(onda, 2), 0.06 * (1 - onda) + 0.01) * (1 - onda) * 1.4
        G += T.flare(0, 0, 0.6 * (1 - onda) + 0.05, 0.0, 0.01) * pulso(t, 0.2, 0.45) * 1.5
        H += T.gauss(0, 0, 0.2) * pulso(t, 0.2, 0.4) * 2.0
    return G * env, H * env


def batarangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    gira = (1 - ease_out(rel(t, 0.0, 0.35), 2)) * 14 + 0.3
    M = T.polys([(_morcego(-0.05, 0, 1.2, t * gira), 1.0)])
    G += M * 0.9 * (1 - rel(t, 0.7, 0.9))
    bate = rel(t, 0.12, 0.55)
    if bate > 0:
        G += T.polys([(estrela(0.05, 0, 0.45 * ease_out(bate, 2) + 0.02, 0.3, 8, 0.25), 1.0)], 0.01) * (1 - bate) * 1.2
        q = np.random.default_rng(12)
        for k in range(12):
            a = q.uniform(0, TAU)
            d0, d1 = 0.1 + 0.6 * bate, 0.18 + 0.75 * bate
            G += T.lines([(0.05 + d0 * math.cos(a), d0 * math.sin(a), 0.05 + d1 * math.cos(a), d1 * math.sin(a), 1)], 0.01) * (1 - bate)
        H += T.gauss(0.05, 0, 0.08) * (1 - bate) * 1.8
    return G * env, H * env


def gancho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.lines([(0.0, -1.0, 0.0, -1.0 + 0.75 * desce, 1)], 0.012) * (1 - rel(t, 0.5, 0.7))
    G += T.polys([([(-0.06, -0.25 * desce - 0.02), (0.06, -0.25 * desce - 0.02), (0.0, -0.25 * desce + 0.1)], 1.0)]) * desce * (1 - rel(t, 0.5, 0.7))
    escudo = ease_out(rel(t, 0.25, 0.6), 3)
    if escudo > 0:
        G += T.ring(0.42 * escudo, 0.04, 0, 0, squash=1.25) * 1.1
        G += T.ring(0.42 * escudo, 0.25, 0, 0, squash=1.25) * 0.18
        G += T.polys([(_morcego(0, 0.02, 1.6 * escudo, 0.0), 1.0)]) * 0.95
        H += T.gauss(0, 0, 0.12) * pulso(t, 0.3, 0.6) * 1.2
    return G * env, H * env


def bomba_de_fumaca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    estoura = pulso(t, 0.0, 0.18)
    G += T.gauss(0, 0.1, 0.12) * estoura * 1.6
    H += T.gauss(0, 0.1, 0.05) * estoura * 2.0
    abre = ease_out(rel(t, 0.05, 0.8), 2)
    q = np.random.default_rng(21)
    nuvem = T.zero()
    for k in range(16):
        a = q.uniform(0, TAU)
        d = q.uniform(0.1, 0.75) * abre
        r = q.uniform(0.12, 0.22) * (0.5 + 0.7 * abre)
        nuvem += T.gauss(d * math.cos(a), 0.1 + d * math.sin(a) * 0.7 - 0.15 * abre, r)
    textura = np.clip(0.8 + 0.25 * T.noise(np.random.default_rng(4), 0.08, 3), 0.6, 1)
    G += np.clip(nuvem, 0, 1.2) * textura * 0.75
    return G * env, H * env


def doenca_terminal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    tomoe = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.ring(0.18 * tomoe, 0.025) * 1.2 * (1 - rel(t, 0.65, 0.85))
    for k in range(3):
        a = TAU * k / 3 + t * 6
        G += T.gauss(0.18 * tomoe * math.cos(a), 0.18 * tomoe * math.sin(a), 0.035) * 1.3 * (1 - rel(t, 0.65, 0.85))
    voam = rel(t, 0.15, 0.9)
    if voam > 0:
        q = np.random.default_rng(31)
        for k in range(9):
            a = q.uniform(-math.pi, 0.2) if k % 2 else q.uniform(0, TAU)
            d = 0.15 + 0.8 * ease_out(voam, 1.6) * q.uniform(0.7, 1.1)
            cx, cy = d * math.cos(a), d * math.sin(a) - 0.2 * voam
            bate = 0.06 * math.sin(TAU * (t * 5 + k * 0.3))
            asa = [(cx - 0.09, cy - bate), (cx - 0.02, cy + 0.015), (cx, cy - 0.01), (cx + 0.02, cy + 0.015), (cx + 0.09, cy - bate), (cx, cy + 0.035)]
            G += T.polys([(asa, 1.0)]) * (1 - rel(t, 0.7, 0.95)) * 0.95
    tosse = rel(t, 0.2, 0.75)
    if tosse > 0:
        q = np.random.default_rng(8)
        gotas = [(q.uniform(-0.15, 0.15), 0.1 + 0.6 * tosse * q.uniform(0.5, 1.0) ** 0.5, 1.0) for _ in range(10)]
        G += T.splats(gotas, 0.022) * (1 - rel(t, 0.65, 0.85)) * 1.1
    return G * env, H * env


def juntas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    parte = rel(t, 0.25, 0.75)
    for fio, ang0 in ((0, 0.35), (1, -0.35)):
        for k in range(-5, 6):
            if k == 0:
                continue
            base = k * 0.11
            lado = 1 if k > 0 else -1
            x = base * math.cos(ang0) + lado * 0.5 * ease_out(parte, 2) * abs(base)
            y = base * math.sin(ang0) + 0.3 * parte ** 2 * (abs(k) / 5)
            elo_ang = ang0 + parte * k * 0.9 + fio * 0.4
            G += T.ring(0.035, 0.012, x, y, squash=1.8 - 0.8 * ((k + fio) % 2)) * (1 - rel(t, 0.75, 0.95)) * 1.1
    estalo = rel(t, 0.2, 0.5)
    if estalo > 0:
        G += T.polys([(estrela(0, 0, 0.35 * ease_out(estalo, 2) + 0.02, 0.0, 10, 0.25), 1.0)], 0.01) * (1 - estalo) * 1.3
        H += T.gauss(0, 0, 0.07) * (1 - estalo) * 2.0
    return G * env, H * env


def endurecer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(6):
        aparece = ease_out(rel(t, 0.05 + 0.07 * k, 0.3 + 0.07 * k), 2)
        if aparece <= 0:
            continue
        a = TAU * k / 6 + 0.5
        r = 0.42 - 0.08 * aparece
        cx, cy = r * math.cos(a), r * math.sin(a)
        hexa = _hexagono(cx, cy, 0.17 * aparece, a)
        G += T.polys([(hexa, 1.0)], 0.004) * 0.45
        G += T.lines([(*p, *q, 1) for p, q in zip(hexa, hexa[1:] + hexa[:1])], 0.012) * 1.2
        H += T.lines([(cx, cy, *hexa[k % 6], 1)], 0.006) * 0.5 * aparece
    fecha = rel(t, 0.5, 0.75)
    G += T.ring(0.42, 0.03) * pulso(t, 0.5, 0.8) * 1.2
    H += T.gauss(0, 0, 0.3) * fecha * (1 - rel(t, 0.75, 0.9)) * 0.5
    return G * env, H * env


def agora_e_meu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    olho = T.polys([([(-0.5 * abre, 0), (0, -0.22 * abre), (0.5 * abre, 0), (0, 0.22 * abre)], 1.0)], 0.03)
    G += olho * 0.25
    for k in range(4):
        G += T.ring((0.05 + 0.045 * k) * abre, 0.012) * (1.2 - 0.15 * k) * abre
    H += T.gauss(0, 0, 0.03) * abre * 1.5
    prende = ease_out(rel(t, 0.3, 0.65), 2)
    if prende > 0:
        x0, y0 = -0.95, 0.75
        n = 9
        for k in range(n):
            f = k / (n - 1) * prende
            x = x0 + (0.0 - x0) * f
            y = y0 + (0.25 - y0) * f + 0.05 * math.sin(f * 6 + t * 8)
            G += T.ring(0.03, 0.01, x, y, squash=1.0 + 0.8 * (k % 2)) * 1.1
        G += T.ring(0.3, 0.02, 0, 0.0) * pulso(t, 0.55, 0.8) * 1.2
    return G * env, H * env


REGISTRO = [
    ("mu_pagina_no_relogio", pagina_no_relogio, GRANDE, "Light · o relógio abre, o nome é escrito e o coração para", False),
    ("mu_modo_serio", modo_serio, GRANDE, "Saitama · os olhos sérios, a aura subindo e a onda de choque", False),
    ("mu_batarangue", batarangue, GRANDE, "Batman · o batarangue cravando e as faíscas", False),
    ("mu_gancho", gancho, GRANDE, "Batman · o cabo do gancho e o escudo do morcego", False),
    ("mu_bomba_de_fumaca", bomba_de_fumaca, GRANDE, "Batman · a fumaça densa se espalhando", False),
    ("mu_doenca_terminal", doenca_terminal, GRANDE, "Itachi · o tomoe, a tosse de sangue e os corvos", False),
    ("mu_juntas", juntas, GRANDE, "Inosuke · as correntes arrebentando elo por elo", False),
    ("mu_endurecer", endurecer, GRANDE, "Eren · as placas de cristal fechando em volta", False),
    ("mu_agora_e_meu", agora_e_meu, GRANDE, "Makima · o olho de anéis e a corrente que prende", False),
]
