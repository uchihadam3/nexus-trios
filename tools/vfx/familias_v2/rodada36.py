"""Rodada 36 das habilidades próprias: Bebop, Esqueleto, She-Ra, Lion-O, Cheetara, Homer e Bart.

Bebop
- investida_de_javali: as presas de javali vindo de cabeça baixa, a poeira e o tranco (Preso).
- pancada_do_bebop: o soco pesado e as placas de metal cobrindo o próprio corpo (Escudo e Fortalecido).
- bebop_preparo: o Preparo do Atropelo — o bufo de vapor pelo nariz e as patadas no chão (laço).
- atropelo: a manada de pisadas atravessando todos os rivais e a onda de poeira (Preso).

Esqueleto
- maldicao_do_esqueleto: a caveira verde de fumaça em cima do rival e as correntes de runas (Silenciado e Amaldiçoado).
- esqueleto_preparo: o Preparo do Domínio de Snake Mountain — o Cajado da Caveira brilhando roxo (laço).
- dominio_de_snake_mountain: a montanha da serpente no fundo e os raios verdes caindo em todos (Silenciado e Enfraquecido).

She-Ra
- espada_protetora: a Espada da Proteção com a joia, o corte dourado e o brilho (Fortalecido).
- pela_honra_de_grayskull: a espada erguida, os raios de luz em leque e o escudo no trio (Escudo, Fortalecido e Reviver).
- shera_preparo: o Preparo do Golpe da Princesa — a espada no alto e as faíscas em espiral (laço).
- golpe_da_princesa: o voo com as asas de luz e o chute no rival (Exposto).

Lion-O
- visao_alem_do_alcance: o Olho de Thundera na espada acendendo e o feixe atravessando o rival (Atrasa o Preparo).
- liono_preparo: o Preparo do Thunder, Thunder! — a espada crescendo e o olho vermelho piscando (laço).
- thunder_thunder: o símbolo do gato no céu, os raios e o golpe enorme (Exposto e Fortalecido no trio).

Cheetara
- bastao_giratorio: o bastão girando num disco e as batidas (Marcado e Exposto).
- corrida_felina: o risco amarelo com as pintas de guepardo passando por todos (Lento).
- cheetara_preparo: o Preparo do Golpe certeiro — o bastão esticado e o foco (laço).
- golpe_certeiro_cheetara: a estocada reta do bastão num ponto e a estrela do acerto (Interrompe o Preparo).

Homer
- barriga_de_aco: a barrigada que empurra o ar e a energia guardando (Guarda energia).
- rosquinha: a rosquinha com granulado, a mordida e a vida voltando (Vida e Guarda energia).
- homer_preparo: o Preparo do D'oh! — a energia guardada pulsando e o vapor de raiva (laço).
- d_oh: o balão "D'oh!" estourando e a energia guardada solta no rival (Exposto).

Bart
- provocacao_do_bart: a pichação "El Barto" em rabiscos no ar e o rival irritado (Atrasa e Provocado).
- travessura_maxima: a fileira de bombinhas estourando em sequência e a explosão final (Exposto).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, ESPADA, GEMA, anel, aura, cheio, circulo, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


def _poeira(T, cx, cy, s, k, seed=3, n=10):
    q = np.random.default_rng(seed)
    pts = [(cx + q.normal(0, s), cy + q.normal(0, s * 0.6), k * q.uniform(0.4, 1.0)) for _ in range(n)]
    return T.splats(pts, s * 0.7)


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


def _caveira(T, cx, cy, s, k):
    """A caveira: o crânio, os olhos e os dentes."""
    if k <= 0:
        return 0.0, 0.0
    cranio = [(cx + s * math.cos(a), cy - s * 0.15 + s * 0.85 * math.sin(a)) for a in np.linspace(math.pi, TAU, 16)]
    cranio += [(cx + s * 0.8, cy + s * 0.4), (cx + s * 0.5, cy + s * 0.75), (cx - s * 0.5, cy + s * 0.75), (cx - s * 0.8, cy + s * 0.4)]
    g, h = icone(T, cranio, k * 1.1, 0.4)
    for lado in (-1, 1):
        g2, h2 = cheio(T, poe(circulo(12), cx + lado * s * 0.38, cy - s * 0.05, s * 0.22), k * 0.6)
        g, h = g - g2 * 0.6, h + T.gauss(cx + lado * s * 0.38, cy - s * 0.05, s * 0.08) * k * 2.0
    g = g + T.lines([(cx - s * 0.4 + s * 0.2 * m, cy + s * 0.5, cx - s * 0.4 + s * 0.2 * m, cy + s * 0.72, 1.0) for m in range(5)], s * 0.04) * k * 1.1
    return g, h


# ------------------------------------------------------------------ Bebop

def _presas(T, cx, cy, s, k):
    G = 0.0
    for lado in (-1, 1):
        pts = [(cx, cy + lado * s * 0.25), (cx + s * 0.5, cy + lado * s * 0.35), (cx + s * 0.85, cy + lado * s * 0.1)]
        G = G + T.polyline(pts, s * 0.08) * k * 1.3
    return G


def investida_de_javali(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.6)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        x = -0.85 + 1.1 * u
        G += T.gauss(x, 0.0, 0.2, 0.15) * k * 0.9
        G += _presas(T, x + 0.08, 0.0, 0.45, k)
        H += T.gauss(x + 0.05, -0.05, 0.02) * k * 1.4
        G += _poeira(T, x - 0.25, 0.25, 0.08, k, int(t * 20), 10) * 0.9
        G += T.tapered([(x - 0.7, 0.0, x - 0.15, 0.0, 1.0)], 0.1) * k * 0.6
    g, h = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.3, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.8, 0.7, 0.35, 1.4)
    G += estouro(T, t, 0.3, 0.8, 14, 4, 0.45, 0.0, 0.5, 0.014)
    return G * env, H * env


def pancada_do_bebop(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.4, 0.55)
    if k > 0:
        P, nos = _punho(T, -0.5 + 0.95 * u, 0.0, 3.0, 0)
        G += P * 0.95 * k
        H += nos * 0.45 * k
    g, h = clarao(T, t, 0.22, 0.42, 0.5, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    for j in range(6):
        a = TAU * j / 6 + 0.3
        s = surge(t, 0.4 + 0.04 * j, 0.6 + 0.04 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            cx, cy = -0.35 + 0.3 * math.cos(a), 0.0 + 0.3 * math.sin(a)
            placa = [(cx - 0.09 * s, cy - 0.07 * s), (cx + 0.09 * s, cy - 0.07 * s), (cx + 0.08 * s, cy + 0.07 * s), (cx - 0.08 * s, cy + 0.07 * s)]
            g2, h2 = icone(T, placa, 1.1, 0.5)
            G, H = G + g2, H + h2
            H += T.gauss(cx - 0.05 * s, cy - 0.03 * s, 0.01) * 1.5
    g3, h3 = aura(T, t, 0.45, 1.0, 0.35, 0.0, 0.6)
    return (G + g3 * 0.5) * env, (H + h3 * 0.5) * env


def bebop_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        u = ((t * 2) + (0.5 if lado > 0 else 0)) % 1
        G += _poeira(T, lado * (0.1 + 0.2 * u), -0.05 - 0.05 * u, 0.04 + 0.04 * u, 1 - u, int(t * 2) + (lado > 0), 6) * 0.8
    pis = abs(math.sin(t * TAU * 2))
    G += onda_no_chao(T, (t * 2) % 1, 0.0, 1.0, 0.5, 0.3, 1.0)
    G += T.gauss(0, 0.05, 0.15) * (0.4 + 0.2 * pis)
    G += _presas(T, -0.1, 0.05, 0.25, 1.0)
    return G, H


def atropelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.75)
    for j in range(14):
        v = j / 13
        if v > u:
            break
        x = -0.9 + 1.8 * v
        y = 0.32 + (0.05 if j % 2 else -0.04)
        k = 1 - rel(t, 0.6 + 0.02 * j, 0.85 + 0.01 * j)
        for lado in (-1, 1):
            G += T.gauss(x + lado * 0.025, y, 0.02, 0.03) * k * 1.3
    if 0 < u < 1:
        x = -0.9 + 1.8 * u
        G += _poeira(T, x - 0.1, 0.1, 0.12, 1.0, int(t * 15), 16) * 0.7
        G += T.gauss(x, 0.0, 0.15, 0.2) * 0.8
    for x in (-0.55, 0.0, 0.55):
        g, h = clarao(T, t, 0.15 + 0.3 * (x + 0.9) / 1.8, 0.3 + 0.3 * (x + 0.9) / 1.8, x, 0.05, 0.55)
        G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.95, 1.0, 0.35, 1.4)
    return G * env, H * env


# ------------------------------------------------------------------ Esqueleto

def maldicao_do_esqueleto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.05, 0.85)
    q = np.random.default_rng(int(t * 12))
    pts = [(0.45 + q.normal(0, 0.12), -0.2 + q.normal(0, 0.1) - 0.15 * rel(t, 0.0, 0.9), k * q.uniform(0.3, 0.8)) for _ in range(18)]
    G += T.splats(pts, 0.06) * 0.5
    s = surge(t, 0.1, 0.35) * (1 - rel(t, 0.8, 0.92))
    g, h = _caveira(T, 0.45, -0.35, 0.18 * s, 1.0 if s > 0 else 0)
    G, H = G + g, H + h
    for j in range(2):
        u = rel(t, 0.35 + 0.1 * j, 0.95)
        if 0 < u < 1:
            a0 = t * 3 + j * math.pi
            G += T.arc_band(0.24, 0.022, a0, a0 + 4.5 * min(1, u * 2), 0.45, 0, 0.45, 0.1, 0.0) * (1 - rel(u, 0.8, 1)) * 1.3
            for m in range(6):
                a = a0 + 0.7 * m
                G += T.gauss(0.45 + 0.24 * math.cos(a), 0.1 + 0.24 * 0.45 * math.sin(a), 0.016) * (1 - rel(u, 0.8, 1)) * 1.3
    g2, h2 = clarao(T, t, 0.35, 0.55, 0.45, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


_CABECA_DE_CARNEIRO = [(-0.45, -0.3), (-0.2, -0.55), (0.2, -0.55), (0.45, -0.3), (0.35, 0.25), (0.15, 0.55), (-0.15, 0.55), (-0.35, 0.25)]


def esqueleto_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(0.0, -0.1, 0.0, 0.55, 1.0)], 0.025) * 1.1
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = icone(T, poe(_CABECA_DE_CARNEIRO, 0.0, -0.25, 0.22), 1.1 + 0.3 * b, 0.5)
    G, H = G + g, H + h
    for lado in (-1, 1):
        G += T.arc_band(0.1, 0.025, 0, math.pi * 1.4, 1.0, lado * 0.3, lado * 0.13, -0.32, 0.6) * 1.2
        H += T.gauss(lado * 0.06, -0.25, 0.015) * (1.5 + b)
    G += T.gauss(0, -0.25, 0.3) * (0.35 + 0.2 * b)
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 8, int(t * 2), 0.0, -0.25, 0.35)
    return G, H


def dominio_de_snake_mountain(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    if s > 0:
        monte = [(-0.95, 0.35), (-0.45, -0.25 * s - 0.05), (-0.2, -0.55 * s), (0.05, -0.3 * s - 0.05), (0.5, 0.35)]
        G += T.polyline(monte, 0.015) * 1.0
        G += T.polys([(monte, 1.0)], 0.02) * 0.25
        cobra = [(-0.2 + 0.2 * math.sin(v * 9) * (1 - v), -0.55 * s + 0.75 * v * s) for v in np.linspace(0, 1, 24)]
        G += T.polyline(cobra, 0.025) * 1.2
        H += T.gauss(-0.2, -0.55 * s, 0.02) * s * 2.0
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.35 + 0.08 * j, 0.6 + 0.08 * j)
        if k > 0:
            g, h = _raio(T, t, x + 0.1, -1.0, x, 0.05, k, 0.018, j)
            G, H = G + g, H + h
        g2, h2 = clarao(T, t, 0.42 + 0.08 * j, 0.62 + 0.08 * j, x, 0.05, 0.6)
        G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.35, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ She-Ra

def espada_protetora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.55))
    if s > 0:
        g, h = icone(T, poe(ESPADA, -0.3, -0.2, 0.45 * s, 0.3), 1.2, 0.5)
        G, H = G + g, H + h
        g2, h2 = cheio(T, poe(GEMA, -0.3 - 0.06 * s, -0.2 + 0.18 * s, 0.05 * s), 1.4)
        G, H = G + g2, H + h2 * 2
    g3, h3 = corte(T, t, 0.3, 0.6, -0.5, 1.5, 0.1, 0.35, 0.0, 0.1)
    G, H = G + g3 * 1.2, H + h3
    g4, h4 = clarao(T, t, 0.4, 0.6, 0.4, 0.0, 1.1, 1.2)
    G, H = G + g4, H + h4
    G += particulas(T, t, 0.45, 1.0, 18, 6, 0.4, 0.0, 0.35, 0.5, 0.012)
    return G * env, H * env


def pela_honra_de_grayskull(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.75, 0.9))
    if s > 0:
        g, h = icone(T, poe(ESPADA, 0, -0.45, 0.4 * s, 0), 1.2, 0.5)
        G, H = G + g, H + h
        H += T.gauss(0, -0.8, 0.04) * s * 2.0
    k = pulso(t, 0.2, 0.85)
    if k > 0:
        for j in range(9):
            a = -math.pi / 2 + (j - 4) * 0.3
            G += T.tapered([(0, -0.8, 0.9 * math.cos(a), -0.8 + 0.9 * math.sin(a) + 0.9, 1.0)], 0.035) * k * 0.6
    for x in (-0.55, 0.0, 0.55):
        w = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
        if w > 0:
            G += T.arc_band(0.22 * w, 0.03, -2.6, -0.5, 1.0, 0, x, 0.25, 0.0) * 1.2
            G += T.gauss(x, 0.1, 0.15, 0.2) * w * 0.4
    G += particulas(T, t, 0.4, 1.0, 20, 4, 0, 0.1, 0.8, 0.6, 0.012)
    return G * env, H * env


def shera_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(ESPADA, 0, -0.05, 0.5, 0), 1.1, 0.5)
    G, H = G + g, H + h
    g2, h2 = cheio(T, poe(GEMA, 0, 0.35, 0.05), 1.4)
    G, H = G + g2, H + h2 * 2
    for j in range(8):
        a = t * TAU + TAU * j / 8
        r = 0.15 + 0.25 * ((t + j / 8) % 1)
        g3, h3 = cheio(T, poe(estrela_pts(4, 0.35), r * math.cos(a), -0.3 + r * 0.6 * math.sin(a), 0.03), 1.2)
        G, H = G + g3, H + h3
    H += T.gauss(0, -0.55, 0.03) * (1.4 + 0.6 * math.sin(t * 10))
    return G, H


def golpe_da_princesa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        x = -0.8 + 1.15 * u
        y = -0.3 + 0.3 * u
        for lado in (-1, 1):
            asa = [(-x0, lado * y0) for x0, y0 in ASA]
            g, h = icone(T, poe(asa, x - 0.1, y, 0.22), k * 1.0, 0.45)
            G, H = G + g, H + h
        G += T.tapered([(x - 0.5, y - 0.15, x + 0.1, y, 1.0)], 0.08) * k * 1.0
        H += T.gauss(x + 0.1, y, 0.03) * k * 1.6
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.4, 0.0, 1.4, 1.4)
    G, H = G + g2, H + h2
    w = rel(t, 0.35, 0.8)
    if 0 < w < 1:
        G += T.ring(0.05 + 0.55 * ease_out(w, 2), 0.04 * (1 - 0.5 * w), 0.4, 0.0) * (1 - w) * 1.3
    G += particulas(T, t, 0.35, 1.0, 16, 8, 0.4, 0.0, 0.4, 0.5, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Lion-O

def _olho(T, cx, cy, s, k):
    if k <= 0:
        return 0.0, 0.0
    olho = [(cx + s * math.cos(a), cy + s * 0.45 * math.sin(a) * (1 if math.sin(a) > 0 else 1)) for a in np.linspace(0, TAU, 24, endpoint=False)]
    g, h = icone(T, olho, k * 1.1, 0.4)
    g2, h2 = cheio(T, poe(circulo(14), cx, cy, s * 0.35), k * 1.3)
    return g + g2, h + h2 + T.gauss(cx, cy, s * 0.12) * k * 2.0


def visao_alem_do_alcance(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.75, 0.9))
    g, h = _olho(T, -0.5, -0.1, 0.16 * s, 1.0 if s > 0 else 0)
    G, H = G + g, H + h
    k = pulso(t, 0.25, 0.7)
    if k > 0:
        G += T.tapered([(-0.5, -0.1, 0.55, 0.0, 1.0)], 0.06 * k + 0.01) * 1.3
        H += T.lines([(-0.5, -0.1, 0.55, 0.0, 1.0)], 0.012) * k * 1.6
    g2, h2 = clarao(T, t, 0.3, 0.6, 0.55, 0.0, 1.0)
    G, H = G + g2, H + h2
    w = rel(t, 0.4, 0.95)
    if 0 < w < 1:
        G += T.arc_band(0.18, 0.025, -math.pi / 2, -math.pi / 2 + TAU * (1 - w), 1.0, 0, 0.55, 0.0, 0.0) * 1.3
    return G * env, H * env


def liono_preparo(T, t, rng):
    G, H = vazio(T)
    cresce = 0.35 + 0.15 * ((t * 1.5) % 1)
    g, h = icone(T, poe(ESPADA, 0, 0.0, cresce, 0), 1.1, 0.5)
    G, H = G + g, H + h
    pis = 0.5 + 0.5 * math.sin(t * TAU * 3)
    g2, h2 = _olho(T, 0, cresce * 0.55, 0.06, 1.0 + pis * 0.5)
    G, H = G + g2, H + h2
    G += T.gauss(0, 0, 0.3) * (0.3 + 0.2 * pis)
    return G, H


_GATO = [(-0.8, 0.0), (-0.6, -0.8), (-0.25, -0.35), (0.25, -0.35), (0.6, -0.8), (0.8, 0.0), (0.5, 0.55), (0.0, 0.75), (-0.5, 0.55)]


def thunder_thunder(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        G += T.ring(0.3 * s, 0.03, 0.0, -0.55) * 1.3
        g, h = icone(T, poe(_GATO, 0.0, -0.55, 0.22 * s), 1.1, 0.5)
        G, H = G + g, H + h
        G += T.gauss(0, -0.55, 0.35 * s) * 0.4
    for j in range(3):
        k = pulso(t, 0.3 + 0.06 * j, 0.55 + 0.06 * j)
        if k > 0:
            g2, h2 = _raio(T, t, 0.0 + 0.1 * (j - 1), -0.3, 0.45 + 0.08 * (j - 1), 0.05, k, 0.02, j)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.4, 0.65, 0.45, 0.05, 1.5, 1.5)
    G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.42, 0.95, 1.0, 0.35, 1.6)
    G += estouro(T, t, 0.42, 0.95, 18, 5, 0.45, 0.05, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Cheetara

def _bastao(T, cx, cy, a, comp, k):
    return T.lines([(cx - comp * math.cos(a), cy - comp * math.sin(a), cx + comp * math.cos(a), cy + comp * math.sin(a), 1.0)], 0.04) * k * 1.4


def bastao_giratorio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.7)
    a = t * 30
    x = -0.3 + 0.55 * ease_out(rel(t, 0.0, 0.3))
    G += _bastao(T, x, 0.0, a, 0.3, k)
    G += T.ring(0.3, 0.04, x, 0.0) * k * 0.5
    for j in range(4):
        g, h = clarao(T, t, 0.25 + 0.1 * j, 0.33 + 0.1 * j, x + 0.3, -0.1 + 0.07 * j, 0.45)
        G, H = G + g, H + h
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.018, 0.55, 0.0) * 1.3 + T.ring(0.07 * m, 0.012, 0.55, 0.0) * 1.2
    return G * env, H * env


def corrida_felina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.3)
    k = 1 - rel(t, 0.55, 0.75)
    if u > 0 and k > 0:
        x = -0.95 + 1.9 * u
        G += T.tapered([(-0.95, 0.05, x, 0.05, 1.0)], 0.13) * k * 1.0
        q = np.random.default_rng(5)
        for _ in range(int(14 * u) + 1):
            px = q.uniform(-0.95, x)
            G += T.ring(0.02, 0.007, px, 0.05 + q.uniform(-0.06, 0.06)) * k * 1.2
        H += T.gauss(x, 0.05, 0.03) * k * 1.5
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        g, h = clarao(T, t, 0.1 + 0.1 * j, 0.25 + 0.1 * j, x, 0.05, 0.55)
        G, H = G + g, H + h
    G += particulas(T, t, 0.3, 0.9, 16, 3, 0, 0.1, 0.8, 0.3, 0.012)
    return G * env, H * env


def cheetara_preparo(T, t, rng):
    G, H = vazio(T)
    G += _bastao(T, 0.0, 0.0, 0.0, 0.45, 1.0)
    u = (t * 2) % 1
    H += T.gauss(-0.45 + 0.9 * u, 0.0, 0.02) * 2.0
    G += T.ring(0.15 + 0.1 * math.sin(t * 8), 0.012, 0.45, 0.0) * 1.0
    G += T.gauss(0, 0, 0.25) * (0.3 + 0.15 * math.sin(t * 10))
    return G, H


def golpe_certeiro_cheetara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.2), 2)
    k = 1 - rel(t, 0.4, 0.55)
    if k > 0:
        xe = -0.4 + 0.8 * u
        G += _bastao(T, xe - 0.35, 0.0, 0.0, 0.35, k)
        G += T.tapered([(-0.9, 0.0, xe - 0.6, 0.0, 1.0)], 0.06) * k * 0.6
    g, h = clarao(T, t, 0.18, 0.4, 0.4, 0.0, 1.4, 1.5)
    G, H = G + g, H + h
    s = surge(t, 0.2, 0.4) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g2, h2 = icone(T, poe(estrela_pts(4, 0.25), 0.4, 0.0, 0.25 * s, 0.4), 1.3, 0.6)
        G, H = G + g2, H + h2
    w = rel(t, 0.2, 0.7)
    if 0 < w < 1:
        G += T.ring(0.05 + 0.45 * ease_out(w, 2), 0.035 * (1 - 0.5 * w), 0.4, 0.0) * (1 - w) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Homer

def _energia(T, t, cx, cy, s, k):
    """A bolinha de energia guardada (que enche)."""
    if k <= 0:
        return 0.0, 0.0
    G = T.ring(s, s * 0.15, cx, cy) * k * 1.2
    G = G + T.gauss(cx, cy, s * 0.7) * k * (0.8 + 0.2 * math.sin(t * 14))
    return G, T.gauss(cx, cy, s * 0.3) * k * 1.6


def barriga_de_aco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        G += T.arc_band(0.25 + 0.05 * u, 0.06, -1.3, 1.3, 1.0, 0, -0.35 + 0.35 * u, 0.1, 0.0) * k * 1.2
        G += T.gauss(-0.3 + 0.35 * u, 0.1, 0.2, 0.25) * k * 0.6
    for j in range(3):
        w = rel(t, 0.25 + 0.06 * j, 0.6 + 0.06 * j)
        if 0 < w < 1:
            G += T.arc_band(0.3 + 0.4 * w, 0.025, -0.8, 0.8, 1.0, 0, -0.1, 0.1, 0.0) * (1 - w) * 1.2
    g, h = clarao(T, t, 0.28, 0.45, 0.45, 0.1, 0.9)
    G, H = G + g, H + h
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.9, 1))
    g2, h2 = _energia(T, t, -0.45, -0.45, 0.08 * s, 1.0 if s > 0 else 0)
    G += converge(T, t, 0.45, 0.85, 10, 3, -0.45, -0.45, 0.35)
    return (G + g2) * env, (H + h2) * env


def _rosquinha(T, cx, cy, s, k, mordida=0.0):
    g, h = icone(T, poe(circulo(28), cx, cy, s), k * 1.1, 0.5)
    g = g - T.gauss(cx, cy, s * 0.3) * k * 0.6
    g = g + T.ring(s * 0.62, s * 0.3, cx, cy) * k * 0.5
    q = np.random.default_rng(3)
    granulado = []
    for _ in range(14):
        a, r = q.uniform(0, TAU), q.uniform(0.45, 0.85) * s
        b = q.uniform(0, math.pi)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        granulado.append((x - 0.06 * s * math.cos(b), y - 0.06 * s * math.sin(b), x + 0.06 * s * math.cos(b), y + 0.06 * s * math.sin(b), 1.0))
    g = g + T.lines(granulado, s * 0.05) * k * 1.4
    if mordida > 0:
        for m in range(3):
            g = g - T.gauss(cx + s * 0.9, cy - s * 0.3 + s * 0.3 * m, s * 0.22) * mordida * 2
    return g, h


def rosquinha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.65, 0.8))
    if s > 0:
        g, h = _rosquinha(T, 0.0, -0.2, 0.2 * s, 1.0, rel(t, 0.35, 0.45))
        G, H = G + g, H + h
    for j in range(5):
        w = rel(t, 0.4 + 0.03 * j, 0.8)
        if 0 < w < 1:
            a = -0.3 + 0.3 * j
            G += T.gauss(0.2 + 0.2 * w * math.cos(a), -0.25 + 0.3 * w * w, 0.012) * (1 - w) * 1.4
    g2, h2 = aura(T, t, 0.5, 1.0, 0.35, 0.0, 0.9)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.55, 0.95, 0.1, 0.6, 0.03, 0.0)
    s2 = surge(t, 0.6, 0.8) * (1 - rel(t, 0.9, 1))
    g3, h3 = _energia(T, t, -0.45, -0.45, 0.1 * s2, 1.0 if s2 > 0 else 0)
    return (G + g3) * env, (H + h3) * env


def homer_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = _energia(T, t, 0.0, 0.05, 0.13 * (1 + 0.15 * b), 1.0)
    G, H = G + g, H + h
    for lado in (-1, 1):
        u = ((t * 2) + (0.5 if lado > 0 else 0)) % 1
        G += _poeira(T, lado * (0.15 + 0.1 * u), -0.25 - 0.2 * u, 0.03 + 0.03 * u, 1 - u, int(t * 2), 5) * 0.9
    return G, H


def d_oh(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.38, 0.45))
    if s > 0:
        balao = [((0.3 + 0.07 * (j % 2)) * s * math.cos(TAU * j / 16), -0.25 + (0.2 + 0.05 * (j % 2)) * s * math.sin(TAU * j / 16)) for j in range(16)]
        g, h = icone(T, [(x - 0.35, y) for x, y in balao], 1.2, 0.4)
        G, H = G + g, H + h
        G += T.ring(0.07 * s, 0.02, -0.45, -0.25) * 1.3
        G += T.lines([(-0.32, -0.32 * s - 0.0, -0.32, -0.18, 1.0), (-0.22, -0.32, -0.22, -0.18, 1.0)], 0.018) * s * 1.2
    u = ease_in(rel(t, 0.3, 0.5), 1.5)
    if 0 < u < 1:
        x = -0.35 + 0.9 * u
        G += T.gauss(x, 0.0, 0.1 + 0.05 * u) * 1.4
        H += T.gauss(x, 0.0, 0.04) * 1.8
        G += T.tapered([(x - 0.4, 0.0, x, 0.0, 1.0)], 0.1) * 0.9
    g2, h2 = clarao(T, t, 0.48, 0.7, 0.55, 0.0, 1.6, 1.5)
    G, H = G + g2, H + h2
    for j in range(2):
        w = rel(t, 0.5 + 0.08 * j, 0.95)
        if 0 < w < 1:
            G += T.ring(0.06 + 0.6 * ease_out(w, 2), 0.04 * (1 - 0.5 * w), 0.55, 0.0) * (1 - w) * 1.3
    G += estouro(T, t, 0.5, 0.95, 18, 6, 0.55, 0.0, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Bart

def provocacao_do_bart(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.55)
    if u > 0:
        letras = []
        q = np.random.default_rng(8)
        for j in range(7):
            x0 = -0.2 + 0.13 * j
            pts = [(x0 + 0.06 * math.sin(m * 1.7 + j), -0.35 + 0.1 * math.cos(m * 2.3 + j * 3) + 0.02 * q.normal()) for m in range(6)]
            letras.append(pts)
        n = int(len(letras) * min(1, u * 1.2)) + 1
        for pts in letras[:n]:
            G += T.polyline(pts, 0.018) * (1 - rel(t, 0.88, 1)) * 1.3
        G += T.lines([(-0.25, -0.18, 0.7, -0.2, 1.0)], 0.01) * min(1, u * 1.5) * (1 - rel(t, 0.88, 1)) * 1.0
    for j in range(6):
        w = rel(t, 0.1 + 0.05 * j, 0.6 + 0.05 * j)
        if 0 < w < 1:
            G += T.gauss(-0.55 + 0.6 * w, -0.3 + 0.05 * math.sin(j * 3) - 0.1 * w, 0.012) * (1 - w) * 1.4
    g, h = clarao(T, t, 0.5, 0.7, 0.45, 0.1, 0.7)
    G, H = G + g, H + h
    s = surge(t, 0.6, 0.8) * (1 - rel(t, 0.9, 1))
    if s > 0:
        for lado in (-1, 1):
            G += T.lines([(0.45 + lado * 0.04, 0.05, 0.45 + lado * 0.1 * s, -0.05, 1.0)], 0.015) * 1.3
    return G * env, H * env


def travessura_maxima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(6):
        x = -0.5 + 0.18 * j
        a0 = 0.05 + 0.06 * j
        s = surge(t, 0.0, 0.15) * (1 - rel(t, a0 + 0.1, a0 + 0.12))
        if s > 0:
            g, h = icone(T, [(x - 0.03, 0.3), (x + 0.03, 0.3), (x + 0.03, 0.15), (x - 0.03, 0.15)], s * 1.1, 0.5)
            G, H = G + g, H + h
            H += T.gauss(x, 0.12, 0.012) * 2.0
        g2, h2 = clarao(T, t, a0 + 0.1, a0 + 0.2, x, 0.2, 0.35)
        G, H = G + g2, H + h2
        G += estouro(T, t, a0 + 0.1, a0 + 0.35, 6, j, x, 0.2, 0.15, 0.01)
    g3, h3 = clarao(T, t, 0.48, 0.7, 0.55, 0.05, 1.5, 1.5)
    G, H = G + g3, H + h3
    G += estouro(T, t, 0.5, 0.95, 18, 9, 0.55, 0.05, 0.6, 0.014)
    w = rel(t, 0.5, 0.95)
    if 0 < w < 1:
        G += T.ring(0.06 + 0.55 * ease_out(w, 2), 0.04 * (1 - 0.5 * w), 0.55, 0.05) * (1 - w) * 1.3
    G += raios(T, t, 0.5, 0.8, 5, 4, 0.55, 0.05, 0.35, 0.01)
    return G * env, H * env


REGISTRO = [
    ("investida_de_javali", investida_de_javali, GRANDE, "Bebop · as presas de javali e a poeira", False),
    ("pancada_do_bebop", pancada_do_bebop, GRANDE, "Bebop · o soco e as placas de metal", False),
    ("bebop_preparo", bebop_preparo, MEDIA, "Bebop · o bufo e as patadas (Preparo, laço)", True),
    ("atropelo", atropelo, GRANDE, "Bebop · as pisadas atravessando todos", False),
    ("maldicao_do_esqueleto", maldicao_do_esqueleto, GRANDE, "Esqueleto · a caveira verde e as correntes", False),
    ("esqueleto_preparo", esqueleto_preparo, MEDIA, "Esqueleto · o Cajado da Caveira brilhando (Preparo, laço)", True),
    ("dominio_de_snake_mountain", dominio_de_snake_mountain, GRANDE, "Esqueleto · a montanha da serpente e os raios", False),
    ("espada_protetora", espada_protetora, GRANDE, "She-Ra · a espada com a joia e o corte dourado", False),
    ("pela_honra_de_grayskull", pela_honra_de_grayskull, GRANDE, "She-Ra · a espada erguida e a luz no trio", False),
    ("shera_preparo", shera_preparo, MEDIA, "She-Ra · a espada e as faíscas em espiral (Preparo, laço)", True),
    ("golpe_da_princesa", golpe_da_princesa, GRANDE, "She-Ra · as asas de luz e o chute", False),
    ("visao_alem_do_alcance", visao_alem_do_alcance, GRANDE, "Lion-O · o Olho de Thundera e o feixe", False),
    ("liono_preparo", liono_preparo, MEDIA, "Lion-O · a espada crescendo e o olho (Preparo, laço)", True),
    ("thunder_thunder", thunder_thunder, GRANDE, "Lion-O · o símbolo do gato, os raios e o golpe", False),
    ("bastao_giratorio", bastao_giratorio, GRANDE, "Cheetara · o bastão girando", False),
    ("corrida_felina", corrida_felina, GRANDE, "Cheetara · o risco com as pintas de guepardo", False),
    ("cheetara_preparo", cheetara_preparo, MEDIA, "Cheetara · o bastão esticado (Preparo, laço)", True),
    ("golpe_certeiro_cheetara", golpe_certeiro_cheetara, GRANDE, "Cheetara · a estocada reta e a estrela", False),
    ("barriga_de_aco", barriga_de_aco, GRANDE, "Homer · a barrigada e a energia guardando", False),
    ("rosquinha", rosquinha, GRANDE, "Homer · a rosquinha com granulado e a mordida", False),
    ("homer_preparo", homer_preparo, MEDIA, "Homer · a energia pulsando e o vapor (Preparo, laço)", True),
    ("d_oh", d_oh, GRANDE, "Homer · o balão D'oh! e a energia solta", False),
    ("provocacao_do_bart", provocacao_do_bart, GRANDE, "Bart · a pichação no ar", False),
    ("travessura_maxima", travessura_maxima, GRANDE, "Bart · as bombinhas e a explosão", False),
]
