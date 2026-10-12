"""Rodada 24 das habilidades próprias: Sekiro, Malenia, Agente 47, Geralt de Rívia, Isaac Clarke e Gordon Freeman.

Sekiro
- deflexao_sekiro: a katana apara o golpe: a faísca grande e o eco do metal (Acelerado e Esquiva).
- mikiri: o pé pisando na lança do rival e o kanji vermelho do perigo (Paralisado).
- golpe_mortal: o golpe de execução: o corte vertical e o sangue em leque (Preparo interrompido).

Malenia
- lamina_de_miquella: a lâmina protética em arco duplo e a vida voltando para ela (Roubo de vida).
- malenia_preparo: o Preparo da Flor escarlate — Malenia sobe no ar e o botão vermelho abre (laço).
- flor_escarlate: a flor escarlate explode em pétalas de podridão (Fortalecido).

Agente 47
- disfarce: o terno trocado, a seringa e o veneno (Silenciado e Envenenado).
- garrote: o fio do garrote apertando em volta (Exposto).
- agent47_preparo: o Preparo do Tiro planejado — a luneta com a cruz andando devagar (laço).
- tiro_planejado: o tiro de precisão com o rastro longo e o impacto (Silenciado).

Geralt de Rívia
- sinal_de_quen: o sinal Quen dourado no ar e a bolha em volta dele (Escudo e Protegido).
- sinal_de_igni: o sinal Igni e o leque de fogo em todos (Queimando).
- sinal_de_axii: o sinal Axii roxo e o rival hipnotizado (Confuso e Silenciado).

Isaac Clarke
- desmembramento: os três raios azuis do cortador de plasma e os cortes nos membros (Enfraquecido e Preso).

Gordon Freeman
- pe_de_cabra: o pé de cabra girando e o golpe com o lambda (Preso e Marcado).
- zero_point: o canhão gravitacional: o anel laranja de energia empurrando todos (Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (CHAMA, GOTA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, flor, icone, onda_no_chao, particulas,
                         poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


# ------------------------------------------------------------------ Sekiro

def deflexao_sekiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.5, 0.7)
    if k > 0:
        L = T.polys([(lamina(-0.5, 0.35, 0.35, -0.4, 0.04, ease_out(rel(t, 0.0, 0.15))), 1.0)])
        G += L * 1.2 * k
    fa = pulso(t, 0.12, 0.4)
    if fa > 0:
        G += T.flare(0.0, 0.0, 0.9 * fa + 0.01, 0.25, 0.03) * 1.4
        H += T.gauss(0, 0, 0.06) * fa * 2.5
    G += estouro(T, t, 0.12, 0.5, 18, 2, 0, 0, 0.6, 0.012)
    for j in range(3):
        G += anel(T, t, 0.15 + 0.08 * j, 0.6 + 0.08 * j, 0.05, 0.5 + 0.1 * j, 0.02, 0.0, 1.0, 1.0)
    return G * env, H * env


def mikiri(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.3)
    k = 1 - rel(t, 0.6, 0.8)
    if u > 0:
        x = 0.8 - 0.8 * ease_out(u, 2)
        G += T.lines([(x, 0.1, x + 0.9, 0.1, 1.0)], 0.025) * k * 1.2
        G += T.polys([([(x - 0.12, 0.1), (x, 0.05), (x, 0.15)], 1.0)]) * k * 1.2
    pe = surge(t, 0.3, 0.45) * k
    if pe > 0:
        G += T.gauss(0.05, 0.05, 0.08, 0.04) * 1.3 * pe
        G += anel(T, t, 0.3, 0.7, 0.05, 0.4, 0.03, 0.1, 3.0)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.45, 0.6))
    if s > 0:
        kanji = [(-0.12, -0.55, 0.12, -0.55, 1.0), (0.0, -0.65, 0.0, -0.35, 1.0), (-0.1, -0.45, 0.1, -0.45, 1.0), (-0.12, -0.35, 0.12, -0.35, 1.0)]
        G += T.lines([(a * 1.6 * s, b, c * 1.6 * s, d, w) for a, b, c, d, w in kanji], 0.025) * 1.4
        G += T.gauss(0, -0.5, 0.2 * s + 0.001) * 0.6
    return G * env, H * env


def golpe_mortal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = corte(T, t, 0.1, 0.4, -math.pi / 2 + 0.15, 1.6, 0.11, 0.0, 0.0)
    G, H = G + g * 1.3, H + h
    g2, h2 = clarao(T, t, 0.18, 0.4, 0, 0, 1.0)
    G, H = G + g2, H + h2
    q = np.random.default_rng(4)
    for j in range(14):
        u = rel(t, 0.25, 0.85)
        if 0 < u < 1:
            a = -math.pi * q.uniform(0.15, 0.85)
            d = 0.7 * ease_out(u) * q.uniform(0.4, 1)
            g3, h3 = cheio(T, poe(GOTA, d * math.cos(a), d * math.sin(a) + 0.4 * u * u, 0.07, -a + math.pi / 2), (1 - u) * 1.3)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Malenia

def lamina_de_miquella(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j, (a, t0) in enumerate(((0.6, 0.0), (-0.6, 0.15))):
        g, h = corte(T, t, t0, t0 + 0.35, a, 1.5, 0.09, 0.2, 0.0, 0.25)
        G, H = G + g * 1.2, H + h
    u = rel(t, 0.45, 0.9)
    if 0 < u < 1:
        for j in range(6):
            v = (u + j / 6) % 1
            x = 0.3 - 0.8 * v
            y = 0.05 * math.sin(v * 10 + j)
            G += T.gauss(x, y, 0.04) * (1 - u) * 1.2
            H += T.gauss(x, y, 0.015) * (1 - u) * 1.5
    return G * env, H * env


def malenia_preparo(T, t, rng):
    G, H = vazio(T)
    sobe = 0.05 * math.sin(t * 4)
    for j in range(6):
        a = TAU * j / 6 + t * 0.6
        abre = 0.6 + 0.4 * math.sin(t * 3)
        pet = poe([(0, 0), (0.4, -0.5), (0, -1.0), (-0.4, -0.5)], 0, -0.1 + sobe, 0.38 * abre, a)
        g, h = icone(T, pet, 0.9, 0.5)
        G, H = G + g, H + h
    G += T.gauss(0, -0.1 + sobe, 0.1) * 1.3
    return G, H


def flor_escarlate(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        g, h = icone(T, poe(flor(8, 1.0, 0.25), 0, 0, 0.45 * s, t * 2), 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.3, 0.55, 0, 0, 1.4, 1.5)
    G, H = G + g2, H + h2
    q = np.random.default_rng(6)
    for j in range(30):
        u = rel(t, 0.3, 1.0)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.9 * ease_out(u, 2) * q.uniform(0.3, 1)
            pet = poe([(0, 0), (0.4, -0.5), (0, -1.0), (-0.4, -0.5)], d * math.cos(a), d * math.sin(a) + 0.2 * u, 0.05, a + u * 6)
            g3, h3 = cheio(T, pet, (1 - u) * 1.2)
            G, H = G + g3, H + h3
    G += anel(T, t, 0.3, 0.9, 0.1, 0.9, 0.05, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Agente 47

def disfarce(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.45, 0.6))
    if s > 0:
        terno = [(-0.2, -0.3), (0.2, -0.3), (0.28, 0.35), (-0.28, 0.35)]
        g, h = icone(T, [(x * s - 0.35, y * s) for x, y in terno], 1.0, 0.4)
        G, H = G + g, H + h
        G += T.lines([(-0.35, -0.25 * s, -0.35, 0.25 * s, 1.0)], 0.025) * 1.2
    u = rel(t, 0.35, 0.65)
    if 0 < u < 1:
        x = -0.3 + 0.8 * ease_out(u)
        G += T.lines([(x - 0.3, 0.0, x, 0.0, 1.0)], 0.025) * 1.3
        G += T.lines([(x - 0.3, -0.04, x - 0.3, 0.04, 1.0)], 0.02) * 1.2
        H += T.gauss(x, 0.0, 0.02) * 1.5
    k = pulso(t, 0.6, 1.0)
    for j in range(8):
        a = TAU * j / 8 + t * 2
        G += T.gauss(0.55 + 0.25 * math.cos(a), 0.25 * math.sin(a) - 0.2 * k, 0.05) * k * 1.2
    return G * env, H * env


def garrote(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    aperta = ease_in(rel(t, 0.1, 0.6), 1.5)
    k = 1 - rel(t, 0.8, 0.95)
    r = 0.4 - 0.25 * aperta
    G += T.ring(r, 0.015, 0.0, 0.0, 0.5) * k * 1.4
    H += T.ring(r, 0.005, 0.0, 0.0, 0.5) * k * 1.2
    for lado in (-1, 1):
        G += T.lines([(lado * r, 0.0, lado * (r + 0.35), -0.1, 1.0)], 0.015) * k * 1.2
        G += T.gauss(lado * (r + 0.38), -0.1, 0.04) * k
    g, h = clarao(T, t, 0.55, 0.75, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def agent47_preparo(T, t, rng):
    G, H = vazio(T)
    x, y = 0.05 * math.sin(t * 2), 0.04 * math.sin(t * 3)
    G += T.ring(0.35, 0.03, 0, 0) * 1.1
    G += T.lines([(-0.35, y, 0.35, y, 1.0), (x, -0.35, x, 0.35, 1.0)], 0.008) * 1.3
    H += T.gauss(x, y, 0.02) * 2
    G += T.gauss(0, 0, 0.36) * 0.25
    return G, H


def tiro_planejado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.2, -0.85, 0.0, 0.7)
    G, H = G + g, H + h
    u = ease_out(rel(t, 0.05, 0.2), 3)
    k = 1 - rel(t, 0.3, 0.75)
    if u > 0:
        G += T.lines([(-0.85, 0.0, -0.85 + 1.7 * u, 0.0, 1.0)], 0.012) * k * 1.4
        G += T.tapered([(-0.85, 0.0, -0.85 + 1.7 * u, 0.0, 0.3)], 0.04) * k * 0.6
    g2, h2 = clarao(T, t, 0.18, 0.4, 0.8, 0.0, 1.1, 1.4)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.18, 0.55, 14, 7, 0.8, 0.0, 0.45, 0.013)
    G += T.ring(0.18, 0.015, 0.8, 0.0) * pulso(t, 0.0, 0.25) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Geralt

def _sinal(T, s, forma, cx=0.0, cy=-0.45):
    if forma == 'quen':
        pts = [(0, -1), (0.87, 0.5), (-0.87, 0.5), (0, -1), (0, 0.5)]
    elif forma == 'igni':
        pts = [(-0.7, 0.7), (0, -1), (0.7, 0.7), (-0.7, 0.7)]
    else:
        pts = [(0, -1), (0.6, 0.6), (-0.6, 0.6), (0, -1), (0, 0.6), (-0.3, 0.0), (0.3, 0.0)]
    pts = poe(pts, cx, cy, 0.25 * s, 0)
    return T.polyline(pts, 0.03) * 1.5, T.polyline(pts, 0.01) * 1.3


def sinal_de_quen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.65))
    g, h = _sinal(T, s, 'quen')
    G, H = G + g, H + h
    b = ease_out(rel(t, 0.25, 0.55), 2) * (1 - rel(t, 0.88, 1))
    if b > 0:
        G += T.ring(0.55 * b, 0.04, 0, 0.05) * 1.2 + T.gauss(0, 0.05, 0.5 * b) * 0.3
        H += T.arc_band(0.5 * b, 0.02, -2.4, -1.6, 1.0, 0, 0, 0.05, 1.0)
        q = np.random.default_rng(int(t * 20))
        for _ in range(2):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0.55 * b * math.cos(a), 0.05 + 0.55 * b * math.sin(a), 0.55 * b * math.cos(a + 0.5), 0.05 + 0.55 * b * math.sin(a + 0.5), 3, 0.04), 0.01)
    G += anel(T, t, 0.25, 0.7, 0.1, 0.55, 0.03, 0.05)
    return G * env, H * env


def sinal_de_igni(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.4, 0.55))
    g, h = _sinal(T, s, 'igni', -0.5, -0.4)
    G, H = G + g, H + h
    u = rel(t, 0.2, 0.85)
    if 0 < u < 1:
        q = np.random.default_rng(7)
        for j in range(30):
            v = (u * 1.3 + j / 30) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            ang = q.uniform(-0.5, 0.5)
            x = -0.45 + 1.3 * v * math.cos(ang)
            y = 0.0 + 1.3 * v * math.sin(ang) * 0.6
            g2, h2 = icone(T, poe(CHAMA, x, y, 0.05 + 0.15 * v, math.pi / 2 + ang), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g2, H + h2
    return G * env, H * env


def sinal_de_axii(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.45, 0.6))
    g, h = _sinal(T, s, 'axii', -0.5, -0.4)
    G, H = G + g, H + h
    u = rel(t, 0.25, 0.6)
    if 0 < u < 1:
        for j in range(3):
            G += T.ring(0.08 + 0.1 * j + 0.2 * u, 0.015, -0.5 + 1.0 * ease_out(u), -0.1, 0.8) * (1 - u) * 1.3
    k = pulso(t, 0.55, 1.0)
    for j in range(3):
        pts = []
        for v in np.linspace(0, 1, 30):
            a = v * TAU * 1.5 + t * 6 + j * 2
            r = 0.05 + 0.15 * v
            pts.append((0.55 + r * math.cos(a), -0.35 + r * 0.5 * math.sin(a)))
        G += T.polyline(pts, 0.012) * k * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Isaac

def desmembramento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    mira = pulso(t, 0.0, 0.35)
    for dy in (-0.08, 0.0, 0.08):
        G += T.lines([(-0.8, dy, 0.6, dy * 2.5, 1.0)], 0.006) * mira * 1.3
    for j, (a, y0) in enumerate(((0.9, -0.3), (-0.9, 0.0), (0.2, 0.3))):
        g, h = corte(T, t, 0.3 + 0.1 * j, 0.55 + 0.1 * j, a, 0.8, 0.07, 0.45, y0)
        G, H = G + g * 1.2, H + h
        g2, h2 = clarao(T, t, 0.32 + 0.1 * j, 0.5 + 0.1 * j, 0.45, y0, 0.45)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Gordon

def pe_de_cabra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.45)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        a = -2.0 + 2.6 * ease_in(u, 1.5)
        c, s_ = math.cos(a), math.sin(a)
        x0, y0 = -0.1, 0.1
        x1, y1 = x0 + 0.65 * c, y0 + 0.65 * s_
        G += T.lines([(x0, y0, x1, y1, 1.0)], 0.03) * k * 1.3
        G += T.lines([(x1, y1, x1 + 0.1 * math.cos(a + 2.2), y1 + 0.1 * math.sin(a + 2.2), 1.0)], 0.03) * k * 1.3
        G += T.arc_band(0.65, 0.04, -2.0, a, 1.0, 0, x0, y0, 1.0) * k * 0.6
    g, h = clarao(T, t, 0.42, 0.6, 0.45, 0.2, 0.8)
    G, H = G + g, H + h
    ls = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if ls > 0:
        G += T.lines([(-0.08 * ls + 0.45, -0.35, 0.45, -0.55, 1.0), (0.45, -0.55, 0.12 * ls + 0.45, -0.35, 1.0), (0.42, -0.5, 0.36, -0.55, 1.0)], 0.025) * 1.3
        G += T.ring(0.15 * ls, 0.015, 0.45, -0.47) * 1.2
    return G * env, H * env


def zero_point(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.25, 16, 3, -0.6, 0.0, 0.4, 0.012)
    g, h = clarao(T, t, 0.2, 0.4, -0.6, 0.0, 0.9)
    G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.25 + 0.08 * j, 0.85 + 0.05 * j)
        if 0 < u < 1:
            x = -0.6 + 1.5 * ease_out(u, 2)
            G += T.arc_band(0.3 + 0.2 * u, 0.04 * (1 - 0.5 * u), -1.1, 1.1, 1.0, 0, x - 0.3, 0.0, 1.0) * (1 - u) * 1.5
    G += particulas(T, t, 0.3, 1.0, 26, 4, 0.2, 0.0, 0.8, 0.0, 0.012, 0.6)
    return G * env, H * env


REGISTRO = [
    ("deflexao_sekiro", deflexao_sekiro, GRANDE, "Sekiro · a deflexão e a faísca", False),
    ("mikiri", mikiri, GRANDE, "Sekiro · o pisão na lança e o kanji", False),
    ("golpe_mortal", golpe_mortal, GRANDE, "Sekiro · o golpe mortal", False),
    ("lamina_de_miquella", lamina_de_miquella, GRANDE, "Malenia · o arco duplo e a vida voltando", False),
    ("malenia_preparo", malenia_preparo, MEDIA, "Malenia · o botão abrindo (Preparo, laço)", True),
    ("flor_escarlate", flor_escarlate, GRANDE, "Malenia · a flor escarlate explodindo", False),
    ("disfarce", disfarce, GRANDE, "Agente 47 · o terno e a seringa", False),
    ("garrote", garrote, GRANDE, "Agente 47 · o fio apertando", False),
    ("agent47_preparo", agent47_preparo, MEDIA, "Agente 47 · a luneta (Preparo, laço)", True),
    ("tiro_planejado", tiro_planejado, GRANDE, "Agente 47 · o tiro de precisão", False),
    ("sinal_de_quen", sinal_de_quen, GRANDE, "Geralt · o sinal Quen e a bolha", False),
    ("sinal_de_igni", sinal_de_igni, GRANDE, "Geralt · o sinal Igni e o fogo", False),
    ("sinal_de_axii", sinal_de_axii, GRANDE, "Geralt · o sinal Axii e o transe", False),
    ("desmembramento", desmembramento, GRANDE, "Isaac · o cortador de plasma", False),
    ("pe_de_cabra", pe_de_cabra, GRANDE, "Gordon · o pé de cabra e o lambda", False),
    ("zero_point", zero_point, GRANDE, "Gordon · o canhão gravitacional", False),
]
