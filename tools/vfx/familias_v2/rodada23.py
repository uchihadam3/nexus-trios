"""Rodada 23 das habilidades próprias: Liu Kang, Raiden (Mortal Kombat), Jin Kazama, Kazuya Mishima, Sora e 2B.

Liu Kang
- bola_de_fogo_liukang: a bola de fogo do Shaolin voando reta e explodindo (Exposto e Queimando).
- liukang_preparo: o Preparo do Dragão flamejante — o fogo girando em volta dele em espiral (laço).
- dragao_flamejante: o dragão de fogo serpenteando até o rival e mordendo (Queimando).

Raiden (Mortal Kombat)
- raio_celeste: os raios caindo do céu em cada rival (Eletrificado).
- barreira_eletrica: a cúpula de eletricidade sobre o trio (Escudo, Protegido e Barreira).
- raidenmk_preparo: o Preparo do Trovão dos deuses — os olhos acesos e as faíscas no chapéu (laço).
- trovao_dos_deuses: a tempestade inteira desce: os raios grossos e o clarão (Paralisado).

Jin Kazama
- postura_mishima: a guarda do karatê Mishima e o brilho azul em volta (Protegido e Acelerado).
- contra_ataque: o aparo (a faísca) e o chute de volta que paralisa.
- gene_do_diabo: as asas negras e o chifre do Devil Jin, e o raio da testa (Exposto e Eletrificado).

Kazuya Mishima
- pisao_demoniaco: o pisão com os raios roxos no chão (Fortalecido).
- raio_do_diabo: o laser roxo saindo da testa (Acelerado e Fortalecido).
- kazuya_preparo: o Preparo da Forma Devil — os raios roxos subindo pelo corpo (laço).
- forma_devil: as asas do Devil abrem, o clarão roxo e o golpe que queima.

Sora
- cura_sora: o feitiço Cura: a flor verde e as folhas subindo (Regeneração e Acelerado).
- sora_preparo: o Preparo da Forma final — a coroa e a chave-espada girando (laço).
- forma_final: as duas chaves-espada flutuando e a luz prateada sobre o trio.

2B
- lamina_virtuosa: o giro da espada com as fitas de luz branca (Marcado e Exposto).
- apoio_do_pod: o Pod dispara a rajada de tiros em todos os rivais (Marcado).
- modo_berserk: a viseira cai, a aura vermelha e o golpe pesado da espada grande.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, COROA, ESPADA, FOLHA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, flor, icone,
                         onda_no_chao, particulas, poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _raio(T, t, x0, y0, x1, y1, k, w=0.02, seed=0):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, 0.1)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.5


def _chave(cx, cy, s, ang):
    lam = poe([(-0.04, -1.0), (0.04, -1.0), (0.04, 0.4), (-0.04, 0.4)], cx, cy, s, ang)
    dente = poe([(0.04, -1.0), (0.3, -1.0), (0.3, -0.85), (0.15, -0.85), (0.15, -0.75), (0.04, -0.75)], cx, cy, s, ang)
    guarda = poe([(-0.25, 0.4), (0.25, 0.4), (0.25, 0.5), (-0.25, 0.5)], cx, cy, s, ang)
    return lam, dente, guarda


# ------------------------------------------------------------------ Liu Kang

def bola_de_fogo_liukang(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.1, 0.6)
    if 0 < u < 1:
        x = -0.6 + 1.3 * u
        g, h = icone(T, poe(CHAMA, x, 0.0, 0.27, math.pi / 2), 1.4, 0.6)
        G, H = G + g, H + h * 1.5
        G += T.tapered([(x - 0.6, 0.0, x - 0.15, 0.0, 0.5)], 0.1) * 0.9
    g2, h2 = clarao(T, t, 0.58, 0.78, 0.7, 0.0, 1.0)
    G, H = G + g2, H + h2
    for j in range(6):
        k = pulso(t, 0.6 + 0.02 * j, 0.95)
        a = TAU * j / 6
        g3, h3 = icone(T, poe(CHAMA, 0.7 + 0.2 * math.cos(a), 0.16 * math.sin(a), 0.11 * k), k, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def liukang_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(8):
        v = j / 8
        a = t * 6 + TAU * v * 1.5
        r = 0.2 + 0.35 * v
        g, h = icone(T, poe(CHAMA, r * math.cos(a), 0.15 + r * 0.6 * math.sin(a) - 0.4 * v, 0.13 * (1 - 0.4 * v)), 1.2 - 0.5 * v, 0.6)
        G, H = G + g, H + h
    return G, H


def dragao_flamejante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.6), 1.5)
    if u > 0:
        corpo = [(-0.8 + 1.5 * v * u, 0.05 + 0.25 * math.sin(v * 9 - t * 12) * (1 - v * 0.5)) for v in np.linspace(0, 1, 30)]
        for i in range(len(corpo) - 1):
            w = 0.03 + 0.07 * (i / 30)
            G += T.lines([(corpo[i][0], corpo[i][1], corpo[i + 1][0], corpo[i + 1][1], 1.0)], w) * 1.1 * (1 - rel(t, 0.8, 0.95))
        hx, hy = corpo[-1]
        g, h = icone(T, [(hx + 0.18, hy), (hx + 0.02, hy - 0.12), (hx - 0.1, hy - 0.08), (hx - 0.12, hy + 0.06), (hx + 0.02, hy + 0.1)], 1.3 * (1 - rel(t, 0.8, 0.95)), 0.6)
        G, H = G + g, H + h * 1.5
        for lado in (-1, 1):
            G += T.lines([(hx - 0.05, hy - 0.08, hx - 0.18, hy - 0.2 * lado - 0.05, 1.0)], 0.012) * (1 - rel(t, 0.8, 0.95))
    g2, h2 = clarao(T, t, 0.55, 0.75, 0.7, 0.05, 1.2, 1.4)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.55, 0.95, 16, 5, 0.7, 0.05, 0.5, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Raiden

def raio_celeste(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.1 + 0.12 * j, 0.4 + 0.12 * j)
        if k > 0:
            g, h = _raio(T, t, x + 0.1, -0.95, x, 0.2, k, 0.025, j)
            G, H = G + g, H + h
            G += T.gauss(x, 0.2, 0.12) * k * 0.8
    for j in range(5):
        G += T.gauss(-0.7 + 0.35 * j, -0.85, 0.15, 0.06) * 0.5 * pulso(t, 0.0, 0.9)
    return G * env, H * env


def barreira_eletrica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.arc_band(0.75 * s, 0.04, math.pi, TAU, 0.8, 0, 0, 0.35, 1.0) * 1.2
        G += T.gauss(0, 0.1, 0.6 * s + 0.001, 0.35 * s + 0.001) * 0.3
        q = np.random.default_rng(int(t * 25))
        for _ in range(3):
            a1 = q.uniform(math.pi, TAU)
            a2 = a1 + q.uniform(-0.6, 0.6)
            p1 = (0.75 * s * math.cos(a1), 0.35 + 0.6 * s * math.sin(a1))
            p2 = (0.75 * s * math.cos(a2), 0.35 + 0.6 * s * math.sin(a2))
            bolt = jagged(q, p1[0], p1[1], p2[0], p2[1], 4, 0.06)
            G += T.polyline(bolt, 0.012) * 1.2
    G += onda_no_chao(T, t, 0.3, 0.9, 0.85, 0.35)
    return G * env, H * env


def raidenmk_preparo(T, t, rng):
    G, H = vazio(T)
    chapeu = [(-0.6, -0.15), (0.0, -0.55), (0.6, -0.15)]
    G += T.polyline(chapeu + [chapeu[0]], 0.03) * 1.2
    for lado in (-1, 1):
        H += T.gauss(lado * 0.13, 0.0, 0.04) * (1.5 + 0.5 * math.sin(t * 15))
        G += T.gauss(lado * 0.13, 0.0, 0.09) * 0.9
    q = np.random.default_rng(int(t * 20))
    for _ in range(2):
        x = q.uniform(-0.35, 0.35)
        G += T.polyline(jagged(q, x, -0.25, x + q.uniform(-0.15, 0.15), -0.55, 3, 0.05), 0.01) * 1.2
    return G, H


def trovao_dos_deuses(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    nuvem = pulso(t, 0.0, 0.9)
    for j in range(7):
        G += T.gauss(-0.9 + 0.3 * j, -0.85, 0.18, 0.08) * 0.7 * nuvem
    for j, x in enumerate((-0.6, -0.2, 0.2, 0.6)):
        k = pulso(t, 0.2 + 0.04 * j, 0.6 + 0.04 * j)
        if k > 0:
            g, h = _raio(T, t, x + 0.15 * math.sin(j), -0.85, x, 0.35, k, 0.04, j + 3)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.25, 0.5, 0, 0.0, 1.5, 1.6)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.25, 0.85, 1.0, 0.35, 1.6)
    return G * env, H * env


# ------------------------------------------------------------------ Jin

def postura_mishima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        P, nos = _punho(T, -0.15, -0.1, 1.8 * s, -0.4)
        G += P * 0.8
        H += nos * 0.4
        P2, nos2 = _punho(T, 0.15, 0.1, 1.6 * s, math.pi + 0.4)
        G += P2 * 0.7
    g, h = aura(T, t, 0.15, 1.0, 0.42, 0.0, 1.0)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.8, 0.15, 0.65, 0.03, 0.0)
    return G * env, H * env


def contra_ataque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    fa = pulso(t, 0.05, 0.3)
    if fa > 0:
        G += T.flare(-0.2, 0.0, 0.7 * fa + 0.01, 0.3, 0.03) * 1.4
        H += T.gauss(-0.2, 0.0, 0.07) * fa * 2
        G += T.gauss(-0.2, 0.0, 0.15) * fa
    u = rel(t, 0.3, 0.55)
    if 0 < u < 1:
        a = -1.2 + 1.4 * ease_out(u)
        G += T.tapered([(-0.1, 0.25, -0.1 + 0.7 * math.cos(a), 0.25 + 0.7 * math.sin(a), 1.0)], 0.07) * 1.2
        G += T.arc_band(0.7, 0.03, -1.2, a, 1.0, 0, -0.1, 0.25, 1.0) * 0.8
    g2, h2 = clarao(T, t, 0.5, 0.7, 0.55, -0.1, 0.9)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.5, 0.85, 12, 3, 0.55, -0.1, 0.45, 0.014)
    return G * env, H * env


def gene_do_diabo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        asa = [(lado * x * 0.85 * s, -0.1 + y * 0.75 * s) for x, y in ASA]
        g, h = icone(T, asa, 0.7, 0.5)
        G, H = G + g, H + h
    if s > 0:
        g, h = cheio(T, [(-0.04, -0.35), (0.04, -0.35), (0.0, -0.35 - 0.2 * s)], 1.5)
        G, H = G + g, H + h * 2
    u = rel(t, 0.4, 0.7)
    if 0 < u < 1:
        G += T.lines([(0, -0.38, 0.95, -0.1, 1.0)], 0.04) * pulso(u, 0, 1) * 1.3
        H += T.lines([(0, -0.38, 0.95, -0.1, 1.0)], 0.012) * pulso(u, 0, 1) * 1.5
    g2, h2 = clarao(T, t, 0.6, 0.8, 0.8, -0.12, 0.8)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Kazuya

def pisao_demoniaco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.15, 0.35, 0, 0.35, 0.9)
    G, H = G + g, H + h
    for j in range(6):
        k = pulso(t, 0.18 + 0.03 * j, 0.6 + 0.03 * j)
        if k > 0:
            a = math.pi + math.pi * (j + 0.5) / 6
            g2, h2 = _raio(T, t, 0, 0.35, 0.7 * math.cos(a), 0.35 + 0.6 * math.sin(a), k, 0.018, j)
            G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.15, 0.75, 0.9, 0.35, 1.6)
    g3, h3 = aura(T, t, 0.3, 1.0, 0.35, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


def raio_do_diabo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = pulso(t, 0.0, 0.3)
    H += T.gauss(-0.4, -0.35, 0.04) * s * 2.5
    G += T.gauss(-0.4, -0.35, 0.1) * s
    u = rel(t, 0.15, 0.45)
    k = 1 - rel(t, 0.5, 0.7)
    if u > 0:
        x1 = -0.4 + 1.3 * ease_out(u, 3)
        G += T.lines([(-0.4, -0.35, x1, -0.1, 1.0)], 0.05) * k * 1.0
        H += T.lines([(-0.4, -0.35, x1, -0.1, 1.0)], 0.015) * k * 1.5
    g2, h2 = clarao(T, t, 0.4, 0.6, 0.85, -0.1, 0.7)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.3, 0.9, 0.1, 0.5, 0.03, 0.0)
    return G * env, H * env


def kazuya_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(3):
        x = -0.25 + 0.25 * j
        g, h = _raio(T, t, x, 0.4, x + 0.1 * math.sin(t * 5 + j), -0.45, 0.8, 0.015, j)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.3, 0.45) * (0.4 + 0.15 * math.sin(t * 8))
    return G, H


def forma_devil(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        asa = [(lado * x * 1.0 * s, -0.15 + y * 0.9 * s) for x, y in ASA]
        g, h = icone(T, asa, 0.8, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.2, 0.45, 0, -0.1, 1.3, 1.5)
    G, H = G + g2, H + h2
    g3, h3 = corte(T, t, 0.45, 0.7, -0.5, 1.4, 0.1, 0.35, 0.05)
    G, H = G + g3 * 1.2, H + h3
    for j in range(5):
        k = pulso(t, 0.55 + 0.03 * j, 0.95)
        g4, h4 = icone(T, poe(CHAMA, 0.25 + 0.1 * j, 0.1 - 0.08 * (j % 2), 0.09 * k), k, 0.6)
        G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Sora

def cura_sora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    g, h = icone(T, poe(flor(6, 1.0, 0.3), 0, 0.15, 0.25 * s, t * 2), 1.2, 0.5)
    G, H = G + g, H + h
    H += T.gauss(0, 0.15, 0.06 * s + 0.001) * 1.5
    for j in range(8):
        u = rel(t, 0.2 + 0.05 * j, 0.8 + 0.03 * j)
        if 0 < u < 1:
            a = TAU * j / 8 + u * 3
            r = 0.2 + 0.35 * u
            g2, h2 = cheio(T, poe(FOLHA, r * math.cos(a), 0.15 - 0.5 * u + 0.15 * math.sin(a), 0.06, a), (1 - u) * 1.3)
            G, H = G + g2, H + h2
    G += anel(T, t, 0.3, 0.85, 0.1, 0.55, 0.03, 0.15)
    return G * env, H * env


def sora_preparo(T, t, rng):
    G, H = vazio(T)
    a = t * 5
    lam, dente, guarda = _chave(0, 0.05, 0.6, a)
    G += T.polys([(lam, 1.0), (dente, 1.0), (guarda, 1.0)]) * 1.1
    g, h = cheio(T, poe(COROA, 0, -0.65, 0.18, 0), 1.3)
    return G + g, H + h * (1.2 + 0.4 * math.sin(t * 10))


def forma_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        lam, dente, guarda = _chave(lado * 0.5, -0.05 + 0.04 * math.sin(t * 8 + lado), 0.6 * s, lado * 0.4)
        G += T.polys([(lam, 1.0), (dente, 1.0), (guarda, 1.0)]) * 1.1
    g, h = clarao(T, t, 0.25, 0.5, 0, -0.1, 1.0)
    G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 40, 8, 0, 0.0, 0.8, 0.5, 0.013)
    G += anel(T, t, 0.35, 0.9, 0.2, 0.9, 0.035, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ 2B

def lamina_virtuosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    giro = rel(t, 0.0, 0.55)
    if 0 < giro < 1:
        a0 = giro * TAU * 1.5
        G += T.arc_band(0.55, 0.11, a0, a0 + 2.5, 0.55, 0, 0, 0.0, 1.0, True) * (1 - giro) * 1.7
        H += T.arc_band(0.5, 0.015, a0, a0 + 2.5, 0.55, 0, 0, 0.0, 1.0) * (1 - giro) * 1.2
        for j in range(3):
            pts = [(0.65 * math.cos(a0 - 0.4 * j - v), 0.65 * 0.55 * math.sin(a0 - 0.4 * j - v)) for v in np.linspace(0, 1.2, 16)]
            G += T.polyline(pts, 0.008) * (1 - giro) * 0.9
    g2, h2 = corte(T, t, 0.45, 0.7, 0.3, 1.2, 0.07, 0.4, 0.0)
    G, H = G + g2, H + h2
    return G * env, H * env


def apoio_do_pod(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.88, 1))
    pod = [(-0.12, -0.08), (0.12, -0.08), (0.16, 0.0), (0.12, 0.12), (-0.12, 0.12), (-0.16, 0.0)]
    g, h = icone(T, [(x * 1.3 * s - 0.55, y * 1.3 * s - 0.4) for x, y in pod], 1.1, 0.5)
    G, H = G + g, H + h
    for j in range(9):
        u = rel(t, 0.15 + 0.05 * j, 0.4 + 0.05 * j)
        if 0 < u < 1:
            alvo = (-0.4 + 0.45 * (j % 3), 0.1 + 0.05 * (j % 2))
            x = -0.35 + (alvo[0] + 0.35) * u
            y = -0.4 + (alvo[1] + 0.4) * u
            G += T.tapered([(x - 0.2 * (alvo[0] + 0.35), y - 0.2 * (alvo[1] + 0.4), x, y, 1.0)], 0.035) * 1.5
        if u >= 1:
            G += T.gauss(-0.4 + 0.45 * (j % 3), 0.1 + 0.05 * (j % 2), 0.05) * (1 - rel(t, 0.4 + 0.05 * j, 0.6 + 0.05 * j)) * 1.1
    return G * env, H * env


def modo_berserk(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = aura(T, t, 0.0, 0.7, 0.45, 0.0, 1.2)
    G, H = G + g, H + h
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.35, 0.5))
    if s > 0:
        G += T.lines([(-0.18, -0.3, 0.18, -0.3, 1.0)], 0.04 * s) * 1.3
    desce = ease_in(rel(t, 0.3, 0.5), 2)
    k = 1 - rel(t, 0.65, 0.8)
    if desce > 0 and k > 0:
        g2, h2 = icone(T, poe(ESPADA, 0.1 + 0.3 * desce, -0.2 + 0.25 * desce, 0.55, -1.0 + 2.2 * desce), k * 1.2, 0.5)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.48, 0.68, 0.45, 0.2, 1.2, 1.4)
    G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.48, 0.9, 0.9, 0.35)
    return G * env, H * env


REGISTRO = [
    ("bola_de_fogo_liukang", bola_de_fogo_liukang, GRANDE, "Liu Kang · a bola de fogo", False),
    ("liukang_preparo", liukang_preparo, MEDIA, "Liu Kang · o fogo em espiral (Preparo, laço)", True),
    ("dragao_flamejante", dragao_flamejante, GRANDE, "Liu Kang · o dragão de fogo", False),
    ("raio_celeste", raio_celeste, GRANDE, "Raiden · os raios do céu", False),
    ("barreira_eletrica", barreira_eletrica, GRANDE, "Raiden · a cúpula elétrica", False),
    ("raidenmk_preparo", raidenmk_preparo, MEDIA, "Raiden · os olhos e as faíscas (Preparo, laço)", True),
    ("trovao_dos_deuses", trovao_dos_deuses, GRANDE, "Raiden · a tempestade inteira", False),
    ("postura_mishima", postura_mishima, GRANDE, "Jin · a guarda e o brilho", False),
    ("contra_ataque", contra_ataque, GRANDE, "Jin · o aparo e o chute", False),
    ("gene_do_diabo", gene_do_diabo, GRANDE, "Jin · as asas e o raio da testa", False),
    ("pisao_demoniaco", pisao_demoniaco, GRANDE, "Kazuya · o pisão e os raios roxos", False),
    ("raio_do_diabo", raio_do_diabo, GRANDE, "Kazuya · o laser da testa", False),
    ("kazuya_preparo", kazuya_preparo, MEDIA, "Kazuya · os raios subindo (Preparo, laço)", True),
    ("forma_devil", forma_devil, GRANDE, "Kazuya · as asas do Devil e o golpe", False),
    ("cura_sora", cura_sora, GRANDE, "Sora · a flor e as folhas", False),
    ("sora_preparo", sora_preparo, MEDIA, "Sora · a coroa e a chave girando (Preparo, laço)", True),
    ("forma_final", forma_final, GRANDE, "Sora · as duas chaves-espada", False),
    ("lamina_virtuosa", lamina_virtuosa, GRANDE, "2B · o giro com as fitas", False),
    ("apoio_do_pod", apoio_do_pod, GRANDE, "2B · a rajada do Pod", False),
    ("modo_berserk", modo_berserk, GRANDE, "2B · a aura e a espada grande", False),
]
