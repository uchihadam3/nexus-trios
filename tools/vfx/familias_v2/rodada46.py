"""Rodada 46 das habilidades próprias: Mulher-Gato, Espantalho, Asa Noturna, Dipper, Mabel e Yennefer.

Mulher-Gato
- garras_felinas: as três garras rasgando duas vezes em X e as gotas (Sangrando).
- chicote_da_gata: o chicote estalando, enrolando no rival e o buff quebrando (Preso e Dissipar).
- mulher_gato_preparo: o Preparo do Grande roubo — os olhos de gato acesos no escuro e o chicote balançando (laço).
- grande_roubo: as garras no rival e a joia arrancada voando de volta, o brilho sendo puxado (Enfraquecido).

Espantalho
- nuvem_do_medo: as nuvens de gás verde saindo do tubo e cobrindo os rivais, as espirais do pavor (Confuso e Envenenado).
- foice_do_espantalho: a foice girando em meia-lua e os fiapos de palha voando (Enfraquecido).
- espantalho_preparo: o Preparo do Pesadelo vivo — a foice erguida, os olhos acesos e o gás rodando (laço).
- pesadelo_vivo: o rosto gigante do pesadelo surgindo em cima dos rivais com a boca rasgada e os tentáculos (Lento).

Asa Noturna
- bastoes_de_choque: os dois bastões batendo e o choque azul no rival (Eletrificado).
- salto_mortal: os mortais em sequência, os rastros em arco e o símbolo do pássaro (Esquiva e Acelerado).
- combo_do_asa_noturna: a sequência de bastões de todos os lados, o chute e a descarga final (Paralisado).

Dipper Pines
- consultar_o_diario: o diário 3 abrindo, a página brilhando e a lupa marcando o rival (Exposto e Marcado).
- lanterna_de_dipper: o cone da lanterna e o clarão nos olhos do rival (Cego).
- dipper_preparo: o Preparo do Mistério resolvido — o diário aberto, as páginas virando e o pinheiro (laço).
- misterio_resolvido: a roda de símbolos do mistério girando e o feixe que desvenda o rival (Dissipar).

Mabel Pines
- glitter: o canhão de glitter espalhando brilho e estrelinhas em todos os rivais (Confuso).
- mabel_mania: o arco-íris, os corações e as estrelas cadentes no trio (Acelerado e Fortalecido).

Yennefer
- raio_arcano_yen: a estrela de obsidiana acesa e o raio violeta de caos no rival (Eletrificado).
- barreira_de_yennefer: a cúpula violeta com as runas descendo sobre o trio (Barreira e Protegido).
- yennefer_preparo: o Preparo do Dissipar — as mãos erguidas e o caos violeta rodando numa esfera (laço).
- dissipar_de_yennefer: o círculo de runas embaixo dos rivais e a onda que arranca os buffs para cima.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CORACAO, GEMA, GOTA, anel, cheio, circulo, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _garras(T, t, a, b, cx, cy, ang, comp=0.7, larg=0.05, gap=0.09):
    G, H = 0.0, 0.0
    for m in (-1, 0, 1):
        dx, dy = -math.sin(ang) * gap * m, math.cos(ang) * gap * m
        g, h = corte(T, t, a + 0.015 * (m + 1), b + 0.015 * (m + 1), ang, comp, larg, cx + dx, cy + dy, 0.05)
        G, H = G + g, H + h
    return G, H


_OLHO_GATO = [(-1, 0), (-0.5, -0.45), (0.2, -0.5), (1, 0), (0.2, 0.5), (-0.5, 0.45)]


# ------------------------------------------------------------------ Mulher-Gato

def garras_felinas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = _garras(T, t, 0.05, 0.3, 0.45, 0.0, 0.9)
    G, H = G + g * 1.2, H + h
    g, h = _garras(T, t, 0.22, 0.47, 0.45, 0.0, -0.9)
    G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.2, 0.45, 0.45, 0.0, 1.0)
    G, H = G + g2, H + h2
    q = np.random.default_rng(21)
    for j in range(10):
        w = rel(t, 0.3 + 0.02 * j, 0.85)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.4), q.uniform(-0.45, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.032), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    # as marcas das garras ficando
    k = pulso(t, 0.45, 1.0)
    for ang in (0.9, -0.9):
        for m in (-1, 0, 1):
            dx, dy = -math.sin(ang) * 0.09 * m, math.cos(ang) * 0.09 * m
            c, s = math.cos(ang) * 0.25, math.sin(ang) * 0.25
            G += T.tapered([(0.45 + dx - c, dy - s, 0.45 + dx + c, dy + s, 1.0)], 0.012) * k * 0.6
    return G * env, H * env


def _chicote(T, x0, y0, x1, y1, amp, fase, k, w=0.012):
    pts = []
    for u in np.linspace(0, 1, 30):
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + amp * math.sin(u * 7 + fase) * u * (1 - u) * 4
        pts.append((x, y))
    return T.polyline(pts, w) * k


def chicote_da_gata(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.3, 0.42)
    if u > 0 and k > 0:
        G += _chicote(T, -0.6, 0.0, -0.6 + 1.05 * u, -0.05, 0.15 * (1 - u), t * 30, k * 1.4, 0.02)
    g, h = clarao(T, t, 0.27, 0.42, 0.45, -0.05, 0.6, 1.0)
    G, H = G + g, H + h
    enrola = ease_out(rel(t, 0.3, 0.5), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if enrola > 0 and kk > 0:
        G += _chicote(T, -0.6, 0.0, 0.3, -0.02, 0.03, 0, kk * 1.1, 0.017)
        for m in range(3):
            a0 = -2.5 + m * 0.4
            G += T.arc_band(0.14 - 0.02 * m, 0.016, a0, a0 + TAU * enrola * 0.85, 2.0, 0, 0.45, -0.1 + 0.08 * m, 1.0) * kk * 1.3
    # o buff quebrando
    q = np.random.default_rng(22)
    for _ in range(7):
        w = rel(t, 0.5, 0.85)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0)
            d = 0.05 + 0.3 * ease_out(w)
            g2, h2 = icone(T, poe([(0, -1), (0.8, 0.7), (-0.6, 0.5)], 0.45 + d * math.cos(a), -0.3 + d * math.sin(a) + 0.3 * w * w, 0.03, a + 8 * w),
                           (1 - w) * 1.1, 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


def mulher_gato_preparo(T, t, rng):
    G, H = vazio(T)
    pisca = 1.0 if (t % 1) < 0.9 else 0.15
    for lado in (-1, 1):
        g, h = icone(T, poe(_OLHO_GATO, lado * 0.16, -0.1, 0.1), pisca * 1.2, 0.55)
        G, H = G + g, H + h
        G += T.lines([(lado * 0.16, -0.17, lado * 0.16, -0.03, 1.0)], 0.01) * pisca * 1.4
        G += T.gauss(lado * 0.16, -0.1, 0.12) * pisca * 0.3
    G += _chicote(T, -0.1, 0.35, 0.45, 0.25, 0.12, t * TAU * 1.5, 1.0, 0.012)
    return G, H


def grande_roubo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = _garras(T, t, 0.0, 0.25, 0.45, 0.0, 1.1, 0.6, 0.05)
    G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.15, 0.4, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    u = ease_in(rel(t, 0.3, 0.75), 1.3)
    if 0 < u < 1:
        x = 0.45 - 1.0 * u
        y = -0.25 * math.sin(math.pi * u)
        g3, h3 = icone(T, poe(GEMA, x, y, 0.12, u * 6), 1.4, 0.6)
        G, H = G + g3, H + h3
        H += T.gauss(x, y, 0.03) * 1.5
        G += T.tapered([(x + 0.3, y + 0.1 * u, x, y, 0.8)], 0.04) * 0.8
    for j in range(3):
        w = rel(t, 0.3 + 0.08 * j, 0.8 + 0.08 * j)
        if 0 < w < 1:
            G += T.lines([(0.45 - 1.0 * w, 0.06 * (j - 1), 0.45 - 1.0 * w + 0.12, 0.06 * (j - 1), 1.0)], 0.01) * (1 - w) * 1.3
    s = surge(t, 0.72, 0.88) * (1 - rel(t, 0.9, 1))
    if s > 0:
        G += anel(T, t, 0.72, 0.95, 0.05, 0.25, 0.02, 0.0) * 1.0
        H += T.flare(-0.55, 0.0, 0.25 * s, 0.4, 0.008) * 1.5
    G += particulas(T, t, 0.35, 0.95, 12, 23, 0.0, -0.1, 0.4, 0.3, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Espantalho

def _nuvem(T, cx, cy, s, k, seed, t):
    q = np.random.default_rng(seed)
    G = 0.0
    for _ in range(6):
        dx, dy = q.uniform(-1, 1) * s, q.uniform(-0.5, 0.5) * s
        r = s * q.uniform(0.45, 0.8) * (1 + 0.08 * math.sin(t * 6 + dx * 10))
        G = G + T.gauss(cx + dx, cy + dy, r, r * 0.8) * k
    return G


def _espiral(T, cx, cy, r, gira, k, w=0.01):
    pts = [(cx + r * u * math.cos(gira + u * 9), cy + r * u * math.sin(gira + u * 9) * 0.8) for u in np.linspace(0.05, 1, 30)]
    return T.polyline(pts, w) * k


def nuvem_do_medo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(6):
        u = rel(t, 0.03 * j, 0.5 + 0.03 * j)
        if u > 0:
            x = -0.7 + 1.5 * ease_out(min(u, 1.0), 1.5) * (0.4 + 0.12 * j)
            s = 0.08 + 0.12 * min(u, 1.0)
            G += _nuvem(T, x, -0.05 + 0.04 * (j % 3), s, 0.2 * (1 - rel(t, 0.8, 1.0)), 40 + j, t)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = surge(t, 0.35 + 0.06 * i, 0.55 + 0.06 * i) * (1 - rel(t, 0.85, 1))
        if k > 0:
            G += _espiral(T, cx, -0.3, 0.13 * k, -t * 8, 1.4, 0.013)
        for m in range(3):
            w = rel(t, 0.4 + 0.1 * m + 0.05 * i, 0.8 + 0.1 * m + 0.05 * i)
            if 0 < w < 1:
                g, h = cheio(T, poe(GOTA, cx - 0.08 + 0.08 * m, 0.05 + 0.25 * w, 0.025), (1 - w) * 1.0)
                G, H = G + g, H + h
    return G * env, H * env


def _foice(T, px, py, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    hx, hy = px + c * s, py + sn * s
    G = T.lines([(px, py, hx, hy, 1.0)], s * 0.035) * k * 1.2
    G += T.arc_band(s * 0.42, s * 0.07, ang + math.pi / 2 + 0.2, ang + math.pi * 1.15, 1.0, 0, hx - c * s * 0.42 * 0 + sn * s * 0.0, hy, 1.0) * k * 1.2
    return G


def foice_do_espantalho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.4 + 2.6 * u
        G += _foice(T, 0.0, 0.25, ang, 0.55, k)
        if 0 < u < 1:
            G += T.arc_band(0.75, 0.06, ang - 1.0, ang, 1.0, 0, 0.0, 0.25, 1.0) * k * 0.7
    g, h = corte(T, t, 0.3, 0.55, -0.2, 1.3, 0.09, 0.45, 0.0, 0.25)
    G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.45, 0.0, 1.1)
    G, H = G + g2, H + h2
    q = np.random.default_rng(24)
    for j in range(12):
        w = rel(t, 0.35, 0.95)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0.3)
            d = 0.1 + 0.45 * ease_out(w)
            x, y = 0.45 + d * math.cos(a), d * math.sin(a) + 0.4 * w * w
            b = q.uniform(0, TAU) + w * 5
            G += T.lines([(x, y, x + 0.05 * math.cos(b), y + 0.05 * math.sin(b), 1.0)], 0.007) * (1 - w) * 1.3
    return G * env, H * env


def espantalho_preparo(T, t, rng):
    G, H = vazio(T)
    G += _foice(T, 0.15, 0.4, -1.75, 0.75, 1.0)
    for lado in (-1, 1):
        b = 0.6 + 0.4 * math.sin(t * TAU * 3 + lado)
        H += T.gauss(-0.15 + lado * 0.07, -0.1, 0.018) * b * 1.8
        G += T.gauss(-0.15 + lado * 0.07, -0.1, 0.04) * b * 0.8
    for m in range(5):
        a = t * TAU + TAU * m / 5
        G += _nuvem(T, -0.15 + 0.35 * math.cos(a), 0.05 + 0.18 * math.sin(a), 0.06, 0.3, 50 + m, t)
    return G, H


def pesadelo_vivo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        cy = -0.45
        G += T.gauss(0, cy, 0.55 * s, 0.3 * s) * 0.22
        for lado in (-1, 1):
            g, h = icone(T, poe(_OLHO_GATO, lado * 0.22 * s, cy - 0.05, 0.1 * s, lado * 0.35), 1.3, 0.6)
            G, H = G + g, H + h
            H += T.gauss(lado * 0.22 * s, cy - 0.05, 0.02) * 2.0 * s
        dentes = []
        for j in range(9):
            x = (-0.3 + 0.075 * j) * s
            dentes.append((x, cy + 0.15 * s + (0.06 * s if j % 2 else 0.0)))
        G += T.polyline(dentes, 0.014) * 1.4
        G += T.arc_band(0.32 * s, 0.02, 0.4, math.pi - 0.4, 1.6, 0, 0, cy + 0.0, 0.0) * 1.0
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.35 + 0.05 * i, 0.65 + 0.05 * i)
        k = 1 - rel(t, 0.8, 0.95)
        if u > 0 and k > 0:
            pts = [(cx * 0.4 + (cx - cx * 0.4) * v + 0.06 * math.sin(v * 9 + t * 10), -0.3 + 0.35 * v) for v in np.linspace(0, min(1.0, u * 1.2), 20)]
            G += T.polyline(pts, 0.016) * k * 1.3
        g2, h2 = clarao(T, t, 0.55 + 0.05 * i, 0.75 + 0.05 * i, cx, 0.05, 0.4, 0.9)
        G, H = G + g2, H + h2
        G += _espiral(T, cx, 0.05, 0.1 * pulso(t, 0.6, 1.0), -t * 6, 1.0, 0.009)
    return G * env, H * env


# ------------------------------------------------------------------ Asa Noturna

def bastoes_de_choque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (a0, lado) in enumerate(((0.0, -1), (0.15, 1))):
        u = ease_in(rel(t, a0, a0 + 0.2), 1.8)
        k = 1 - rel(t, a0 + 0.25, a0 + 0.35)
        if k > 0:
            ang = lado * (1.6 - 1.1 * u) - math.pi / 2 * 0
            px, py = 0.45 - lado * 0.25, -0.1
            x2, y2 = px + 0.4 * math.cos(-math.pi / 2 + lado * (1.5 - 1.2 * u)) * -lado, py + 0.4 * math.sin(-math.pi / 2 + lado * (1.5 - 1.2 * u))
            G += T.lines([(px, py + 0.25, x2, y2 + 0.25, 1.0)], 0.03) * k * 1.3
            H += T.gauss(x2, y2 + 0.25, 0.02) * k * 1.5
            G += raios(T, t, a0, a0 + 0.35, 2, 30 + j, x2, y2 + 0.25, 0.08, 0.006)
        g, h = clarao(T, t, a0 + 0.17, a0 + 0.35, 0.45, 0.0, 0.8, 1.1)
        G, H = G + g, H + h
    G += raios(T, t, 0.35, 0.9, 6, 33, 0.45, 0.0, 0.3, 0.009) * 1.1
    G += anel(T, t, 0.35, 0.75, 0.05, 0.4, 0.03, 0.0)
    return G * env, H * env


_PASSARO = [(-1, -0.3), (-0.55, -0.15), (-0.2, 0.05), (0, 0.45), (0.2, 0.05), (0.55, -0.15), (1, -0.3), (0.45, 0.05), (0, 0.15), (-0.45, 0.05)]


def salto_mortal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.18 * j, 0.3 + 0.18 * j)
        cx = -0.55 + 0.45 * j
        if 0 < u < 1:
            a = -math.pi / 2 + TAU * ease_in(u, 1.2)
            G += T.arc_band(0.18, 0.04, -math.pi / 2, a, 1.0, 0, cx, -0.1, 1.0) * (1 - 0.4 * u) * 1.2
            x, y = cx + 0.18 * math.cos(a), -0.1 + 0.18 * math.sin(a)
            G += T.gauss(x, y, 0.04, 0.04) * 1.2
            H += T.gauss(x, y, 0.015) * 1.4
        w = rel(t, 0.3 + 0.18 * j, 0.6 + 0.18 * j)
        if 0 < w < 1:
            G += T.ring(0.18, 0.012, cx, -0.1) * (1 - w) * 0.5
    s = surge(t, 0.6, 0.8) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, poe(_PASSARO, 0.35, -0.1, 0.28 * s), 1.3, 0.5)
        G, H = G + g, H + h
    for m in range(4):
        u = (t * 2.2 + m / 4) % 1
        G += T.lines([(0.85 - 1.7 * u, -0.35 + 0.12 * m, 0.65 - 1.7 * u, -0.35 + 0.12 * m, 1.0)], 0.005) * pulso(t, 0.0, 0.9) * 0.8
    return G * env, H * env


def combo_do_asa_noturna(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    angs = (0.7, -0.7, 0.0, 1.4, -1.2)
    for j, a in enumerate(angs):
        a0 = 0.03 + 0.09 * j
        g, h = corte(T, t, a0, a0 + 0.15, a, 0.6, 0.05, 0.45 + 0.04 * math.cos(j), 0.03 * math.sin(j * 2))
        G, H = G + g * 1.1, H + h
        k = pulso(t, a0 + 0.05, a0 + 0.17)
        if k > 0:
            H += T.gauss(0.45, 0.0, 0.03) * k * 1.4
            G += _zap(T, int(t * 40) + j, 0.45, 0.0, 0.45 + 0.2 * math.cos(a + 1.5), 0.2 * math.sin(a + 1.5), 0.007, 3, 0.4) * k * 1.2
    u = ease_in(rel(t, 0.48, 0.6), 2)
    k2 = 1 - rel(t, 0.65, 0.75)
    if u > 0 and k2 > 0:
        P, nos = _punho(T, 0.1 + 0.3 * u, 0.2 - 0.2 * u, 1.3, -0.5)
        G += P * 0.9 * k2
        H += nos * 0.4 * k2
    g2, h2 = clarao(T, t, 0.58, 0.85, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.6, 1.0, 7, 41, 0.45, 0.0, 0.45, 0.01) * 1.2
    G += anel(T, t, 0.6, 0.95, 0.05, 0.7, 0.04, 0.0, 1.0, 1.4)
    s = surge(t, 0.62, 0.8) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g3, h3 = icone(T, poe(_PASSARO, 0.45, -0.4, 0.2 * s), 1.2, 0.5)
        G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Dipper

def _diario(T, cx, cy, s, abre, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        larg = 0.8 * abre + 0.05
        pts = [(cx, cy - 0.55 * s), (cx + lado * larg * s, cy - 0.6 * s), (cx + lado * larg * s, cy + 0.6 * s), (cx, cy + 0.55 * s)]
        g, h = icone(T, pts, k, 0.4)
        G, H = G + g, H + h
        if abre > 0.5:
            for m in range(4):
                y = cy - 0.35 * s + 0.2 * s * m
                G = G + T.lines([(cx + lado * 0.12 * s, y, cx + lado * (larg - 0.12) * s, y, 1.0)], 0.005) * k * 0.8
    if abre > 0.5:
        # a mão de seis dedos com o 3 da capa (o símbolo do diário)
        G = G + T.polyline([(cx - 0.55 * s, cy - 0.35 * s), (cx - 0.4 * s, cy - 0.42 * s), (cx - 0.3 * s, cy - 0.3 * s),
                            (cx - 0.42 * s, cy - 0.22 * s), (cx - 0.3 * s, cy - 0.12 * s), (cx - 0.4 * s, cy - 0.02 * s),
                            (cx - 0.55 * s, cy - 0.08 * s)], 0.008) * k * 1.3
    return G, H


def consultar_o_diario(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.6, 0.72)
    if k > 0:
        g, h = _diario(T, -0.55, 0.0, 0.3, abre, k * 1.1)
        G, H = G + g, H + h
        G += T.gauss(-0.55, -0.1, 0.15) * pulso(t, 0.15, 0.6) * 0.7
    u = ease_in(rel(t, 0.3, 0.55), 1.4)
    k2 = 1 - rel(t, 0.88, 1)
    if u > 0 and k2 > 0:
        x = -0.4 + 0.85 * u
        G += T.ring(0.1, 0.018, x, -0.05) * k2 * 1.3
        G += T.lines([(x + 0.07, 0.02, x + 0.18, 0.12, 1.0)], 0.02) * k2 * 1.3
        G += T.gauss(x, -0.05, 0.08) * k2 * 0.35
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.22 * m, 0.014, 0.45, 0.0) * 1.2
        G += T.ring(0.13 * m, 0.01, 0.45, 0.0) * 1.0
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.17 * m * math.cos(a), 0.17 * m * math.sin(a), 0.45 + 0.28 * m * math.cos(a), 0.28 * m * math.sin(a), 1.0)], 0.01) * 1.3
    return G * env, H * env


def lanterna_de_dipper(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    liga = 1.0 if t > 0.12 or (t * 30) % 1 < 0.5 else 0.2
    G += T.polys([([(-0.55, -0.04), (-0.4, -0.05), (-0.4, 0.05), (-0.55, 0.04)], 1.0)], 0.004) * k * 1.2
    if t > 0.08:
        cone = [(-0.4, -0.03), (0.6, -0.28), (0.6, 0.28), (-0.4, 0.03)]
        G += T.polys([(cone, 1.0)], 0.06) * k * liga * 0.45
        G += T.gauss(-0.1, 0.0, 0.3, 0.1) * k * liga * 0.3
    H += T.gauss(-0.4, 0.0, 0.025) * k * liga * 2.0
    g, h = clarao(T, t, 0.25, 0.65, 0.45, -0.05, 1.3, 1.4)
    G, H = G + g, H + h
    for lado in (-1, 1):
        s = pulso(t, 0.3, 0.9)
        G += T.lines([(0.45 + lado * 0.06 - 0.03, -0.12, 0.45 + lado * 0.06 + 0.03, -0.06, 1.0),
                      (0.45 + lado * 0.06 + 0.03, -0.12, 0.45 + lado * 0.06 - 0.03, -0.06, 1.0)], 0.009) * s * 1.3
    return G * env, H * env


def _pinheiro(T, cx, cy, s, k):
    pts = [(cx, cy - s), (cx + 0.35 * s, cy - 0.4 * s), (cx + 0.18 * s, cy - 0.4 * s), (cx + 0.5 * s, cy + 0.2 * s), (cx + 0.08 * s, cy + 0.2 * s),
           (cx + 0.08 * s, cy + 0.5 * s), (cx - 0.08 * s, cy + 0.5 * s), (cx - 0.08 * s, cy + 0.2 * s), (cx - 0.5 * s, cy + 0.2 * s),
           (cx - 0.18 * s, cy - 0.4 * s), (cx - 0.35 * s, cy - 0.4 * s)]
    return icone(T, pts, k, 0.5)


def dipper_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _diario(T, 0.0, 0.15, 0.32, 1.0, 1.0)
    G, H = G + g, H + h
    u = (t * 2) % 1
    larg = 0.26 * math.cos(math.pi * u)
    G += T.polys([([(0, 0.15 - 0.17), (larg, 0.15 - 0.19), (larg, 0.15 + 0.19), (0, 0.15 + 0.17)], 1.0)], 0.004) * 0.6
    g2, h2 = _pinheiro(T, 0.0, -0.3, 0.13, 1.0 + 0.3 * math.sin(t * TAU))
    return G + g2, H + h2


_SIMBOLOS = [[(0, -1), (0.87, 0.5), (-0.87, 0.5)], estrela_pts(5, 0.45), circulo(6, 1.0), [(-1, 0), (0, -1), (1, 0), (0, 1)]]


def misterio_resolvido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    k = abre * (1 - rel(t, 0.7, 0.85))
    if k > 0:
        G += T.ring(0.42, 0.016, -0.4, -0.1) * k * 1.1
        G += T.ring(0.3, 0.01, -0.4, -0.1) * k * 0.9
        for j in range(10):
            a = t * 2.5 + TAU * j / 10
            g, h = icone(T, poe(_SIMBOLOS[j % 4], -0.4 + 0.36 * math.cos(a), -0.1 + 0.36 * math.sin(a), 0.04, a), k * 1.1, 0.5)
            G, H = G + g, H + h
        g, h = icone(T, poe([(0, -1), (0.87, 0.5), (-0.87, 0.5)], -0.4, -0.1, 0.16, t * -1.5), k * 1.2, 0.4)
        G, H = G + g, H + h
        H += T.gauss(-0.4, -0.12, 0.025) * k * 1.6
    u = rel(t, 0.4, 0.65)
    k2 = 1 - rel(t, 0.65, 0.8)
    if u > 0 and k2 > 0:
        ponta = -0.4 + 0.85 * min(1.0, ease_in(u) * 1.3)
        G += T.tapered([(-0.4, -0.1, ponta, 0.0, 1.0)], 0.14) * k2 * 0.8
        G += T.lines([(-0.4, -0.1, ponta, 0.0, 1.0)], 0.02) * k2 * 1.4
        H += T.lines([(-0.4, -0.1, ponta, 0.0, 1.0)], 0.007) * k2
    g2, h2 = clarao(T, t, 0.55, 0.8, 0.45, 0.0, 1.5, 1.4)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.58, 0.95, 14, 25, 0.45, 0.0, 0.55, 0.012)
    G += particulas(T, t, 0.6, 1.0, 12, 26, 0.45, -0.1, 0.15, 0.6, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Mabel

def glitter(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    G += T.polys([([(-0.75, 0.0), (-0.55, -0.08), (-0.5, 0.0), (-0.55, 0.08)], 1.0)], 0.005) * pulso(t, 0.0, 0.6) * 1.0
    g, h = clarao(T, t, 0.05, 0.25, -0.5, 0.0, 0.5, 0.8)
    G, H = G + g, H + h
    q = np.random.default_rng(27)
    for j in range(36):
        a0 = q.uniform(0.05, 0.25)
        ang = q.uniform(-0.6, 0.6)
        vel = q.uniform(0.8, 1.5)
        u = rel(t, a0, a0 + 0.6)
        if 0 < u < 1:
            d = vel * ease_out(u, 1.5)
            x, y = -0.5 + d * math.cos(ang), d * math.sin(ang) + 0.25 * u * u
            brilho = 0.6 + 0.4 * math.sin(t * 40 + j)
            if j % 3 == 0:
                g2, h2 = cheio(T, poe(estrela_pts(4, 0.35), x, y, 0.035, u * 4), (1 - rel(u, 0.75, 1)) * brilho * 1.3)
                G, H = G + g2, H + h2
            else:
                H += T.gauss(x, y, 0.01) * (1 - rel(u, 0.75, 1)) * brilho * 1.8
                G += T.gauss(x, y, 0.018) * (1 - rel(u, 0.75, 1)) * brilho * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.5 + 0.05 * i, 1.0)
        if k > 0:
            for m in range(3):
                a = t * 8 + TAU * m / 3
                g3, h3 = cheio(T, poe(estrela_pts(5, 0.45), cx + 0.11 * math.cos(a), -0.3 + 0.04 * math.sin(a), 0.03), k * 1.3)
                G, H = G + g3, H + h3
    return G * env, H * env


def mabel_mania(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.85, 1)
    for m in range(4):
        G += T.arc_band(0.75 - 0.06 * m, 0.03, math.pi, math.pi + math.pi * abre, 1.8, 0, 0.0, 0.3, 0.0) * k * (1.2 - 0.15 * m)
    q = np.random.default_rng(28)
    for j in range(5):
        a0 = 0.2 + 0.08 * j
        u = rel(t, a0, a0 + 0.35)
        if 0 < u < 1:
            x0 = q.uniform(-0.9, 0.2)
            x, y = x0 + 0.7 * u, -0.8 + 0.6 * u
            g, h = cheio(T, poe(estrela_pts(5, 0.45), x, y, 0.04, u * 5), 1.3)
            G, H = G + g, H + h
            G += T.tapered([(x - 0.3, y - 0.26, x, y, 0.8)], 0.025) * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        for m in range(3):
            u = rel(t, 0.35 + 0.05 * i + 0.1 * m, 0.85 + 0.05 * i + 0.1 * m)
            if 0 < u < 1:
                g, h = cheio(T, poe(CORACAO, cx - 0.1 + 0.1 * m + 0.03 * math.sin(u * 10), 0.1 - 0.35 * u, 0.035), (1 - u) * 1.3)
                G, H = G + g, H + h
        s = surge(t, 0.4 + 0.05 * i, 0.6 + 0.05 * i) * (1 - rel(t, 0.85, 1))
        if s > 0:
            G += T.polyline([(cx - 0.06 * s, -0.12), (cx, -0.12 - 0.08 * s), (cx + 0.06 * s, -0.12)], 0.014) * 1.3
            G += T.polyline([(cx - 0.06 * s, -0.04), (cx, -0.04 - 0.08 * s), (cx + 0.06 * s, -0.04)], 0.014) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Yennefer

_OBSIDIANA = estrela_pts(8, 0.42)


def raio_arcano_yen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    c = pulso(t, 0.0, 0.4)
    if c > 0:
        g, h = icone(T, poe(_OBSIDIANA, -0.55, -0.3, 0.07 + 0.02 * c, t * 3), c * 1.3, 0.6)
        G, H = G + g, H + h
        G += T.gauss(-0.55, 0.0, 0.08) * c * 1.0
        G += converge(T, t, 0.0, 0.3, 10, 29, -0.55, 0.0, 0.35, 0.008)
    k = pulso(t, 0.25, 0.65)
    if k > 0:
        for j in range(2):
            G += _zap(T, int(t * 35) + 5 * j, -0.53, 0.0, 0.45, 0.0, 0.02 - 0.008 * j, 5, 0.2) * k * 1.4
        H += _zap(T, int(t * 35), -0.53, 0.0, 0.45, 0.0, 0.007, 5, 0.2) * k
        G += T.tapered([(-0.53, 0.0, 0.45, 0.0, 1.0)], 0.08) * k * 0.4
    g2, h2 = clarao(T, t, 0.35, 0.65, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.5, 0.95, 4, 30, 0.45, 0.0, 0.22, 0.007)
    return G * env, H * env


def barreira_de_yennefer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        d = ease_out(rel(t, 0.05 + 0.05 * i, 0.45 + 0.05 * i), 2)
        if d > 0 and k > 0:
            G += T.arc_band(0.22, 0.025, math.pi, math.pi + math.pi * d, 1.0, 0, cx, 0.25, 0.0) * k * 1.2
            G += T.gauss(cx, 0.12, 0.17, 0.13) * d * k * 0.35
            G += T.ring(0.22, 0.012, cx, 0.25, 4.0) * d * k * 1.0
            for m in range(5):
                v = ((t * 0.8 + m / 5 + 0.1 * i) % 1)
                a = math.pi + math.pi * (0.15 + 0.7 * m / 4)
                x, y = cx + 0.22 * math.cos(a), 0.25 + 0.22 * math.sin(a)
                g, h = icone(T, poe(_SIMBOLOS[m % 4], x, y, 0.025, v * 3), d * k * 1.1, 0.5)
                G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.75, 0.1, 1.0, 0.03, 0.25, 3.0)
    return G * env, H * env


def yennefer_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        G += T.gauss(lado * 0.25, 0.1, 0.04) * 1.0
        H += T.gauss(lado * 0.25, 0.1, 0.015) * 1.5
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    G += T.gauss(0, -0.15, 0.16 + 0.03 * b) * 0.7
    for m in range(3):
        a = t * TAU * (1 + 0.3 * m) + m * 2.1
        G += T.arc_band(0.2 + 0.03 * m, 0.016, a, a + 2.2, 1.0 + 0.4 * m, m * 0.6, 0, -0.15, 1.0) * 1.2
    for lado in (-1, 1):
        G += T.lines([(lado * 0.25, 0.1, lado * 0.08, -0.08, 1.0)], 0.006) * (0.5 + 0.5 * b)
    H += T.gauss(0, -0.15, 0.03) * (1.3 + b)
    return G, H


def dissipar_de_yennefer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        G += T.ring(0.22 * ease_out(rel(t, 0.05 + 0.05 * i, 0.3 + 0.05 * i), 2), 0.016, cx, 0.3, 3.0) * (1 - rel(t, 0.8, 0.95)) * 1.3
        G += T.ring(0.15 * ease_out(rel(t, 0.1 + 0.05 * i, 0.35 + 0.05 * i), 2), 0.01, cx, 0.3, 3.0) * (1 - rel(t, 0.8, 0.95)) * 1.0
        for m in range(6):
            a = t * 2 + TAU * m / 6
            g2, h2 = icone(T, poe(_SIMBOLOS[m % 4], cx + 0.19 * math.cos(a), 0.3 + 0.19 / 3 * math.sin(a), 0.022), pulso(t, 0.1 + 0.05 * i, 0.85) * 1.1, 0.5)
            G, H = G + g2, H + h2
        # a coluna que arranca os buffs para cima
        k = pulso(t, 0.35 + 0.05 * i, 0.8 + 0.05 * i)
        if k > 0:
            G += T.gauss(cx, 0.0, 0.08, 0.35) * k * 0.6
            H += T.gauss(cx, 0.0, 0.02, 0.3) * k * 0.8
        q = np.random.default_rng(31 + i)
        for j in range(6):
            w = rel(t, 0.4 + 0.05 * i + 0.03 * j, 0.9)
            if 0 < w < 1:
                x = cx + q.uniform(-0.1, 0.1)
                y = 0.0 - 0.9 * ease_in(w, 1.4)
                g3, h3 = icone(T, poe([(0, -1), (0.8, 0.7), (-0.6, 0.5)], x, y, 0.03, w * 8 + j), (1 - w) * 1.2, 0.5)
                G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.35, 0.9, 1.0, 0.3, 1.4)
    return G * env, H * env


REGISTRO = [
    ("garras_felinas", garras_felinas, GRANDE, "Mulher-Gato · as garras em X", False),
    ("chicote_da_gata", chicote_da_gata, GRANDE, "Mulher-Gato · o chicote enrolando", False),
    ("mulher_gato_preparo", mulher_gato_preparo, MEDIA, "Mulher-Gato · os olhos de gato no escuro (Preparo, laço)", True),
    ("grande_roubo", grande_roubo, GRANDE, "Mulher-Gato · a joia arrancada", False),
    ("nuvem_do_medo", nuvem_do_medo, GRANDE, "Espantalho · as nuvens do gás do medo", False),
    ("foice_do_espantalho", foice_do_espantalho, GRANDE, "Espantalho · a foice em meia-lua", False),
    ("espantalho_preparo", espantalho_preparo, MEDIA, "Espantalho · a foice e o gás rodando (Preparo, laço)", True),
    ("pesadelo_vivo", pesadelo_vivo, GRANDE, "Espantalho · o rosto do pesadelo", False),
    ("bastoes_de_choque", bastoes_de_choque, GRANDE, "Asa Noturna · os bastões e o choque", False),
    ("salto_mortal", salto_mortal, GRANDE, "Asa Noturna · os mortais e o pássaro", False),
    ("combo_do_asa_noturna", combo_do_asa_noturna, GRANDE, "Asa Noturna · o combo de bastões", False),
    ("consultar_o_diario", consultar_o_diario, GRANDE, "Dipper · o diário e a lupa", False),
    ("lanterna_de_dipper", lanterna_de_dipper, GRANDE, "Dipper · o cone da lanterna", False),
    ("dipper_preparo", dipper_preparo, MEDIA, "Dipper · o diário folheando (Preparo, laço)", True),
    ("misterio_resolvido", misterio_resolvido, GRANDE, "Dipper · a roda de símbolos e o feixe", False),
    ("glitter", glitter, GRANDE, "Mabel · o canhão de glitter", False),
    ("mabel_mania", mabel_mania, GRANDE, "Mabel · o arco-íris e os corações", False),
    ("raio_arcano_yen", raio_arcano_yen, GRANDE, "Yennefer · a obsidiana e o raio violeta", False),
    ("barreira_de_yennefer", barreira_de_yennefer, GRANDE, "Yennefer · as cúpulas de runas", False),
    ("yennefer_preparo", yennefer_preparo, MEDIA, "Yennefer · o caos rodando nas mãos (Preparo, laço)", True),
    ("dissipar_de_yennefer", dissipar_de_yennefer, GRANDE, "Yennefer · as runas arrancando os buffs", False),
]
