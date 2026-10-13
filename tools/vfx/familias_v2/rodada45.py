"""Rodada 45 das habilidades próprias: Gwen, Viúva Negra, Gavião Arqueiro, Gamora, Drax e Mulher-Aranha.

Gwen Tennyson
- rajada_de_mana: o hexágono de mana na mão e o feixe rosa de hexágonos que acerta o rival.
- barreira_de_mana: as colmeias de hexágonos rosa fechando em cima de cada um do trio (Barreira e Escudo).
- gwen_preparo: o Preparo da Lucubra — as mãos acesas e o anel de runas hexagonais girando (laço).
- lucubra: o círculo de mana no alto, as ondas rosa varrendo os rivais e os buffs quebrando como vidro.

Viúva Negra
- mordida_da_viuva: os discos elétricos dos braceletes voando e os raios prendendo o rival (Eletrificado e Paralisado).
- chave_de_pernas: as pernas em tesoura girando o rival e jogando no chão, a mira vermelha (Exposto).
- viuva_preparo: o Preparo da Missão cumprida — a ampulheta vermelha pulsando e os bastões faiscando (laço).
- missao_cumprida: o avanço em risco vermelho, os dois bastões cruzando e a ampulheta acendendo.

Gavião Arqueiro
- flecha_explosiva: a flecha cravando no rival com a ponta piscando (Marca explosiva).
- flecha_de_rede: a flecha que abre em rede e enrola o rival (Preso).
- gaviao_preparo: o Preparo da Chuva de flechas — o arco puxado ao máximo, a corda tremendo (laço).
- chuva_de_flechas: a rajada de flechas subindo e caindo em cima de todos os rivais (Exposto).

Gamora
- godslayer_corte: a Godslayer abrindo a lâmina e o corte em arco com as gotas vermelhas (Sangrando).
- golpe_acrobatico: o mortal no ar e o calcanhar descendo no rival (Enfraquecido).
- gamora_preparo: o Preparo da Execução — a espada de lado com o brilho verde correndo pelo fio (laço).
- execucao_de_gamora: o vulto passando pelo rival e o corte enorme que demora e abre.

Drax
- facas_gemeas: as duas facas cruzando em X e girando de volta.
- grito_de_drax: as tatuagens vermelhas acendendo e o grito em ondas nos rivais (Provocado e Protegido).
- drax_preparo: o Preparo d'O Destruidor — os punhos fechados, as tatuagens pulsando e o chão rachando (laço).
- o_destruidor: a corrida e o soco gigante que racha o chão (Enfraquecido).

Mulher-Aranha
- rajada_venenosa: a mão carregando a energia amarela e a rajada em zigue-zague com o veneno (Envenenado e Eletrificado).
- voo_planado: as asas de teia abertas, o mergulho e as imagens que ficam (Esquiva).
- mulher_aranha_preparo: o Preparo do Choque total — as duas mãos estalando bioeletricidade (laço).
- choque_total: o raio enorme caindo no rival e a estática presa nele (Paralisado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (AMPULHETA, GOTA, anel, cheio, circulo, clarao, converge, corte, estouro, icone, onda_no_chao,
                         particulas, poe, raios, runas, surge)

_HEX = circulo(6, 1.0)


def _hex(T, x, y, s, k, ang=0.0, miolo=0.3):
    return icone(T, poe(_HEX, x, y, s, ang + math.pi / 6), k, miolo)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


# ------------------------------------------------------------------ Gwen

def rajada_de_mana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    c = pulso(t, 0.0, 0.35)
    if c > 0:
        g, h = _hex(T, -0.6, 0.0, 0.13 + 0.04 * c, c * 1.3, t * 6)
        G, H = G + g, H + h
        G += converge(T, t, 0.0, 0.3, 10, 3, -0.6, 0.0, 0.3, 0.008)
    u = rel(t, 0.2, 0.6)
    k = 1 - rel(t, 0.55, 0.7)
    if u > 0 and k > 0:
        ponta = -0.55 + 1.0 * min(1.0, ease_in(u, 1.3) * 1.3)
        G += T.tapered([(-0.55, 0.0, ponta, 0.0, 1.0)], 0.15) * k * 0.8
        G += T.lines([(-0.55, 0.0, ponta, 0.0, 1.0)], 0.022) * k * 1.4
        H += T.lines([(-0.55, 0.0, ponta, 0.0, 1.0)], 0.006) * k * 0.9
        for j in range(5):
            x = -0.5 + ((t * 2.5 + j / 5) % 1) * (ponta + 0.5)
            g, h = _hex(T, x, 0.0, 0.075, k * 1.0, t * 9 + j)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.42, 0.65, 0.45, 0.0, 1.1, 1.3)
    G, H = G + g2, H + h2
    q = np.random.default_rng(11)
    for j in range(8):
        w = rel(t, 0.45, 0.9)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            g3, h3 = _hex(T, 0.45 + 0.35 * w * math.cos(a), 0.3 * w * math.sin(a), 0.03 * (1 - 0.5 * w), (1 - w) * 1.1, a + w * 6)
            G, H = G + g3, H + h3
    return G * env, H * env


def barreira_de_mana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        for j, (dx, dy) in enumerate(((0, -0.17), (-0.15, -0.085), (0.15, -0.085), (-0.15, 0.085), (0.15, 0.085), (0, 0.0), (0, 0.17))):
            m = surge(t, 0.05 + 0.04 * i + 0.025 * j, 0.25 + 0.04 * i + 0.025 * j)
            if m > 0:
                g, h = _hex(T, cx + dx * m, 0.0 + dy * m, 0.095 * m, k * 0.9, 0.0, 0.25)
                G, H = G + g, H + h
        brilho = rel((t * 1.3 + 0.2 * i) % 1, 0.0, 1.0)
        G += T.lines([(cx - 0.22, -0.25 + 0.5 * brilho, cx + 0.22, -0.25 + 0.5 * brilho, 1.0)], 0.008) * k * pulso(t, 0.3, 0.9) * 0.9
        # o debuff (o pontinho escuro) dissolvendo na barreira
        w = rel(t, 0.45 + 0.05 * i, 0.75 + 0.05 * i)
        if 0 < w < 1:
            G += particulas(T, w, 0.0, 1.0, 6, 20 + i, cx, -0.05, 0.08, 0.3, 0.01) * 0.8
    G += anel(T, t, 0.25, 0.7, 0.1, 1.1, 0.03, 0.0, 2.2)
    return G * env, H * env


def gwen_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        b = 0.5 + 0.5 * math.sin(t * TAU * 2 + lado)
        G += T.gauss(lado * 0.2, 0.0, 0.06) * (0.9 + 0.5 * b)
        H += T.gauss(lado * 0.2, 0.0, 0.02) * (1.2 + b)
    for j in range(6):
        a = t * TAU + TAU * j / 6
        g, h = _hex(T, 0.38 * math.cos(a), 0.38 * 0.55 * math.sin(a), 0.045, 1.0, -a)
        G, H = G + g, H + h
    G += T.ring(0.38, 0.012, 0, 0, 1.8) * 1.0
    g2, h2 = _hex(T, 0.0, 0.0, 0.12, 0.6 + 0.3 * math.sin(t * TAU), t * 2, 0.15)
    return G + g2, H + h2


def lucubra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = runas(T, t, 0.0, 0.75, 0.6, 12, -0.5, 2.8, 2.0, _HEX, 0.04)
    G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.25 + 0.08 * j, 0.75 + 0.08 * j)
        if 0 < u < 1:
            x = -1.0 + 2.0 * ease_out(u, 1.4)
            G += T.arc_band(0.6, 0.05 * (1 - 0.4 * u), -0.9, 0.9, 0.5, 0, x - 0.6, 0.0, 1.0) * (1 - rel(u, 0.75, 1)) * 1.3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.45 + 0.08 * i
        g2, h2 = clarao(T, t, a0, a0 + 0.2, cx, 0.0, 0.45, 1.0)
        G, H = G + g2, H + h2
        # o buff quebrando como vidro
        q = np.random.default_rng(30 + i)
        for _ in range(6):
            w = rel(t, a0 + 0.05, a0 + 0.4)
            if 0 < w < 1:
                a = q.uniform(0, TAU)
                d = 0.05 + 0.25 * ease_out(w)
                tri = [(0, -1), (0.8, 0.7), (-0.6, 0.5)]
                g3, h3 = icone(T, poe(tri, cx + d * math.cos(a), -0.1 + d * math.sin(a) + 0.2 * w * w, 0.03, a + 8 * w), (1 - w) * 1.1, 0.5)
                G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Viúva Negra

def mordida_da_viuva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(2):
        u = rel(t, 0.05 + 0.08 * j, 0.35 + 0.08 * j)
        if 0 < u < 1:
            x = -0.6 + 1.05 * ease_in(u, 1.2)
            y = (-0.05 + 0.1 * j) * (1 - u)
            G += T.ring(0.05, 0.016, x, y) * 1.4
            H += T.gauss(x, y, 0.022) * 1.6
            G += T.tapered([(x - 0.25, y, x, y, 0.8)], 0.02) * 0.8
            G += raios(T, t, 0.0, 1.0, 2, 40 + j, x, y, 0.06, 0.006) * 0.8
    k = pulso(t, 0.38, 0.95)
    if k > 0:
        G += raios(T, t, 0.38, 0.95, 6, 7, 0.45, 0.0, 0.3, 0.009) * 1.2
        G += T.ring(0.22, 0.015, 0.45, 0.0, 1.0) * k * (0.6 + 0.4 * math.sin(t * 60)) * 1.1
    g, h = clarao(T, t, 0.38, 0.58, 0.45, 0.0, 1.0, 1.2)
    G, H = G + g, H + h
    return G * env, H * env


def chave_de_pernas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_out(rel(t, 0.0, 0.25), 2)
    gira = ease_in(rel(t, 0.25, 0.5), 1.6)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        rot = gira * math.pi * 1.5
        for lado in (-1, 1):
            a0 = rot + (0 if lado > 0 else math.pi)
            G += T.arc_band(0.3 - 0.05 * fecha, 0.075, a0 - 1.2 * fecha, a0 + 0.1, 1.0, 0, 0.45, -0.05, 0.0) * k * 1.2
        if gira > 0:
            G += T.arc_band(0.3, 0.03, rot - 2.0, rot, 1.0, 0, 0.45, -0.05, 1.0) * k * gira * 0.9
    g, h = clarao(T, t, 0.48, 0.7, 0.45, 0.3, 1.3, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.5, 0.9, 0.7, 0.35, 1.5)
    G += estouro(T, t, 0.5, 0.9, 12, 6, 0.45, 0.3, 0.45, 0.012)
    m = surge(t, 0.6, 0.78) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.11 * m, 0.012, 0.45, -0.05) * 1.3
        G += T.lines([(0.45 - 0.17 * m, -0.05, 0.45 - 0.06 * m, -0.05, 1.0), (0.45 + 0.06 * m, -0.05, 0.45 + 0.17 * m, -0.05, 1.0),
                      (0.45, -0.05 - 0.17 * m, 0.45, -0.05 - 0.06 * m, 1.0), (0.45, -0.05 + 0.06 * m, 0.45, -0.05 + 0.17 * m, 1.0)], 0.01) * 1.3
    return G * env, H * env


def viuva_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = icone(T, poe(AMPULHETA, 0, 0, 0.16), 0.9 + 0.5 * b, 0.6)
    G, H = G + g, H + h
    G += T.gauss(0, 0, 0.25) * (0.25 + 0.2 * b)
    for lado in (-1, 1):
        x = lado * 0.35
        G += T.lines([(x, 0.3, x + lado * 0.05, -0.25, 1.0)], 0.014) * 1.1
        G += _zap(T, int(t * 30) + (lado > 0), x + lado * 0.05, -0.25, x + lado * 0.05 + 0.08, -0.38, 0.006, 3, 0.4) * 1.2
        H += T.gauss(x + lado * 0.05, -0.25, 0.018) * 1.5
    return G, H


def missao_cumprida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.25)
    if 0 < u < 1:
        for m in range(4):
            y = -0.2 + 0.13 * m
            G += T.tapered([(-0.9, y, -0.9 + 1.3 * ease_in(u), y * 0.3, 1.0)], 0.03) * (1 - u) * 1.2
    for j, ang in enumerate((0.75, -0.75)):
        g, h = corte(T, t, 0.25 + 0.06 * j, 0.5 + 0.06 * j, ang, 1.1, 0.07, 0.45, 0.0)
        G, H = G + g * 1.2, H + h
        G += raios(T, t, 0.28 + 0.06 * j, 0.6 + 0.06 * j, 3, 50 + j, 0.45, 0.0, 0.35, 0.007)
    g2, h2 = clarao(T, t, 0.32, 0.6, 0.45, 0.0, 1.5, 1.5)
    G, H = G + g2, H + h2
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g3, h3 = icone(T, poe(AMPULHETA, 0.45, 0.0, 0.2 * s), 1.2, 0.6)
        G, H = G + g3, H + h3
    G += estouro(T, t, 0.35, 0.9, 16, 9, 0.45, 0.0, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Gavião Arqueiro

def _flecha(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s, y - sn * s, x, y, 1.0)], s * 0.05) * k * 1.3
    ponta = [(x + c * s * 0.25, y + sn * s * 0.25), (x - sn * s * 0.1, y + c * s * 0.1), (x + sn * s * 0.1, y - c * s * 0.1)]
    g, h = icone(T, ponta, k * 1.3, 0.6)
    bx, by = x - c * s, y - sn * s
    for lado in (-1, 1):
        G += T.lines([(bx + c * s * 0.2, by + sn * s * 0.2, bx - lado * sn * s * 0.12, by + lado * c * s * 0.12, 1.0)], s * 0.035) * k * 1.0
    return G + g, h


def flecha_explosiva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.4)
    if 0 < u < 1:
        x = -0.75 + 1.15 * u
        g, h = _flecha(T, x, -0.02 * math.sin(math.pi * u), 0.0, 0.45, 1.0)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.7, 0.0, x - 0.3, 0.0, 0.7)], 0.02) * 0.8
    if t >= 0.3:
        k = 1 - rel(t, 0.85, 0.95)
        g, h = _flecha(T, 0.35, 0.0, 0.0, 0.45, k)
        G, H = G + g, H + h
        pisca = 1.0 if (t * 8) % 1 < 0.5 else 0.25
        H += T.gauss(0.42, 0.0, 0.025) * pisca * k * 2.0
        G += T.gauss(0.42, 0.0, 0.06) * pisca * k * 0.8
        G += T.ring(0.08 + 0.1 * ((t * 4) % 1), 0.008, 0.42, 0.0) * (1 - (t * 4) % 1) * k * 1.2
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.42, 0.0, 0.7, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.3, 0.6, 8, 3, 0.42, 0.0, 0.25, 0.01)
    return G * env, H * env


def flecha_de_rede(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.4)
    if 0 < u < 1:
        x = -0.75 + 1.0 * u
        g, h = _flecha(T, x, 0.0, 0.0, 0.45, 1.0)
        G, H = G + g, H + h
    abre = ease_out(rel(t, 0.3, 0.5), 2)
    k = 1 - rel(t, 0.88, 1)
    if abre > 0 and k > 0:
        aperta = 1 - 0.25 * ease_in(rel(t, 0.5, 0.75))
        r = 0.28 * abre * aperta
        cx, cy = 0.45, 0.0
        segs = []
        for j in range(8):
            a = TAU * j / 8 + 0.3 * abre
            segs.append((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), 1.0))
        G += T.lines(segs, 0.008) * k * 1.2
        for f in (0.35, 0.7, 1.0):
            G += T.polyline([(cx + r * f * math.cos(TAU * j / 8 + 0.3 * abre), cy + r * f * math.sin(TAU * j / 8 + 0.3 * abre)) for j in range(9)],
                            0.007) * k * 1.2
        for j in range(8):
            a = TAU * j / 8 + 0.3 * abre
            H += T.gauss(cx + r * math.cos(a), cy + r * math.sin(a), 0.012) * k * 1.2
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.45, 0.0, 0.6, 0.8)
    return (G + g2) * env, (H + h2) * env


def gaviao_preparo(T, t, rng):
    G, H = vazio(T)
    treme = 0.006 * math.sin(t * 70)
    G += T.arc_band(0.38, 0.025, -1.1, 1.1, 1.0, 0, -0.15, 0.0, 0.0) * 1.2
    puxa = -0.15 - 0.1 + treme
    G += T.lines([(-0.15 + 0.38 * math.cos(-1.1), 0.38 * math.sin(-1.1), puxa, 0.0, 1.0),
                  (puxa, 0.0, -0.15 + 0.38 * math.cos(1.1), 0.38 * math.sin(1.1), 1.0)], 0.006) * 1.3
    g, h = _flecha(T, 0.38, 0.0, 0.0, 0.62, 1.0)
    G, H = G + g, H + h
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    H += T.gauss(0.45, 0.0, 0.02) * (1.2 + b)
    G += T.gauss(0.45, 0.0, 0.07) * (0.4 + 0.3 * b)
    return G, H


def chuva_de_flechas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(12)
    for j in range(7):
        u = rel(t, 0.02 * j, 0.25 + 0.02 * j)
        if 0 < u < 1:
            x0 = -0.75 + 0.03 * j
            a = -1.1 + 0.08 * j
            d = 1.2 * ease_out(u)
            g, h = _flecha(T, x0 + d * math.cos(a), 0.2 + d * math.sin(a), a, 0.24, 1 - rel(u, 0.7, 1))
            G, H = G + g, H + h
    for j in range(22):
        x = q.uniform(-0.85, 0.85)
        a0 = 0.35 + q.uniform(0, 0.3)
        u = rel(t, a0, a0 + 0.22)
        if 0 < u < 1:
            y = -0.95 + 1.15 * ease_in(u, 1.5)
            g, h = _flecha(T, x + 0.08 * u, y, 1.35, 0.24, 1.0)
            G, H = G + g, H + h
        w = rel(t, a0 + 0.22, a0 + 0.45)
        if 0 < w < 1:
            G += T.ring(0.03 + 0.06 * w, 0.008, x + 0.08, 0.22, 2.5) * (1 - w) * 1.2
            g, h = _flecha(T, x + 0.08, 0.2, 1.35, 0.17, (1 - w) * 0.9)
            G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.55, 0.8, x, 0.1, 0.35, 0.7)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Gamora

def _espada_curva(T, x, y, ang, s, ext, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s * 0.25, y - sn * s * 0.25, x, y, 1.0)], s * 0.05) * k * 1.2
    if ext <= 0:
        return G, 0.0
    pts = []
    for v in np.linspace(0, ext, 10):
        dx, dy = s * v, s * 0.12 * math.sin(math.pi * v * 0.8)
        pts.append((x + c * dx - sn * dy, y + sn * dx + c * dy))
    G += T.polyline(pts, s * 0.07) * k * 1.4
    H = T.polyline(pts, s * 0.02) * k * 1.0
    return G, H


def godslayer_corte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    ext = ease_out(rel(t, 0.0, 0.2), 3)
    u = ease_in(rel(t, 0.18, 0.4), 1.6)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.3 + 2.4 * u
        g, h = _espada_curva(T, 0.0, 0.1, ang, 0.5, ext, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.5, 0.06, ang - 1.0, ang, 1.0, 0, 0.0, 0.1, 1.0) * k * 0.8
    g2, h2 = corte(T, t, 0.32, 0.55, 0.5, 1.2, 0.08, 0.45, 0.0, 0.12)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.35, 0.55, 0.45, 0.0, 1.0)
    G, H = G + g3, H + h3
    q = np.random.default_rng(14)
    for j in range(9):
        w = rel(t, 0.38 + 0.02 * j, 0.85)
        if 0 < w < 1:
            vx, vy = q.uniform(0.1, 0.5), q.uniform(-0.5, -0.1)
            g4, h4 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.035), (1 - w) * 1.2)
            G, H = G + g4, H + h4
    return G * env, H * env


def golpe_acrobatico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.4)
    if 0 < u < 1:
        a = math.pi + math.pi * ease_in(u, 1.3)
        cx, cy, r = 0.0, 0.0, 0.42
        x, y = cx + r * math.cos(a), cy + r * 0.8 * math.sin(a)
        G += T.arc_band(r, 0.04, math.pi + 0.0, a, 0.8, 0, cx, cy, 1.0) * 1.1
        P, nos = _punho(T, x, y, 1.0, a + math.pi / 2)
        G += P * 0.9
        H += nos * 0.4
    g, h = clarao(T, t, 0.38, 0.6, 0.45, 0.0, 1.3, 1.3)
    G, H = G + g, H + h
    G += anel(T, t, 0.4, 0.8, 0.05, 0.4, 0.03, 0.0)
    G += estouro(T, t, 0.4, 0.85, 12, 4, 0.45, 0.0, 0.5, 0.012)
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.28 + 0.1 * j + 0.1 * rel(t, 0.55, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.07 * m), (0.52, y0)], 0.014) * m * 1.2
    return G * env, H * env


def gamora_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _espada_curva(T, -0.35, 0.25, -0.5, 0.8, 1.0, 1.2)
    G, H = G + g, H + h
    u = (t * 1.5) % 1
    c, sn = math.cos(-0.5), math.sin(-0.5)
    dx, dy = 0.8 * u, 0.8 * 0.12 * math.sin(math.pi * u * 0.8)
    x, y = -0.35 + c * dx - sn * dy, 0.25 + sn * dx + c * dy
    H += T.gauss(x, y, 0.02) * 2.0
    G += T.gauss(x, y, 0.06) * 0.7
    H += T.flare(x, y, 0.08, 0.3, 0.006) * (1 - abs(2 * u - 1))
    return G, H


def execucao_de_gamora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.2)
    if 0 < u < 1:
        G += T.tapered([(-0.9, 0.05, -0.9 + 1.8 * ease_in(u), 0.05, 1.0)], 0.08) * (1 - 0.5 * u) * 1.1
        G += T.gauss(-0.9 + 1.8 * ease_in(u), 0.05, 0.05, 0.12) * 1.2
    linha = rel(t, 0.2, 0.3)
    k = 1 - rel(t, 0.75, 0.85)
    if linha > 0 and k > 0:
        a = -0.9
        L = 1.4 * linha
        x1, y1 = 0.45 - math.cos(a) * L / 2, -math.sin(a) * L / 2
        x2, y2 = 0.45 + math.cos(a) * L / 2, math.sin(a) * L / 2
        abre = ease_out(rel(t, 0.5, 0.7), 2)
        G += T.lines([(x1, y1, x2, y2, 1.0)], 0.01 + 0.05 * abre) * k * 1.5
        H += T.lines([(x1, y1, x2, y2, 1.0)], 0.004 + 0.012 * abre) * k * 1.2
    g, h = clarao(T, t, 0.5, 0.75, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.52, 0.95, 0.05, 0.8, 0.04, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.52, 0.95, 18, 7, 0.45, 0.0, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Drax

_FACA = [(0, -1), (0.16, -0.6), (0.14, 0.2), (0.3, 0.25), (0.3, 0.35), (0.08, 0.35), (0.08, 0.9), (-0.08, 0.9), (-0.08, 0.35),
         (-0.3, 0.35), (-0.3, 0.25), (-0.14, 0.2), (-0.16, -0.6)]


def facas_gemeas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.5)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        for lado in (-1, 1):
            a = lado * (1.2 - 2.0 * u) - math.pi / 2 * 0
            x = 0.45 + lado * 0.25 * (1 - u)
            g, h = icone(T, poe(_FACA, x, -0.25 * (1 - u), 0.28, a), k * 1.2, 0.5)
            G, H = G + g, H + h
    for j, ang in enumerate((0.8, -0.8)):
        g2, h2 = corte(T, t, 0.28 + 0.02 * j, 0.52 + 0.02 * j, ang, 1.0, 0.07, 0.45, 0.0)
        G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.3, 0.52, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g3, H + h3
    w = rel(t, 0.5, 0.85)
    if 0 < w < 1:
        for lado in (-1, 1):
            x = 0.45 - 1.0 * ease_out(w)
            g4, h4 = icone(T, poe(_FACA, x, lado * 0.15 * math.sin(math.pi * w), 0.18, w * 20 * lado), (1 - w) * 1.1, 0.5)
            G, H = G + g4, H + h4
    G += estouro(T, t, 0.3, 0.75, 12, 8, 0.45, 0.0, 0.45, 0.012)
    return G * env, H * env


def _tatuagens(T, cx, cy, s, k):
    segs = [[(-0.6, -0.8), (-0.3, -0.5), (-0.45, -0.1), (-0.2, 0.3), (-0.35, 0.8)],
            [(0.6, -0.8), (0.3, -0.5), (0.45, -0.1), (0.2, 0.3), (0.35, 0.8)],
            [(-0.15, -0.9), (0.0, -0.6), (0.15, -0.9)]]
    G = 0.0
    for p in segs:
        G = G + T.polyline([(cx + x * s, cy + y * s) for x, y in p], 0.012) * k
    return G


def grito_de_drax(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    acende = pulso(t, 0.0, 0.85)
    G += _tatuagens(T, -0.55, 0.0, 0.3, acende * (1.0 + 0.3 * math.sin(t * 30)) * 1.3)
    H += _tatuagens(T, -0.55, 0.0, 0.3, acende * 0.5)
    for j in range(4):
        u = rel(t, 0.12 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.1 * u, 0.045 * (1 - 0.5 * u), -0.55, 0.55, 0.7, 0, -0.55, -0.05, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = surge(t, 0.45 + 0.06 * i, 0.62 + 0.06 * i) * (1 - rel(t, 0.88, 1))
        if m > 0 and i > 0:
            for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
                x, y = cx + 0.06 * math.cos(a + math.pi / 4), -0.3 + 0.06 * math.sin(a + math.pi / 4)
                G += T.arc_band(0.05 * m, 0.014, a + 0.4, a + 1.2, 1.0, 0, x, y, 0.0) * 1.3
    k2 = pulso(t, 0.3, 1.0)
    G += T.gauss(-0.55, 0.0, 0.3, 0.35) * k2 * 0.45
    H += T.gauss(-0.55, 0.0, 0.08) * k2 * 0.5
    return G * env, H * env


def drax_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2.5)
    G += _tatuagens(T, 0.0, -0.05, 0.35, 0.8 + 0.6 * b)
    for lado in (-1, 1):
        P, nos = _punho(T, lado * 0.32, 0.25, 1.1, -math.pi / 2)
        G += P * 0.9
        H += nos * 0.3
    q = np.random.default_rng(int(t * 3))
    for j in range(3):
        a = q.uniform(-0.5, 0.5)
        G += _zap(T, int(t * 6) + j, 0.0, 0.38, 0.5 * math.sin(a) + (j - 1) * 0.3, 0.38 + 0.03 * math.cos(a), 0.007, 3, 0.15) * (0.6 + 0.4 * b)
    return G, H


def o_destruidor(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.6)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        x = -0.75 + 1.0 * u
        G += T.gauss(x - 0.05, 0.05, 0.12, 0.2) * k * 0.6
        P, nos = _punho(T, x + 0.2, 0.0, 2.0, 0)
        G += P * k
        H += nos * 0.5 * k
        for m in range(3):
            G += T.tapered([(x - 0.6, -0.15 + 0.15 * m, x - 0.1, -0.15 + 0.15 * m, 0.8)], 0.025) * k * u
    g, h = clarao(T, t, 0.28, 0.55, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.8, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    G += onda_no_chao(T, t, 0.32, 0.9, 1.0, 0.38, 1.6)
    for j in range(5):
        w = rel(t, 0.32, 0.5)
        if w > 0:
            a = -0.4 + 0.2 * j
            G += _zap(T, 60 + j, 0.45, 0.38, 0.45 + 0.6 * w * math.cos(a) * (1 if j % 2 else -1), 0.38 + 0.08 * w, 0.01, 4, 0.2) * \
                (1 - rel(t, 0.8, 0.95)) * 1.2
    G += estouro(T, t, 0.3, 0.85, 18, 10, 0.45, 0.0, 0.7, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Mulher-Aranha

def rajada_venenosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    c = pulso(t, 0.0, 0.32)
    if c > 0:
        G += T.gauss(-0.6, 0.0, 0.08 + 0.04 * c) * c * 1.2
        H += T.gauss(-0.6, 0.0, 0.025) * c * 1.8
        G += raios(T, t, 0.0, 0.32, 3, 70, -0.6, 0.0, 0.14, 0.006)
    k = pulso(t, 0.22, 0.62)
    if k > 0:
        for j in range(2):
            G += _zap(T, int(t * 40) + 7 * j, -0.58, 0.0, 0.45, 0.0, 0.016 - 0.007 * j, 5, 0.18) * k * 1.4
        H += _zap(T, int(t * 40), -0.58, 0.0, 0.45, 0.0, 0.006, 5, 0.18) * k
    g, h = clarao(T, t, 0.3, 0.6, 0.45, 0.0, 1.1, 1.3)
    G, H = G + g, H + h
    q = np.random.default_rng(16)
    for j in range(8):
        w = rel(t, 0.4 + 0.03 * j, 0.95)
        if 0 < w < 1:
            dx = q.uniform(-0.15, 0.15)
            g2, h2 = cheio(T, poe(GOTA, 0.45 + dx, -0.15 + 0.5 * w * w, 0.04), (1 - w) * 1.1)
            G, H = G + g2, H + h2
    G += particulas(T, t, 0.4, 0.95, 12, 17, 0.45, 0.0, 0.15, 0.4, 0.012)
    return G * env, H * env


def _asas_de_teia(T, x, y, s, abre, k):
    G = 0.0
    for lado in (-1, 1):
        pts = [(x, y - 0.1 * s), (x + lado * s * abre, y - 0.35 * s), (x + lado * s * 0.85 * abre, y + 0.3 * s), (x, y + 0.35 * s)]
        g, _ = icone(T, pts, k, 0.3)
        G = G + g
        for f in (0.4, 0.75):
            G = G + T.lines([(x, y, x + lado * s * abre * f, y - 0.35 * s * f + 0.3 * s * f * 0.5, 1.0)], 0.005) * k
    return G


def voo_planado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 3)
    k = 1 - rel(t, 0.85, 1)
    for m in range(4):
        tm = t - 0.06 * m
        u = rel(tm, 0.1, 0.8)
        x = -0.6 + 1.2 * ease_out(u, 1.2)
        y = -0.3 + 0.3 * math.sin(math.pi * u)
        km = k * (1 if m == 0 else 0.35 / m)
        G += _asas_de_teia(T, x, y, 0.45, abre, km * 1.1)
        if m == 0:
            H += T.gauss(x, y, 0.025) * k * 1.2
    for j in range(5):
        u = (t * 2 + j / 5) % 1
        y = -0.4 + 0.15 * j
        G += T.lines([(0.8 - 1.6 * u, y, 0.6 - 1.6 * u, y, 1.0)], 0.005) * pulso(t, 0.05, 0.95) * 0.9
    return G * env, H * env


def mulher_aranha_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        x = lado * 0.25
        b = 0.5 + 0.5 * math.sin(t * TAU * 3 + lado)
        G += T.gauss(x, 0.0, 0.07 + 0.02 * b) * 1.1
        H += T.gauss(x, 0.0, 0.025) * (1.5 + b)
        G += raios(T, t, -0.1, 1.1, 4, 80 + (lado > 0), x, 0.0, 0.26, 0.008)
    G += _zap(T, int(t * 20), -0.25, 0.0, 0.25, 0.0, 0.008, 4, 0.35) * (0.6 + 0.4 * math.sin(t * 40))
    return G, H


def choque_total(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.25, 12, 18, -0.55, 0.0, 0.4, 0.008)
    k = pulso(t, 0.2, 0.6)
    if k > 0:
        for j in range(3):
            G += _zap(T, int(t * 30) + 11 * j, 0.45 + 0.1 * (j - 1), -1.0, 0.45, 0.0, 0.03 - 0.008 * j, 6, 0.2) * k * 1.4
        H += _zap(T, int(t * 30), 0.45, -1.0, 0.45, 0.0, 0.012, 6, 0.2) * k * 1.2
        G += _zap(T, int(t * 30) + 3, -0.55, 0.0, 0.45, 0.0, 0.014, 5, 0.2) * k * 1.2
    g, h = clarao(T, t, 0.22, 0.6, 0.45, 0.0, 2.0, 1.7)
    G, H = G + g, H + h
    G += anel(T, t, 0.25, 0.7, 0.05, 0.6, 0.04, 0.0, 1.0, 1.4)
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += raios(T, t, 0.5, 1.0, 5, 90, 0.45, 0.0, 0.22, 0.007)
        G += T.ring(0.2, 0.012, 0.45, 0.0, 1.0) * m * (0.6 + 0.4 * math.sin(t * 70)) * 1.2
    G += estouro(T, t, 0.25, 0.75, 16, 19, 0.45, 0.0, 0.6, 0.012)
    return G * env, H * env


REGISTRO = [
    ("rajada_de_mana", rajada_de_mana, GRANDE, "Gwen · o feixe de hexágonos de mana", False),
    ("barreira_de_mana", barreira_de_mana, GRANDE, "Gwen · as colmeias de mana no trio", False),
    ("gwen_preparo", gwen_preparo, MEDIA, "Gwen · as runas hexagonais girando (Preparo, laço)", True),
    ("lucubra", lucubra, GRANDE, "Gwen · a Lucubra varrendo os rivais", False),
    ("mordida_da_viuva", mordida_da_viuva, GRANDE, "Viúva Negra · os discos elétricos", False),
    ("chave_de_pernas", chave_de_pernas, GRANDE, "Viúva Negra · a tesoura de pernas", False),
    ("viuva_preparo", viuva_preparo, MEDIA, "Viúva Negra · a ampulheta e os bastões (Preparo, laço)", True),
    ("missao_cumprida", missao_cumprida, GRANDE, "Viúva Negra · os bastões cruzados", False),
    ("flecha_explosiva", flecha_explosiva, GRANDE, "Gavião Arqueiro · a flecha que pisca", False),
    ("flecha_de_rede", flecha_de_rede, GRANDE, "Gavião Arqueiro · a flecha que vira rede", False),
    ("gaviao_preparo", gaviao_preparo, MEDIA, "Gavião Arqueiro · o arco puxado (Preparo, laço)", True),
    ("chuva_de_flechas", chuva_de_flechas, GRANDE, "Gavião Arqueiro · a chuva de flechas", False),
    ("godslayer_corte", godslayer_corte, GRANDE, "Gamora · a Godslayer abrindo e cortando", False),
    ("golpe_acrobatico", golpe_acrobatico, GRANDE, "Gamora · o mortal e o calcanhar", False),
    ("gamora_preparo", gamora_preparo, MEDIA, "Gamora · o brilho correndo pela lâmina (Preparo, laço)", True),
    ("execucao_de_gamora", execucao_de_gamora, GRANDE, "Gamora · o corte que demora e abre", False),
    ("facas_gemeas", facas_gemeas, GRANDE, "Drax · as facas em X", False),
    ("grito_de_drax", grito_de_drax, GRANDE, "Drax · as tatuagens e o grito", False),
    ("drax_preparo", drax_preparo, MEDIA, "Drax · os punhos e as tatuagens pulsando (Preparo, laço)", True),
    ("o_destruidor", o_destruidor, GRANDE, "Drax · o soco que racha o chão", False),
    ("rajada_venenosa", rajada_venenosa, GRANDE, "Mulher-Aranha · a rajada bioelétrica", False),
    ("voo_planado", voo_planado, GRANDE, "Mulher-Aranha · as asas de teia", False),
    ("mulher_aranha_preparo", mulher_aranha_preparo, MEDIA, "Mulher-Aranha · as mãos estalando (Preparo, laço)", True),
    ("choque_total", choque_total, GRANDE, "Mulher-Aranha · o raio enorme", False),
]
