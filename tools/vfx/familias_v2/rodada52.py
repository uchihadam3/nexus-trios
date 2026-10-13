"""Rodada 52 das habilidades próprias: Valak, Drácula, Xenomorfo, Predador, Darth Vader e Yoda.

Valak
- aparicao_de_valak: o rosto da freira surgindo no escuro diante de cada rival, os olhos amarelos (Confuso).
- sombra_profana: o hábito escuro envolvendo a Valak e a cruz virada (Protegido e Esquiva).
- valak_preparo: o Preparo da Possessão — a cruz de cabeça para baixo girando e os olhos piscando (laço).
- possessao: a sombra entrando no rival, os olhos dele ficando amarelos (Amaldiçoado).

Drácula
- mordida_do_conde: a capa abrindo, as presas e a vida voltando em gotas (Roubo de vida).
- nuvem_de_morcegos: a capa virando morcegos que voam em nuvem até o rival (Invocação).
- dracula_preparo: o Preparo do Fogo infernal — a capa erguida e as bolas de fogo girando (laço).
- fogo_infernal: as colunas de fogo do inferno subindo debaixo de todos os rivais (Queimando).

Xenomorfo
- segunda_mandibula: a cabeça alongada abrindo e a segunda boca disparando no rival (Envenenado).
- emboscada_xenomorfa: a sombra na parede, o sensor de movimento apitando e a mira (Marcado e Exposto).
- xenomorfo_preparo: o Preparo da Cauda perfurante — a cauda erguida balançando e a baba ácida (laço).
- cauda_perfurante: a cauda de lâmina atravessando o rival e o ácido (Envenenado).

Predador
- canhao_de_plasma: os três pontos vermelhos da mira e o tiro de plasma (Marcado).
- camuflagem_predador: o corpo ficando transparente em ondas de distorção (Esquiva).
- predador_preparo: o Preparo do Troféu — o disco de lâminas abrindo e girando (laço).
- trofeu: o disco de lâminas voando em arco, cortando e voltando.

Darth Vader
- esganadura_da_forca: a mão fechando e o rival suspenso, sem ar (Paralisado).
- sabre_vermelho_vader: o sabre de luz vermelho ligando e o corte pesado (Enfraquecido).
- vader_preparo: o Preparo do Lado sombrio — o sabre erguido e a respiração em ondas (laço).
- lado_sombrio: os relâmpagos vermelhos do lado sombrio e o corte final (Silenciado).

Yoda
- empurrao_da_forca: a mãozinha estendida e a onda da Força empurrando o rival (Atrasa o Preparo).
- escudo_da_forca: as bolhas verdes da Força sobre o trio (Barreira e Carga).
- yoda_preparo: o Preparo do Sabre do mestre — o Yoda flutuando na meditação e as pedras girando (laço).
- sabre_do_mestre: o sabre verde girando como um pião, os saltos e os cortes.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CHAMA, CRUZ, GOTA, anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao, particulas, poe,
                         raios, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _espiral(T, cx, cy, r, gira, k, w=0.01):
    pts = [(cx + r * u * math.cos(gira + u * 9), cy + r * u * math.sin(gira + u * 9) * 0.8) for u in np.linspace(0.05, 1, 30)]
    return T.polyline(pts, w) * k


def _freira(T, cx, cy, s, k, olhos=1.0):
    veu = [(0, -1.0), (0.55, -0.85), (0.75, -0.2), (0.85, 0.9), (-0.85, 0.9), (-0.75, -0.2), (-0.55, -0.85)]
    G, H = icone(T, poe(veu, cx, cy, s), k * 0.8, 0.3)
    rosto = [(math.cos(a) * 0.38, -0.15 + 0.5 * math.sin(a)) for a in np.linspace(0, TAU, 20)]
    g2, h2 = icone(T, poe(rosto, cx, cy, s), k * 1.1, 0.55)
    G, H = G + g2, H + h2
    for lado in (-1, 1):
        G = G + T.gauss(cx + lado * s * 0.15, cy - s * 0.25, s * 0.08) * k * -0.5
        H = H + T.gauss(cx + lado * s * 0.15, cy - s * 0.25, s * 0.035) * k * olhos * 2.2
    G = G + T.polyline([(cx - s * 0.15, cy + s * 0.1), (cx, cy + s * 0.05), (cx + s * 0.15, cy + s * 0.1)], s * 0.04) * k * 0.8
    return G, H


def _morcego(T, cx, cy, s, k, bate):
    corpo = [(math.cos(a) * 0.25, math.sin(a) * 0.4) for a in np.linspace(0, TAU, 14)]
    g, h = cheio(T, poe(corpo, cx, cy, s), k)
    for lado in (-1, 1):
        asa = [(0.2 * lado, -0.1), (0.6 * lado, -0.4 - 0.3 * bate), (1.0 * lado, -0.2 - 0.2 * bate), (0.85 * lado, 0.1), (0.65 * lado, 0.0),
               (0.5 * lado, 0.2), (0.35 * lado, 0.05)]
        g2, h2 = cheio(T, poe(asa, cx, cy, s), k)
        g, h = g + g2, h + h2
    return g, h


_CABECA_XENO = [(-0.9, 0.1), (-0.6, -0.15), (0.0, -0.3), (0.7, -0.5), (1.2, -0.55), (0.9, -0.3), (0.5, -0.1), (0.2, 0.1), (-0.3, 0.3), (-0.8, 0.35)]


def _cauda(T, x0, y0, x1, y1, t, w, k, onda=0.06):
    pts = []
    for u in np.linspace(0, 1, 24):
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + onda * math.sin(u * 7 - t * 12) * math.sin(math.pi * u)
        pts.append((x, y))
    G = T.tapered([(pts[j][0], pts[j][1], pts[j + 1][0], pts[j + 1][1], 1.0) for j in range(len(pts) - 1)], w) * k
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    c, sn = math.cos(ang), math.sin(ang)
    ponta = [(x1 + c * w * 3.5, y1 + sn * w * 3.5), (x1 - sn * w * 1.5, y1 + c * w * 1.5), (x1 + sn * w * 1.5, y1 - c * w * 1.5)]
    g, h = icone(T, ponta, k * 1.3, 0.6)
    return G + g, h


def _disco(T, cx, cy, s, gira, k, abre=1.0):
    G = T.ring(s * 0.35, s * 0.1, cx, cy) * k * 1.2
    G += T.gauss(cx, cy, s * 0.15) * k * 1.0
    for j in range(6):
        a = gira + TAU * j / 6
        pts = [(cx + s * 0.35 * math.cos(a - 0.2), cy + s * 0.35 * math.sin(a - 0.2)),
               (cx + s * (0.35 + 0.65 * abre) * math.cos(a + 0.25), cy + s * (0.35 + 0.65 * abre) * math.sin(a + 0.25)),
               (cx + s * 0.35 * math.cos(a + 0.4), cy + s * 0.35 * math.sin(a + 0.4))]
        G += T.polys([(pts, 1.0)], 0.003) * k * 1.3
    return G, T.gauss(cx, cy, s * 0.1) * k * 1.3


def _sabre(T, x, y, ang, s, liga, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s * 0.22, y - sn * s * 0.22, x, y, 1.0)], s * 0.06) * k * 1.1
    if liga > 0:
        x2, y2 = x + c * s * liga, y + sn * s * liga
        G += T.tapered([(x, y, x2, y2, 1.0)], s * 0.09) * k * 0.8
        G += T.lines([(x, y, x2, y2, 1.0)], s * 0.035) * k * 1.4
        H = T.lines([(x, y, x2, y2, 1.0)], s * 0.018) * k * 1.4
        return G, H
    return G, 0.0


def _bolha(T, cx, cy, r, k):
    G = T.ring(r, r * 0.08, cx, cy) * k * 1.2
    G += T.gauss(cx, cy, r * 0.85) * k * 0.2
    H = T.arc_band(r * 0.7, r * 0.08, -2.6, -1.8, 1.0, 0, cx, cy, 1.0) * k * 0.9
    return G, H


# ------------------------------------------------------------------ Valak

def aparicao_de_valak(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    kk = 1 - rel(t, 0.82, 0.95)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        s = ease_out(rel(t, 0.1 + 0.15 * i, 0.3 + 0.15 * i), 2)
        if s > 0 and kk > 0:
            treme = 0.01 * math.sin(t * 60 + i)
            g, h = _freira(T, cx + treme, -0.3, 0.22 * (0.6 + 0.4 * s), kk * s, 1.0 if (t * 6 + i) % 1 < 0.8 else 0.2)
            G, H = G + g, H + h
            G += T.gauss(cx, -0.25, 0.2) * s * kk * -0.15
        k2 = surge(t, 0.5 + 0.08 * i, 0.7 + 0.08 * i) * kk
        if k2 > 0:
            G += _espiral(T, cx, 0.1, 0.1 * k2, -t * 8, 1.2, 0.011)
    return G * env, H * env


def sombra_profana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        for m in range(3):
            a = t * 3 + m * 2.1
            G += T.arc_band(0.3 + 0.04 * m, 0.06, a, a + 3.0, 0.8, 0, 0.0, 0.0, 1.0) * k * 0.8
        G += T.gauss(0.0, 0.0, 0.3, 0.38) * k * 0.35
        g, h = icone(T, poe(CRUZ, 0.0, -0.05, 0.1, math.pi), k * 1.2, 0.5)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(lado * 0.04, -0.28, 0.012) * k * 2.0
    for m in range(3):
        tm = t - 0.08 * (m + 1)
        if tm > 0.3:
            x = 0.15 * (m + 1) * math.sin(tm * 6)
            G += T.gauss(x, 0.0, 0.2, 0.3) * 0.12 * (1 - rel(t, 0.85, 0.97))
    return G * env, H * env


def valak_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(CRUZ, 0.0, 0.0, 0.15, math.pi + 0.3 * math.sin(t * TAU)), 1.1, 0.5)
    G, H = G + g, H + h
    pisca = 1.0 if (t * 1.6) % 1 < 0.85 else 0.1
    for lado in (-1, 1):
        H += T.gauss(lado * 0.08, -0.32, 0.016) * pisca * 2.2
        G += T.gauss(lado * 0.08, -0.32, 0.04) * pisca * 0.8
    G += T.gauss(0.0, 0.0, 0.3) * 0.15
    return G, H


def possessao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = _freira(T, -0.55, -0.2, 0.21 * s, 1.0)
        G, H = G + g, H + h
    u = rel(t, 0.25, 0.55)
    if 0 < u < 1:
        x = -0.4 + 0.85 * ease_in(u, 1.2)
        for m in range(4):
            G += T.gauss(x - 0.06 * m, -0.1 + 0.05 * math.sin(u * 10 + m), 0.08 - 0.012 * m, 0.06) * (0.5 - 0.1 * m)
    k = pulso(t, 0.5, 1.0)
    if k > 0:
        G += T.gauss(0.45, 0.0, 0.18, 0.25) * k * 0.4
        for lado in (-1, 1):
            H += T.gauss(0.45 + lado * 0.05, -0.12, 0.014) * k * 2.2
    g2, h2 = clarao(T, t, 0.5, 0.72, 0.45, 0.0, 1.5, 1.4)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.52, 0.88, 0.05, 0.6, 0.04, 0.0)
    G += particulas(T, t, 0.55, 1.0, 12, 132, 0.45, 0.0, 0.15, 0.4, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Drácula

def _capa(T, cx, cy, s, abre, k):
    pts = [(cx, cy - s * 0.6), (cx + s * (0.3 + 0.7 * abre), cy - s * (0.8 + 0.1 * abre)), (cx + s * (0.4 + 0.8 * abre), cy + s * 0.4),
           (cx + s * 0.2, cy + s * 0.9), (cx - s * 0.2, cy + s * 0.9), (cx - s * (0.4 + 0.8 * abre), cy + s * 0.4),
           (cx - s * (0.3 + 0.7 * abre), cy - s * (0.8 + 0.1 * abre))]
    return icone(T, pts, k, 0.3)


def mordida_do_conde(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.5, 0.62)
    u = ease_in(rel(t, 0.15, 0.35), 2)
    if k > 0:
        g, h = _capa(T, -0.3 + 0.55 * u, 0.0, 0.3, abre, k)
        G, H = G + g, H + h
    for lado in (-1, 1):
        kk = pulso(t, 0.3, 0.55)
        if kk > 0:
            G += T.polys([([(0.45 + lado * 0.04, -0.12), (0.45 + lado * 0.07, -0.12), (0.45 + lado * 0.055, -0.0)], 1.0)], 0.002) * kk * 1.5
    g2, h2 = clarao(T, t, 0.32, 0.52, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g2, H + h2
    for j in range(7):
        w = rel(t, 0.45 + 0.04 * j, 0.95)
        if 0 < w < 1:
            x = 0.45 - 1.0 * ease_in(w)
            y = -0.05 * (j - 3) * (1 - w) - 0.15 * math.sin(math.pi * w)
            g3, h3 = cheio(T, poe(GOTA, x, y, 0.028, -math.pi / 2), (1 - rel(w, 0.8, 1)) * 1.2)
            G, H = G + g3, H + h3
    G += T.gauss(-0.55, 0.0, 0.15) * pulso(t, 0.8, 1.0) * 0.6
    return G * env, H * env


def nuvem_de_morcegos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.2, 0.35))
    if abre > 0:
        g, h = _capa(T, -0.55, 0.0, 0.25, 1.0, abre)
        G, H = G + g, H + h
    q = np.random.default_rng(133)
    for j in range(14):
        a0 = 0.15 + q.uniform(0, 0.2)
        u = rel(t, a0, a0 + 0.55)
        if 0 < u < 1:
            x = -0.55 + 1.0 * ease_in(u, 1.1) + 0.1 * math.sin(u * 12 + j)
            y = q.uniform(-0.3, 0.2) - 0.15 * math.sin(math.pi * u) + 0.05 * math.sin(u * 15 + j)
            g, h = _morcego(T, x, y, 0.07, 1.1, math.sin(t * 40 + j))
            G, H = G + g, H + h
            H += T.gauss(x + 0.01, y - 0.005, 0.005) * 1.5
    k = pulso(t, 0.6, 1.0)
    if k > 0:
        G += T.gauss(0.45, 0.0, 0.18) * k * 0.35
    return G * env, H * env


def dracula_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _capa(T, 0.0, 0.1, 0.28, 0.9, 1.0)
    G, H = G + g, H + h
    for j in range(3):
        a = t * TAU + TAU * j / 3
        x, y = 0.4 * math.cos(a), -0.15 + 0.15 * math.sin(a)
        g2, h2 = icone(T, poe(CHAMA, x, y, 0.06 + 0.01 * math.sin(t * 20 + j)), 1.2, 0.7)
        G, H = G + g2, H + h2
        H += T.gauss(x, y + 0.02, 0.02) * 1.3
    for lado in (-1, 1):
        H += T.gauss(lado * 0.05, -0.38, 0.012) * 2.0
    return G, H


def fogo_infernal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        sobe = ease_out(rel(t, 0.15 + 0.08 * i, 0.4 + 0.08 * i), 2)
        k = 1 - rel(t, 0.75 + 0.05 * i, 0.9 + 0.05 * i)
        G += T.ring(0.16 * min(1, rel(t, 0.05 + 0.08 * i, 0.2 + 0.08 * i) * 1.0 + 0.0), 0.02, cx, 0.35, 3.0) * (1 - rel(t, 0.4, 0.6)) * 1.3
        if sobe > 0 and k > 0:
            alto = 0.7 * sobe
            G += T.gauss(cx, 0.35 - alto * 0.5, 0.1, alto * 0.5 + 0.01) * k * 0.8
            for m in range(5):
                y = 0.35 - alto * (m / 5)
                g, h = icone(T, poe(CHAMA, cx + 0.04 * math.sin(t * 20 + m + i), y, 0.08 + 0.02 * math.sin(t * 15 + m), 0.0), k * (1.1 - 0.12 * m), 0.7)
                G, H = G + g, H + h
            H += T.gauss(cx, 0.35 - alto * 0.3, 0.03, alto * 0.3 + 0.01) * k * 0.8
    G += particulas(T, t, 0.25, 1.0, 26, 134, 0.0, 0.2, 0.8, 0.8, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Xenomorfo

def segunda_mandibula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.6, 0.72))
    if s > 0:
        g, h = icone(T, poe(_CABECA_XENO, -0.4, -0.05, 0.32 * s), 1.1, 0.35)
        G, H = G + g, H + h
        H += T.lines([(-0.45, -0.07, -0.2, -0.13, 1.0)], 0.006) * s * 1.0
    u = ease_in(rel(t, 0.25, 0.38), 2) * (1 - ease_in(rel(t, 0.42, 0.55), 2))
    if u > 0:
        x0, x1 = -0.12, -0.12 + 0.5 * u
        G += T.lines([(x0, 0.0, x1, 0.0, 1.0)], 0.022) * 1.2
        G += T.ring(0.03, 0.012, x1, 0.0) * 1.3
        for m in range(3):
            G += T.lines([(x1 + 0.02, -0.02 + 0.02 * m, x1 + 0.05, -0.02 + 0.02 * m, 1.0)], 0.006) * 1.3
    g2, h2 = clarao(T, t, 0.35, 0.55, 0.45, 0.0, 1.0, 1.1)
    G, H = G + g2, H + h2
    q = np.random.default_rng(135)
    for j in range(8):
        w = rel(t, 0.38 + 0.03 * j, 0.95)
        if 0 < w < 1:
            vx = q.uniform(-0.15, 0.15)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx, 0.0 + 0.4 * w * w, 0.026), (1 - w) * 1.1)
            G, H = G + g3, H + h3
    G += particulas(T, t, 0.4, 1.0, 12, 136, 0.45, 0.2, 0.15, 0.3, 0.014)
    return G * env, H * env


def emboscada_xenomorfa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = 1 - rel(t, 0.85, 0.97)
    G += T.arc_band(0.35, 0.012, -math.pi * 0.75, -math.pi * 0.25, 1.0, 0, -0.55, 0.3, 0.0) * k * 0.9
    for m in range(3):
        G += T.arc_band(0.12 + 0.11 * m, 0.006, -math.pi * 0.75, -math.pi * 0.25, 1.0, 0, -0.55, 0.3, 0.0) * k * 0.5
    a = -math.pi * 0.75 + math.pi * 0.5 * ((t * 1.5) % 1)
    G += T.lines([(-0.55, 0.3, -0.55 + 0.35 * math.cos(a), 0.3 + 0.35 * math.sin(a), 1.0)], 0.008) * k * 1.2
    for j in range(3):
        bip = pulso(t, 0.15 + 0.18 * j, 0.28 + 0.18 * j)
        if bip > 0:
            H += T.gauss(-0.48 + 0.04 * j, 0.03 + 0.02 * j, 0.012) * bip * 2.0
            G += T.ring(0.02 + 0.05 * bip, 0.006, -0.48 + 0.04 * j, 0.03 + 0.02 * j) * bip * 1.2
    sombra = ease_out(rel(t, 0.3, 0.55), 2) * (1 - rel(t, 0.85, 0.97))
    if sombra > 0:
        g, h = icone(T, poe(_CABECA_XENO, 0.3, -0.4, 0.14, 0.3), sombra * 0.6, 0.25)
        G, H = G + g, H + h
        G += _cauda(T, 0.15, -0.35, 0.0, -0.2, t, 0.012, sombra * 0.8)[0]
    m = surge(t, 0.55, 0.75) * k
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.0) * 1.2
        for a2 in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.13 * m * math.cos(a2), 0.13 * m * math.sin(a2), 0.45 + 0.26 * m * math.cos(a2), 0.26 * m * math.sin(a2), 1.0)], 0.01) * 1.3
    return G * env, H * env


def xenomorfo_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(_CABECA_XENO, -0.1, 0.0, 0.26), 1.0, 0.35)
    G, H = G + g, H + h
    bal = 0.08 * math.sin(t * TAU * 1.5)
    g2, h2 = _cauda(T, -0.25, 0.25, 0.25 + bal, -0.35, t, 0.016, 1.0)
    G, H = G + g2, H + h2
    u = (t * 2) % 1
    g3, h3 = cheio(T, poe(GOTA, 0.05, 0.05 + 0.3 * u * u, 0.02), (1 - rel(u, 0.85, 1)) * 1.2)
    return G + g3, H + h3


def cauda_perfurante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        x1 = -0.4 + 0.95 * u
        y1 = -0.3 + 0.3 * u
        g, h = _cauda(T, -0.6, 0.2, x1, y1, t, 0.02, k * 1.1, 0.08 * (1 - u))
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.32, 0.55, 0.45, 0.0, 1.5, 1.4)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.34, 0.75, 0.05, 0.5, 0.04, 0.0)
    q = np.random.default_rng(137)
    for j in range(12):
        w = rel(t, 0.35 + 0.025 * j, 0.95)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.4), q.uniform(-0.45, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.03), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    G += particulas(T, t, 0.4, 1.0, 14, 138, 0.45, 0.25, 0.25, 0.4, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Predador

def canhao_de_plasma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    mira = pulso(t, 0.0, 0.45)
    if mira > 0:
        for j in range(3):
            a = -math.pi / 2 + TAU * j / 3 + t * 2
            x, y = 0.45 + 0.04 * math.cos(a), 0.04 * math.sin(a)
            H += T.gauss(x, y, 0.01) * mira * 2.2
            G += T.gauss(x, y, 0.025) * mira * 0.9
            G += T.lines([(-0.5, -0.3, x, y, 1.0)], 0.003) * mira * 0.6
    c = pulso(t, 0.15, 0.4)
    if c > 0:
        G += T.gauss(-0.5, -0.3, 0.06 + 0.03 * c) * c * 1.2
        H += T.gauss(-0.5, -0.3, 0.02) * c * 1.6
    u = rel(t, 0.38, 0.55)
    if 0 < u < 1:
        x, y = -0.5 + 0.95 * ease_in(u), -0.3 + 0.3 * ease_in(u)
        G += T.gauss(x, y, 0.05) * 1.4
        H += T.gauss(x, y, 0.02) * 1.8
        G += T.tapered([(x - 0.35, y - 0.11, x, y, 0.8)], 0.06) * 1.0
    g2, h2 = clarao(T, t, 0.52, 0.75, 0.45, 0.0, 1.4, 1.4)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.54, 0.9, 0.05, 0.55, 0.04, 0.0)
    G += estouro(T, t, 0.54, 0.9, 12, 139, 0.45, 0.0, 0.45, 0.013)
    return G * env, H * env


def camuflagem_predador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    some = ease_in(rel(t, 0.1, 0.6), 1.3)
    corpo = [(-0.2, 0.4), (-0.26, -0.05), (-0.18, -0.3), (-0.08, -0.4), (0.08, -0.4), (0.18, -0.3), (0.26, -0.05), (0.2, 0.4)]
    g, h = icone(T, corpo, (1 - some) * 0.9 + 0.1, 0.35 * (1 - some))
    G, H = G + g, H + h
    for m in range(6):
        y = -0.4 + 0.15 * m
        fase = (t * 2 + m * 0.17) % 1
        G += T.lines([(-0.28 + 0.04 * math.sin(t * 20 + m), y, 0.28 + 0.04 * math.sin(t * 17 + m), y, 1.0)], 0.006) * some * (0.4 + 0.6 * fase) * 1.0
    for j in range(3):
        u = rel(t, 0.15 + 0.15 * j, 0.6 + 0.15 * j)
        if 0 < u < 1:
            G += T.ring(0.2 + 0.25 * u, 0.008, 0.0, 0.0, 0.7) * (1 - u) * 1.0
    if some > 0.3:
        for lado in (-1, 1):
            H += T.gauss(lado * 0.05, -0.3, 0.008) * pulso(t, 0.4, 1.0) * 1.5
    return G * env, H * env


def predador_preparo(T, t, rng):
    G, H = vazio(T)
    abre = 0.6 + 0.4 * math.sin(t * TAU * 2)
    g, h = _disco(T, 0.0, 0.0, 0.4, t * TAU * 1.5, 1.1, abre)
    G, H = G + g, H + h
    for j in range(3):
        a = -math.pi / 2 + TAU * j / 3
        H += T.gauss(0.04 * math.cos(a), -0.38 + 0.04 * math.sin(a), 0.008) * 1.8
    return G, H


def trofeu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.75)
    if 0 < u < 1:
        if u < 0.5:
            v = ease_in(u * 2, 1.2)
            x, y = -0.55 + 1.0 * v, -0.1 - 0.35 * math.sin(math.pi * v)
        else:
            v = ease_out((u - 0.5) * 2, 1.2)
            x, y = 0.45 - 1.0 * v, -0.1 + 0.3 * math.sin(math.pi * v)
        g, h = _disco(T, x, y, 0.2, t * 40, 1.2, 1.0)
        G, H = G + g, H + h
        G += T.gauss(x, y, 0.13) * 0.25
    for j in range(2):
        g2, h2 = corte(T, t, 0.35 + 0.05 * j, 0.55 + 0.05 * j, 0.6 - 1.2 * j, 0.9, 0.07, 0.45, 0.0)
        G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.37, 0.6, 0.45, 0.0, 1.6, 1.5)
    G, H = G + g3, H + h3
    G += estouro(T, t, 0.38, 0.85, 16, 140, 0.45, 0.0, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Darth Vader

def esganadura_da_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if k > 0:
        for j in range(4):
            a = -0.5 + 0.33 * j
            L = 0.12 * (1 - 0.6 * fecha)
            x0, y0 = -0.5, -0.15
            G += T.lines([(x0, y0, x0 + L * math.cos(a), y0 + L * math.sin(a), 1.0),
                          (x0 + L * math.cos(a), y0 + L * math.sin(a), x0 + L * math.cos(a) + 0.05 * fecha, y0 + L * math.sin(a) + 0.04 * fecha, 1.0)], 0.014) * k * 1.2
        G += T.gauss(-0.52, -0.15, 0.05) * k * 0.8
    sobe = ease_out(rel(t, 0.25, 0.5), 2)
    if sobe > 0 and k > 0:
        y = -0.12 * sobe
        aperta = 0.6 + 0.4 * math.sin(t * 35)
        G += T.ring(0.07, 0.016, 0.45, -0.18 + y, 0.45) * k * aperta * 1.3
        G += T.gauss(0.45, y, 0.12, 0.2) * k * 0.3
        for j in range(3):
            G += T.arc_band(0.1 + 0.05 * j, 0.008, 0.0, TAU, 0.4, 0, 0.45, -0.18 + y, 0.0) * k * pulso((t * 2 + j / 3) % 1, 0.0, 1.0) * 0.7
        G += onda_no_chao(T, t, 0.3, 0.6, 0.3, 0.38, 0.8)
    G += converge(T, t, 0.2, 0.6, 10, 141, 0.45, -0.15, 0.4, 0.007)
    return G * env, H * env


def sabre_vermelho_vader(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    liga = ease_out(rel(t, 0.0, 0.18), 2)
    u = ease_in(rel(t, 0.22, 0.42), 2)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        ang = -2.2 + 2.6 * u
        g, h = _sabre(T, -0.05 + 0.05 * math.cos(ang), 0.25, ang, 0.6, liga, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.55, 0.06, ang - 1.0, ang, 1.0, 0, -0.05, 0.25, 1.0) * k * 0.7
    g2, h2 = corte(T, t, 0.35, 0.55, 0.7, 1.2, 0.08, 0.45, 0.0)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.37, 0.58, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g3, H + h3
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.3 + 0.1 * j + 0.1 * rel(t, 0.55, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.07 * m), (0.52, y0)], 0.014) * m * 1.2
    return G * env, H * env


def vader_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _sabre(T, 0.0, 0.3, -math.pi / 2, 0.65, 1.0, 1.0)
    G, H = G + g, H + h
    resp = (t * 1.2) % 1
    G += T.arc_band(0.2 + 0.25 * resp, 0.01, -0.6, 0.6, 1.0, 0, 0.0, 0.0, 0.0) * (1 - resp) * 1.0
    G += T.arc_band(0.2 + 0.25 * resp, 0.01, math.pi - 0.6, math.pi + 0.6, 1.0, 0, 0.0, 0.0, 0.0) * (1 - resp) * 1.0
    return G, H


def lado_sombrio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.45)
    if k > 0:
        for j in range(3):
            G += _zap(T, int(t * 35) + 5 * j, -0.5, -0.1 + 0.05 * (j - 1), 0.45, 0.0 + 0.06 * (j - 1), 0.012, 5, 0.25) * k * 1.3
        H += _zap(T, int(t * 35), -0.5, -0.1, 0.45, 0.0, 0.005, 5, 0.25) * k
        G += raios(T, t, 0.1, 0.45, 4, 142, 0.45, 0.0, 0.2, 0.008)
    liga = ease_out(rel(t, 0.3, 0.42), 2)
    u = ease_in(rel(t, 0.42, 0.58), 2)
    kk = 1 - rel(t, 0.68, 0.78)
    if liga > 0 and kk > 0:
        ang = -2.3 + 2.7 * u
        g, h = _sabre(T, 0.05, 0.25, ang, 0.65, liga, kk)
        G, H = G + g, H + h
    g2, h2 = corte(T, t, 0.52, 0.7, 0.7, 1.3, 0.09, 0.45, 0.0)
    G, H = G + g2 * 1.3, H + h2
    g3, h3 = clarao(T, t, 0.53, 0.78, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g3, H + h3
    m = surge(t, 0.7, 0.85) * (1 - rel(t, 0.9, 1))
    if m > 0:
        G += T.ring(0.07 * m, 0.012, 0.45, -0.3) * 1.3
        G += T.lines([(0.4, -0.35, 0.5, -0.25, 1.0)], 0.012) * m * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Yoda

def empurrao_da_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = pulso(t, 0.0, 0.5)
    if s > 0:
        for j in range(3):
            a = -0.3 + 0.3 * j
            G += T.lines([(-0.55, 0.05, -0.55 + 0.09 * math.cos(a), 0.05 + 0.09 * math.sin(a), 1.0)], 0.014) * s * 1.2
        G += T.gauss(-0.55, 0.05, 0.04) * s * 1.0
    for j in range(4):
        u = rel(t, 0.1 + 0.06 * j, 0.5 + 0.06 * j)
        if 0 < u < 1:
            x = -0.45 + 0.9 * ease_out(u)
            G += T.arc_band(0.12 + 0.12 * u, 0.025 * (1 - 0.5 * u), -0.9, 0.9, 1.0, 0, x - 0.1, 0.0, 0.0) * (1 - rel(u, 0.7, 1)) * 1.2
    g, h = clarao(T, t, 0.4, 0.6, 0.45, 0.0, 1.1, 1.2)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.42, 0.8, 0.5, 0.35, 1.2)
    rec = ease_out(rel(t, 0.45, 0.65), 2) * (1 - rel(t, 0.85, 1))
    if rec > 0:
        G += T.tapered([(0.45, 0.0, 0.45 + 0.2 * rec, -0.02, 1.0)], 0.04) * 0.8
        G += T.ring(0.08, 0.01, 0.6, -0.3) * rec * 1.2
        G += T.lines([(0.6, -0.3, 0.6 - 0.05 * rec, -0.3 - 0.04, 1.0)], 0.008) * rec * 1.2
    return G * env, H * env


def escudo_da_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.1 + 0.08 * i, 0.35 + 0.08 * i)
        if s > 0 and k > 0:
            g, h = _bolha(T, cx, 0.05, 0.22 * s, k)
            G, H = G + g, H + h
            onda = (t * 1.2 + 0.3 * i) % 1
            G += T.ring(0.22 * s * onda, 0.006, cx, 0.05) * (1 - onda) * k * 1.0
    G += converge(T, t, 0.0, 0.3, 10, 143, 0.0, 0.0, 0.6, 0.007)
    G += particulas(T, t, 0.4, 1.0, 16, 144, 0.0, 0.05, 0.6, 0.3, 0.01)
    return G * env, H * env


def yoda_preparo(T, t, rng):
    G, H = vazio(T)
    flut = 0.03 * math.sin(t * TAU)
    corpo = [(-0.55, -0.25), (-0.25, -0.1), (-0.18, -0.3), (0.18, -0.3), (0.25, -0.1), (0.55, -0.25), (0.25, 0.05), (0.2, 0.3), (-0.2, 0.3), (-0.25, 0.05)]
    g, h = icone(T, poe(corpo, 0.0, -0.05 + flut, 0.5), 1.0, 0.4)
    G, H = G + g, H + h
    G += T.gauss(0.0, 0.35, 0.2, 0.04) * 0.4
    for j in range(4):
        a = t * TAU * 0.7 + TAU * j / 4
        x, y = 0.4 * math.cos(a), 0.0 + 0.15 * math.sin(a)
        pedra = [(-1, -0.4), (-0.3, -0.9), (0.6, -0.7), (1, 0.1), (0.4, 0.8), (-0.6, 0.6)]
        g2, h2 = icone(T, poe(pedra, x, y, 0.04, a), 1.0, 0.45)
        G, H = G + g2, H + h2
    return G, H


def sabre_do_mestre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.55)
    if 0 < u < 1:
        x = -0.55 + 0.95 * ease_in(u, 1.1)
        y = -0.1 - 0.25 * abs(math.sin(u * TAU * 1.5))
        a = t * 30
        g, h = _sabre(T, x, y, a, 0.3, 1.0, 1.0)
        G, H = G + g, H + h
        g2, h2 = _sabre(T, x, y, a + math.pi, 0.3, 1.0, 0.6)
        G, H = G + g2 * 0.5, H + h2 * 0.5
        G += T.ring(0.22, 0.01, x, y) * 0.6
    for j, ang in enumerate((0.8, -0.8, 0.1, 1.4)):
        a0 = 0.42 + 0.06 * j
        g3, h3 = corte(T, t, a0, a0 + 0.16, ang, 0.8, 0.06, 0.45, 0.0)
        G, H = G + g3 * 1.2, H + h3
    g4, h4 = clarao(T, t, 0.45, 0.72, 0.45, 0.0, 1.6, 1.5)
    G, H = G + g4, H + h4
    G += estouro(T, t, 0.5, 0.9, 14, 145, 0.45, 0.0, 0.5, 0.013)
    return G * env, H * env


REGISTRO = [
    ("aparicao_de_valak", aparicao_de_valak, GRANDE, "Valak · a freira surgindo no escuro", False),
    ("sombra_profana", sombra_profana, GRANDE, "Valak · o hábito e a cruz virada", False),
    ("valak_preparo", valak_preparo, MEDIA, "Valak · a cruz virada e os olhos (Preparo, laço)", True),
    ("possessao", possessao, GRANDE, "Valak · a sombra entrando no rival", False),
    ("mordida_do_conde", mordida_do_conde, GRANDE, "Drácula · a capa, as presas e o sangue voltando", False),
    ("nuvem_de_morcegos", nuvem_de_morcegos, GRANDE, "Drácula · a nuvem de morcegos", False),
    ("dracula_preparo", dracula_preparo, MEDIA, "Drácula · a capa e o fogo girando (Preparo, laço)", True),
    ("fogo_infernal", fogo_infernal, GRANDE, "Drácula · as colunas de fogo", False),
    ("segunda_mandibula", segunda_mandibula, GRANDE, "Xenomorfo · a segunda boca", False),
    ("emboscada_xenomorfa", emboscada_xenomorfa, GRANDE, "Xenomorfo · o sensor e a sombra", False),
    ("xenomorfo_preparo", xenomorfo_preparo, MEDIA, "Xenomorfo · a cauda erguida (Preparo, laço)", True),
    ("cauda_perfurante", cauda_perfurante, GRANDE, "Xenomorfo · a cauda atravessando", False),
    ("canhao_de_plasma", canhao_de_plasma, GRANDE, "Predador · os três pontos e o plasma", False),
    ("camuflagem_predador", camuflagem_predador, GRANDE, "Predador · a camuflagem", False),
    ("predador_preparo", predador_preparo, MEDIA, "Predador · o disco abrindo (Preparo, laço)", True),
    ("trofeu", trofeu, GRANDE, "Predador · o disco voando e voltando", False),
    ("esganadura_da_forca", esganadura_da_forca, GRANDE, "Darth Vader · a mão fechando e o rival suspenso", False),
    ("sabre_vermelho_vader", sabre_vermelho_vader, GRANDE, "Darth Vader · o sabre vermelho", False),
    ("vader_preparo", vader_preparo, MEDIA, "Darth Vader · o sabre erguido e a respiração (Preparo, laço)", True),
    ("lado_sombrio", lado_sombrio, GRANDE, "Darth Vader · os relâmpagos e o corte", False),
    ("empurrao_da_forca", empurrao_da_forca, GRANDE, "Yoda · a onda da Força", False),
    ("escudo_da_forca", escudo_da_forca, GRANDE, "Yoda · as bolhas da Força", False),
    ("yoda_preparo", yoda_preparo, MEDIA, "Yoda · a meditação e as pedras (Preparo, laço)", True),
    ("sabre_do_mestre", sabre_do_mestre, GRANDE, "Yoda · o sabre girando e os cortes", False),
]
