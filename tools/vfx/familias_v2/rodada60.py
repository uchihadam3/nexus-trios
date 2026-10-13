"""Rodada 60 das habilidades próprias: Jiraiya, Tsunade, Sailor Mars, Steven, Garnet e Johnny Bravo.

Jiraiya
- rasengan_jiraiya: o Rasengan girando na palma e o estouro no rival (Exposto).
- invocacao_gamabunta: o selo de invocação no chão, a fumaça e o sapo gigante com a espada (Preso).
- jiraiya_preparo: o Preparo do Óleo de sapo — o sapo pequeno no ombro e o óleo borbulhando (laço).
- oleo_de_sapo_em_chamas: o jato de óleo e o fogo do sapo varrendo todos os rivais (Queimando).

Tsunade
- soco_de_cem_toneladas: o dedo/punho de Tsunade e o chão rachando em volta do rival.
- ninjutsu_medico: as mãos verdes de chakra sobre o aliado (Vida e Purificar).
- tsunade_preparo: o Preparo da Força de cem selos — o losango na testa e as marcas se espalhando (laço).
- forca_de_cem_selos: as marcas do selo correndo pelo corpo e a luz levantando o aliado caído.

Sailor Mars
- fogo_de_marte: o fogo de Marte em espiral até o rival (Queimando).
- pergaminho_sagrado: o pergaminho de papel (ofuda) voando e o círculo sagrado no trio (Purificar e Protegido).
- sailormars_preparo: o Preparo da Flecha flamejante — o arco de fogo puxado (laço).
- flecha_flamejante_de_marte: a flecha de fogo voando e explodindo no rival (Queimando).

Steven
- escudo_da_rosa: o escudo cor-de-rosa com a rosa abrindo na frente do trio (Escudo e Barreira).
- saliva_curativa: a gota brilhante e os brilhinhos curando o aliado (Vida).
- steven_preparo: o Preparo da Bolha — a bolha cor-de-rosa crescendo na mão (laço).
- bolha_de_steven: a bolha prendendo o rival e flutuando (Preso).

Garnet
- futuro_previsto: o terceiro olho abrindo e as linhas do futuro saindo (Protegido e Esquiva).
- manoplas_garnet: as duas manoplas e o choque elétrico no rival (Eletrificado).
- garnet_preparo: o Preparo da Fusão perfeita — as duas gemas (Ruby e Safira) girando e se juntando (laço).
- fusao_perfeita: as manoplas gigantes e o soco duplo com raios.

Johnny Bravo
- pose_johnny: a pose de músculos, o topete brilhando e os corações nos rivais (Provocado e Protegido).
- soco_de_karate: o "HUAH!" e o golpe de karatê em linha reta.
- johnny_preparo: o Preparo dos Músculos de aço — os bíceps flexionando e os óculos brilhando (laço).
- musculos_de_aco: os bíceps gigantes e o soco que amassa o rival (Enfraquecido).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, CORACAO, CRUZ, ESPADA, GEMA, GOTA, anel, clarao, corte, estouro, flor, icone, onda_no_chao,
                         particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _rasengan(T, x, y, r, t, k):
    G = T.gauss(x, y, r * 0.7) * k * 1.2 + T.ring(r, r * 0.12, x, y) * k * 1.2
    for j in range(4):
        a = t * 18 + TAU * j / 4
        G += T.arc_band(r * (0.4 + 0.15 * j), r * 0.08, a, a + 2.5, 1.0, 0, x, y, 1.0) * k * 1.2
    return G, T.gauss(x, y, r * 0.25) * k * 2.0


def _sapo(T, x, y, s, k):
    """O sapo gigante: o corpo largo, os olhos no alto e a boca."""
    corpo = [(-1.0, 0.5), (-0.9, -0.1), (-0.6, -0.45), (-0.2, -0.55), (0.2, -0.55), (0.6, -0.45), (0.9, -0.1), (1.0, 0.5)]
    g, h = icone(T, poe(corpo, x, y, s), k * 1.1, 0.45)
    G, H = g, h
    for lado in (-1, 1):
        G += T.ring(s * 0.18, s * 0.04, x + lado * s * 0.45, y - s * 0.6) * k * 1.3
        H += T.gauss(x + lado * s * 0.45, y - s * 0.6, s * 0.05) * k * 1.8
    G += T.arc_band(s * 0.7, s * 0.03, 0.25, math.pi - 0.25, 1.0, 0, x, y - s * 0.35, 0.0) * k * 1.1
    return G, H


def _selo_invocacao(T, cx, cy, r, k):
    G = T.ring(r, 0.012, cx, cy, 3.0) * k * 1.2
    segs = [(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a) / 3, 1.0) for a in np.linspace(0, TAU, 6, endpoint=False)]
    return G + T.lines(segs, 0.008) * k


def _losango(T, x, y, s, k):
    pts = [(x, y - s), (x + s * 0.6, y), (x, y + s), (x - s * 0.6, y)]
    return icone(T, pts, k * 1.3, 0.85)


def _ofuda(T, x, y, s, ang, k):
    """O pergaminho de papel (ofuda) com os traços escritos."""
    pts = [(-0.35, -1), (0.35, -1), (0.35, 1), (-0.35, 1)]
    g, h = icone(T, poe(pts, x, y, s, ang), k * 1.1, 0.45)
    c, sn = math.cos(ang), math.sin(ang)
    segs = []
    for j in range(4):
        v = -0.6 + 0.4 * j
        segs.append((x - sn * v * s - c * 0.15 * s, y + c * v * s - sn * 0.15 * s, x - sn * v * s + c * 0.15 * s, y + c * v * s + sn * 0.15 * s, 1.0))
    return g + T.lines(segs, s * 0.06) * k, h


def _arco(T, x, y, s, puxa, k):
    G = T.arc_band(s, s * 0.06, -1.2, 1.2, 1.0, 0, x - s * 0.6, y, 0.0) * k * 1.3
    ty, by = y - s * math.sin(1.2), y + s * math.sin(1.2)
    tx = x - s * 0.6 + s * math.cos(1.2)
    px = tx - s * 0.5 * puxa
    G += T.lines([(tx, ty, px, y, 1.0), (px, y, tx, by, 1.0)], s * 0.025) * k
    return G


def _rosa(T, x, y, s, k, abre=1.0):
    G, H = 0.0, 0.0
    for camada in range(3):
        r = s * (0.35 + 0.3 * camada) * (0.4 + 0.6 * abre)
        for j in range(5):
            a = TAU * j / 5 + camada * 0.6
            pts = poe([(0, 0), (0.35, -0.4), (0.0, -1.0), (-0.35, -0.4)], x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a), r, a + math.pi / 2)
            g, h = icone(T, pts, k * (1.1 - 0.2 * camada), 0.5)
            G, H = G + g, H + h
    return G, H


def _terceiro_olho(T, x, y, s, abre, k):
    G = T.arc_band(s, s * 0.1, math.pi + 0.5, TAU - 0.5, 1.0, 0, x, y + s * 0.55 * abre, 0.0) * k * 1.2
    G += T.arc_band(s, s * 0.1, 0.5, math.pi - 0.5, 1.0, 0, x, y - s * 0.55 * abre, 0.0) * k * 1.2
    H = T.gauss(x, y, s * 0.3 * abre + 0.003) * k * 2.0
    return G + T.ring(s * 0.3 * abre + 0.003, s * 0.06, x, y) * k * abre, H


def _oculos(T, x, y, s, k):
    G = T.polys([([(x - s, y - s * 0.2), (x - s * 0.1, y - s * 0.2), (x - s * 0.2, y + s * 0.3), (x - s * 0.9, y + s * 0.3)], 1.0),
                 ([(x + s * 0.1, y - s * 0.2), (x + s, y - s * 0.2), (x + s * 0.9, y + s * 0.3), (x + s * 0.2, y + s * 0.3)], 1.0)], 0.004) * k
    return G + T.lines([(x - s * 0.1, y - s * 0.1, x + s * 0.1, y - s * 0.1, 1.0)], s * 0.08) * k


def _biceps(T, x, y, s, lado, k):
    """O braço dobrado mostrando o músculo (lado = -1 esquerda, 1 direita)."""
    pts = [(0, 0.3), (0.5 * lado, 0.25), (0.75 * lado, 0.0), (0.7 * lado, -0.45), (0.85 * lado, -0.75), (0.6 * lado, -0.8), (0.5 * lado, -0.4),
           (0.3 * lado, -0.35), (0.15 * lado, -0.15), (0, -0.1)]
    return icone(T, poe(pts, x, y, s), k * 1.1, 0.55)


# ------------------------------------------------------------------ Jiraiya

def rasengan_jiraiya(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.2, 0.42), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        x = -0.5 + 0.9 * u
        g, h = _rasengan(T, x, -0.05, 0.08 + 0.06 * min(1, t / 0.2), t, k)
        G, H = G + g, H + h
        if u > 0:
            G += T.tapered([(x - 0.4, -0.05, x - 0.08, -0.05, 0.8)], 0.06) * k
    g, h = clarao(T, t, 0.38, 0.6, 0.45, -0.05, 1.5, 1.4)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.4 + 0.05 * j, 0.8 + 0.05 * j, 0.05, 0.55 - 0.1 * j, 0.03, -0.05, 1.0, 1.3)
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        G += T.ring(0.2, 0.01, 0.45, -0.05) * m * (0.6 + 0.4 * math.sin(t * 30))
    return G * env, H * env


def invocacao_gamabunta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    s = ease_out(rel(t, 0.0, 0.25), 2)
    kc = 1 - rel(t, 0.85, 0.97)
    if s > 0:
        G += _selo_invocacao(T, -0.3, 0.36, 0.45 * s, kc)
    f = rel(t, 0.25, 0.6)
    if 0 < f < 1:
        for j in range(7):
            a = TAU * j / 7
            d = 0.3 * ease_out(f)
            G += T.gauss(-0.3 + d * math.cos(a), 0.05 + d * math.sin(a) * 0.6 - 0.2 * f, 0.08 + 0.08 * f) * (1 - f) * 0.9
    sapo = surge(t, 0.35, 0.6)
    if sapo > 0:
        g, h = _sapo(T, -0.3, 0.2, 0.32 * sapo, kc)
        G, H = G + g, H + h
        g, h = icone(T, poe(ESPADA, 0.0, -0.05, 0.18 * sapo, math.pi / 2 + 0.5), kc, 0.5)
        G, H = G + g, H + h
    m = surge(t, 0.6, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(3):
            G += T.ring(0.14, 0.012, 0.45, -0.2 + 0.15 * j, 3.0) * m * 1.2
    return G * env, H * env


def jiraiya_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _sapo(T, -0.15, 0.15, 0.28, 1.0)
    G, H = G + g, H + h
    for j in range(4):
        r = (t * 1.5 + j / 4) % 1
        G += T.ring(0.03 + 0.05 * r, 0.01, 0.2 + 0.08 * j, 0.0 - 0.45 * r) * (1 - r) * 1.3
    G += T.gauss(0.3, -0.05, 0.16) * (0.5 + 0.3 * math.sin(t * TAU * 3))
    for j in range(3):
        g, h = icone(T, poe(CHAMA, 0.35 + 0.12 * (j - 1), -0.1, 0.1 + 0.015 * math.sin(t * TAU * 2 + j)), 0.8, 0.6)
        G, H = G + g, H + h
    return G, H


def oleo_de_sapo_em_chamas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    u = rel(t, 0.05, 0.35)
    if 0 < u < 1:
        pts = [(-0.55 + 1.3 * v * ease_out(u), -0.15 + 0.15 * math.sin(math.pi * v) * -1 + 0.4 * v * v) for v in np.linspace(0, 1, 24)]
        G += T.polyline(pts, 0.04) * (1 - rel(u, 0.7, 1)) * 0.9
    fogo = pulso(t, 0.3, 0.9)
    if fogo > 0:
        q = np.random.default_rng(623 + int(t * 20))
        for _ in range(20):
            v = q.uniform(0, 1)
            x = -0.5 + 1.3 * v
            y = 0.1 - 0.1 * math.sin(math.pi * v) + q.uniform(-0.12, 0.12)
            g, h = icone(T, poe(CHAMA, x, y, 0.06 + 0.06 * v, -0.4), fogo, 0.6)
            G, H = G + g, H + h
        G += T.tapered([(-0.55, -0.05, 0.85, 0.05, 1.0)], 0.2) * fogo * 0.5
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.45 + 0.05 * i, 0.68 + 0.05 * i, cx, 0.0, 0.8, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.35, 1.0, 26, 624, 0.15, 0.0, 0.8, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Tsunade

def soco_de_cem_toneladas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2.3)
    k = 1 - rel(t, 0.45, 0.58)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.5 + 0.75 * u, -0.05, 2.6, 0)
        G += P * k
        H += nos * 0.5 * k
        G += T.tapered([(-0.95, -0.05, -0.65 + 0.75 * u, -0.05, 1.0)], 0.12) * k * 0.6
    g, h = clarao(T, t, 0.3, 0.55, 0.45, -0.05, 1.7, 1.6)
    G, H = G + g, H + h
    racha = ease_out(rel(t, 0.32, 0.55), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if racha > 0:
        for j in range(8):
            a = TAU * j / 8 + 0.2
            G += _zap(T, 625 + j, 0.45, 0.38, 0.45 + 0.4 * racha * math.cos(a), 0.38 + 0.12 * racha * math.sin(a), 0.012, 4, 0.15) * kk * 1.2
    G += onda_no_chao(T, t, 0.32, 0.9, 0.9, 0.38, 1.7)
    G += estouro(T, t, 0.32, 0.85, 18, 633, 0.45, -0.05, 0.65, 0.015)
    return G * env, H * env


def ninjutsu_medico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        for lado in (-1, 1):
            G += T.gauss(lado * 0.12, -0.2, 0.1, 0.07) * k * 1.3
            G += T.lines([(lado * 0.04 + lado * 0.04 * j, -0.27, lado * 0.06 + lado * 0.04 * j, -0.13, 1.0) for j in range(4)], 0.014) * k
        G += T.gauss(0.0, 0.0, 0.3, 0.2) * k * pulso(t, 0.15, 0.9) * 0.6
    for j in range(8):
        r = (t * 1.4 + j / 8) % 1
        H += T.gauss(-0.25 + 0.07 * j, 0.05 - 0.45 * r, 0.012) * math.sin(math.pi * r) * 1.6
    c = surge(t, 0.4, 0.6) * (1 - rel(t, 0.85, 1))
    if c > 0:
        g, h = icone(T, poe(CRUZ, 0.0, -0.5, 0.07 * c), 1.2, 0.8)
        G, H = G + g, H + h
    d = rel(t, 0.5, 0.95)
    if 0 < d < 1:
        for j in range(3):
            G += T.ring(0.025, 0.007, -0.1 + 0.1 * j, 0.0 - 0.4 * d) * (1 - d) * 1.2
    return G * env, H * env


def tsunade_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _losango(T, 0.0, -0.4, 0.1, 1.0)
    G, H = G + g, H + h
    H += T.gauss(0.0, -0.4, 0.05) * (0.6 + 0.4 * math.sin(t * TAU * 2)) * 2.0
    # as marcas do selo descendo pelo corpo
    for lado in (-1, 1):
        u = (t % 1)
        pts = [(lado * (0.06 + 0.2 * v + 0.05 * math.sin(v * 12)), -0.3 + 0.7 * v) for v in np.linspace(0, u, 20)]
        if len(pts) > 1:
            G += T.polyline(pts, 0.02) * 1.1
    G += T.gauss(0.0, 0.0, 0.25, 0.4) * 0.3
    return G, H


def forca_de_cem_selos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    g, h = _losango(T, -0.55, -0.45, 0.06, pulso(t, 0.0, 0.6) + 0.01)
    G, H = G + g, H + h
    u = rel(t, 0.05, 0.4)
    if u > 0:
        for lado in (-1, 1):
            pts = [(-0.55 + lado * (0.04 + 0.12 * v + 0.03 * math.sin(v * 12)), -0.4 + 0.7 * v) for v in np.linspace(0, min(1, u), 20)]
            if len(pts) > 1:
                G += T.polyline(pts, 0.012) * (1 - rel(t, 0.6, 0.75)) * 1.1
    # a luz descendo e o aliado caído levantando
    luz = pulso(t, 0.35, 0.95)
    if luz > 0:
        G += T.gauss(0.3, -0.1, 0.12, 0.6) * luz * 1.0
        H += T.lines([(0.3, -0.9, 0.3, 0.38, 1.0)], 0.012) * luz * 1.2
        sobe = ease_out(rel(t, 0.5, 0.85), 2)
        G += T.lines([(0.3, 0.38, 0.3 + 0.0, 0.38 - 0.5 * sobe, 1.0)], 0.05) * luz
        G += T.gauss(0.3, 0.38 - 0.55 * sobe, 0.05) * luz
    G += anel(T, t, 0.5, 0.9, 0.1, 0.9, 0.035, 0.38, 3.0, 1.4)
    for cx in (-0.45, 0.0, 0.45):
        g, h = icone(T, poe(CRUZ, cx, -0.5, 0.05), pulso(t, 0.55, 1.0), 0.8)
        G, H = G + g, H + h
    G += particulas(T, t, 0.45, 1.0, 20, 634, 0.3, 0.2, 0.3, 0.8, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Sailor Mars

def fogo_de_marte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.45)
    if 0 < u < 1:
        e = ease_out(u, 1.5)
        for j in range(10):
            v = j / 10
            if v > e:
                break
            x = -0.55 + 1.0 * v
            y = -0.05 + 0.12 * math.sin(v * 12 - t * 20)
            g, h = icone(T, poe(CHAMA, x, y, 0.09 + 0.06 * v, -math.pi / 2 + 0.3 * math.sin(v * 12)), 1 - rel(u, 0.85, 1), 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.35, 0.58, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    q = pulso(t, 0.45, 1.0)
    if q > 0:
        for j in range(4):
            g, h = icone(T, poe(CHAMA, 0.33 + 0.08 * j, 0.1 - 0.04 * (j % 2), 0.08 + 0.02 * math.sin(t * 25 + j)), q, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.35, 1.0, 14, 635, 0.45, 0.0, 0.25, 0.6, 0.012)
    return G * env, H * env


def pergaminho_sagrado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.05 + 0.06 * i, 0.35 + 0.06 * i)
        if 0 < u < 1:
            x = -0.7 + (cx + 0.7) * ease_out(u)
            g, h = _ofuda(T, x, -0.35 - 0.1 * math.sin(math.pi * u), 0.09, 0.3 * math.sin(u * 8), 1.0)
            G, H = G + g, H + h
        elif u >= 1:
            k = 1 - rel(t, 0.85, 0.97)
            g, h = _ofuda(T, cx, -0.35, 0.09, 0.0, k)
            G, H = G + g, H + h
            G += T.ring(0.25, 0.014, cx, 0.0, 0.9) * k * pulso(t, 0.35 + 0.06 * i, 1.0) * 1.2
    G += anel(T, t, 0.4, 0.85, 0.1, 0.9, 0.03, 0.38, 3.0, 1.3)
    for cx in (-0.45, 0.0, 0.45):
        g, h = clarao(T, t, 0.4, 0.6, cx, -0.05, 0.5, 0.8)
        G, H = G + g, H + h
    return G * env, H * env


def sailormars_preparo(T, t, rng):
    G, H = vazio(T)
    puxa = 0.7 + 0.3 * math.sin(t * TAU * 2)
    G += _arco(T, 0.1, -0.05, 0.4, puxa, 1.0)
    for j in range(5):
        a = TAU * j / 5 + t * TAU
        g, h = icone(T, poe(CHAMA, 0.1 + 0.35 * math.cos(a) * 0.6, -0.05 + 0.35 * math.sin(a), 0.06, a + math.pi / 2), 0.9, 0.6)
        G, H = G + g, H + h
    G += T.lines([(-0.25 - 0.2 * puxa, -0.05, 0.25, -0.05, 1.0)], 0.012) * 1.2
    H += T.gauss(0.25, -0.05, 0.03) * 2.0
    return G, H


def flecha_flamejante_de_marte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.4, 0.5))
    if k > 0:
        G += _arco(T, -0.45, -0.05, 0.35, 1 - rel(t, 0.25, 0.3), k)
    u = rel(t, 0.28, 0.5)
    if 0 < u < 1:
        x = -0.4 + 0.85 * ease_in(u, 1.5)
        G += T.tapered([(x - 0.4, -0.05, x, -0.05, 1.0)], 0.04) * 1.3
        for j in range(5):
            g, h = icone(T, poe(CHAMA, x - 0.08 * j, -0.05 + 0.03 * math.sin(t * 40 + j), 0.07 - 0.01 * j, -math.pi / 2), 1.0 - 0.15 * j, 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.48, 0.72, 0.45, -0.05, 1.8, 1.7)
    G, H = G + g, H + h
    G += anel(T, t, 0.5, 0.9, 0.05, 0.75, 0.05, -0.05, 1.0, 1.5)
    q = pulso(t, 0.55, 1.0)
    if q > 0:
        for j in range(6):
            a = TAU * j / 6
            g, h = icone(T, poe(CHAMA, 0.45 + 0.2 * math.cos(a), -0.05 + 0.2 * math.sin(a), 0.08), q, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.5, 1.0, 20, 636, 0.45, -0.05, 0.3, 0.7, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Steven

def escudo_da_rosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.35) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        G += T.ring(0.42 * s, 0.03, 0.0, -0.05, 0.9) * 1.3 + T.gauss(0.0, -0.05, 0.4 * s) * 0.3
        g, h = _rosa(T, 0.0, -0.05, 0.22 * s, 1.0, ease_out(rel(t, 0.15, 0.5)))
        G, H = G + g, H + h
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1))
    if m > 0:
        for cx in (-0.45, 0.0, 0.45):
            G += T.ring(0.24 * m, 0.012, cx, 0.0, 0.9) * 1.1
            g, h = icone(T, poe(CORACAO, cx, -0.42, 0.04 * m), 1.0, 0.8)
            G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.75, 0.1, 0.8, 0.035, -0.05, 1.0, 1.3)
    return G * env, H * env


def saliva_curativa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.35)
    if 0 < u < 1:
        x, y = -0.5 + 0.5 * ease_in(u), -0.3 + 0.2 * u
        g, h = icone(T, poe(GOTA, x, y, 0.1), 1.0, 0.8)
        G, H = G + g, H + h
        H += T.gauss(x, y, 0.02) * 2.0
    g, h = clarao(T, t, 0.33, 0.55, 0.0, -0.1, 0.8, 1.0)
    G, H = G + g, H + h
    for j in range(10):
        r = (t * 1.2 + j / 10) % 1
        a = TAU * j / 10
        H += T.gauss(0.25 * math.cos(a) * (1 - r * 0.5), -0.1 + 0.25 * math.sin(a) - 0.3 * r, 0.012) * math.sin(math.pi * r) * pulso(t, 0.3, 1.0) * 1.8
    c = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1))
    if c > 0:
        g, h = icone(T, poe(CORACAO, 0.0, -0.5, 0.07 * c), 1.2, 0.8)
        G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.25, 0.35) * pulso(t, 0.35, 1.0) * 0.3
    return G * env, H * env


def steven_preparo(T, t, rng):
    G, H = vazio(T)
    r = 0.15 + 0.12 * ((t * 0.5) % 1 if False else 0.5 + 0.5 * math.sin(t * TAU))
    G += T.ring(r, 0.016, 0.1, -0.05) * 1.3 + T.gauss(0.1, -0.05, r * 0.8) * 0.25
    H += T.arc_band(r * 0.75, 0.01, -2.4, -1.6, 1.0, 0, 0.1, -0.05, 0.0) * 1.4
    G += T.gauss(-0.15, 0.05, 0.08) * 0.8
    return G, H


def bolha_de_steven(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = rel(t, 0.05, 0.4)
    k = 1 - rel(t, 0.88, 0.98)
    if 0 < u < 1:
        x = -0.5 + 0.95 * ease_in(u, 1.4)
        G += T.ring(0.1, 0.014, x, -0.05) * 1.2
        H += T.arc_band(0.07, 0.006, -2.4, -1.6, 1.0, 0, x, -0.05, 0.0) * 1.4
    pega = ease_out(rel(t, 0.38, 0.6), 2)
    if pega > 0 and k > 0:
        flutua = 0.15 * rel(t, 0.55, 1.0) + 0.03 * math.sin(t * 8)
        r = 0.1 + 0.18 * pega
        G += T.ring(r, 0.018, 0.45, -0.05 - flutua) * k * 1.3 + T.gauss(0.45, -0.05 - flutua, r * 0.8) * k * 0.2
        H += T.arc_band(r * 0.75, 0.01, -2.4, -1.6, 1.0, 0, 0.45, -0.05 - flutua, 0.0) * k * 1.4
    g, h = clarao(T, t, 0.38, 0.55, 0.45, -0.05, 0.8, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Garnet

def futuro_previsto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.05, 0.3), 2) * (1 - rel(t, 0.85, 0.97))
    if abre > 0:
        g, h = _terceiro_olho(T, 0.0, -0.45, 0.16, abre, 1.0)
        G, H = G + g, H + h
    # as linhas do futuro: os caminhos se abrindo
    u = rel(t, 0.25, 0.7)
    if 0 < u < 1:
        for j in range(5):
            a = -0.9 + 0.45 * j
            pts = [(0.0 + 0.6 * v * math.cos(a) * ease_out(u), -0.4 + 0.6 * v * math.sin(a) * ease_out(u) + 0.05 * math.sin(v * 8 + j)) for v in np.linspace(0, 1, 16)]
            G += T.polyline(pts, 0.008) * (1 - u) * 1.2
    G += T.ring(0.4, 0.016, 0.0, 0.0, 0.9) * pulso(t, 0.35, 1.0) * 1.0
    G += particulas(T, t, 0.3, 1.0, 12, 637, 0.0, -0.1, 0.4, 0.3, 0.01)
    return G * env, H * env


def manoplas_garnet(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.58)
    if u > 0 and k > 0:
        for lado in (-1, 1):
            P, nos = _punho(T, -0.5 + 0.75 * u, -0.05 + lado * 0.12, 2.0, 0)
            G += P * k
            H += nos * 0.4 * k
    g, h = clarao(T, t, 0.3, 0.5, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    m = pulso(t, 0.35, 1.0)
    if m > 0:
        for j in range(4):
            G += _zap(T, 638 + j + int(t * 15), 0.3, -0.3 + 0.15 * j, 0.6, -0.25 + 0.15 * j, 0.009, 3, 0.4) * m * 1.3
    G += estouro(T, t, 0.32, 0.7, 12, 642, 0.45, -0.05, 0.5, 0.012)
    return G * env, H * env


def garnet_preparo(T, t, rng):
    G, H = vazio(T)
    junta = 0.5 + 0.5 * math.sin(t * TAU)
    for lado in (-1, 1):
        a = t * TAU * 2 + (0 if lado < 0 else math.pi)
        r = 0.3 * (1 - 0.7 * junta)
        g, h = icone(T, poe(GEMA, r * math.cos(a), -0.05 + r * math.sin(a) * 0.6, 0.15), 1.1, 0.7)
        G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.1) * junta * 1.2
    H += T.gauss(0.0, -0.05, 0.03) * junta * 2.0
    return G, H


def fusao_perfeita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    for lado in (-1, 1):
        a = t * 20
        r = 0.2 * (1 - ease_in(rel(t, 0.0, 0.2)))
        g, h = icone(T, poe(GEMA, -0.55 + lado * r * math.cos(a), -0.3 + r * math.sin(a), 0.07), 1 - rel(t, 0.2, 0.3), 0.7)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.15, 0.3, -0.55, -0.3, 0.8, 1.0)
    G, H = G + g, H + h
    u = ease_in(rel(t, 0.25, 0.45), 2.3)
    k = 1 - rel(t, 0.58, 0.7)
    if u > 0 and k > 0:
        for lado in (-1, 1):
            P, nos = _punho(T, -0.5 + 0.75 * u, -0.05 + lado * 0.15, 3.0, 0)
            G += P * k
            H += nos * 0.5 * k
        G += T.tapered([(-1.0, -0.05, -0.7 + 0.75 * u, -0.05, 1.0)], 0.16) * k * 0.6
    g, h = clarao(T, t, 0.42, 0.66, 0.45, -0.05, 2.0, 1.9)
    G, H = G + g, H + h
    for j in range(5):
        G += _zap(T, 643 + j + int(t * 15), 0.45, -0.05, 0.45 + 0.5 * math.cos(TAU * j / 5), -0.05 + 0.4 * math.sin(TAU * j / 5), 0.01, 4, 0.35) * pulso(t, 0.45, 0.9) * 1.3
    G += anel(T, t, 0.44, 0.85, 0.05, 0.8, 0.05, -0.05, 1.0, 1.5)
    return G * env, H * env


# ------------------------------------------------------------------ Johnny Bravo

def pose_johnny(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        for lado in (-1, 1):
            g, h = _biceps(T, -0.55 + lado * 0.1, 0.05, 0.38 * s, lado, 1.0)
            G, H = G + g, H + h
        G += _oculos(T, -0.55, -0.35, 0.08 * s, 1.0)
        # o topete brilhando
        G += T.arc_band(0.09 * s, 0.035, math.pi, TAU, 1.0, 0, -0.55, -0.48, 0.0) * 1.2
        H += T.flare(-0.5, -0.55, 0.12 * pulso(t, 0.2, 0.5) + 0.01, 0.3, 0.012) * 1.4
    p = surge(t, 0.35, 0.55) * (1 - rel(t, 0.85, 1))
    if p > 0:
        G += T.ring(0.33 * p, 0.016, -0.55, -0.05, 0.9) * 1.1
    for i, cx in enumerate((-0.05, 0.25, 0.55)):
        m = surge(t, 0.4 + 0.05 * i, 0.58 + 0.05 * i) * (1 - rel(t, 0.85, 1))
        if m > 0:
            g, h = icone(T, poe(CORACAO, cx, -0.45 - 0.05 * math.sin(t * 10 + i), 0.05 * m), 1.2, 0.8)
            G, H = G + g, H + h
    return G * env, H * env


def soco_de_karate(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.1, 0.3), 2.5)
    k = 1 - rel(t, 0.45, 0.58)
    if u > 0 and k > 0:
        x = -0.5 + 0.75 * u
        G += T.polys([([(x - 0.3, -0.1), (x + 0.05, -0.1), (x + 0.1, -0.05), (x + 0.05, 0.0), (x - 0.3, 0.0)], 1.0)], 0.004) * k * 1.1
        for j in range(3):
            G += T.tapered([(x - 0.6, -0.08 + 0.04 * j, x - 0.3, -0.08 + 0.04 * j, 0.8)], 0.012) * k
    g, h = clarao(T, t, 0.28, 0.48, 0.45, -0.05, 1.2, 1.3)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.6, 0.04, 0.45, 0.035, -0.05, 1.0, 1.3)
    G += estouro(T, t, 0.3, 0.65, 10, 648, 0.45, -0.05, 0.45, 0.012)
    return G * env, H * env


def johnny_preparo(T, t, rng):
    G, H = vazio(T)
    flex = 0.85 + 0.15 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        g, h = _biceps(T, lado * 0.12, 0.1, 0.45 * flex, lado, 1.0)
        G, H = G + g, H + h
    G += _oculos(T, 0.0, -0.35, 0.15, 1.0)
    H += T.flare(0.06, -0.33, 0.1 * (0.5 + 0.5 * math.sin(t * TAU * 2)) + 0.01, 0.3, 0.012) * 1.4
    return G, H


def musculos_de_aco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.4))
    if s > 0:
        for lado in (-1, 1):
            g, h = _biceps(T, -0.55 + lado * 0.1, 0.0, 0.32 * s, lado, 1.0)
            G, H = G + g, H + h
        H += T.flare(-0.45, -0.2, 0.15 * s + 0.01, 0.3, 0.012) * 1.2
    u = ease_in(rel(t, 0.3, 0.48), 2.3)
    k = 1 - rel(t, 0.6, 0.72)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.5 + 0.75 * u, -0.05, 3.0, 0)
        G += P * k
        H += nos * 0.5 * k
    g, h = clarao(T, t, 0.45, 0.66, 0.45, -0.05, 1.8, 1.7)
    G, H = G + g, H + h
    G += anel(T, t, 0.46, 0.85, 0.05, 0.7, 0.05, -0.05, 1.0, 1.5)
    m = pulso(t, 0.6, 1.0)
    if m > 0:
        G += T.lines([(0.75, -0.35, 0.75, -0.15, 1.0), (0.7, -0.21, 0.75, -0.15, 1.0), (0.8, -0.21, 0.75, -0.15, 1.0)], 0.012) * m * 1.2
    G += estouro(T, t, 0.46, 0.85, 14, 649, 0.45, -0.05, 0.6, 0.014)
    return G * env, H * env


REGISTRO = [
    ("rasengan_jiraiya", rasengan_jiraiya, GRANDE, "Jiraiya · o Rasengan e o estouro", False),
    ("invocacao_gamabunta", invocacao_gamabunta, GRANDE, "Jiraiya · o selo, a fumaça e o sapo gigante", False),
    ("jiraiya_preparo", jiraiya_preparo, MEDIA, "Jiraiya · o sapo e o óleo borbulhando (Preparo, laço)", True),
    ("oleo_de_sapo_em_chamas", oleo_de_sapo_em_chamas, GRANDE, "Jiraiya · o óleo e o fogo varrendo", False),
    ("soco_de_cem_toneladas", soco_de_cem_toneladas, GRANDE, "Tsunade · o soco e o chão rachando", False),
    ("ninjutsu_medico", ninjutsu_medico, GRANDE, "Tsunade · as mãos verdes de chakra", False),
    ("tsunade_preparo", tsunade_preparo, MEDIA, "Tsunade · o losango e as marcas (Preparo, laço)", True),
    ("forca_de_cem_selos", forca_de_cem_selos, GRANDE, "Tsunade · as marcas e a luz levantando o aliado", False),
    ("fogo_de_marte", fogo_de_marte, GRANDE, "Sailor Mars · o fogo em espiral", False),
    ("pergaminho_sagrado", pergaminho_sagrado, GRANDE, "Sailor Mars · os pergaminhos e o círculo sagrado", False),
    ("sailormars_preparo", sailormars_preparo, MEDIA, "Sailor Mars · o arco de fogo puxado (Preparo, laço)", True),
    ("flecha_flamejante_de_marte", flecha_flamejante_de_marte, GRANDE, "Sailor Mars · a flecha de fogo", False),
    ("escudo_da_rosa", escudo_da_rosa, GRANDE, "Steven · o escudo e a rosa abrindo", False),
    ("saliva_curativa", saliva_curativa, GRANDE, "Steven · a gota e os brilhinhos", False),
    ("steven_preparo", steven_preparo, MEDIA, "Steven · a bolha crescendo (Preparo, laço)", True),
    ("bolha_de_steven", bolha_de_steven, GRANDE, "Steven · a bolha prendendo o rival", False),
    ("futuro_previsto", futuro_previsto, GRANDE, "Garnet · o terceiro olho e as linhas do futuro", False),
    ("manoplas_garnet", manoplas_garnet, GRANDE, "Garnet · as manoplas e o choque", False),
    ("garnet_preparo", garnet_preparo, MEDIA, "Garnet · as duas gemas se juntando (Preparo, laço)", True),
    ("fusao_perfeita", fusao_perfeita, GRANDE, "Garnet · as manoplas gigantes e os raios", False),
    ("pose_johnny", pose_johnny, GRANDE, "Johnny Bravo · a pose e os corações", False),
    ("soco_de_karate", soco_de_karate, GRANDE, "Johnny Bravo · o golpe de karatê", False),
    ("johnny_preparo", johnny_preparo, MEDIA, "Johnny Bravo · os bíceps e os óculos (Preparo, laço)", True),
    ("musculos_de_aco", musculos_de_aco, GRANDE, "Johnny Bravo · os bíceps e o soco", False),
]
