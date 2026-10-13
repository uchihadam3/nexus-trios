"""Mecânicas únicas refeitas, lote b (filmes e terror): o impacto conta o nome da mecânica.

- mu_estrangulamento (Darth Vader): a mão invisível da Força fechando os dedos em volta do alvo;
- mu_implacavel (Jason): a máscara de hóquei e o golpe que para no limite;
- mu_vitima (Michael Myers): a silhueta atrás do alvo e a faca que brilha;
- mu_outro_ghostface (Ghostface): a outra máscara aparece e corta em X;
- mu_sete_dias (Samara): a TV de chiado, o anel de luz e o cabelo escorrendo;
- mu_atras (Valak): a freira surgindo da sombra atrás do alvo, olhos acesos e a cruz virada;
- mu_golpe_voltou (Harry Potter): o escudo de amor da mãe e o golpe voltando;
- mu_horcrux (Voldemort): a horcrux rachando em cacos e a fumaça de cobra.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio


def _oval(cx, cy, rx, ry, n=24, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(TAU * k / n) * c - ry * math.sin(TAU * k / n) * s, cy + rx * math.cos(TAU * k / n) * s + ry * math.sin(TAU * k / n) * c) for k in range(n)]


def _contorno(T, pts, larg):
    return T.lines([(*a, *b, 1) for a, b in zip(pts, pts[1:] + pts[:1])], larg)


def estrangulamento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    fecha = ease_out(rel(t, 0.0, 0.45), 2)
    cy = -0.12
    for k in range(4):
        a0 = -2.3 + 0.75 * k
        r = 0.55 - 0.3 * fecha
        G += T.arc_band(r, 0.035, a0, a0 + 0.55, cx=0, cy=cy, taper=1.0) * 1.1
    G += T.arc_band(0.55 - 0.3 * fecha, 0.04, 0.6, 1.4, cx=0, cy=cy, taper=1.0) * 0.9
    aperta = rel(t, 0.3, 0.95)
    if aperta > 0:
        for k in range(3):
            f = ((aperta * 2.5 + k / 3) % 1)
            G += T.ring(0.42 * (1 - f) + 0.05, 0.015, 0, cy) * (1 - f) * 0.9
        H += T.gauss(0, cy, 0.06) * pulso(t, 0.35, 0.9) * 0.9
    sobe = ease_out(rel(t, 0.3, 0.8), 2)
    G += T.lines([(x, 0.55, x, 0.55 - 0.18 * sobe, 1) for x in (-0.08, 0.08)], 0.01) * 0.6 * sobe
    return G * env, H * env


def implacavel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    mascara = _oval(0, -0.02, 0.26 * surge + 0.01, 0.34 * surge + 0.01)
    G += T.polys([(mascara, 1.0)], 0.004) * 0.35 + _contorno(T, mascara, 0.014) * 1.1
    q = np.random.default_rng(5)
    furos = [(x * surge, y * surge, 1.0) for x, y in [(-0.1, -0.12), (0.1, -0.12), (-0.05, 0.05), (0.05, 0.05), (0, 0.15), (-0.13, 0.12), (0.13, 0.12)]]
    G += T.splats(furos, 0.022) * 0.9
    G += T.lines([(-0.2 * surge, -0.2, -0.04, -0.06, 1), (0.2 * surge, -0.2, 0.04, -0.06, 1)], 0.02) * 0.8
    golpe = rel(t, 0.35, 0.7)
    if golpe > 0:
        x = -0.9 + 0.7 * ease_in(min(golpe * 1.6, 1), 2)
        G += T.tapered([(x - 0.4, -0.45, x, -0.25, 1)], 0.03) * (1 - rel(t, 0.6, 0.8))
        para = pulso(t, 0.5, 0.75)
        G += T.polys([(estrela(-0.3, -0.27, 0.22 * para + 0.01, 0.2, 8, 0.3), 1.0)], 0.008) * para * 1.3
        G += T.ring(0.5, 0.03, 0, 0) * para * 1.0
        H += T.gauss(-0.3, -0.27, 0.05) * para * 1.8
    return G * env, H * env


def vitima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sombra = ease_out(rel(t, 0.0, 0.45), 2)
    corpo = [(-0.22, 0.75), (-0.2, -0.05), (-0.12, -0.35), (0, -0.45), (0.12, -0.35), (0.2, -0.05), (0.22, 0.75)]
    G += T.polys([([(x * sombra, y * 0.9 + 0.1 * (1 - sombra)) for x, y in corpo], 1.0)], 0.03) * 0.35 * sombra
    G += T.gauss(0, -0.42, 0.14 * sombra) * 0.4
    faca = rel(t, 0.25, 0.65)
    if faca > 0:
        y = -0.8 + 0.6 * ease_out(faca, 2)
        lamina = [(0.28, y - 0.25), (0.33, y + 0.1), (0.29, y + 0.12)]
        G += T.polys([(lamina, 1.0)], 0.003) * 1.1 + T.lines([(0.31, y + 0.12, 0.31, y + 0.28, 1)], 0.03) * 0.8
        brilho = pulso(t, 0.45, 0.65)
        G += T.flare(0.3, y - 0.12, 0.3 * brilho + 0.01, 0.0, 0.006) * brilho * 1.6
        H += T.gauss(0.3, y - 0.12, 0.03) * brilho * 2.0
    marca = rel(t, 0.55, 0.9)
    G += T.ring(0.38, 0.03, 0, 0.05) * pulso(t, 0.55, 0.95) * 1.1
    return G * env, H * env


def outro_ghostface(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    cx = 0.45 - 0.2 * surge
    mascara = [(cx - 0.12, -0.35), (cx, -0.45), (cx + 0.12, -0.35), (cx + 0.1, 0.1), (cx, 0.25), (cx - 0.1, 0.1)]
    G += T.polys([(mascara, 1.0)], 0.01) * 0.85 * surge * (1 - rel(t, 0.75, 0.95))
    for s in (-1, 1):
        G += T.polys([(_oval(cx + s * 0.05, -0.2, 0.03, 0.07, 12, s * 0.3), 1.0)]) * -0.8 * surge
    G += T.polys([(_oval(cx, 0.05, 0.03, 0.08, 12), 1.0)]) * -0.8 * surge
    corta = rel(t, 0.35, 0.65)
    if corta > 0:
        for a in (0.7, -0.7):
            G += T.tapered([(-0.4 * math.cos(a) - 0.1, -0.4 * math.sin(a), (-0.4 + 0.8 * ease_out(corta, 2)) * math.cos(a) - 0.1, (-0.4 + 0.8 * ease_out(corta, 2)) * math.sin(a), 1)], 0.035) * (1 - rel(t, 0.65, 0.85)) * 1.2
        H += T.gauss(-0.1, 0, 0.05) * pulso(t, 0.45, 0.7) * 1.8
    return np.clip(G, 0, None) * env, H * env


def sete_dias(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    liga = ease_out(rel(t, 0.0, 0.2), 2)
    tela = [(-0.42 * liga, -0.3), (0.42 * liga, -0.3), (0.42 * liga, 0.28), (-0.42 * liga, 0.28)]
    chiado = np.clip(T.noise(np.random.default_rng(int(t * 30) % 9), 0.015, 1) * 0.8 + 0.4, 0, 1)
    G += T.polys([(tela, 1.0)], 0.004) * chiado * 0.45 * (1 - rel(t, 0.7, 0.9))
    G += _contorno(T, [(-0.48 * liga, -0.36), (0.48 * liga, -0.36), (0.48 * liga, 0.34), (-0.48 * liga, 0.34)], 0.02) * 0.9
    anel = rel(t, 0.15, 0.6)
    G += T.ring(0.2 * ease_out(anel, 2) + 0.01, 0.025, 0, -0.01) * min(1, anel * 3) * 1.4 * (1 - rel(t, 0.7, 0.9))
    H += T.ring(0.2 * ease_out(anel, 2) + 0.01, 0.01, 0, -0.01) * min(1, anel * 3) * (1 - rel(t, 0.7, 0.9))
    cabelo = rel(t, 0.45, 1.0)
    if cabelo > 0:
        q = np.random.default_rng(4)
        segs = []
        for k in range(16):
            x = q.uniform(-0.3, 0.3)
            comp = 0.7 * ease_out(cabelo, 1.5) * q.uniform(0.6, 1.0)
            pts = [(x + 0.03 * math.sin(i * 0.9 + k), -0.25 + comp * i / 8) for i in range(9)]
            G += T.polyline(pts, 0.012) * 0.75
    return G * env, H * env


def atras(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.5), 2)
    base = 0.75
    alto = base - 1.25 * sobe
    veu = [(-0.3, base), (-0.24, alto + 0.35), (-0.14, alto + 0.08), (0, alto), (0.14, alto + 0.08), (0.24, alto + 0.35), (0.3, base)]
    G += T.polys([(veu, 1.0)], 0.03) * 0.55 * (1 - rel(t, 0.8, 0.95))
    rosto = _oval(0, alto + 0.22, 0.09, 0.12)
    G += T.polys([(rosto, 1.0)], 0.01) * 0.6 * sobe
    olhos = pulso(t, 0.35, 0.95)
    for s in (-1, 1):
        G += T.gauss(s * 0.04, alto + 0.2, 0.018) * olhos * 1.8
        H += T.gauss(s * 0.04, alto + 0.2, 0.01) * olhos * 2.0
    cruz = rel(t, 0.4, 0.75)
    if cruz > 0:
        G += T.lines([(0, alto + 0.42, 0, alto + 0.62, 1), (-0.05, alto + 0.57, 0.05, alto + 0.57, 1)], 0.018) * cruz * 1.1
    G += T.gauss(0, base - 0.05, 0.4) * 0.25 * sobe
    return G * env, H * env


def golpe_voltou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    escudo = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.ring(0.42 * escudo + 0.01, 0.04) * 1.2
    G += T.ring(0.42 * escudo + 0.01, 0.3) * 0.18
    for k in range(10):
        a = TAU * k / 10 + t * 2
        G += T.gauss(0.42 * escudo * math.cos(a), 0.42 * escudo * math.sin(a), 0.025) * 0.8
    vem = rel(t, 0.2, 0.45)
    if vem > 0:
        x = -0.95 + 0.53 * ease_in(vem, 2)
        G += T.tapered([(x - 0.3, 0, x, 0, 1)], 0.04) * (1 - rel(t, 0.44, 0.46)) * 1.2
    volta = rel(t, 0.45, 0.85)
    if volta > 0:
        x = -0.42 - 0.6 * ease_out(volta, 2)
        G += T.tapered([(x + 0.3, 0, x, 0, 1)], 0.05) * (1 - rel(t, 0.8, 0.95)) * 1.4
        H += T.tapered([(x + 0.3, 0, x, 0, 1)], 0.02) * (1 - rel(t, 0.8, 0.95))
        G += T.polys([(estrela(-0.42, 0, 0.25 * pulso(t, 0.45, 0.65) + 0.01, 0.0, 8, 0.3), 1.0)], 0.01) * pulso(t, 0.45, 0.65) * 1.3
    return G * env, H * env


def horcrux(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pend = 1 - rel(t, 0.3, 0.4)
    medalhao = _oval(0, 0, 0.16, 0.2)
    G += (T.polys([(medalhao, 1.0)], 0.004) * 0.5 + _contorno(T, medalhao, 0.014) + T.lines([(0, -0.2, 0, -0.45, 1)], 0.01)) * pend
    G += T.polys([([(-0.06, 0.06), (0.0, -0.08), (0.06, 0.06), (0.0, 0.0)], 1.0)]) * 0.9 * pend
    racha = rel(t, 0.2, 0.35)
    G += T.polyline([(-0.02, -0.18), (0.04, -0.05), (-0.03, 0.04), (0.03, 0.18)], 0.01) * racha * pend * 1.5
    quebra = rel(t, 0.35, 0.9)
    if quebra > 0:
        q = np.random.default_rng(6)
        for k in range(14):
            a = q.uniform(0, TAU)
            d = 0.75 * ease_out(quebra, 2) * q.uniform(0.4, 1.0)
            cx, cy = d * math.cos(a), d * math.sin(a)
            s = 0.04 * q.uniform(0.6, 1.2)
            caco = [(cx + s * math.cos(a + j * 2.1 + quebra * 5), cy + s * math.sin(a + j * 2.1 + quebra * 5)) for j in range(3)]
            G += T.polys([(caco, 1.0)]) * (1 - rel(t, 0.7, 0.95)) * 0.9
        cobra = [(0.5 * math.sin(i * 0.8 + t * 6) * (i / 14) * ease_out(quebra, 2), -0.1 - 0.06 * i * ease_out(quebra, 2)) for i in range(15)]
        G += T.polyline(cobra, 0.04) * 0.5 * (1 - rel(t, 0.75, 0.95))
        G += T.gauss(0, 0, 0.12) * pulso(t, 0.33, 0.55) * 1.4
        H += T.gauss(0, 0, 0.05) * pulso(t, 0.33, 0.5) * 2.0
    return G * env, H * env


REGISTRO = [
    ("mu_estrangulamento", estrangulamento, GRANDE, "Darth Vader · a mão da Força fechando em volta do alvo", False),
    ("mu_implacavel", implacavel, GRANDE, "Jason · a máscara e o golpe que para no limite", False),
    ("mu_vitima", vitima, GRANDE, "Michael Myers · a silhueta atrás do alvo e a faca brilhando", False),
    ("mu_outro_ghostface", outro_ghostface, GRANDE, "Ghostface · a outra máscara e o corte em X", False),
    ("mu_sete_dias", sete_dias, GRANDE, "Samara · a TV de chiado, o anel e o cabelo escorrendo", False),
    ("mu_atras", atras, GRANDE, "Valak · a freira surgindo da sombra, olhos acesos e a cruz", False),
    ("mu_golpe_voltou", golpe_voltou, GRANDE, "Harry Potter · o escudo da mãe e o golpe voltando", False),
    ("mu_horcrux", horcrux, GRANDE, "Voldemort · a horcrux rachando em cacos e a fumaça de cobra", False),
]
