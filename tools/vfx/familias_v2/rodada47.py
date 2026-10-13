"""Rodada 47 das habilidades próprias: Nêmesis, Zeus, Poseidon, Atena, Ares e Apolo.

Nêmesis
- tentaculo_do_nemesis: o tentáculo de carne saindo do braço e enrolando no rival (Preso).
- lanca_foguetes: o clarão do lança-foguetes, o foguete com o rastro de fogo e a marca vermelha piscando (Marca explosiva).
- nemesis_preparo: o Preparo da Perseguição sem fim — a sombra enorme com o olho aceso e os passos tremendo o chão (laço).
- perseguicao_sem_fim: as pegadas pesadas chegando e o soco enorme no rival (Lento).

Zeus
- raio_do_olimpo: o raio de Zeus arremessado e o estalo no rival (Eletrificado).
- egide: a Égide — o escudo redondo com a Górgona — surgindo sobre o trio (Escudo e Protegido).
- zeus_preparo: o Preparo da Fúria de Zeus — as nuvens se juntando e os relâmpagos dentro delas (laço).
- furia_de_zeus: as nuvens de tempestade e os raios enormes caindo seguidos no rival (Paralisado).

Poseidon
- tridente_de_poseidon: a estocada do tridente com o jato de água em espiral (Exposto).
- correnteza: a corrente varrendo os rivais e os redemoinhos prendendo cada um (Preso e Lento).
- poseidon_preparo: o Preparo do Maremoto — o tridente erguido e a água subindo em espiral (laço).
- maremoto: a onda gigante se erguendo e quebrando em cima de todos, a espuma e as gotas.

Atena
- escudo_de_atena: o escudo redondo com a coruja brilhando na frente de cada um do trio (Barreira e Escudo).
- lanca_da_sabedoria: a estocada da lança dourada e as folhas de oliveira (Enfraquecido).
- estrategia_divina: a coruja abrindo as asas e as linhas douradas ligando o trio (Fortalecido e Carga).

Ares
- espada_da_guerra: o corte pesado da espada larga e as brasas voando.
- grito_de_batalha_ares: o elmo de crista, o grito vermelho e as setas de força no trio (Fortalecido).
- ares_preparo: o Preparo do Massacre — a espada arrastando no chão, as faíscas e a aura vermelha (laço).
- massacre_de_ares: o salto, a espada cravando e o chão rachando em vermelho debaixo de todos (Exposto).

Apolo
- flecha_de_sol: o arco dourado, a flecha de sol e o clarão que cega (Cego).
- cura_de_apolo: o disco do sol sobre o aliado, os raios mornos descendo e as notas da lira (Vida e Regeneração).
- apolo_preparo: o Preparo da Carruagem do sol — o sol nascendo atrás com os raios girando (laço).
- carruagem_do_sol: o sol em chamas cruzando por cima dos rivais e o fogo chovendo (Queimando).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, FOLHA, GOTA, NOTA, RAIO, anel, cheio, clarao, corte, estouro, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _nuvem(T, cx, cy, s, k, seed, t):
    q = np.random.default_rng(seed)
    G = 0.0
    for _ in range(7):
        dx, dy = q.uniform(-1, 1) * s, q.uniform(-0.4, 0.4) * s
        r = s * q.uniform(0.4, 0.7) * (1 + 0.06 * math.sin(t * 5 + dx * 10))
        G = G + T.gauss(cx + dx, cy + dy, r, r * 0.7) * k
    return G


def _tentaculo(T, x0, y0, x1, y1, t, w, k, onda=0.06):
    pts = []
    for u in np.linspace(0, 1, 26):
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + onda * math.sin(u * 8 - t * 20) * math.sin(math.pi * u)
        pts.append((x, y))
    return T.polyline(pts, w) * k


# ------------------------------------------------------------------ Nêmesis

def tentaculo_do_nemesis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if u > 0 and k > 0:
        G += _tentaculo(T, -0.55, 0.05, -0.55 + 0.95 * u, 0.0, t, 0.045, k * 1.2)
        G += T.tapered([(-0.55 + 0.95 * u - 0.1, 0.0, -0.55 + 0.95 * u + 0.05, 0.0, 1.0)], 0.04) * k * 0.8
    enrola = ease_out(rel(t, 0.3, 0.55), 2)
    if enrola > 0 and k > 0:
        for m in range(3):
            a0 = -2.0 + 0.6 * m
            G += T.arc_band(0.15 - 0.015 * m, 0.03, a0, a0 + TAU * 0.85 * enrola, 0.4, 0, 0.45, -0.12 + 0.11 * m, 1.0) * k * 1.3
        aperta = 0.6 + 0.4 * math.sin(t * 30)
        G += T.gauss(0.45, 0.0, 0.12, 0.18) * enrola * k * 0.4 * aperta
    q = np.random.default_rng(42)
    for j in range(6):
        w = rel(t, 0.45 + 0.05 * j, 0.95)
        if 0 < w < 1:
            x = 0.35 + q.uniform(0, 0.2)
            g, h = cheio(T, poe(GOTA, x, 0.1 + 0.4 * w * w, 0.025), (1 - w) * 1.0)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.45, 0.0, 0.7, 0.9)
    return (G + g2) * env, (H + h2) * env


def _foguete(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    corpo = [(x + c * s, y + sn * s), (x + c * s * 0.6 - sn * s * 0.15, y + sn * s * 0.6 + c * s * 0.15),
             (x - c * s * 0.6 - sn * s * 0.15, y - sn * s * 0.6 + c * s * 0.15), (x - c * s * 0.8 - sn * s * 0.3, y - sn * s * 0.8 + c * s * 0.3),
             (x - c * s * 0.8 + sn * s * 0.3, y - sn * s * 0.8 - c * s * 0.3), (x - c * s * 0.6 + sn * s * 0.15, y - sn * s * 0.6 - c * s * 0.15),
             (x + c * s * 0.6 + sn * s * 0.15, y + sn * s * 0.6 - c * s * 0.15)]
    return icone(T, corpo, k * 1.2, 0.55)


def lanca_foguetes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.polys([([(-0.75, -0.06), (-0.5, -0.06), (-0.5, 0.06), (-0.75, 0.06)], 1.0)], 0.005) * pulso(t, 0.0, 0.5) * 0.9
    g, h = clarao(T, t, 0.05, 0.2, -0.48, 0.0, 0.6, 1.1)
    G, H = G + g, H + h
    u = ease_in(rel(t, 0.08, 0.38), 1.4)
    if 0 < u < 1:
        x = -0.45 + 0.85 * u
        g2, h2 = _foguete(T, x, 0.0, 0.0, 0.13, 1.0)
        G, H = G + g2, H + h2
        for m in range(4):
            g3, h3 = icone(T, poe(CHAMA, x - 0.12 - 0.05 * m, 0.0, 0.04 - 0.006 * m, math.pi / 2), 1.2 - 0.2 * m, 0.7)
            G, H = G + g3, H + h3
        G += T.gauss(x - 0.35, 0.0, 0.2, 0.05) * 0.35
    g4, h4 = clarao(T, t, 0.36, 0.55, 0.42, 0.0, 1.1, 1.3)
    G, H = G + g4, H + h4
    G += estouro(T, t, 0.38, 0.75, 12, 43, 0.42, 0.0, 0.4, 0.012)
    if t > 0.45:
        k = 1 - rel(t, 0.88, 1)
        pisca = 1.0 if (t * 7) % 1 < 0.5 else 0.25
        G += T.ring(0.13, 0.016, 0.45, 0.0) * pisca * k * 1.3
        H += T.gauss(0.45, 0.0, 0.025) * pisca * k * 1.8
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.15 * math.cos(a), 0.15 * math.sin(a), 0.45 + 0.22 * math.cos(a), 0.22 * math.sin(a), 1.0)], 0.011) * pisca * k * 1.3
    G += particulas(T, t, 0.4, 1.0, 14, 44, 0.42, 0.0, 0.15, 0.35, 0.02) * 0.6
    return G * env, H * env


def nemesis_preparo(T, t, rng):
    G, H = vazio(T)
    passo = (t * 2) % 1
    treme = 0.01 * math.sin(t * 60) * (1 - passo)
    corpo = [(-0.22, 0.4), (-0.28, -0.05), (-0.18, -0.3), (-0.08, -0.38), (0.08, -0.38), (0.18, -0.3), (0.28, -0.05), (0.22, 0.4)]
    g, h = icone(T, poe(corpo, treme, 0.0, 1.0), 0.6, 0.2)
    G, H = G + g, H + h
    b = 0.6 + 0.4 * math.sin(t * TAU * 2)
    H += T.gauss(0.05 + treme, -0.27, 0.018) * b * 2.0
    G += T.gauss(0.05 + treme, -0.27, 0.05) * b * 0.9
    G += T.ring(0.1 + 0.4 * passo, 0.02, 0, 0.42, 3.0) * (1 - passo) * 1.3
    return G, H


def perseguicao_sem_fim(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        a0 = 0.05 + 0.1 * j
        x = -0.75 + 0.27 * j
        k = pulso(t, a0, a0 + 0.5)
        if k > 0:
            pe = [(-0.6, -1), (0.6, -1), (0.7, 0.6), (0, 1), (-0.7, 0.6)]
            g, h = icone(T, poe(pe, x, 0.36 - 0.03 * (j % 2), 0.08, math.pi / 2), k * 1.1, 0.5)
            G, H = G + g, H + h
            G += anel(T, t, a0, a0 + 0.3, 0.03, 0.2, 0.02, 0.38, 3.0, 1.0)
    u = ease_in(rel(t, 0.38, 0.52), 2)
    k2 = 1 - rel(t, 0.6, 0.7)
    if u > 0 and k2 > 0:
        P, nos = _punho(T, -0.1 + 0.45 * u, 0.0, 2.6, 0)
        G += P * k2
        H += nos * 0.5 * k2
    g2, h2 = clarao(T, t, 0.5, 0.75, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.52, 0.9, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    G += onda_no_chao(T, t, 0.52, 0.95, 0.9, 0.38, 1.5)
    G += estouro(T, t, 0.52, 0.9, 16, 45, 0.45, 0.0, 0.6, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Zeus

def raio_do_olimpo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 1.4)
    c = pulso(t, 0.0, 0.2)
    if c > 0:
        g, h = icone(T, poe(RAIO, -0.6, -0.25, 0.14, -0.4), c * 1.4, 0.6)
        G, H = G + g, H + h
    if 0 < u < 1:
        x, y = -0.6 + 1.05 * u, -0.25 + 0.25 * u
        g, h = icone(T, poe(RAIO, x, y, 0.13, math.pi / 2 - 0.3), 1.5, 0.7)
        G, H = G + g, H + h
        H += T.gauss(x, y, 0.04) * 1.4
        G += T.tapered([(x - 0.4, y - 0.1, x, y, 0.8)], 0.05) * 0.8
    k = pulso(t, 0.28, 0.6)
    if k > 0:
        for j in range(3):
            G += _zap(T, int(t * 35) + j * 7, 0.45, 0.0, 0.45 + 0.35 * math.cos(j * 2.1 + 0.5), 0.3 * math.sin(j * 2.1 + 0.5), 0.012, 4, 0.3) * k * 1.3
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.3, 1.4)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.4, 0.95, 4, 46, 0.45, 0.0, 0.22, 0.008)
    return G * env, H * env


def _gorgona(T, cx, cy, s, k, t):
    G = T.ring(s, s * 0.12, cx, cy) * k * 1.3
    G += T.gauss(cx, cy, s * 0.9) * k * 0.35
    G += T.ring(s * 0.75, s * 0.04, cx, cy) * k * 0.9
    for j in range(10):
        a = TAU * j / 10
        pts = [(cx + s * (0.35 + 0.3 * v) * math.cos(a + 0.25 * math.sin(v * 6 + t * 6)),
                cy + s * (0.35 + 0.3 * v) * math.sin(a + 0.25 * math.sin(v * 6 + t * 6))) for v in np.linspace(0, 1, 8)]
        G += T.polyline(pts, s * 0.04) * k * 1.0
    for lado in (-1, 1):
        G += T.gauss(cx + lado * s * 0.12, cy - s * 0.05, s * 0.06) * k * 1.5
    G += T.lines([(cx - s * 0.12, cy + s * 0.15, cx + s * 0.12, cy + s * 0.15, 1.0)], s * 0.03) * k * 1.0
    return G


def egide(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    s = surge(t, 0.0, 0.3)
    if s > 0 and k > 0:
        G += _gorgona(T, 0.0, -0.3, 0.22 * s, k, t)
        H += T.gauss(0.0, -0.3, 0.05) * k * pulso(t, 0.0, 0.5) * 1.5
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        d = ease_out(rel(t, 0.25 + 0.05 * i, 0.55 + 0.05 * i), 2)
        if d > 0 and k > 0:
            G += T.arc_band(0.22, 0.03, math.pi, math.pi + math.pi * d, 1.0, 0, cx, 0.3, 0.0) * k * 1.3
            G += T.ring(0.22, 0.012, cx, 0.3, 4.0) * d * k * 1.0
            G += T.gauss(cx, 0.18, 0.17, 0.12) * d * k * 0.35
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.2 + 0.05 * i, 0.45 + 0.05 * i)
        if 0 < u < 1:
            G += T.tapered([(0.0, -0.3, cx * u, -0.3 + 0.45 * u, 1.0)], 0.02) * (1 - u) * 1.2
    return G * env, H * env


def zeus_preparo(T, t, rng):
    G, H = vazio(T)
    G += _nuvem(T, 0.0, -0.3, 0.25, 0.4, 47, t)
    flash = 1.0 if (t * 3.3) % 1 < 0.15 else 0.0
    if flash:
        G += _zap(T, int(t * 3.3), -0.1, -0.3, 0.05, -0.05, 0.01, 4, 0.4) * 1.4
        G += T.gauss(0.0, -0.3, 0.2, 0.1) * 0.6
    g, h = icone(T, poe(RAIO, 0.0, 0.2, 0.12, 0.0), 1.2 + 0.3 * math.sin(t * TAU * 2), 0.6)
    G, H = G + g, H + h
    H += T.gauss(0.0, 0.2, 0.03) * 1.2
    return G, H


def furia_de_zeus(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    nuv = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.8, 0.95))
    if nuv > 0:
        G += _nuvem(T, 0.3, -0.75, 0.45 * nuv, 0.28, 48, t)
    for j in range(4):
        a0 = 0.25 + 0.1 * j
        k = pulso(t, a0, a0 + 0.12)
        if k > 0:
            x0 = 0.3 + 0.2 * math.sin(j * 2.3)
            G += _zap(T, 50 + j, x0, -0.75, 0.45, 0.0, 0.035, 6, 0.22) * k * 1.5
            H += _zap(T, 50 + j, x0, -0.75, 0.45, 0.0, 0.012, 6, 0.22) * k * 1.3
    g, h = clarao(T, t, 0.25, 0.7, 0.45, 0.0, 2.0, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.75, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    G += onda_no_chao(T, t, 0.3, 0.85, 0.8, 0.38, 1.4)
    m = pulso(t, 0.6, 1.0)
    if m > 0:
        G += raios(T, t, 0.6, 1.0, 5, 49, 0.45, 0.0, 0.22, 0.008)
        G += T.ring(0.2, 0.012, 0.45, 0.0) * m * (0.6 + 0.4 * math.sin(t * 70)) * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Poseidon

def _tridente(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    hx, hy = x + c * s, y + sn * s
    G = T.lines([(x, y, hx, hy, 1.0)], s * 0.035) * k * 1.2
    G += T.lines([(hx - sn * s * 0.18, hy + c * s * 0.18, hx + sn * s * 0.18, hy - c * s * 0.18, 1.0)], s * 0.03) * k * 1.2
    for m in (-1, 0, 1):
        bx, by = hx + sn * s * 0.18 * m * -1, hy - c * s * 0.18 * m * -1
        G += T.lines([(bx, by, bx + c * s * 0.25, by + sn * s * 0.25, 1.0)], s * 0.03) * k * 1.2
        G += T.polys([([(bx + c * s * 0.32, by + sn * s * 0.32), (bx + c * s * 0.22 - sn * s * 0.05, by + sn * s * 0.22 + c * s * 0.05),
                        (bx + c * s * 0.22 + sn * s * 0.05, by + sn * s * 0.22 - c * s * 0.05)], 1.0)], 0.003) * k * 1.3
    return G


def tridente_de_poseidon(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.28), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        x = -0.85 + 0.6 * u
        G += _tridente(T, x, 0.0, 0.0, 0.65, k)
        if u > 0.2:
            for m in range(2):
                pts = [(x + 0.65 + v * (0.45 - x - 0.65), 0.07 * math.sin(v * 14 + t * 30 + m * math.pi)) for v in np.linspace(0, 1, 20)]
                G += T.polyline(pts, 0.014) * k * 1.2
    g, h = clarao(T, t, 0.25, 0.45, 0.45, 0.0, 1.1, 1.2)
    G, H = G + g, H + h
    q = np.random.default_rng(51)
    for j in range(12):
        w = rel(t, 0.28, 0.85)
        if 0 < w < 1:
            a = q.uniform(-math.pi * 0.9, -0.1)
            v = q.uniform(0.3, 0.6)
            x, y = 0.45 + v * w * math.cos(a), v * w * math.sin(a) + 0.7 * w * w
            g2, h2 = cheio(T, poe(GOTA, x, y, 0.025), (1 - w) * 1.2)
            G, H = G + g2, H + h2
    G += anel(T, t, 0.28, 0.7, 0.05, 0.4, 0.03, 0.0)
    return G * env, H * env


def correnteza(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for m in range(5):
        u = rel(t, 0.03 * m, 0.55 + 0.03 * m)
        if 0 < u < 1:
            y = -0.2 + 0.1 * m
            x0 = -1.0 + 2.0 * ease_out(u, 1.3)
            pts = [(x0 - 0.5 + 0.5 * v, y + 0.03 * math.sin(v * 10 + t * 15)) for v in np.linspace(0, 1, 16)]
            G += T.polyline(pts, 0.014) * (1 - rel(u, 0.7, 1)) * 1.2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = ease_out(rel(t, 0.3 + 0.05 * i, 0.5 + 0.05 * i), 2) * (1 - rel(t, 0.85, 0.97))
        if k > 0:
            for m in range(3):
                a = -t * 12 + m * 2.1
                G += T.arc_band(0.08 + 0.05 * m, 0.02, a, a + 2.4, 0.4, 0, cx, 0.3 - 0.07 * m, 1.0) * k * 1.3
            G += T.gauss(cx, 0.22, 0.12, 0.08) * k * 0.4
    return G * env, H * env


def poseidon_preparo(T, t, rng):
    G, H = vazio(T)
    G += _tridente(T, 0.0, 0.4, -math.pi / 2, 0.6, 1.0)
    H += T.gauss(0.0, -0.3, 0.03) * (1.2 + 0.4 * math.sin(t * TAU * 2))
    for m in range(2):
        pts = []
        for v in np.linspace(0, 1, 30):
            a = v * 12 + t * TAU * 2 + m * math.pi
            pts.append((0.13 * math.cos(a), 0.4 - 0.7 * v + 0.0 * math.sin(a)))
        G += T.polyline(pts, 0.013) * 1.1
    q = np.random.default_rng(52)
    for j in range(6):
        u = (t + j / 6) % 1
        x = q.uniform(-0.2, 0.2)
        g, h = cheio(T, poe(GOTA, x, 0.35 - 0.6 * u, 0.022, math.pi), (1 - u) * 1.0)
        G, H = G + g, H + h
    return G, H


def maremoto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.4), 2)
    avanca = ease_in(rel(t, 0.35, 0.7), 1.5)
    k = 1 - rel(t, 0.75, 0.88)
    if sobe > 0 and k > 0:
        x0 = -0.9 + 1.1 * avanca
        alto = 0.75 * sobe
        crista = []
        for v in np.linspace(0, 1, 30):
            x = x0 - 0.6 + 0.9 * v
            y = 0.38 - alto * math.sin(math.pi * v * 0.8) ** 1.5
            crista.append((x, y))
        cx, cy = crista[-1]
        for v in np.linspace(0, 1, 10):
            a = -math.pi / 2 + math.pi * 1.2 * v
            crista.append((cx + 0.15 * sobe * math.cos(a), cy + 0.15 * sobe + 0.15 * sobe * math.sin(a)))
        corpo = crista + [(x0 + 0.3, 0.4), (x0 - 0.6, 0.4)]
        G += T.polys([(corpo, 1.0)], 0.01) * k * 0.45
        G += T.polyline(crista, 0.025) * k * 1.4
        H += T.polyline(crista[:30], 0.008) * k * 0.8
        q = np.random.default_rng(int(t * 25))
        for _ in range(10):
            px, py = crista[q.integers(15, 38)]
            G += T.gauss(px + q.uniform(-0.04, 0.04), py + q.uniform(-0.04, 0.04), 0.012) * k * 1.4
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        g, h = clarao(T, t, 0.5 + 0.06 * i, 0.72 + 0.06 * i, cx, 0.0, 0.45, 0.9)
        G, H = G + g, H + h
    q = np.random.default_rng(53)
    for j in range(18):
        w = rel(t, 0.65, 1.0)
        if 0 < w < 1:
            x = q.uniform(-0.8, 0.8)
            v = q.uniform(0.2, 0.5)
            g2, h2 = cheio(T, poe(GOTA, x + 0.2 * w * q.uniform(-1, 1), -0.1 - v * w + 0.9 * w * w, 0.022), (1 - w) * 1.1)
            G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.6, 1.0, 1.0, 0.38, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ Atena

def _coruja(T, cx, cy, s, k, asas=0.0):
    G, H = 0.0, 0.0
    corpo = [(0, -0.75), (0.35, -0.95), (0.45, -0.55), (0.45, 0.35), (0.2, 0.8), (-0.2, 0.8), (-0.45, 0.35), (-0.45, -0.55), (-0.35, -0.95)]
    g, h = icone(T, poe(corpo, cx, cy, s), k, 0.35)
    G, H = G + g, H + h
    for lado in (-1, 1):
        G = G + T.ring(s * 0.18, s * 0.04, cx + lado * s * 0.2, cy - s * 0.35) * k * 1.3
        H = H + T.gauss(cx + lado * s * 0.2, cy - s * 0.35, s * 0.05) * k * 1.5
        if asas > 0:
            pts = [(cx + lado * s * 0.4, cy - s * 0.3), (cx + lado * s * (0.4 + 1.2 * asas), cy - s * (0.3 + 0.5 * asas)),
                   (cx + lado * s * (0.4 + 1.1 * asas), cy + s * 0.1), (cx + lado * s * (0.4 + 0.7 * asas), cy + s * 0.45), (cx + lado * s * 0.4, cy + s * 0.35)]
            g2, h2 = icone(T, pts, k, 0.35)
            G, H = G + g2, H + h2
    G = G + T.polys([([(cx - s * 0.06, cy - s * 0.18), (cx + s * 0.06, cy - s * 0.18), (cx, cy - s * 0.05)], 1.0)], 0.003) * k * 1.2
    return G, H


def escudo_de_atena(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.05 + 0.07 * i, 0.3 + 0.07 * i)
        if s > 0 and k > 0:
            r = 0.2 * s
            G += T.ring(r, 0.025, cx, 0.0) * k * 1.3
            G += T.ring(r * 0.82, 0.01, cx, 0.0) * k * 1.0
            G += T.gauss(cx, 0.0, r * 0.9) * k * 0.3
            g, h = _coruja(T, cx, 0.02, r * 0.55, k * 1.0)
            G, H = G + g, H + h
            b = rel((t * 1.2 + 0.25 * i) % 1, 0.0, 1.0)
            a = -2.4 + 1.6 * b
            H += T.gauss(cx + r * 0.85 * math.cos(a), r * 0.85 * math.sin(a), 0.015) * k * 1.6
    G += anel(T, t, 0.3, 0.75, 0.1, 1.0, 0.03, 0.0, 2.0)
    return G * env, H * env


def lanca_da_sabedoria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.42, 0.52)
    if k > 0:
        x = -0.75 + 1.0 * u
        G += T.lines([(x - 0.6, 0.0, x, 0.0, 1.0)], 0.018) * k * 1.2
        g, h = icone(T, [(x + 0.18, 0.0), (x, -0.06), (x - 0.03, 0.0), (x, 0.06)], k * 1.4, 0.6)
        G, H = G + g, H + h
        if u > 0.3:
            G += T.tapered([(x - 0.5, 0.0, x + 0.1, 0.0, 1.0)], 0.07) * k * 0.6
    g2, h2 = clarao(T, t, 0.22, 0.42, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.24, 0.6, 0.05, 0.4, 0.03, 0.0)
    q = np.random.default_rng(54)
    for j in range(8):
        w = rel(t, 0.25 + 0.03 * j, 0.9)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0)
            d = 0.1 + 0.35 * ease_out(w)
            g3, h3 = icone(T, poe(FOLHA, 0.45 + d * math.cos(a), d * math.sin(a) + 0.3 * w * w, 0.035, a + w * 6), (1 - w) * 1.1, 0.5)
            G, H = G + g3, H + h3
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.3 + 0.1 * j + 0.1 * rel(t, 0.5, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.07 * m), (0.52, y0)], 0.014) * m * 1.2
    return G * env, H * env


def estrategia_divina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    s = surge(t, 0.0, 0.3)
    asas = ease_out(rel(t, 0.15, 0.45), 2)
    if s > 0 and k > 0:
        g, h = _coruja(T, 0.0, -0.45, 0.2 * s, k * 1.1, asas)
        G, H = G + g, H + h
    pontos = [(-0.55, 0.15), (0.0, 0.15), (0.55, 0.15)]
    u = rel(t, 0.35, 0.65)
    if u > 0 and k > 0:
        for (x1, y1), (x2, y2) in ((pontos[0], pontos[1]), (pontos[1], pontos[2]), (pontos[0], (0.0, -0.45)), (pontos[2], (0.0, -0.45))):
            e = min(1.0, u * 1.3)
            G += T.lines([(x1, y1, x1 + (x2 - x1) * e, y1 + (y2 - y1) * e, 1.0)], 0.008) * k * 1.2
        for x, y in pontos:
            G += T.ring(0.05, 0.01, x, y) * k * 1.3
            H += T.gauss(x, y, 0.018) * k * 1.4
    for i, (cx, _) in enumerate(pontos):
        w = rel(t, 0.55 + 0.05 * i, 0.95)
        if 0 < w < 1:
            for m in range(2):
                y0 = 0.3 - 0.4 * w - 0.08 * m
                G += T.polyline([(cx - 0.06, y0 + 0.06), (cx, y0), (cx + 0.06, y0 + 0.06)], 0.014) * (1 - w) * 1.3
    G += particulas(T, t, 0.3, 0.95, 16, 55, 0.0, 0.0, 0.6, 0.4, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Ares

_ESPADA_LARGA = [(0, -1), (0.16, -0.8), (0.16, 0.3), (0.42, 0.3), (0.42, 0.42), (0.1, 0.42), (0.1, 0.85), (0.18, 0.92),
                 (0, 1.0), (-0.18, 0.92), (-0.1, 0.85), (-0.1, 0.42), (-0.42, 0.42), (-0.42, 0.3), (-0.16, 0.3), (-0.16, -0.8)]


def espada_da_guerra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.32), 2)
    k = 1 - rel(t, 0.45, 0.58)
    if k > 0:
        ang = -2.5 + 2.8 * u
        cx, cy = 0.05 + 0.3 * math.cos(ang), 0.15 + 0.3 * math.sin(ang)
        g, h = icone(T, poe(_ESPADA_LARGA, cx, cy, 0.32, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.55, 0.09, ang - 1.0, ang, 1.0, 0, 0.05, 0.15, 1.0) * k * 0.8
    g2, h2 = corte(T, t, 0.28, 0.5, 0.6, 1.3, 0.11, 0.45, 0.0, 0.1)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.3, 0.52, 0.45, 0.0, 1.3, 1.3)
    G, H = G + g3, H + h3
    q = np.random.default_rng(56)
    for j in range(14):
        w = rel(t, 0.3, 0.95)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0.2)
            v = q.uniform(0.3, 0.7)
            x, y = 0.45 + v * w * math.cos(a), v * w * math.sin(a) + 0.5 * w * w
            H += T.gauss(x, y, 0.008) * (1 - w) * 1.6
            G += T.gauss(x, y, 0.016) * (1 - w) * 1.0
    return G * env, H * env


_ELMO_CRISTA = [(-0.5, 0.6), (-0.55, -0.1), (-0.4, -0.5), (0.0, -0.65), (0.4, -0.5), (0.55, -0.1), (0.5, 0.6), (0.2, 0.6), (0.15, 0.1),
                (-0.15, 0.1), (-0.2, 0.6)]


def grito_de_batalha_ares(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        cx, cy = 0.0, -0.4
        g, h = icone(T, poe(_ELMO_CRISTA, cx, cy, 0.18 * s), 1.2, 0.4)
        G, H = G + g, H + h
        G += T.arc_band(0.2 * s, 0.05 * s, math.pi + 0.3, TAU - 0.3, 1.0, 0, cx, cy - 0.08 * s, 0.0) * 1.2
        for j in range(9):
            a = math.pi + 0.35 + (math.pi - 0.7) * j / 8
            G += T.lines([(cx + 0.18 * s * math.cos(a), cy - 0.08 * s + 0.18 * s * math.sin(a),
                           cx + 0.24 * s * math.cos(a), cy - 0.08 * s + 0.24 * s * math.sin(a), 1.0)], 0.01) * 1.1
    for j in range(4):
        u = rel(t, 0.15 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.ring(0.1 + 0.8 * u, 0.04 * (1 - 0.5 * u), 0.0, -0.4, 1.4) * (1 - u) * 1.2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        w = rel(t, 0.45 + 0.05 * i, 0.95)
        if 0 < w < 1:
            for m in range(2):
                y0 = 0.3 - 0.35 * w - 0.08 * m
                G += T.polyline([(cx - 0.07, y0 + 0.07), (cx, y0), (cx + 0.07, y0 + 0.07)], 0.016) * (1 - w) * 1.4
            G += T.gauss(cx, 0.15, 0.12) * pulso(w, 0.0, 1.0) * 0.4
    return G * env, H * env


def ares_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(_ESPADA_LARGA, 0.0, 0.05, 0.38, -2.2), 1.1, 0.5)
    G, H = G + g, H + h
    G += T.gauss(0.0, 0.0, 0.3, 0.35) * (0.18 + 0.08 * math.sin(t * TAU * 2))
    q = np.random.default_rng(int(t * 12))
    for _ in range(6):
        a = q.uniform(-math.pi * 0.95, -math.pi * 0.05)
        d = q.uniform(0.05, 0.25)
        x, y = 0.3 + d * math.cos(a), 0.38 + d * math.sin(a)
        H += T.gauss(x, y, 0.008) * 1.8
        G += T.lines([(0.3, 0.38, x, y, 1.0)], 0.004) * 1.0
    return G, H


def massacre_de_ares(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.35)
    if 0 < u < 1:
        x = -0.6 + 0.6 * u
        y = 0.1 - 0.6 * math.sin(math.pi * u)
        g, h = icone(T, poe(_ESPADA_LARGA, x, y, 0.22, math.pi * 0.9 * u), 1.2, 0.5)
        G, H = G + g, H + h
        G += T.gauss(x, y, 0.12) * 0.4
    k = 1 - rel(t, 0.8, 0.92)
    if t > 0.35 and k > 0:
        g, h = icone(T, poe(_ESPADA_LARGA, 0.0, 0.15, 0.25, math.pi), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.33, 0.6, 0.0, 0.35, 1.8, 1.6)
    G, H = G + g2, H + h2
    racha = ease_out(rel(t, 0.36, 0.55), 2)
    if racha > 0 and k > 0:
        for j in range(6):
            lado = -1 if j % 2 else 1
            alcance = (0.3 + 0.12 * (j // 2)) * racha
            G += _zap(T, 60 + j, 0.0, 0.38, lado * alcance, 0.38 + 0.04 * ((j % 3) - 1), 0.016, 4, 0.12) * k * 1.4
            H += _zap(T, 60 + j, 0.0, 0.38, lado * alcance, 0.38 + 0.04 * ((j % 3) - 1), 0.006, 4, 0.12) * k
    G += onda_no_chao(T, t, 0.36, 0.95, 1.1, 0.38, 1.7)
    for cx in (-0.55, 0.0, 0.55):
        G += estouro(T, t, 0.4, 0.85, 8, 61, cx, 0.3, 0.3, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Apolo

def _sol(T, cx, cy, r, gira, k, n=12):
    G = T.gauss(cx, cy, r * 0.9) * k * 1.2
    G += T.ring(r, r * 0.12, cx, cy) * k * 1.2
    segs = []
    for j in range(n):
        a = gira + TAU * j / n
        r2 = r * (1.6 if j % 2 else 1.35)
        segs.append((cx + r * 1.15 * math.cos(a), cy + r * 1.15 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a), 1.0))
    G += T.tapered(segs, r * 0.12) * k * 1.2
    return G, T.gauss(cx, cy, r * 0.4) * k * 1.4


def flecha_de_sol(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.arc_band(0.25, 0.022, -1.1, 1.1, 1.0, 0, -0.75, 0.0, 0.0) * pulso(t, 0.0, 0.4) * 1.2
    u = ease_in(rel(t, 0.08, 0.32), 1.4)
    if 0 < u < 1:
        x = -0.55 + 1.0 * u
        G += T.lines([(x - 0.3, 0.0, x, 0.0, 1.0)], 0.014) * 1.3
        g, h = _sol(T, x + 0.03, 0.0, 0.04, t * 10, 1.0, 8)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.7, 0.0, x - 0.2, 0.0, 1.0)], 0.05) * 0.8
    g2, h2 = clarao(T, t, 0.3, 0.65, 0.45, 0.0, 1.6, 1.6)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.3, 0.75, 0.05, 0.5, 0.035, 0.0)
    for j in range(10):
        a = TAU * j / 10 + 0.2
        k = pulso(t, 0.32, 0.8)
        if k > 0:
            G += T.tapered([(0.45 + 0.08 * math.cos(a), 0.08 * math.sin(a), 0.45 + 0.4 * k * math.cos(a), 0.4 * k * math.sin(a), 1.0)], 0.016) * k * 0.9
    return G * env, H * env


def cura_de_apolo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g, h = _sol(T, 0.0, -0.5, 0.1 * s, t * 1.5, 1.0)
        G, H = G + g, H + h
    k = pulso(t, 0.2, 0.95)
    if k > 0:
        for m in range(5):
            x = -0.2 + 0.1 * m
            G += T.tapered([(0.0 + 0.02 * (m - 2), -0.38, x, 0.25, 1.0)], 0.03) * k * 0.6
        G += T.gauss(0.0, 0.1, 0.25, 0.3) * k * 0.35
    q = np.random.default_rng(57)
    for j in range(5):
        u = rel(t, 0.3 + 0.08 * j, 0.8 + 0.08 * j)
        if 0 < u < 1:
            x = q.uniform(-0.3, 0.3)
            g2, h2 = icone(T, poe(NOTA, x + 0.05 * math.sin(u * 8), 0.2 - 0.4 * u, 0.04), (1 - rel(u, 0.7, 1)) * 1.2, 0.7)
            G, H = G + g2, H + h2
    G += particulas(T, t, 0.25, 1.0, 16, 58, 0.0, 0.2, 0.25, 0.5, 0.011)
    return G * env, H * env


def apolo_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _sol(T, 0.0, 0.05, 0.16, t * TAU * 0.5, 1.0, 16)
    G, H = G + g, H + h
    G += T.ring(0.34 + 0.03 * math.sin(t * TAU * 2), 0.01, 0.0, 0.05) * 0.8
    G += T.lines([(-0.45, 0.38, 0.45, 0.38, 1.0)], 0.008) * 0.8
    return G, H


def carruagem_do_sol(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.65)
    if 0 < u < 1:
        x = -1.0 + 2.0 * ease_in(u, 1.1)
        y = -0.55 + 0.1 * math.sin(math.pi * u)
        g, h = _sol(T, x, y, 0.13, t * 8, 1.0)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.8, y + 0.05, x - 0.1, y, 1.0)], 0.13) * 0.7
        for m in range(5):
            g2, h2 = icone(T, poe(CHAMA, x - 0.2 - 0.12 * m, y + 0.02 * math.sin(t * 30 + m), 0.07 - 0.008 * m, math.pi / 2), 1.1 - 0.15 * m, 0.7)
            G, H = G + g2, H + h2
    q = np.random.default_rng(59)
    for j in range(16):
        x = q.uniform(-0.8, 0.8)
        a0 = 0.15 + (x + 1.0) / 2.0 * 0.45
        w = rel(t, a0, a0 + 0.3)
        if 0 < w < 1:
            g3, h3 = icone(T, poe(CHAMA, x, -0.5 + 0.8 * ease_in(w), 0.045, math.pi), (1 - rel(w, 0.8, 1)) * 1.2, 0.7)
            G, H = G + g3, H + h3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.45 + 0.08 * i
        g4, h4 = clarao(T, t, a0, a0 + 0.2, cx, 0.1, 0.5, 1.0)
        G, H = G + g4, H + h4
        k = pulso(t, a0 + 0.1, 1.0)
        if k > 0:
            for m in range(3):
                g5, h5 = icone(T, poe(CHAMA, cx - 0.08 + 0.08 * m, 0.25 - 0.03 * math.sin(t * 20 + m), 0.04 + 0.01 * math.sin(t * 15 + m * 2)), k * 1.1, 0.7)
                G, H = G + g5, H + h5
    return G * env, H * env


REGISTRO = [
    ("tentaculo_do_nemesis", tentaculo_do_nemesis, GRANDE, "Nêmesis · o tentáculo enrolando", False),
    ("lanca_foguetes", lanca_foguetes, GRANDE, "Nêmesis · o foguete e a marca", False),
    ("nemesis_preparo", nemesis_preparo, MEDIA, "Nêmesis · a sombra e os passos (Preparo, laço)", True),
    ("perseguicao_sem_fim", perseguicao_sem_fim, GRANDE, "Nêmesis · as pegadas e o soco", False),
    ("raio_do_olimpo", raio_do_olimpo, GRANDE, "Zeus · o raio arremessado", False),
    ("egide", egide, GRANDE, "Zeus · a Égide sobre o trio", False),
    ("zeus_preparo", zeus_preparo, MEDIA, "Zeus · as nuvens e o raio na mão (Preparo, laço)", True),
    ("furia_de_zeus", furia_de_zeus, GRANDE, "Zeus · os raios caindo seguidos", False),
    ("tridente_de_poseidon", tridente_de_poseidon, GRANDE, "Poseidon · o tridente e o jato", False),
    ("correnteza", correnteza, GRANDE, "Poseidon · a corrente e os redemoinhos", False),
    ("poseidon_preparo", poseidon_preparo, MEDIA, "Poseidon · a água subindo no tridente (Preparo, laço)", True),
    ("maremoto", maremoto, GRANDE, "Poseidon · a onda gigante", False),
    ("escudo_de_atena", escudo_de_atena, GRANDE, "Atena · os escudos da coruja", False),
    ("lanca_da_sabedoria", lanca_da_sabedoria, GRANDE, "Atena · a lança e as folhas de oliveira", False),
    ("estrategia_divina", estrategia_divina, GRANDE, "Atena · a coruja e as linhas do trio", False),
    ("espada_da_guerra", espada_da_guerra, GRANDE, "Ares · a espada larga e as brasas", False),
    ("grito_de_batalha_ares", grito_de_batalha_ares, GRANDE, "Ares · o elmo e o grito", False),
    ("ares_preparo", ares_preparo, MEDIA, "Ares · a espada arrastando (Preparo, laço)", True),
    ("massacre_de_ares", massacre_de_ares, GRANDE, "Ares · o chão rachando em vermelho", False),
    ("flecha_de_sol", flecha_de_sol, GRANDE, "Apolo · a flecha de sol", False),
    ("cura_de_apolo", cura_de_apolo, GRANDE, "Apolo · o sol e as notas da lira", False),
    ("apolo_preparo", apolo_preparo, MEDIA, "Apolo · o sol nascendo (Preparo, laço)", True),
    ("carruagem_do_sol", carruagem_do_sol, GRANDE, "Apolo · o sol cruzando e o fogo chovendo", False),
]
