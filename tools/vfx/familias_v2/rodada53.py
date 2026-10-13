"""Rodada 53 das habilidades próprias: Luke, Palpatine, Neo, Agente Smith, John Wick e T-800.

Luke Skywalker
- sabre_verde_luke: o sabre verde ligando e o corte em arco.
- defletir: o sabre girando na frente e os tiros vermelhos voltando (Refletir e Protegido).
- luke_preparo: o Preparo do Tiro na trincheira — a mira do X-Wing travando e a voz "use a Força" (laço).
- tiro_na_trincheira: os dois torpedos de prótons fazendo a curva e entrando no alvo.

Palpatine
- raio_da_forca_palpatine: os relâmpagos azuis saindo dos dedos e prendendo o rival (Eletrificado).
- tudo_conforme_o_plano: o capuz no escuro, o sorriso e as peças caindo nos rivais (Enfraquecido).
- palpatine_preparo: o Preparo do Poder ilimitado — as mãos erguidas e a eletricidade entre elas (laço).
- poder_ilimitado: a tempestade de relâmpagos das duas mãos em todos os rivais (Paralisado).

Neo
- kung_fu: a chuva de código verde e a sequência de golpes de kung fu.
- parar_as_balas: a mão erguida e as balas paradas no ar com as ondas, depois caindo (Esquiva e Refletir).
- neo_preparo: o Preparo do O escolhido — o código verde escorrendo em volta dele (laço).
- o_escolhido: o Neo vendo o código, mergulhando no rival e o rival se desfazendo em código (Dissipar).

Agente Smith
- soco_do_agente_smith: o soco reto com o terno e os óculos, o estalo do impacto.
- copias_do_smith: as cópias do Smith surgindo uma atrás da outra (Marcado e Invocação).
- smith_preparo: o Preparo do Assimilar — a mão escorrendo código preto-esverdeado (laço).
- assimilar: a mão no peito do rival e o código passando para o Smith (Copiar).

John Wick
- tiro_na_testa_wick: o tiro preciso, o clarão do cano e a mira na testa (Marcado).
- lapis: o lápis girando e cravando no rival.
- wick_preparo: o Preparo do Excomunicado — a moeda de ouro girando no ar (laço).
- excomunicado: a rajada de tiros, os cartuchos voando e o último tiro.

T-800
- escopeta_t800: a escopeta engatilhando e o tiro com os chumbos (Guarda energia).
- eu_voltarei: o endoesqueleto aparecendo e a placa de escudo de metal (Escudo e Guarda energia).
- t800_preparo: o Preparo do Hasta la vista — a mira vermelha da visão do Exterminador (laço).
- hasta_la_vista: a energia guardada indo toda num tiro gigante (Libera a energia).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao, particulas, poe, raios, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _sabre(T, x, y, ang, s, liga, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s * 0.22, y - sn * s * 0.22, x, y, 1.0)], s * 0.06) * k * 1.1
    if liga > 0:
        x2, y2 = x + c * s * liga, y + sn * s * liga
        G += T.tapered([(x, y, x2, y2, 1.0)], s * 0.09) * k * 0.8
        G += T.lines([(x, y, x2, y2, 1.0)], s * 0.035) * k * 1.4
        return G, T.lines([(x, y, x2, y2, 1.0)], s * 0.018) * k * 1.4
    return G, 0.0


def _codigo(T, t, x0, x1, y0, y1, n, k, seed, vel=1.5):
    """A chuva de código verde: colunas de traços curtos descendo."""
    q = np.random.default_rng(seed)
    segs = []
    for j in range(n):
        x = q.uniform(x0, x1)
        fase = q.uniform(0, 1)
        L = q.uniform(0.15, 0.35)
        cab = y0 + ((t * vel + fase) % 1) * (y1 - y0 + L)
        for m in range(5):
            y = cab - m * L / 5
            if y0 <= y <= y1:
                segs.append((x, y - 0.012, x, y + 0.012, (1 - m / 5)))
    return T.lines(segs, 0.006) * k * 1.3 if segs else 0.0


def _bala(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    pts = [(x + c * s, y + sn * s), (x + c * s * 0.4 - sn * s * 0.3, y + sn * s * 0.4 + c * s * 0.3),
           (x - c * s - sn * s * 0.3, y - sn * s + c * s * 0.3), (x - c * s + sn * s * 0.3, y - sn * s - c * s * 0.3),
           (x + c * s * 0.4 + sn * s * 0.3, y + sn * s * 0.4 - c * s * 0.3)]
    return cheio(T, pts, k)


def _mira(T, cx, cy, r, k, w=0.012):
    G = T.ring(r, w, cx, cy) * k * 1.2
    for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
        G += T.lines([(cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a), cx + r * 1.3 * math.cos(a), cy + r * 1.3 * math.sin(a), 1.0)], w * 0.8) * k * 1.3
    return G


def _oculos(T, cx, cy, s, k):
    G = 0.0
    for lado in (-1, 1):
        G = G + T.polys([([(cx + lado * s * 0.15, cy - s * 0.12), (cx + lado * s * 0.75, cy - s * 0.15), (cx + lado * s * 0.7, cy + s * 0.12),
                           (cx + lado * s * 0.2, cy + s * 0.15)], 1.0)], 0.003) * k * 1.3
    G = G + T.lines([(cx - s * 0.15, cy - s * 0.05, cx + s * 0.15, cy - s * 0.05, 1.0)], s * 0.05) * k
    return G


def _cabeca_terno(T, cx, cy, s, k):
    G, H = icone(T, poe([(math.cos(a) * 0.55, math.sin(a) * 0.7) for a in np.linspace(0, TAU, 20)], cx, cy, s), k, 0.4)
    G = G + _oculos(T, cx, cy - s * 0.1, s, k)
    terno = [(cx - s * 1.0, cy + s * 1.8), (cx - s * 0.9, cy + s * 0.9), (cx - s * 0.3, cy + s * 0.75), (cx, cy + s * 1.3), (cx + s * 0.3, cy + s * 0.75),
             (cx + s * 0.9, cy + s * 0.9), (cx + s * 1.0, cy + s * 1.8)]
    g2, h2 = icone(T, terno, k * 0.8, 0.3)
    return G + g2, H + h2


def _moeda(T, cx, cy, r, gira, k):
    sq = max(0.08, abs(math.cos(gira)))
    pts = [(cx + r * sq * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, TAU, 24)]
    g, h = icone(T, pts, k, 0.5)
    G = g
    if sq > 0.4:
        G = G + T.polyline([(cx + r * sq * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a)) for a in np.linspace(0, TAU, 20)], r * 0.06) * k * 1.0
    return G, h + T.gauss(cx - r * sq * 0.3, cy - r * 0.3, r * 0.2) * k * 1.2


def _cartucho(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    return cheio(T, [(x - c * s - sn * s * 0.4, y - sn * s + c * s * 0.4), (x + c * s - sn * s * 0.4, y + sn * s + c * s * 0.4),
                     (x + c * s + sn * s * 0.4, y + sn * s - c * s * 0.4), (x - c * s + sn * s * 0.4, y - sn * s - c * s * 0.4)], k)


def _escopeta(T, x, y, s, k):
    G = T.lines([(x - s * 0.3, y, x + s, y, 1.0)], s * 0.08) * k * 1.2
    G += T.lines([(x - s * 0.3, y + s * 0.07, x + s * 0.8, y + s * 0.07, 1.0)], s * 0.06) * k * 1.0
    G += T.polys([([(x - s * 0.3, y - s * 0.05), (x - s * 0.8, y + s * 0.05), (x - s * 0.8, y + s * 0.25), (x - s * 0.3, y + s * 0.12)], 1.0)], 0.003) * k * 1.0
    return G


def _cranio_metal(T, cx, cy, s, k):
    G, H = icone(T, poe([(-0.6, 0.2), (-0.65, -0.4), (-0.3, -0.85), (0.3, -0.85), (0.65, -0.4), (0.6, 0.2), (0.35, 0.6), (0.25, 0.85),
                         (-0.25, 0.85), (-0.35, 0.6)], cx, cy, s), k, 0.45)
    for lado in (-1, 1):
        G = G + T.ring(s * 0.16, s * 0.04, cx + lado * s * 0.27, cy - s * 0.15) * k * 1.0
        H = H + T.gauss(cx + lado * s * 0.27, cy - s * 0.15, s * 0.08) * k * 2.0
    for j in range(5):
        G = G + T.lines([(cx - s * 0.25 + s * 0.125 * j, cy + s * 0.55, cx - s * 0.25 + s * 0.125 * j, cy + s * 0.8, 1.0)], s * 0.03) * k * 1.0
    return G, H


# ------------------------------------------------------------------ Luke

def sabre_verde_luke(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    liga = ease_out(rel(t, 0.0, 0.18), 2)
    u = ease_in(rel(t, 0.2, 0.42), 2)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        ang = -2.3 + 2.6 * u
        g, h = _sabre(T, -0.05 + 0.05 * math.cos(ang), 0.25, ang, 0.6, liga, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.55, 0.06, ang - 1.0, ang, 1.0, 0, -0.05, 0.25, 1.0) * k * 0.7
    g2, h2 = corte(T, t, 0.33, 0.55, 0.6, 1.2, 0.08, 0.45, 0.0, 0.1)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.35, 0.58, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g3, H + h3
    G += estouro(T, t, 0.37, 0.8, 12, 146, 0.45, 0.0, 0.45, 0.011)
    return G * env, H * env


def defletir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.9)
    a = t * 22
    g, h = _sabre(T, 0.0, 0.0, a, 0.35, 1.0, k)
    G, H = G + g, H + h
    g2, h2 = _sabre(T, 0.0, 0.0, a + math.pi, 0.25, 1.0, k * 0.5)
    G, H = G + g2 * 0.6, H + h2 * 0.4
    G += T.ring(0.33, 0.008, 0.0, 0.0) * k * 0.8
    for j in range(3):
        a0 = 0.1 + 0.18 * j
        u = rel(t, a0, a0 + 0.15)
        w = rel(t, a0 + 0.15, a0 + 0.35)
        y = -0.15 + 0.15 * j
        if 0 < u < 1:
            x = 0.9 - 0.6 * u
            G += T.tapered([(x + 0.15, y, x, y, 1.0)], 0.02) * 1.4
            H += T.lines([(x + 0.1, y, x, y, 1.0)], 0.006) * 1.2
        if 0 < w < 1:
            x = 0.3 + 0.6 * w
            G += T.tapered([(x - 0.15, y - 0.1 * w, x, y - 0.15 * w, 1.0)], 0.02) * 1.4
            g3, h3 = clarao(T, w, 0.0, 0.3, 0.3, y, 0.15, 0.5)
            G, H = G + g3, H + h3
    return G * env, H * env


def luke_preparo(T, t, rng):
    G, H = vazio(T)
    trava = (t * 1.2) % 1
    r = 0.3 - 0.15 * ease_out(min(1.0, trava * 1.5), 2)
    G += _mira(T, 0.0, 0.0, r, 1.0, 0.012)
    G += T.lines([(-0.4, 0.0, -r - 0.05, 0.0, 1.0), (r + 0.05, 0.0, 0.4, 0.0, 1.0)], 0.004) * 0.8
    if trava > 0.66:
        H += T.gauss(0.0, 0.0, 0.03) * 1.8
        G += T.ring(0.17, 0.006, 0.0, 0.0) * 1.2
    return G, H


def tiro_na_trincheira(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(2):
        u = rel(t, 0.05 + 0.06 * j, 0.5 + 0.06 * j)
        if 0 < u < 1:
            e = ease_in(u, 1.2)
            x = -0.75 + 1.2 * e
            y = -0.3 + 0.1 * j - 0.35 * math.sin(math.pi * e) * (1 - e) + 0.3 * e * e
            H += T.gauss(x, y, 0.025) * 2.0
            G += T.gauss(x, y, 0.06) * 1.2
            G += T.tapered([(x - 0.3, y + 0.1 * (1 - e), x, y, 0.8)], 0.035) * 1.0
    g, h = clarao(T, t, 0.48, 0.78, 0.45, 0.0, 2.0, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.5, 0.95, 0.05, 0.8, 0.05, 0.0, 1.0, 1.5)
    G += estouro(T, t, 0.5, 0.95, 18, 147, 0.45, 0.0, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Palpatine

def _maos_raio(T, t, cx, cy, ang, k, alvo, seed, n=3, w=0.012):
    G = 0.0
    for j in range(n):
        tx, ty = alvo
        G = G + _zap(T, seed + int(t * 35) + 7 * j, cx, cy, tx + 0.05 * (j - 1), ty + 0.05 * (j - 1), w, 5, 0.25)
    return G * k


def raio_da_forca_palpatine(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.1, 0.75)
    if k > 0:
        for lado in (-1, 1):
            G += _maos_raio(T, t, -0.55, 0.05 * lado, 0.0, k * 1.3, (0.45, 0.0), 148 + (lado > 0), 3, 0.012)
            H += _maos_raio(T, t, -0.55, 0.05 * lado, 0.0, k * 0.8, (0.45, 0.0), 148 + (lado > 0), 1, 0.005)
        G += raios(T, t, 0.25, 0.85, 5, 150, 0.45, 0.0, 0.25, 0.008)
        G += T.gauss(0.45, 0.0, 0.15) * k * 0.4
    g, h = clarao(T, t, 0.3, 0.6, 0.45, 0.0, 1.0, 1.1)
    return (G + g) * env, (H + h) * env


def tudo_conforme_o_plano(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        capuz = [(0, -1), (0.6, -0.6), (0.8, 0.2), (0.6, 0.9), (-0.6, 0.9), (-0.8, 0.2), (-0.6, -0.6)]
        g, h = icone(T, poe(capuz, -0.55, -0.2, 0.3), s * 0.7, 0.25)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(-0.55 + lado * 0.05, -0.22, 0.012) * s * 2.2
        G += T.arc_band(0.07, 0.01, 0.4, math.pi - 0.4, 1.6, 0, -0.55, -0.12, 0.0) * s * 1.3 * pulso(t, 0.25, 0.85)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.35 + 0.06 * i, 0.6 + 0.06 * i)
        if 0 < u < 1:
            y = -0.7 + 0.6 * ease_in(u, 1.6)
            peca = [(-0.35, 0.6), (0.35, 0.6), (0.25, 0.35), (0.15, 0.3), (0.2, -0.1), (0.35, -0.4), (0.15, -0.75), (-0.15, -0.75), (-0.35, -0.4),
                    (-0.2, -0.1), (-0.15, 0.3), (-0.25, 0.35)]
            g2, h2 = icone(T, poe(peca, cx, y, 0.1), 1.2, 0.5)
            G, H = G + g2, H + h2
        w = rel(t, 0.6 + 0.06 * i, 0.95)
        if 0 < w < 1:
            G += T.ring(0.04 + 0.12 * w, 0.01, cx, -0.05, 2.0) * (1 - w) * 1.2
            for m in range(2):
                y0 = -0.35 + 0.08 * m + 0.1 * w
                G += T.polyline([(cx - 0.06, y0), (cx, y0 + 0.06), (cx + 0.06, y0)], 0.013) * (1 - w) * 1.2
    return G * env, H * env


def palpatine_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        G += T.gauss(lado * 0.22, -0.05, 0.05) * 1.0
        H += T.gauss(lado * 0.22, -0.05, 0.018) * 1.5
    G += _zap(T, int(t * 25), -0.22, -0.05, 0.22, -0.05, 0.012, 5, 0.4) * 1.3
    G += _zap(T, int(t * 25) + 3, -0.22, -0.05, 0.22, -0.05, 0.008, 5, 0.5) * 0.9
    H += _zap(T, int(t * 25), -0.22, -0.05, 0.22, -0.05, 0.004, 5, 0.4) * 1.0
    G += raios(T, t, -0.1, 1.1, 2, 151, -0.22, -0.05, 0.12, 0.006) + raios(T, t, -0.1, 1.1, 2, 152, 0.22, -0.05, 0.12, 0.006)
    return G, H


def poder_ilimitado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.15, 0.8)
    G += converge(T, t, 0.0, 0.25, 12, 153, -0.7, -0.1, 0.35, 0.008)
    if k > 0:
        for i, cx in enumerate((-0.55, 0.0, 0.55)):
            for lado in (-1, 1):
                G += _maos_raio(T, t, -0.75, -0.1 + 0.06 * lado, 0.0, k * 1.2, (cx, 0.0), 154 + 3 * i + (lado > 0), 2, 0.011)
            H += _maos_raio(T, t, -0.75, -0.1, 0.0, k * 0.7, (cx, 0.0), 160 + i, 1, 0.005)
            G += raios(T, t, 0.25 + 0.05 * i, 0.85, 4, 163 + i, cx, 0.0, 0.18, 0.007)
            G += T.ring(0.15, 0.012, cx, 0.0) * k * (0.6 + 0.4 * math.sin(t * 60 + i)) * 1.0
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        g, h = clarao(T, t, 0.35 + 0.05 * i, 0.6 + 0.05 * i, cx, 0.0, 0.5, 1.0)
        G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Neo

def kung_fu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += _codigo(T, t, -0.9, 0.9, -0.9, 0.4, 22, pulso(t, 0.0, 0.95) * 0.5, 164, 1.2)
    for j in range(5):
        a0 = 0.08 + 0.08 * j
        u = ease_in(rel(t, a0, a0 + 0.08), 2)
        k = 1 - rel(t, a0 + 0.12, a0 + 0.2)
        if u > 0 and k > 0:
            dy = -0.15 + 0.08 * (j % 4)
            P, nos = _punho(T, 0.05 + 0.32 * u, dy, 1.4, 0.2 * (j % 3 - 1))
            G += P * k * 0.9
            H += nos * 0.4 * k
            G += T.tapered([(-0.3, dy, 0.05 + 0.32 * u, dy, 0.8)], 0.03) * k * 0.8
        g, h = clarao(T, t, a0 + 0.06, a0 + 0.18, 0.45, -0.15 + 0.08 * (j % 4), 0.5, 0.9)
        G, H = G + g, H + h
    G += estouro(T, t, 0.45, 0.85, 12, 165, 0.45, 0.0, 0.4, 0.011)
    return G * env, H * env


def parar_as_balas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    mao = pulso(t, 0.0, 0.85)
    if mao > 0:
        P, nos = _punho(T, -0.4, 0.0, 1.0, 0.0)
        G += P * mao * 0.6
    for j in range(4):
        u = ease_out(rel(t, 0.0, 0.25), 2)
        y = -0.2 + 0.13 * j
        x = 0.8 - 0.65 * u
        pare = rel(t, 0.25, 0.6)
        cai = ease_in(rel(t, 0.6, 0.85), 2)
        if k > 0:
            g, h = _bala(T, x + 0.02 * math.sin(t * 30 + j) * pare, y + 0.4 * cai, math.pi + 1.3 * cai, 0.05, k * 1.2)
            G, H = G + g, H + h
            if 0 < pare < 1:
                G += T.ring(0.03 + 0.06 * ((t * 3 + j * 0.25) % 1), 0.006, x, y, 0.5) * (1 - (t * 3 + j * 0.25) % 1) * 1.2
    for m in range(3):
        u = (t * 1.5 + m / 3) % 1
        G += T.arc_band(0.1 + 0.4 * u, 0.01, -0.6, 0.6, 0.7, 0, -0.35, 0.0, 0.0) * (1 - u) * pulso(t, 0.1, 0.8) * 0.9
    return G * env, H * env


def neo_preparo(T, t, rng):
    G, H = vazio(T)
    G += _codigo(T, t, -0.45, 0.45, -0.45, 0.45, 16, 1.0, 166, 1.0)
    corpo = [(-0.12, 0.4), (-0.15, -0.05), (-0.1, -0.3), (-0.05, -0.38), (0.05, -0.38), (0.1, -0.3), (0.15, -0.05), (0.12, 0.4)]
    g, h = icone(T, corpo, 0.7, 0.2)
    G, H = G + g, H + h
    G += _oculos(T, 0.0, -0.31, 0.08, 1.0)
    return G, H


def o_escolhido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += _codigo(T, t, -0.9, 0.9, -0.9, 0.4, 26, pulso(t, 0.0, 0.5) * 0.7, 167, 1.2)
    u = ease_in(rel(t, 0.2, 0.4), 2)
    k = 1 - rel(t, 0.48, 0.58)
    if u > 0 and k > 0:
        x = -0.5 + 0.85 * u
        G += T.gauss(x, 0.0, 0.06, 0.15) * k * 1.0
        H += T.gauss(x, 0.0, 0.025) * k * 1.6
        G += T.tapered([(x - 0.5, 0.0, x, 0.0, 0.8)], 0.08) * k * 0.8
    g, h = clarao(T, t, 0.38, 0.62, 0.45, 0.0, 1.9, 1.7)
    G, H = G + g, H + h
    G += anel(T, t, 0.4, 0.8, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    w = rel(t, 0.45, 1.0)
    if 0 < w < 1:
        q = np.random.default_rng(168)
        segs = []
        for _ in range(40):
            a = q.uniform(0, TAU)
            d = 0.05 + 0.4 * ease_out(w) * q.uniform(0.5, 1)
            x, y = 0.45 + d * math.cos(a), d * math.sin(a) * 0.8 - 0.2 * w
            segs.append((x, y - 0.012, x, y + 0.012, 1 - w))
        G += T.lines(segs, 0.007) * 1.4
    return G * env, H * env


# ------------------------------------------------------------------ Agente Smith

def soco_do_agente_smith(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = pulso(t, 0.0, 0.5)
    if s > 0:
        g, h = _cabeca_terno(T, -0.55, -0.35, 0.16, s)
        G, H = G + g, H + h
    u = ease_in(rel(t, 0.15, 0.32), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.35 + 0.65 * u, 0.0, 2.0, 0)
        G += P * k
        H += nos * 0.5 * k
        G += T.tapered([(-0.6, 0.0, -0.35 + 0.65 * u - 0.1, 0.0, 0.8)], 0.06) * k * 0.7
    g2, h2 = clarao(T, t, 0.3, 0.52, 0.45, 0.0, 1.3, 1.3)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.31, 0.65, 0.05, 0.45, 0.035, 0.0)
    G += _codigo(T, t, 0.3, 0.6, -0.2, 0.2, 8, pulso(t, 0.32, 0.8) * 0.8, 169, 2.0)
    return G * env, H * env


def copias_do_smith(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for j in range(5):
        x = -0.65 + 0.22 * j
        s = surge(t, 0.05 + 0.1 * j, 0.25 + 0.1 * j)
        if s > 0 and kk > 0:
            g, h = _cabeca_terno(T, x, -0.25 + 0.03 * (j % 2), 0.13 * s, kk * (1.0 - 0.1 * j))
            G, H = G + g, H + h
            G += _codigo(T, t, x - 0.1, x + 0.1, -0.5, 0.2, 4, (1 - s) * 1.0 + 0.1, 170 + j, 2.0) * 0.6
    m = surge(t, 0.6, 0.8) * kk
    if m > 0:
        G += _mira(T, 0.65, 0.05, 0.12 * m, 1.0, 0.01)
    return G * env, H * env


def smith_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.0, 0.0, 1.6, -math.pi / 2)
    G += P * 0.5
    G += _codigo(T, t, -0.2, 0.2, -0.1, 0.45, 10, 1.0, 175, 1.5)
    G += T.gauss(0.0, 0.0, 0.15) * (0.3 + 0.2 * math.sin(t * TAU * 2))
    return G, H


def assimilar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.8, 0.92)
    if k > 0:
        x = -0.5 + 0.85 * u
        P, nos = _punho(T, x, 0.0, 1.5, 0)
        G += P * k * 0.8
        G += T.lines([(-0.55, 0.0, x - 0.08, 0.0, 1.0)], 0.03) * k * 0.8
    espalha = ease_out(rel(t, 0.25, 0.6), 2)
    if espalha > 0 and k > 0:
        G += T.gauss(0.45, 0.0, 0.1 + 0.12 * espalha, 0.15 + 0.15 * espalha) * k * 0.4
        G += _codigo(T, t, 0.45 - 0.2 * espalha, 0.45 + 0.2 * espalha, -0.3, 0.3, 14, k * espalha, 176, 2.5)
    w = rel(t, 0.5, 0.95)
    if 0 < w < 1:
        q = np.random.default_rng(177)
        segs = []
        for _ in range(20):
            y0 = q.uniform(-0.25, 0.25)
            x = 0.45 - 1.0 * ease_in((w + q.uniform(0, 0.3)) % 1)
            segs.append((x, y0 - 0.012, x, y0 + 0.012, 1.0))
        G += T.lines(segs, 0.007) * 1.4
    g2, h2 = clarao(T, t, 0.22, 0.45, 0.45, 0.0, 1.0, 1.1)
    G, H = G + g2, H + h2
    G += T.gauss(-0.55, 0.0, 0.15) * pulso(t, 0.8, 1.0) * 0.6
    return G * env, H * env


# ------------------------------------------------------------------ John Wick

def _pistola(T, x, y, s, k):
    G = T.lines([(x, y, x + s, y, 1.0)], s * 0.14) * k * 1.2
    G += T.polys([([(x, y - s * 0.05), (x + s * 0.2, y - s * 0.05), (x + s * 0.05, y + s * 0.45), (x - s * 0.15, y + s * 0.45)], 1.0)], 0.003) * k * 1.0
    return G


def tiro_na_testa_wick(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    if k > 0:
        G += _pistola(T, -0.7, -0.1, 0.25, k)
    g, h = clarao(T, t, 0.2, 0.32, -0.45, -0.1, 0.5, 1.2)
    G, H = G + g, H + h
    u = rel(t, 0.22, 0.32)
    if 0 < u < 1:
        x = -0.45 + 0.9 * u
        H += T.lines([(x - 0.15, -0.1 + 0.03 * u, x, -0.1 + 0.03 * u, 1.0)], 0.006) * 1.8
    g2, h2 = clarao(T, t, 0.3, 0.45, 0.45, -0.08, 0.6, 1.0)
    G, H = G + g2, H + h2
    m = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += _mira(T, 0.45, -0.08, 0.13 * m, 1.0, 0.011)
    w = rel(t, 0.25, 0.7)
    if 0 < w < 1:
        g3, h3 = _cartucho(T, -0.6 + 0.1 * w, -0.2 - 0.25 * math.sin(math.pi * w) + 0.3 * w * w, w * 15, 0.02, (1 - rel(w, 0.8, 1)) * 1.2)
        G, H = G + g3, H + h3
    return G * env, H * env


def lapis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.5)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        x = -0.5 + 0.9 * u
        a = t * 30 * (1 - u) + 0.0
        c, sn = math.cos(a), math.sin(a)
        G += T.lines([(x - c * 0.16, -0.05 - sn * 0.16, x + c * 0.16, -0.05 + sn * 0.16, 1.0)], 0.02) * k * 1.3
        g, h = cheio(T, [(x + c * 0.22, -0.05 + sn * 0.22), (x + c * 0.16 - sn * 0.018, -0.05 + sn * 0.16 + c * 0.018),
                         (x + c * 0.16 + sn * 0.018, -0.05 + sn * 0.16 - c * 0.018)], k * 1.4)
        G, H = G + g, H + h
        if u < 1:
            G += T.ring(0.1, 0.005, x, -0.05) * k * (1 - u) * 0.8
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.35, 0.75, 10, 178, 0.45, -0.05, 0.35, 0.01)
    return G * env, H * env


def wick_preparo(T, t, rng):
    G, H = vazio(T)
    y = -0.05 - 0.15 * math.sin(math.pi * ((t * 1.2) % 1))
    g, h = _moeda(T, 0.0, y, 0.16, t * TAU * 2, 1.2)
    G, H = G + g, H + h
    return G, H


def excomunicado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    if k > 0:
        G += _pistola(T, -0.7, -0.1, 0.25, k)
    for j in range(6):
        a0 = 0.1 + 0.07 * j
        g, h = clarao(T, t, a0, a0 + 0.06, -0.48, -0.1, 0.35, 1.0)
        G, H = G + g, H + h
        u = rel(t, a0, a0 + 0.08)
        if 0 < u < 1:
            x = -0.45 + 0.9 * u
            dy = 0.03 * (j % 3 - 1)
            H += T.lines([(x - 0.15, -0.1 + dy, x, -0.1 + dy, 1.0)], 0.006) * 1.8
        g2, h2 = clarao(T, t, a0 + 0.06, a0 + 0.15, 0.45 + 0.02 * (j % 2), -0.05 + 0.04 * (j % 3 - 1), 0.4, 0.8)
        G, H = G + g2, H + h2
        w = rel(t, a0, a0 + 0.45)
        if 0 < w < 1:
            g3, h3 = _cartucho(T, -0.6 + 0.12 * w + 0.02 * j, -0.2 - 0.28 * math.sin(math.pi * w) + 0.35 * w * w, w * 15 + j, 0.018, (1 - rel(w, 0.8, 1)) * 1.1)
            G, H = G + g3, H + h3
    g4, h4 = clarao(T, t, 0.58, 0.82, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g4, H + h4
    G += anel(T, t, 0.6, 0.95, 0.05, 0.6, 0.04, 0.0, 1.0, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ T-800

def escopeta_t800(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    recua = 0.05 * pulso(t, 0.3, 0.45)
    k = pulso(t, 0.0, 0.8)
    if k > 0:
        G += _escopeta(T, -0.75 - recua, -0.05 - 0.05 * pulso(t, 0.1, 0.25), 0.42, k)
    g, h = clarao(T, t, 0.28, 0.42, -0.33, -0.05, 0.7, 1.3)
    G, H = G + g, H + h
    q = np.random.default_rng(179)
    for _ in range(10):
        u = rel(t, 0.3, 0.45)
        if 0 < u < 1:
            a = q.uniform(-0.15, 0.15)
            d = 0.8 * u
            H += T.gauss(-0.33 + d * math.cos(a), -0.05 + d * math.sin(a), 0.008) * 1.8
    g2, h2 = clarao(T, t, 0.4, 0.62, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.42, 0.85, 14, 180, 0.45, 0.0, 0.45, 0.012)
    w = rel(t, 0.15, 0.6)
    if 0 < w < 1:
        g3, h3 = _cartucho(T, -0.55 + 0.1 * w, -0.15 - 0.25 * math.sin(math.pi * w) + 0.3 * w * w, w * 12, 0.03, (1 - rel(w, 0.8, 1)) * 1.1)
        G, H = G + g3, H + h3
    G += T.gauss(-0.55, 0.15, 0.08) * pulso(t, 0.55, 1.0) * 0.5
    return G * env, H * env


def eu_voltarei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    s = surge(t, 0.0, 0.3)
    if s > 0 and k > 0:
        g, h = _cranio_metal(T, 0.0, -0.3, 0.14 * s, k)
        G, H = G + g, H + h
    placa = ease_out(rel(t, 0.25, 0.5), 2)
    if placa > 0 and k > 0:
        pts = [(-0.3, -0.05), (0.3, -0.05), (0.33, 0.35), (0.0, 0.45), (-0.33, 0.35)]
        pts = [(x * placa, -0.05 + (y + 0.05) * placa) for x, y in pts]
        g2, h2 = icone(T, pts, k * 1.1, 0.4)
        G, H = G + g2, H + h2
        for x in (-0.22, 0.0, 0.22):
            G += T.gauss(x * placa, 0.05, 0.012) * k * 1.4
        brilho = rel((t * 1.3) % 1, 0.0, 1.0)
        G += T.lines([(-0.3 * placa, -0.05 + 0.45 * brilho * placa, 0.3 * placa, -0.05 + 0.45 * brilho * placa, 1.0)], 0.008) * k * 0.9
    G += converge(T, t, 0.4, 0.8, 10, 181, 0.0, 0.15, 0.5, 0.007)
    return G * env, H * env


def t800_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0.0, 0.0, 0.45, 0.3) * 0.15
    G += _mira(T, 0.05 * math.sin(t * TAU), 0.03 * math.cos(t * TAU * 1.3), 0.15, 1.0, 0.01)
    for j in range(5):
        y = -0.35 + 0.1 * j
        L = 0.1 + 0.1 * ((j * 0.37 + t) % 1)
        G += T.lines([(0.28, y, 0.28 + L, y, 1.0)], 0.006) * 1.0
    H += T.gauss(0.05 * math.sin(t * TAU), 0.03 * math.cos(t * TAU * 1.3), 0.015) * 1.8
    return G, H


def hasta_la_vista(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.35, 16, 182, -0.55, 0.0, 0.45, 0.009)
    c = pulso(t, 0.0, 0.45)
    if c > 0:
        G += _escopeta(T, -0.75, 0.0, 0.3, c)
        G += T.gauss(-0.42, 0.0, 0.05 + 0.06 * c) * c * 1.4
        H += T.gauss(-0.42, 0.0, 0.025) * c * 1.8
    u = rel(t, 0.35, 0.55)
    k = 1 - rel(t, 0.62, 0.75)
    if u > 0 and k > 0:
        ponta = -0.42 + 0.87 * min(1.0, ease_in(u) * 1.3)
        G += T.tapered([(-0.42, 0.0, ponta, 0.0, 1.0)], 0.2) * k * 0.8
        G += T.lines([(-0.42, 0.0, ponta, 0.0, 1.0)], 0.035) * k * 1.4
        H += T.lines([(-0.42, 0.0, ponta, 0.0, 1.0)], 0.012) * k * 1.2
    g, h = clarao(T, t, 0.5, 0.8, 0.45, 0.0, 2.1, 1.9)
    G, H = G + g, H + h
    G += anel(T, t, 0.52, 0.95, 0.05, 0.85, 0.05, 0.0, 1.0, 1.5)
    G += onda_no_chao(T, t, 0.52, 0.95, 1.0, 0.38, 1.4)
    G += estouro(T, t, 0.52, 0.95, 20, 183, 0.45, 0.0, 0.8, 0.015)
    return G * env, H * env


REGISTRO = [
    ("sabre_verde_luke", sabre_verde_luke, GRANDE, "Luke · o sabre verde", False),
    ("defletir", defletir, GRANDE, "Luke · o sabre devolvendo os tiros", False),
    ("luke_preparo", luke_preparo, MEDIA, "Luke · a mira do X-Wing (Preparo, laço)", True),
    ("tiro_na_trincheira", tiro_na_trincheira, GRANDE, "Luke · os torpedos de prótons", False),
    ("raio_da_forca_palpatine", raio_da_forca_palpatine, GRANDE, "Palpatine · os relâmpagos da Força", False),
    ("tudo_conforme_o_plano", tudo_conforme_o_plano, GRANDE, "Palpatine · o capuz e as peças", False),
    ("palpatine_preparo", palpatine_preparo, MEDIA, "Palpatine · a eletricidade entre as mãos (Preparo, laço)", True),
    ("poder_ilimitado", poder_ilimitado, GRANDE, "Palpatine · a tempestade de relâmpagos", False),
    ("kung_fu", kung_fu, GRANDE, "Neo · o código e os golpes", False),
    ("parar_as_balas", parar_as_balas, GRANDE, "Neo · as balas paradas no ar", False),
    ("neo_preparo", neo_preparo, MEDIA, "Neo · o código escorrendo (Preparo, laço)", True),
    ("o_escolhido", o_escolhido, GRANDE, "Neo · o rival se desfazendo em código", False),
    ("soco_do_agente_smith", soco_do_agente_smith, GRANDE, "Agente Smith · o soco de terno", False),
    ("copias_do_smith", copias_do_smith, GRANDE, "Agente Smith · as cópias surgindo", False),
    ("smith_preparo", smith_preparo, MEDIA, "Agente Smith · a mão escorrendo código (Preparo, laço)", True),
    ("assimilar", assimilar, GRANDE, "Agente Smith · o código passando para ele", False),
    ("tiro_na_testa_wick", tiro_na_testa_wick, GRANDE, "John Wick · o tiro e a mira", False),
    ("lapis", lapis, GRANDE, "John Wick · o lápis girando", False),
    ("wick_preparo", wick_preparo, MEDIA, "John Wick · a moeda de ouro (Preparo, laço)", True),
    ("excomunicado", excomunicado, GRANDE, "John Wick · a rajada e os cartuchos", False),
    ("escopeta_t800", escopeta_t800, GRANDE, "T-800 · a escopeta e os chumbos", False),
    ("eu_voltarei", eu_voltarei, GRANDE, "T-800 · o crânio de metal e a placa", False),
    ("t800_preparo", t800_preparo, MEDIA, "T-800 · a visão vermelha (Preparo, laço)", True),
    ("hasta_la_vista", hasta_la_vista, GRANDE, "T-800 · o tiro com toda a energia", False),
]
