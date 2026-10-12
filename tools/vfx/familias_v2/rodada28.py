"""Rodada 28 das habilidades próprias: Genos, Hiei, Sailor Moon, Coringa, Arlequina, Darkseid e Lex Luthor.

Genos
- canhao_incinerador: os braços-canhão soltam o fogo largo em todos (Queimando).
- rajada_de_misseis: os mísseis pequenos com fumaça caindo em todos (Queimando).
- genos_preparo: o Preparo da Sobrecarga — o núcleo no peito brilhando e as aletas soltando vapor (laço).
- sobrecarga_genos: o feixe incandescente gigante e a explosão (Queimando e Exposto).

Hiei
- espada_de_fogo_hiei: a espada em chamas negras num corte rápido.
- jagan: o terceiro olho abre na testa e as chamas negras (Queimando).
- hiei_preparo: o Preparo do Dragão das Trevas — o braço enfaixado com as chamas negras girando (laço).
- dragao_das_trevas: o dragão de chamas negras enorme varrendo todos (Queimando).

Sailor Moon
- cura_lunar: o cetro lunar e a luz de lua crescente caindo como penas (Protegido, Regeneração e Purificar).

Coringa
- gas_do_riso: a nuvem verde do gás do riso e as risadas "HA HA" (Confuso e Envenenado).
- carta_marcada: a carta do Coringa girando e cravando (Preparo atrasado).
- piada_final: a caixa-surpresa abre: o palhaço de mola e a explosão de confete (Confuso e Enfraquecido).

Arlequina
- marreta_arlequina: a marreta gigante girando e o "BONK" (Confuso e Marcado).
- pirueta: a pirueta acrobática com as fitas vermelho e preto (Exposto).
- surpresa_explosiva: as bombinhas com corações caindo e explodindo (Confuso e Marca explosiva).

Darkseid
- feixe_omega: os dois feixes Ômega saindo dos olhos e fazendo curva até o rival (Marcado e Exposto).
- darkseid_preparo: o Preparo da Equação Anti-Vida — os símbolos da equação girando (laço).
- anti_vida: a Equação Anti-Vida desce e prende a mente do rival (Silenciado e Preso).

Lex Luthor
- plano_calculado: a prancheta com o plano, as linhas de cálculo e o golpe certeiro (Enfraquecido e Silenciado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CARTA, CHAMA, CORACAO, LUA, anel, aura, cheio, chuva, clarao, converge, corte, estouro, estrela_pts, icone,
                         onda_no_chao, particulas, poe, raios, runas, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _fogo_em_leque(T, t, u, x0, y0, comp, seed, abre=0.5, k=1.0):
    G, H = vazio(T)
    q = np.random.default_rng(seed)
    for j in range(30):
        v = (u * 1.3 + j / 30) % 1
        if v > ease_out(min(1, u * 2)):
            continue
        ang = q.uniform(-abre, abre)
        x = x0 + comp * v * math.cos(ang)
        y = y0 + comp * v * math.sin(ang) * 0.6
        g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.15 * v, math.pi / 2 + ang), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3 * k, 0.6)
        G, H = G + g, H + h
    return G, H


# ------------------------------------------------------------------ Genos

def canhao_incinerador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for lado in (-1, 1):
        g, h = clarao(T, t, 0.0, 0.25, -0.65, lado * 0.12, 0.5)
        G, H = G + g, H + h
    u = rel(t, 0.1, 0.9)
    if 0 < u < 1:
        g, h = _fogo_em_leque(T, t, u, -0.6, 0.0, 1.5, 3, 0.6)
        G, H = G + g, H + h
    return G * env, H * env


def rajada_de_misseis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(6)
    for j in range(9):
        a0 = 0.03 * j
        u = rel(t, a0, a0 + 0.45)
        alvo_x = -0.5 + 0.5 * (j % 3)
        if 0 < u < 1:
            x = -0.8 + (alvo_x + 0.8) * u
            y = -0.1 - 0.6 * math.sin(math.pi * u) + 0.3 * u
            dx = (alvo_x + 0.8)
            dy = -0.6 * math.pi * math.cos(math.pi * u) + 0.3
            ang = math.atan2(dy, dx)
            G += T.lines([(x - 0.06 * math.cos(ang), y - 0.06 * math.sin(ang), x + 0.06 * math.cos(ang), y + 0.06 * math.sin(ang), 1.0)], 0.02) * 1.3
            G += T.gauss(x - 0.1 * math.cos(ang), y - 0.1 * math.sin(ang), 0.04) * 0.6
        if u >= 1:
            g, h = clarao(T, t, a0 + 0.45, a0 + 0.6, alvo_x, 0.2 + 0.05 * (j % 2), 0.45)
            G, H = G + g, H + h
    return G * env, H * env


def genos_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 10)
    G += T.gauss(0, 0, 0.18 + 0.04 * p) * 1.4
    H += T.gauss(0, 0, 0.07) * (1.5 + p)
    G += T.ring(0.25, 0.025, 0, 0) * 1.2
    for lado in (-1, 1):
        u = (t * 1.2 + (0.5 if lado > 0 else 0)) % 1
        pts = [(lado * (0.2 + 0.3 * u) + 0.03 * math.sin(u * 12), -0.1 - 0.4 * u, (1 - u) * 0.8)]
        G += T.splats(pts, 0.06) * 0.7
    return G, H


def sobrecarga_genos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.25), 3)
    k = 1 - rel(t, 0.55, 0.8)
    if u > 0:
        G += T.lines([(-0.7, 0.0, -0.7 + 1.5 * u, 0.0, 1.0)], 0.2) * 0.7 * k
        H += T.lines([(-0.7, 0.0, -0.7 + 1.5 * u, 0.0, 1.0)], 0.06) * 1.5 * k
    g, h = clarao(T, t, 0.22, 0.5, 0.8, 0.0, 1.5, 1.6)
    G, H = G + g, H + h
    G += estouro(T, t, 0.22, 0.7, 20, 4, 0.8, 0.0, 0.7, 0.016)
    for j in range(5):
        kk = pulso(t, 0.4 + 0.03 * j, 0.95)
        g2, h2 = icone(T, poe(CHAMA, 0.6 + 0.1 * j - 0.2, 0.05 - 0.1 * (j % 2), 0.1 * kk), kk, 0.6)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Hiei

def _chama_negra(T, x, y, s, ang, k):
    g, h = icone(T, poe(CHAMA, x, y, s, ang), k * 0.6, 0.9, 1.6)
    return g, h * 0.5


def espada_de_fogo_hiei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = corte(T, t, 0.05, 0.4, 0.3, 1.6, 0.1, 0.0, 0.0)
    G, H = G + g * 1.2, H + h
    for j in range(7):
        k = pulso(t, 0.1 + 0.03 * j, 0.8)
        v = j / 6
        g2, h2 = _chama_negra(T, -0.6 + 1.2 * v, -0.3 * (v - 0.5) * 0.6 - 0.05, 0.08 * k, 0, k)
        G, H = G + g2, H + h2
    return G * env, H * env


def jagan(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.85, 1))
    if abre > 0:
        olho = [(0.15 * math.cos(a), -0.4 + 0.06 * abre * math.sin(a)) for a in np.linspace(0, TAU, 30)]
        G += T.polyline(olho, 0.02) * 1.3
        G += T.gauss(0, -0.4, 0.03 * abre + 0.001) * 1.5
        H += T.gauss(0, -0.4, 0.015) * 2.0 * abre
    u = rel(t, 0.3, 0.9)
    if 0 < u < 1:
        for j in range(6):
            v = (u * 1.2 + j / 6) % 1
            g2, h2 = _chama_negra(T, 0.0 + 0.7 * v, -0.3 + 0.3 * v + 0.05 * math.sin(v * 10), 0.06 + 0.08 * v, math.pi / 2, (1 - v))
            G, H = G + g2, H + h2
    return G * env, H * env


def hiei_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.1, 0.4, 0.15, -0.3, 1.0)], 0.06) * 0.7
    for j in range(6):
        y = 0.35 - 0.12 * j
        G += T.lines([(-0.18 + 0.035 * j, y, 0.02 + 0.035 * j, y - 0.06, 1.0)], 0.01) * 1.2
    for j in range(6):
        a = t * 5 + TAU * j / 6
        g, h = _chama_negra(T, 0.02 + 0.3 * math.cos(a), 0.05 + 0.3 * math.sin(a), 0.08, a, 1.0)
        G, H = G + g, H + h
    return G, H


def dragao_das_trevas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.6), 1.5)
    k = 1 - rel(t, 0.8, 0.95)
    if u > 0:
        corpo = [(-0.8 + 1.7 * v * u, 0.0 + 0.3 * math.sin(v * 7 - t * 12) * (1 - v * 0.4)) for v in np.linspace(0, 1, 36)]
        for i in range(len(corpo) - 1):
            w = 0.04 + 0.1 * (i / 36)
            G += T.lines([(corpo[i][0], corpo[i][1], corpo[i + 1][0], corpo[i + 1][1], 1.0)], w) * 0.9 * k
            if i % 4 == 0:
                g, h = _chama_negra(T, corpo[i][0], corpo[i][1] - w, 0.04 + 0.05 * i / 36, 0, k)
                G, H = G + g, H + h
        hx, hy = corpo[-1]
        g2, h2 = icone(T, [(hx + 0.22, hy), (hx + 0.02, hy - 0.15), (hx - 0.12, hy - 0.1), (hx - 0.15, hy + 0.08), (hx + 0.02, hy + 0.12)], 1.2 * k, 0.6)
        G, H = G + g2, H + h2
        H += T.gauss(hx + 0.05, hy - 0.05, 0.02) * 2 * k
    G += onda_no_chao(T, t, 0.5, 0.95, 1.0, 0.35, 1.4)
    return G * env, H * env


# ------------------------------------------------------------------ Sailor Moon

def cura_lunar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(0, 0.4, 0, -0.2 * s, 1.0)], 0.02) * 1.2
        g, h = cheio(T, poe(LUA, 0, -0.3 * s - 0.05, 0.12 * s, -math.pi / 2), 1.4)
        G, H = G + g, H + h * 2
        g2, h2 = cheio(T, poe(estrela_pts(5, 0.45), 0, -0.3 * s - 0.05, 0.05 * s), 1.5)
        G, H = G + g2, H + h2 * 2
    g3, h3 = clarao(T, t, 0.25, 0.5, 0, -0.35, 1.0)
    G, H = G + g3, H + h3
    g4, h4 = chuva(T, t, 0.3, 1.0, poe(LUA, 0, 0, 1.0, -math.pi / 2), 14, 5, 0.05, -0.6, 0.45, 0.8, 2.0, 1.2)
    G, H = G + g4, H + h4
    G += anel(T, t, 0.35, 0.95, 0.2, 0.9, 0.035, 0.1)
    return G * env, H * env


# ------------------------------------------------------------------ Coringa

def _ha(T, x, y, s, k):
    segs = []
    for dx in (0.0, 0.18):
        segs += [(x + dx * s, y - 0.08 * s, x + dx * s, y + 0.08 * s, 1.0), (x + dx * s + 0.08 * s, y - 0.08 * s, x + dx * s + 0.08 * s, y + 0.08 * s, 1.0),
                 (x + dx * s, y, x + dx * s + 0.08 * s, y, 1.0)]
    return T.lines(segs, 0.012) * k * 1.4


def gas_do_riso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(5)
    u = ease_out(rel(t, 0.0, 0.6), 2)
    pts = [(-0.5 + 1.2 * u * q.uniform(0.3, 1) + 0.1 * math.sin(t * 3 + j), q.normal(0, 0.18), pulso(t, 0.0, 0.95) * q.uniform(0.3, 0.8)) for j in range(40)]
    G += T.splats(pts, 0.1) * 0.6
    for j in range(4):
        k = pulso(t, 0.3 + 0.1 * j, 0.7 + 0.08 * j)
        G += _ha(T, -0.3 + 0.25 * j, -0.45 + 0.1 * (j % 2), 1.4, k)
    return G * env, H * env


def carta_marcada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.05, 0.5)
    if 0 < u < 1:
        x = -0.65 + 1.3 * ease_in(u, 1.3)
        g, h = icone(T, poe(CARTA, x, 0.0, 0.2, t * 25), 1.2, 0.7)
        G, H = G + g, H + h
        G += T.gauss(x, 0.0, 0.03) * 1.0
    fica = surge(t, 0.48, 0.6) * (1 - rel(t, 0.88, 1))
    if fica > 0:
        g2, h2 = icone(T, poe(CARTA, 0.65, 0.0, 0.22 * fica, 0.3), 1.2, 0.7)
        G, H = G + g2, H + h2
        G += _ha(T, 0.58, -0.02, 0.6 * fica, 1.0)
    G += estouro(T, t, 0.48, 0.8, 10, 3, 0.65, 0.0, 0.35, 0.012)
    return G * env, H * env


def piada_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.65))
    if s > 0:
        g, h = icone(T, [(-0.18 * s, 0.1), (0.18 * s, 0.1), (0.18 * s, 0.4), (-0.18 * s, 0.4)], 1.0, 0.45)
        G, H = G + g, H + h
    mola = ease_out(rel(t, 0.25, 0.45), 3) * (1 - rel(t, 0.55, 0.65))
    if mola > 0:
        pts = [(0.06 * math.sin(v * 20), 0.1 - 0.45 * mola * v) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.012) * 1.2
        G += T.ring(0.1, 0.02, 0, 0.1 - 0.45 * mola - 0.08) * 1.3
        G += _ha(T, -0.08, 0.1 - 0.45 * mola - 0.08, 0.5, 1.0)
    g2, h2 = clarao(T, t, 0.55, 0.75, 0, -0.1, 1.4, 1.5)
    G, H = G + g2, H + h2
    q = np.random.default_rng(8)
    for j in range(30):
        uu = rel(t, 0.58, 1.0)
        if 0 < uu < 1:
            a = q.uniform(0, TAU)
            d = 0.9 * ease_out(uu) * q.uniform(0.3, 1)
            G += T.polys([(poe([(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)], d * math.cos(a), -0.1 + d * math.sin(a) + 0.3 * uu * uu, 0.02, uu * 10 + j), 1.0)]) * (1 - uu) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Arlequina

def marreta_arlequina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.6)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        a = -2.2 + 2.4 * u
        c, sn = math.cos(a), math.sin(a)
        x0, y0 = -0.3, 0.15
        x1, y1 = x0 + 0.6 * c, y0 + 0.6 * sn
        G += T.lines([(x0, y0, x1, y1, 1.0)], 0.025) * k * 1.2
        cab = poe([(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], x1, y1, 0.12, a + math.pi / 2)
        g, h = icone(T, cab, k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.38, 0.55, 0.3, 0.15, 1.0)
    G, H = G + g2, H + h2
    s = surge(t, 0.4, 0.55) * (1 - rel(t, 0.85, 1))
    for j in range(5):
        a = TAU * j / 5 + t * 6
        g3, h3 = cheio(T, poe(estrela_pts(5, 0.45), 0.3 + 0.2 * math.cos(a), -0.15 + 0.08 * math.sin(a), 0.04 * s), s * 1.4)
        G, H = G + g3, H + h3
    return G * env, H * env


def pirueta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.6)
    if 0 < u < 1:
        cx = -0.5 + 1.0 * ease_out(u)
        cy = -0.3 * math.sin(math.pi * u)
        for j, k in ((0, 1.3), (1, 0.8)):
            a0 = u * TAU * 2 + j * math.pi
            G += T.arc_band(0.4, 0.07, a0, a0 + 2.2, 1.0, 0, cx, cy, 1.0, True) * k * (1 - u * 0.5)
    g, h = clarao(T, t, 0.55, 0.75, 0.5, 0.0, 0.9)
    G, H = G + g, H + h
    G += estouro(T, t, 0.55, 0.9, 12, 5, 0.5, 0.0, 0.4, 0.014)
    return G * env, H * env


def surpresa_explosiva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(9)
    for j in range(6):
        a0 = 0.03 * j
        u = rel(t, a0, a0 + 0.4)
        x = -0.6 + 0.24 * j
        if 0 < u < 1:
            y = -0.9 + 1.1 * ease_in(u, 1.6)
            g, h = icone(T, poe(_circ(16), x, y, 0.06), 1.2, 0.5)
            G, H = G + g, H + h
            G += T.lines([(x + 0.04, y - 0.05, x + 0.08, y - 0.1, 1.0)], 0.008) * 1.2
            H += T.gauss(x + 0.08, y - 0.1, 0.015) * 2
        g2, h2 = clarao(T, t, a0 + 0.4, a0 + 0.55, x, 0.2, 0.6)
        G, H = G + g2, H + h2
        for m in range(3):
            uu = rel(t, a0 + 0.4, a0 + 0.8)
            if 0 < uu < 1:
                ang = -math.pi / 2 + (m - 1) * 0.7
                g3, h3 = cheio(T, poe(CORACAO, x + 0.25 * uu * math.cos(ang), 0.2 + 0.25 * uu * math.sin(ang), 0.04), (1 - uu) * 1.3)
                G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Darkseid

def feixe_omega(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = pulso(t, 0.0, 0.3)
    for lado in (-1, 1):
        H += T.gauss(-0.55 + lado * 0.06, -0.3, 0.025) * s * 2.5
    u = ease_out(rel(t, 0.15, 0.55), 2)
    k = 1 - rel(t, 0.6, 0.8)
    if u > 0:
        for lado in (-1, 1):
            pts = []
            for v in np.linspace(0, u, 30):
                x = -0.55 + lado * 0.06 + 1.25 * v
                y = -0.3 + 0.3 * v + lado * 0.35 * math.sin(math.pi * v)
                pts.append((x, y))
            G += T.polyline(pts, 0.03) * k * 1.3
            H += T.polyline(pts, 0.01) * k * 1.4
    g, h = clarao(T, t, 0.5, 0.75, 0.7, 0.0, 1.1)
    G, H = G + g, H + h
    for j in range(3):
        G += T.ring(0.08 + 0.06 * j, 0.012, 0.7, 0.0) * pulso(t, 0.55, 0.95) * 1.1
    return G * env, H * env


def darkseid_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = runas(T, (t * 0.5) % 1, 0.0, 1.0, 0.4, 10, 0.0, 1.0, 1.0)
    G, H = G + g, H + h
    G += T.ring(0.4, 0.015, 0, 0) * 1.0
    for lado in (-1, 1):
        H += T.gauss(lado * 0.06, -0.05, 0.025) * 2.0
    return G, H


def anti_vida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_out(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.85, 1)
    q = np.random.default_rng(4)
    simbolos = []
    for j in range(16):
        x = q.uniform(-0.6, 0.6)
        y = -0.9 + 0.7 * desce + q.uniform(0, 0.3)
        s = 0.03
        tipo = j % 3
        if tipo == 0:
            simbolos += [(x - s, y, x + s, y, 1.0), (x, y - s, x, y + s, 1.0)]
        elif tipo == 1:
            simbolos += [(x - s, y - s, x + s, y + s, 1.0), (x - s, y + s, x + s, y - s, 1.0)]
        else:
            simbolos += [(x - s, y - s * 0.5, x + s, y - s * 0.5, 1.0), (x - s, y + s * 0.5, x + s, y + s * 0.5, 1.0)]
    G += T.lines(simbolos, 0.008) * k * 1.4
    aperta = ease_in(rel(t, 0.4, 0.75), 2)
    if aperta > 0:
        G += T.ring(0.45 - 0.25 * aperta, 0.03, 0.4, -0.15) * k * 1.3
        G += T.gauss(0.4, -0.15, 0.12) * aperta * k
    g, h = aura(T, t, 0.3, 1.0, 0.35, -0.15, 0.7)
    return (G + g) * env, (H + h) * env


# ------------------------------------------------------------------ Lex Luthor

def plano_calculado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.6, 0.75))
    if s > 0:
        G += T.polyline([(-0.75, -0.45), (-0.25, -0.45), (-0.25, 0.15), (-0.75, 0.15), (-0.75, -0.45)], 0.015) * s * 1.2
        segs = [(-0.7, -0.35 + 0.1 * j, -0.7 + 0.35 * ((j * 37) % 10) / 10 + 0.05, -0.35 + 0.1 * j, 1.0) for j in range(5)]
        G += T.lines(segs, 0.008) * s * 1.3
    u = ease_out(rel(t, 0.2, 0.5), 2)
    if u > 0:
        G += T.lines([(-0.25, -0.15, -0.25 + 0.9 * u, 0.0, 1.0)], 0.008) * (1 - rel(t, 0.7, 0.85)) * 1.3
        G += T.lines([(0.65, -0.12, 0.65, 0.12, 1.0), (0.53, 0.0, 0.77, 0.0, 1.0)], 0.01) * u * (1 - rel(t, 0.7, 0.85)) * 1.3
        G += T.ring(0.1, 0.012, 0.65, 0.0) * u * (1 - rel(t, 0.7, 0.85)) * 1.3
    g, h = clarao(T, t, 0.5, 0.7, 0.65, 0.0, 1.1)
    G, H = G + g, H + h
    G += estouro(T, t, 0.5, 0.85, 14, 6, 0.65, 0.0, 0.45, 0.014)
    return G * env, H * env


REGISTRO = [
    ("canhao_incinerador", canhao_incinerador, GRANDE, "Genos · o fogo largo dos canhões", False),
    ("rajada_de_misseis", rajada_de_misseis, GRANDE, "Genos · os mísseis", False),
    ("genos_preparo", genos_preparo, MEDIA, "Genos · o núcleo e o vapor (Preparo, laço)", True),
    ("sobrecarga_genos", sobrecarga_genos, GRANDE, "Genos · o feixe incandescente", False),
    ("espada_de_fogo_hiei", espada_de_fogo_hiei, GRANDE, "Hiei · a espada de chamas negras", False),
    ("jagan", jagan, GRANDE, "Hiei · o terceiro olho", False),
    ("hiei_preparo", hiei_preparo, MEDIA, "Hiei · o braço enfaixado (Preparo, laço)", True),
    ("dragao_das_trevas", dragao_das_trevas, GRANDE, "Hiei · o dragão das chamas negras", False),
    ("cura_lunar", cura_lunar, GRANDE, "Sailor Moon · o cetro e as luas", False),
    ("gas_do_riso", gas_do_riso, GRANDE, "Coringa · o gás do riso", False),
    ("carta_marcada", carta_marcada, GRANDE, "Coringa · a carta girando", False),
    ("piada_final", piada_final, GRANDE, "Coringa · a caixa-surpresa", False),
    ("marreta_arlequina", marreta_arlequina, GRANDE, "Arlequina · a marreta e as estrelinhas", False),
    ("pirueta", pirueta, GRANDE, "Arlequina · a pirueta com as fitas", False),
    ("surpresa_explosiva", surpresa_explosiva, GRANDE, "Arlequina · as bombinhas de coração", False),
    ("feixe_omega", feixe_omega, GRANDE, "Darkseid · os feixes Ômega em curva", False),
    ("darkseid_preparo", darkseid_preparo, MEDIA, "Darkseid · a equação girando (Preparo, laço)", True),
    ("anti_vida", anti_vida, GRANDE, "Darkseid · a Equação Anti-Vida", False),
    ("plano_calculado", plano_calculado, GRANDE, "Lex Luthor · a prancheta e a mira", False),
]
