"""Rodada 59 das habilidades próprias: Rem, Kirito, Spike, Vash, Senku e Hinata.

Rem
- maca_de_ferro: a maça de espinhos na corrente girando e acertando o rival (Exposto).
- cura_de_agua_rem: a água azul girando em volta do aliado e as gotas curando (Vida e Regeneração).
- rem_preparo: o Preparo da Forma de oni — o chifre de luz na testa e a aura subindo (laço).
- forma_de_oni: o chifre acendendo, a maça descendo com força e o rival esmagado (Fortalecido).

Kirito
- vorpal_strike: a espada recuada brilhando e a estocada que atravessa o rival.
- parry_kirito: as duas espadas cruzadas defendendo e as faíscas (Protegido e Acelerado).
- kirito_preparo: o Preparo do Starburst Stream — as duas espadas brilhando (a preta e a azul) (laço).
- starburst_stream: as 16 estocadas das duas espadas em sequência no rival.

Spike
- jeet_kune_do: a postura de Bruce Lee e o chute rápido no rival.
- esquiva_spike: o corpo inclinando para trás e os tiros passando de raspão (Esquiva).
- spike_preparo: o Preparo do Tiro final — a Jericho apontada e o cigarro soltando fumaça (laço).
- tiro_final: o tiro único da Jericho atravessando e o "bang" no rival.

Vash
- tiro_desarmante: o tiro preciso derrubando a arma do rival (Enfraquecido e dissipa).
- tufao_humanoide: o casaco vermelho girando e as balas desviando (Esquiva e Acelerado).
- vash_preparo: o Preparo do Braço de anjo — o braço virando canhão e as penas de luz (laço).
- braco_de_anjo: as asas de luz e o raio gigante do Braço de anjo em todos os rivais.

Senku
- remedio_senku: o frasco de remédio e a cura no aliado, tirando um debuff (Vida e Purificar).
- bateria_senku: a bateria de cobre e zinco ligando os fios no trio e o choque no rival (Carga e Eletrificado).
- senku_preparo: o Preparo da Pólvora — as contas no ar e o frasco borbulhando (laço).
- polvora_senku: a mistura de pólvora, o pavio e a explosão em todos os rivais (Marca explosiva).

Hinata
- punho_suave: a palma com o chakra azul nos pontos de chakra do rival (Paralisado).
- rotacao_hinata: a cúpula de chakra girando em volta dela (Refletir e Protegido).
- hinata_preparo: o Preparo das 64 palmas — o Byakugan ativo e o círculo do trigrama no chão (laço).
- sessenta_e_quatro_palmas: as 64 palmas em sequência fechando os pontos de chakra (Silenciado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CRUZ, GOTA, PENA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _maca(T, x, y, s, k):
    """A maça de ferro: a bola com os espinhos em volta."""
    G = T.gauss(x, y, s * 0.55) * k * 0.9 + T.ring(s * 0.6, s * 0.1, x, y) * k * 1.2
    segs = [(x + s * 0.55 * math.cos(a), y + s * 0.55 * math.sin(a), x + s * 1.0 * math.cos(a), y + s * 1.0 * math.sin(a), 1.0)
            for a in np.linspace(0, TAU, 10, endpoint=False)]
    return G + T.tapered(segs, s * 0.16) * k * 1.3


def _espada_reta(T, x, y, ang, comp, larg, k):
    c, sn = math.cos(ang), math.sin(ang)
    px, py = -sn, c
    pts = [(x + px * larg, y + py * larg), (x + c * comp * 0.9 + px * larg, y + sn * comp * 0.9 + py * larg), (x + c * comp, y + sn * comp),
           (x + c * comp * 0.9 - px * larg, y + sn * comp * 0.9 - py * larg), (x - px * larg, y - py * larg)]
    g, h = icone(T, pts, k * 1.2, 0.6)
    G = g + T.lines([(x + px * larg * 2.5, y + py * larg * 2.5, x - px * larg * 2.5, y - py * larg * 2.5, 1.0)], larg * 0.6) * k
    G += T.lines([(x, y, x - c * comp * 0.22, y - sn * comp * 0.22, 1.0)], larg * 0.7) * k
    return G, h


def _pistola(T, x, y, s, k, ang=0.0):
    pts = [(-0.5, -0.12), (0.7, -0.12), (0.7, 0.05), (-0.05, 0.05), (-0.15, 0.55), (-0.45, 0.55), (-0.35, 0.05), (-0.5, 0.05)]
    return icone(T, poe(pts, x, y, s, ang), k * 1.2, 0.6)


def _frasco(T, x, y, s, k, bolha=0.0, t=0.0):
    pts = [(-0.15, -0.9), (0.15, -0.9), (0.15, -0.4), (0.6, 0.5), (0.5, 0.8), (-0.5, 0.8), (-0.6, 0.5), (-0.15, -0.4)]
    g, h = icone(T, poe(pts, x, y, s), k * 1.1, 0.4)
    G = g + T.polys([(poe([(-0.4, 0.3), (0.4, 0.3), (0.55, 0.55), (0.45, 0.75), (-0.45, 0.75), (-0.55, 0.55)], x, y, s), 1.0)], 0.003) * k * 0.6
    if bolha > 0:
        for j in range(3):
            r = (t * 2 + j / 3) % 1
            G += T.ring(s * (0.06 + 0.04 * r), s * 0.02, x + s * 0.2 * (j - 1), y + s * (0.5 - 1.6 * r)) * bolha * (1 - r) * 1.3
    return G, h


def _palma_aberta(T, x, y, s, k, ang=0.0):
    """A palma da mão aberta de frente para o rival (a palma do Punho suave)."""
    pts = [(-0.3, 0.6), (-0.35, -0.1), (-0.3, -0.6), (-0.18, -0.6), (-0.15, -0.15), (-0.05, -0.75), (0.07, -0.75), (0.08, -0.15),
           (0.16, -0.68), (0.28, -0.66), (0.24, -0.1), (0.36, -0.45), (0.46, -0.4), (0.35, 0.2), (0.25, 0.6)]
    return icone(T, poe(pts, x, y, s, ang), k * 1.1, 0.55)


def _byakugan(T, x, y, s, k):
    G = T.ring(s, s * 0.08, x, y, 1.8) * k * 1.2 + T.gauss(x, y, s * 0.4) * k * 0.5
    segs = []
    for lado in (-1, 1):
        for j in range(3):
            a = lado * (0.3 + 0.3 * j)
            segs.append((x + lado * s * 1.05, y + s * 0.2 * (j - 1) * 0.3, x + lado * s * (1.5 + 0.1 * j), y + s * 0.35 * (j - 1), 0.8))
    return G + T.lines(segs, s * 0.06) * k


def _trigrama(T, cx, cy, r, k, gira=0.0):
    """O círculo dos oito trigramas no chão: o anel e as três barras em cada direção."""
    G = (T.ring(r, 0.012, cx, cy, 3.0) + T.ring(r * 0.75, 0.008, cx, cy, 3.0)) * k * 1.1
    segs = []
    for j in range(8):
        a = TAU * j / 8 + gira
        for q in range(3):
            rr = r * (0.8 + 0.06 * q)
            x0, y0 = cx + rr * math.cos(a - 0.12), cy + rr * math.sin(a - 0.12) / 3
            x1, y1 = cx + rr * math.cos(a + 0.12), cy + rr * math.sin(a + 0.12) / 3
            segs.append((x0, y0, x1, y1, 1.0))
    return G + T.lines(segs, 0.006) * k


# ------------------------------------------------------------------ Rem

def maca_de_ferro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    gira = ease_in(rel(t, 0.0, 0.3), 1.4)
    voa = ease_in(rel(t, 0.3, 0.45), 2)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        if voa <= 0:
            a = TAU * 2.2 * gira
            bx, by = -0.55 + 0.25 * math.cos(a), -0.15 + 0.25 * math.sin(a) * 0.6
        else:
            bx, by = -0.55 + (1.0) * voa, -0.15 + 0.1 * voa
        pts = [(-0.55 + (bx + 0.55) * u, -0.15 + (by + 0.15) * u + 0.04 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 14)]
        G += T.polyline(pts, 0.012) * k * 1.1
        G += T.splats([(px, py, 1.0) for px, py in pts[1::2]], 0.008) * k
        G += _maca(T, bx, by, 0.2, k)
        if voa <= 0 and gira > 0:
            G += T.arc_band(0.25, 0.03, a - 2.0, a, 0.6, 0, -0.55, -0.15, 1.0) * k * 0.9
    g, h = clarao(T, t, 0.42, 0.62, 0.45, -0.05, 1.4, 1.4)
    G, H = G + g, H + h
    G += anel(T, t, 0.43, 0.75, 0.05, 0.6, 0.045, -0.05, 1.0, 1.4)
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        G += T.ring(0.2, 0.01, 0.45, -0.05) * m * (0.6 + 0.4 * math.sin(t * 30))
    G += estouro(T, t, 0.43, 0.85, 14, 601, 0.45, -0.05, 0.55, 0.013)
    return G * env, H * env


def cura_de_agua_rem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.95)
    for j in range(3):
        a0 = t * TAU * 1.5 + TAU * j / 3
        pts = [(0.3 * math.cos(a0 + u * 2.5), -0.05 + 0.3 * math.sin(a0 + u * 2.5) * 0.45 - 0.35 * (1 - u) * (j / 3)) for u in np.linspace(0, 1, 24)]
        segs = [(p[0], p[1], q[0], q[1], 0.3 + 0.7 * i / 24) for i, (p, q) in enumerate(zip(pts, pts[1:]))]
        G += T.lines(segs, 0.02) * k * 1.1
        H += T.gauss(pts[-1][0], pts[-1][1], 0.015) * k * 1.8
    for j in range(6):
        r = (t * 1.5 + j / 6) % 1
        g, h = icone(T, poe(GOTA, -0.25 + 0.1 * j, -0.6 + 0.6 * r, 0.04), k * (1 - r), 0.6)
        G, H = G + g, H + h
    c = surge(t, 0.4, 0.6) * (1 - rel(t, 0.85, 1))
    if c > 0:
        g, h = icone(T, poe(CRUZ, 0.0, -0.45, 0.07 * c), 1.2, 0.8)
        G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.25, 0.35) * k * 0.3
    return G * env, H * env


def rem_preparo(T, t, rng):
    G, H = vazio(T)
    pts = [(-0.04, -0.3), (0.0, -0.62), (0.04, -0.3)]
    g, h = icone(T, pts, 1.3, 0.9)
    G, H = G + g, H + h
    H += T.gauss(0.0, -0.5, 0.06) * (0.7 + 0.3 * math.sin(t * TAU * 3)) * 2.0
    G += T.gauss(0.0, -0.05, 0.25, 0.4) * (0.35 + 0.15 * math.sin(t * TAU * 2))
    for j in range(5):
        u = (t + j / 5) % 1
        x = -0.25 + 0.12 * j
        G += T.tapered([(x, 0.3 - 0.6 * u + 0.15, x, 0.3 - 0.6 * u, 0.8)], 0.02) * math.sin(math.pi * u)
    G += _maca(T, 0.35, 0.15, 0.08, 0.8)
    return G, H


def forma_de_oni(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    c = pulso(t, 0.0, 0.5)
    if c > 0:
        g, h = icone(T, [(-0.59, -0.3), (-0.55, -0.62), (-0.51, -0.3)], c * 1.3, 0.9)
        G, H = G + g, H + h
        H += T.gauss(-0.55, -0.5, 0.07) * c * 2.0
        G += T.gauss(-0.55, -0.1, 0.2, 0.35) * c * 0.5
    u = ease_in(rel(t, 0.2, 0.42), 2.3)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        a = -2.4 + 2.2 * u
        bx, by = -0.1 + 0.6 * math.cos(a), 0.3 + 0.6 * math.sin(a)
        G += T.polyline([(-0.1, 0.3), (bx, by)], 0.014) * k
        G += _maca(T, bx, by, 0.16, k)
        G += T.arc_band(0.6, 0.08, a - 0.9, a, 1.0, 0, -0.1, 0.3, 1.0) * k * 0.6
    g, h = clarao(T, t, 0.4, 0.65, 0.45, -0.05, 1.9, 1.8)
    G, H = G + g, H + h
    for j in range(5):
        lado = -1 if j % 2 else 1
        G += _zap(T, 602 + j, 0.45, 0.38, 0.45 + lado * (0.15 + 0.08 * (j // 2)) * ease_out(rel(t, 0.42, 0.6)), 0.38, 0.012, 4, 0.12) * (1 - rel(t, 0.85, 0.97)) * 1.2
    G += onda_no_chao(T, t, 0.42, 0.9, 0.85, 0.38, 1.6)
    G += estouro(T, t, 0.42, 0.85, 16, 607, 0.45, -0.05, 0.65, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Kirito

def vorpal_strike(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    recua = ease_out(rel(t, 0.0, 0.25), 2)
    avanca = ease_in(rel(t, 0.25, 0.4), 2.5)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        x = -0.6 - 0.1 * recua + 0.75 * avanca
        g, h = _espada_reta(T, x, -0.05, 0.0, 0.45, 0.035, k)
        G, H = G + g, H + h
        G += T.gauss(x + 0.3, -0.05, 0.08, 0.04) * pulso(t, 0.0, 0.35) * 1.4
        if avanca > 0:
            G += T.tapered([(-0.8, -0.05, x + 0.45, -0.05, 1.0)], 0.07) * k * 0.8
    u = rel(t, 0.38, 0.6)
    if 0 < u < 1:
        G += T.tapered([(0.3, -0.05, 0.3 + 0.6 * ease_out(u), -0.05, 1.0)], 0.06) * (1 - u) * 1.4
    g, h = clarao(T, t, 0.36, 0.56, 0.45, -0.05, 1.4, 1.4)
    G, H = G + g, H + h
    G += anel(T, t, 0.38, 0.7, 0.04, 0.45, 0.03, -0.05, 1.0, 1.3)
    return G * env, H * env


def parry_kirito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        g, h = _espada_reta(T, -0.2, 0.25, -0.9, 0.55 * s, 0.03, 1.0)
        G, H = G + g, H + h
        g, h = _espada_reta(T, 0.2, 0.25, -math.pi + 0.9, 0.55 * s, 0.03, 1.0)
        G, H = G + g, H + h
    for j in range(3):
        a0 = 0.25 + 0.15 * j
        g, h = clarao(T, t, a0, a0 + 0.12, 0.0, -0.17, 0.5, 0.9)
        G, H = G + g, H + h
        G += estouro(T, t, a0, a0 + 0.25, 8, 608 + j, 0.0, -0.17, 0.3, 0.008)
    G += T.ring(0.42, 0.016, 0.0, -0.05, 0.9) * pulso(t, 0.2, 1.0) * 0.9
    v = pulso(t, 0.4, 1.0)
    if v > 0:
        for j in range(4):
            y = -0.35 + 0.2 * j
            o = ((t * 3) + j * 0.31) % 1
            G += T.tapered([(-0.85 + 0.3 * o, y, -0.5 + 0.3 * o, y, 0.8)], 0.014) * v
    return G * env, H * env


def kirito_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.8 + 0.3 * math.sin(t * TAU * 2)
    g, h = _espada_reta(T, -0.25, 0.3, -1.25, 0.65, 0.035, p * 0.7)
    G, H = G + g, H + h
    g, h = _espada_reta(T, 0.25, 0.3, -math.pi + 1.25, 0.65, 0.035, p)
    G, H = G + g, H + h
    H += T.lines([(0.25, 0.3, 0.25 + 0.6 * math.cos(-math.pi + 1.25), 0.3 + 0.6 * math.sin(-math.pi + 1.25), 1.0)], 0.008) * p * 1.3
    return G, H


def starburst_stream(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.8, 0.9))
    q = np.random.default_rng(609)
    for j in range(16):
        a0 = 0.1 + 0.042 * j
        ang = q.uniform(-1.2, 1.2) + (math.pi if j % 2 else 0) * 0
        lado = -1 if j % 2 else 1
        u = rel(t, a0, a0 + 0.1)
        if 0 < u < 1:
            ex, ey = 0.45 + 0.08 * math.cos(ang), -0.05 + 0.15 * math.sin(ang) * lado
            G += T.tapered([(ex - 0.5 * math.cos(ang * 0.4), ey - 0.25 * lado * math.sin(ang * 0.4) * 0.5, ex, ey, 1.0)], 0.035) * (1 - u) * 1.5
            H += T.gauss(ex, ey, 0.02) * (1 - u) * 2.0
    if k > 0:
        g, h = _espada_reta(T, -0.45, -0.15, -0.3 + 0.2 * math.sin(t * 40), 0.45, 0.03, k * 0.7)
        G, H = G + g, H + h
        g, h = _espada_reta(T, -0.45, 0.05, 0.3 + 0.2 * math.sin(t * 40 + 1), 0.45, 0.03, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.75, 0.95, 0.45, -0.05, 1.8, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.76, 0.98, 0.05, 0.7, 0.045, -0.05, 1.0, 1.4)
    G += particulas(T, t, 0.15, 1.0, 26, 610, 0.45, -0.05, 0.3, 0.2, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Spike

def jeet_kune_do(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # a mão chamando ("vem") e o chute que estica
    m = pulso(t, 0.0, 0.3)
    if m > 0:
        for j in range(4):
            G += T.lines([(-0.55, -0.25 + 0.03 * j, -0.5 + 0.03 * math.sin(t * 30 + j), -0.3 + 0.03 * j, 1.0)], 0.012) * m
    u = ease_in(rel(t, 0.18, 0.35), 2.5)
    k = 1 - rel(t, 0.5, 0.62)
    if u > 0 and k > 0:
        x = -0.4 + 0.8 * u
        G += T.lines([(-0.45, 0.15, x, -0.05, 1.0)], 0.08) * k * 1.1
        G += T.polys([([(x - 0.03, -0.14), (x + 0.18, -0.11), (x + 0.18, 0.02), (x - 0.03, 0.04)], 1.0)], 0.004) * k * 1.2
        for j in range(3):
            G += T.tapered([(x - 0.4, -0.12 + 0.07 * j, x - 0.08, -0.12 + 0.07 * j, 0.7)], 0.015) * k
    g, h = clarao(T, t, 0.33, 0.52, 0.45, -0.05, 1.2, 1.3)
    G, H = G + g, H + h
    G += anel(T, t, 0.34, 0.65, 0.04, 0.5, 0.035, -0.05, 1.0, 1.3)
    G += estouro(T, t, 0.34, 0.7, 10, 611, 0.45, -0.05, 0.45, 0.012)
    return G * env, H * env


def esquiva_spike(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    inclina = pulso(t, 0.1, 0.7)
    # a silhueta inclinando para trás (os fantasmas)
    for j in range(3):
        a = -0.6 * inclina * (j + 1) / 3
        x0, y0 = 0.0, 0.35
        x1, y1 = x0 + 0.7 * math.sin(a), y0 - 0.7 * math.cos(a)
        G += T.lines([(x0, y0, x1, y1, 1.0)], 0.06) * (0.3 + 0.25 * j)
        G += T.gauss(x1, y1, 0.06) * (0.3 + 0.25 * j)
    for j in range(3):
        u = rel(t, 0.15 + 0.08 * j, 0.45 + 0.08 * j)
        if 0 < u < 1:
            y = -0.35 + 0.1 * j
            x = 0.9 - 1.8 * u
            G += T.tapered([(x + 0.25, y, x, y, 1.0)], 0.018) * 1.3
            H += T.gauss(x, y, 0.01) * 1.8
    G += T.ring(0.45, 0.012, 0.0, -0.05, 0.9) * pulso(t, 0.3, 1.0) * 0.8
    G += particulas(T, t, 0.3, 1.0, 10, 612, 0.0, -0.1, 0.4, 0.3, 0.01)
    return G * env, H * env


def spike_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _pistola(T, 0.0, 0.0, 0.5, 1.0)
    G, H = G + g, H + h
    H += T.gauss(0.35, -0.035, 0.02) * (0.6 + 0.4 * math.sin(t * TAU * 3)) * 1.5
    # o cigarro e a fumaça subindo
    G += T.lines([(-0.35, -0.3, -0.22, -0.32, 1.0)], 0.012) * 1.1
    H += T.gauss(-0.22, -0.32, 0.012) * 1.8
    for j in range(2):
        pts = [(-0.22 + 0.05 * math.sin(u * 8 + t * TAU + j), -0.34 - 0.4 * u) for u in np.linspace(0, 1, 20)]
        G += T.polyline(pts, 0.008) * 0.6
    return G, H


def tiro_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.6, 0.75))
    if k > 0:
        g, h = _pistola(T, -0.6, -0.05, 0.4, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.42, -0.35, -0.08, 0.8, 1.2)
    G, H = G + g, H + h
    u = rel(t, 0.3, 0.42)
    if 0 < u < 1:
        G += T.tapered([(-0.35, -0.08, -0.35 + 0.8 * u, -0.07, 1.0)], 0.02) * 1.6
    g, h = clarao(T, t, 0.4, 0.6, 0.45, -0.07, 1.4, 1.4)
    G, H = G + g, H + h
    G += anel(T, t, 0.41, 0.75, 0.03, 0.55, 0.03, -0.07, 1.0, 1.3)
    G += estouro(T, t, 0.41, 0.8, 12, 613, 0.45, -0.07, 0.5, 0.012)
    # a fumaça do cano depois do tiro
    f = rel(t, 0.42, 1.0)
    if 0 < f < 1:
        pts = [(-0.35 + 0.05 * math.sin(v * 8), -0.08 - 0.35 * v * f) for v in np.linspace(0, 1, 16)]
        G += T.polyline(pts, 0.012) * (1 - f) * 0.9
    return G * env, H * env


# ------------------------------------------------------------------ Vash

def tiro_desarmante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.55, 0.7))
    if k > 0:
        g, h = _pistola(T, -0.6, -0.05, 0.4, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.22, 0.34, -0.35, -0.08, 0.6, 1.0)
    G, H = G + g, H + h
    u = rel(t, 0.22, 0.35)
    if 0 < u < 1:
        G += T.tapered([(-0.35, -0.08, -0.35 + 0.75 * u, -0.06, 1.0)], 0.015) * 1.6
    # a arma do rival voando da mão e girando
    v = rel(t, 0.35, 0.85)
    if 0 < v < 1:
        g, h = _pistola(T, 0.4 + 0.3 * v, -0.05 - 0.4 * math.sin(math.pi * v * 0.8), 0.22, 1 - rel(v, 0.8, 1), v * 10)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.33, 0.48, 0.4, -0.06, 0.7, 1.0)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.lines([(0.45, -0.4, 0.45, -0.2, 1.0), (0.4, -0.26, 0.45, -0.2, 1.0), (0.5, -0.26, 0.45, -0.2, 1.0)], 0.012) * m * 1.2
    return G * env, H * env


def tufao_humanoide(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.95)
    # o casaco vermelho girando
    for j in range(3):
        a = t * TAU * 3 + TAU * j / 3
        G += T.arc_band(0.25, 0.04, a, a + 1.6, 0.4, 0, 0.0, 0.15, 1.0) * k * 1.1
    G += T.lines([(0.0, -0.35, 0.0, 0.3, 1.0)], 0.05) * k * 0.7
    G += T.gauss(0.0, -0.4, 0.06) * k
    # as balas passando de raspão
    for j in range(5):
        u = rel(t, 0.1 + 0.1 * j, 0.35 + 0.1 * j)
        if 0 < u < 1:
            y = -0.4 + 0.18 * j
            lado = 1 if j % 2 else -1
            x = lado * (0.9 - 1.8 * u)
            G += T.tapered([(x + lado * 0.25, y, x, y, 1.0)], 0.014) * 1.3
            H += T.gauss(x, y, 0.009) * 1.6
    G += particulas(T, t, 0.2, 1.0, 12, 614, 0.0, 0.0, 0.4, 0.3, 0.01)
    return G * env, H * env


def vash_preparo(T, t, rng):
    G, H = vazio(T)
    # o braço que vira canhão (o cano comprido) e as penas de luz caindo
    G += T.lines([(-0.35, 0.1, 0.3, 0.0, 1.0)], 0.07) * 1.0
    G += T.ring(0.07, 0.016, 0.33, 0.0) * 1.3
    H += T.gauss(0.33, 0.0, 0.04) * (0.6 + 0.4 * math.sin(t * TAU * 3)) * 2.0
    for j in range(5):
        r = (t + j / 5) % 1
        g, h = icone(T, poe(PENA, -0.4 + 0.18 * j, -0.6 + 0.8 * r, 0.06, 0.5 * math.sin(t * TAU + j)), math.sin(math.pi * r), 0.6)
        G, H = G + g, H + h
    return G, H


def braco_de_anjo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    a = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    if a > 0:
        for lado in (-1, 1):
            for j in range(5):
                ang = -math.pi / 2 + lado * (0.4 + 0.25 * j)
                g, h = icone(T, poe(PENA, -0.6 + 0.35 * a * math.cos(ang), -0.1 + 0.35 * a * math.sin(ang), 0.07 * a, ang + math.pi / 2), 1.0, 0.6)
                G, H = G + g, H + h
        G += T.gauss(-0.6, -0.1, 0.15) * a * 0.8
    u = rel(t, 0.35, 0.8)
    if 0 < u < 1:
        w = 0.25 * math.sin(math.pi * min(1, u * 1.5))
        G += T.tapered([(-0.5, -0.05, -0.5 + 1.5 * ease_out(u), -0.05, 1.0)], w + 0.02) * 1.0
        H += T.lines([(-0.5, -0.05, -0.5 + 1.5 * ease_out(u), -0.05, 1.0)], 0.02) * 1.8
    g, h = clarao(T, t, 0.4, 0.75, 0.2, -0.05, 2.2, 2.0)
    G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.55 + 0.04 * i, 0.8 + 0.04 * i, cx, -0.05, 0.8, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.45, 1.0, 26, 615, 0.1, -0.05, 0.8, 0.5, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Senku

def remedio_senku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.1, 0.45)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        x = -0.5 + 0.5 * ease_in(u) if u > 0 else -0.5
        y = -0.1 - 0.3 * math.sin(math.pi * u)
        g, h = _frasco(T, x, y, 0.22, k, 1.0, t)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.42, 0.6, 0.0, -0.05, 0.9, 1.0)
    G, H = G + g, H + h
    c = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1))
    if c > 0:
        g, h = icone(T, poe(CRUZ, 0.0, -0.45, 0.08 * c), 1.2, 0.8)
        G, H = G + g, H + h
        G += T.ring(0.25 * c, 0.014, 0.0, -0.05, 0.9) * 1.1
    # o debuff saindo do aliado (as bolhinhas escuras subindo e sumindo)
    d = rel(t, 0.5, 0.95)
    if 0 < d < 1:
        for j in range(4):
            G += T.ring(0.025, 0.007, -0.15 + 0.1 * j, -0.05 - 0.4 * d) * (1 - d) * 1.2
    G += particulas(T, t, 0.45, 1.0, 14, 616, 0.0, 0.0, 0.3, 0.6, 0.011)
    return G * env, H * env


def bateria_senku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        # a bateria: as placas de cobre e zinco empilhadas
        for j in range(5):
            G += T.lines([(-0.78, 0.3 - 0.08 * j, -0.48, 0.3 - 0.08 * j, 1.0 if j % 2 else 0.5)], 0.03) * s * 1.1
        G += T.polyline([(-0.81, 0.35), (-0.45, 0.35), (-0.45, -0.05), (-0.81, -0.05), (-0.81, 0.35)], 0.009) * s
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.15 + 0.06 * i, 0.4 + 0.06 * i)
        if u > 0:
            pts = [(-0.5 + (cx - 0.5 + 0.5) * v, 0.1 - 0.15 * math.sin(math.pi * v)) for v in np.linspace(0, min(1, u), 20)]
            if len(pts) > 1:
                G += T.polyline(pts, 0.008) * s * 1.1
                H += T.gauss(pts[-1][0], pts[-1][1], 0.015) * (1 - rel(t, 0.7, 0.9)) * 1.6
    for j in range(3):
        G += _zap(T, 617 + j + int(t * 15), 0.45 - 0.1, -0.2 + 0.1 * j, 0.45 + 0.1, -0.15 + 0.1 * j, 0.008, 3, 0.4) * pulso(t, 0.5, 1.0) * 1.2
    g, h = clarao(T, t, 0.45, 0.62, 0.45, -0.05, 0.8, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


def senku_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _frasco(T, 0.0, 0.1, 0.3, 1.0, 1.0, t)
    G, H = G + g, H + h
    # as contas no ar: os sinais girando em volta
    for j in range(5):
        a = t * TAU + TAU * j / 5
        x, y = 0.38 * math.cos(a), -0.05 + 0.25 * math.sin(a)
        if j % 2:
            G += T.lines([(x - 0.03, y, x + 0.03, y, 1.0), (x, y - 0.03, x, y + 0.03, 1.0)], 0.008) * 1.1
        else:
            G += T.lines([(x - 0.03, y - 0.015, x + 0.03, y - 0.015, 1.0), (x - 0.03, y + 0.015, x + 0.03, y + 0.015, 1.0)], 0.008) * 1.1
    return G, H


def polvora_senku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.35, 0.45))
    if k > 0:
        g, h = _frasco(T, -0.6, 0.0, 0.24, k, 1.0, t)
        G, H = G + g, H + h
    # o pavio aceso correndo até os rivais
    u = rel(t, 0.1, 0.45)
    if 0 < u < 1:
        pts = [(-0.45 + 1.3 * v, 0.3 + 0.03 * math.sin(v * 20)) for v in np.linspace(0, u, 30)]
        G += T.polyline(pts, 0.008) * 0.9
        H += T.gauss(pts[-1][0], pts[-1][1], 0.025) * 2.0
        G += particulas(T, t, 0.1, 0.45, 8, 618, pts[-1][0], pts[-1][1], 0.05, 0.2, 0.008)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        a0 = 0.45 + 0.05 * i
        uu = rel(t, a0, a0 + 0.4)
        if 0 < uu < 1:
            G += T.gauss(cx, 0.0, 0.05 + 0.25 * ease_out(uu)) * (1 - uu) * 1.3
            for j in range(6):
                a = TAU * j / 6 + i
                d = 0.25 * ease_out(uu)
                G += T.ring(0.03 + 0.05 * uu, 0.012, cx + d * math.cos(a), d * math.sin(a) * 0.8) * (1 - uu)
        g, h = clarao(T, t, a0, a0 + 0.2, cx, 0.0, 0.9, 1.1)
        G, H = G + g, H + h
    m = surge(t, 0.6, 0.75) * (1 - rel(t, 0.9, 1))
    if m > 0:
        G += T.ring(0.07 * m, 0.012, 0.45, -0.42) * 1.2
        H += T.gauss(0.53, -0.5, 0.015) * m * (0.5 + 0.5 * math.sin(t * 40)) * 2.0
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.38, 1.5)
    return G * env, H * env


# ------------------------------------------------------------------ Hinata

def punho_suave(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        x = -0.5 + 0.8 * u
        g, h = _palma_aberta(T, x, -0.05, 0.36, k, -math.pi / 2)
        G, H = G + g, H + h
        G += T.gauss(x + 0.1, -0.05, 0.1) * k * 0.9
        H += T.gauss(x + 0.12, -0.05, 0.03) * k * 1.5
    g, h = clarao(T, t, 0.3, 0.5, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g, H + h
    # os pontos de chakra acendendo e apagando no rival
    m = pulso(t, 0.35, 1.0)
    if m > 0:
        pts = [(0.45 + 0.12 * math.cos(a), -0.05 + 0.25 * math.sin(a)) for a in np.linspace(0, TAU, 7, endpoint=False)]
        for j, (px, py) in enumerate(pts):
            H += T.gauss(px, py, 0.015) * m * (0.6 + 0.4 * math.sin(t * 20 + j)) * 1.8
        G += T.polyline(pts + pts[:1], 0.006) * m * 0.8
        for j in range(2):
            G += _zap(T, 619 + j + int(t * 10), 0.35, -0.2 + 0.25 * j, 0.55, -0.1 + 0.25 * j, 0.007, 3, 0.4) * m
    G += anel(T, t, 0.32, 0.65, 0.04, 0.45, 0.03, -0.05, 1.0, 1.2)
    return G * env, H * env


def rotacao_hinata(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.35) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        G += T.gauss(0.0, 0.0, 0.42 * s, 0.38 * s) * 0.35
        G += T.ring(0.42 * s, 0.02, 0.0, 0.0, 1.05) * 1.2
        for j in range(5):
            a = t * TAU * 3 + TAU * j / 5
            G += T.arc_band(0.38 * s, 0.025, a, a + 1.0, 1.0, 0, 0.0, 0.0, 1.0) * 1.1
    # os golpes batendo e voltando (Refletir)
    for j in range(2):
        u = rel(t, 0.35 + 0.15 * j, 0.7 + 0.15 * j)
        if 0 < u < 1:
            x = 0.9 - 0.5 * min(1, u * 2) + 0.5 * max(0, u * 2 - 1)
            y = -0.2 + 0.25 * j
            G += T.tapered([(x + (0.2 if u < 0.5 else -0.2), y, x, y, 1.0)], 0.016) * 1.3
            if 0.45 < u < 0.6:
                H += T.gauss(0.42, y, 0.03) * 2.0
    return G * env, H * env


def hinata_preparo(T, t, rng):
    G, H = vazio(T)
    G += _byakugan(T, 0.0, -0.35, 0.14, 1.0)
    G += _trigrama(T, 0.0, 0.3, 0.45, 1.0, t * TAU * 0.25)
    G += T.gauss(0.0, 0.0, 0.2, 0.3) * (0.3 + 0.15 * math.sin(t * TAU * 2))
    return G, H


def sessenta_e_quatro_palmas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    G += _trigrama(T, 0.15, 0.36, 0.55, surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97)))
    q = np.random.default_rng(621)
    total = 16
    for j in range(total):
        a0 = 0.12 + 0.04 * j
        u = rel(t, a0, a0 + 0.08)
        if 0 < u < 1:
            px, py = 0.45 + q.uniform(-0.1, 0.1), -0.05 + q.uniform(-0.25, 0.25)
            g, h = _palma_aberta(T, px - 0.12 * (1 - u), py, 0.18, 1 - u, -math.pi / 2)
            G, H = G + g, H + h
            H += T.gauss(px, py, 0.02) * (1 - u) * 2.0
            G += T.ring(0.04 + 0.08 * u, 0.008, px, py) * (1 - u) * 1.2
    g, h = clarao(T, t, 0.75, 0.95, 0.45, -0.05, 1.6, 1.5)
    G, H = G + g, H + h
    m = pulso(t, 0.8, 1.0)
    if m > 0:
        G += T.ring(0.08, 0.012, 0.45, 0.05) * m * 1.2 + T.lines([(0.39, 0.0, 0.51, 0.1, 1.0)], 0.012) * m * 1.3
    G += anel(T, t, 0.78, 0.99, 0.05, 0.6, 0.04, -0.05, 1.0, 1.4)
    return G * env, H * env


REGISTRO = [
    ("maca_de_ferro", maca_de_ferro, GRANDE, "Rem · a maça girando na corrente", False),
    ("cura_de_agua_rem", cura_de_agua_rem, GRANDE, "Rem · a água girando e as gotas curando", False),
    ("rem_preparo", rem_preparo, MEDIA, "Rem · o chifre de oni e a aura (Preparo, laço)", True),
    ("forma_de_oni", forma_de_oni, GRANDE, "Rem · o chifre e a maça esmagando", False),
    ("vorpal_strike", vorpal_strike, GRANDE, "Kirito · a estocada que atravessa", False),
    ("parry_kirito", parry_kirito, GRANDE, "Kirito · as espadas cruzadas e as faíscas", False),
    ("kirito_preparo", kirito_preparo, MEDIA, "Kirito · as duas espadas brilhando (Preparo, laço)", True),
    ("starburst_stream", starburst_stream, GRANDE, "Kirito · as 16 estocadas", False),
    ("jeet_kune_do", jeet_kune_do, GRANDE, "Spike · o chamado e o chute", False),
    ("esquiva_spike", esquiva_spike, GRANDE, "Spike · inclinando e as balas de raspão", False),
    ("spike_preparo", spike_preparo, MEDIA, "Spike · a Jericho e o cigarro (Preparo, laço)", True),
    ("tiro_final", tiro_final, GRANDE, "Spike · o tiro único e a fumaça", False),
    ("tiro_desarmante", tiro_desarmante, GRANDE, "Vash · a arma do rival voando", False),
    ("tufao_humanoide", tufao_humanoide, GRANDE, "Vash · o casaco girando e as balas desviando", False),
    ("vash_preparo", vash_preparo, MEDIA, "Vash · o braço-canhão e as penas (Preparo, laço)", True),
    ("braco_de_anjo", braco_de_anjo, GRANDE, "Vash · as asas de luz e o raio gigante", False),
    ("remedio_senku", remedio_senku, GRANDE, "Senku · o frasco de remédio e a cura", False),
    ("bateria_senku", bateria_senku, GRANDE, "Senku · a bateria e os fios no trio", False),
    ("senku_preparo", senku_preparo, MEDIA, "Senku · o frasco e as contas (Preparo, laço)", True),
    ("polvora_senku", polvora_senku, GRANDE, "Senku · o pavio e as explosões", False),
    ("punho_suave", punho_suave, GRANDE, "Hinata · a palma e os pontos de chakra", False),
    ("rotacao_hinata", rotacao_hinata, GRANDE, "Hinata · a cúpula girando e o golpe voltando", False),
    ("hinata_preparo", hinata_preparo, MEDIA, "Hinata · o Byakugan e o trigrama (Preparo, laço)", True),
    ("sessenta_e_quatro_palmas", sessenta_e_quatro_palmas, GRANDE, "Hinata · as 64 palmas", False),
]
