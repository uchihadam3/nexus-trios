"""Rodada 50 das habilidades próprias: Odin, Fenrir, Hel, Jason, Freddy e Michael Myers.

Odin
- gungnir_de_odin: a Gungnir arremessada com as runas acesas na haste, cravando e marcando o rival (Marcado).
- corvos_de_odin: Hugin e Munin saindo em espiral do ombro e voando para o rival (Marcado e Invocação).
- sabedoria_de_asgard: o olho de Odin abrindo e as runas douradas caindo sobre o trio (Carga e Fortalecido).

Fenrir
- mordida_de_fenrir: as mandíbulas do lobo fechando no rival e o sangue (Sangrando).
- uivo_de_fenrir: a lua e o uivo do lobo em ondas geladas sobre os rivais (Enfraquecido e Lento).
- fenrir_preparo: o Preparo do Ragnarök — a corrente Gleipnir arrebentando elo por elo (laço).
- ragnarok: o lobo gigante saltando com as mandíbulas abertas e a vida voltando para ele (Roubo de vida).

Hel
- toque_da_morte: a mão meio-viva meio-osso tocando o rival e a marca da maldição (Amaldiçoado).
- exercito_dos_mortos: as mãos e os mortos subindo do chão gelado e o portal de Helheim (Lento e Invocação).
- hel_preparo: o Preparo do Frio de Helheim — a coroa de gelo e a névoa fria girando (laço).
- frio_de_helheim: a névoa de Helheim cobrindo os rivais e o gelo crescendo em cada um (Congelado).

Jason
- facao_de_jason: o facão descendo em diagonal e o sangue (Sangrando).
- volta_do_lago: a água do lago Crystal subindo e a máscara de hóquei emergindo inteira (Vida e Protegido).
- jason_preparo: o Preparo da Sexta-feira 13 — a máscara, o "ki-ki-ki ma-ma-ma" em ondas (laço).
- sexta_feira_13: os golpes de facão em sequência e a lua cheia vermelha (Sangrando).

Freddy Krueger
- cancao_de_ninar: as notas da canção de ninar ("um, dois, Freddy vem te pegar") e o rival dormindo (Dormindo).
- garra_de_laminas: a luva de lâminas rasgando em quatro riscos e o sangue (Sangrando).
- freddy_preparo: o Preparo do Pesadelo — o chapéu, a luva raspando e as faíscas (laço).
- pesadelo_de_freddy: o suéter listrado do pesadelo, a garra gigante saindo do escuro (Amaldiçoado).

Michael Myers
- faca_de_cozinha: a faca de cozinha erguida e descendo devagar e pesada.
- respiracao_na_mascara: a máscara branca no escuro e a respiração em ondas (Marcado e Enfraquecido).
- myers_preparo: o Preparo da Noite de Halloween — a abóbora acesa e a silhueta parada (laço).
- noite_de_halloween: a lâmina saindo do escuro, as abóboras acesas e o golpe final.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (ASA, GOTA, NOTA, anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


_RUNAS = [[(0, -1), (0, 1), (0.6, 0.3)], [(0, -1), (0, 1), (0.5, -0.5), (0, 0)], [(-0.5, -1), (0, 0), (0.5, -1), (0, 0), (0, 1)],
          [(0, -1), (0, 1), (0.5, 0.5), (0, 0)], [(-0.5, 1), (0, -1), (0.5, 1)]]


def _runa(T, j, cx, cy, s, k, w=0.01):
    return T.polyline([(cx + x * s, cy + y * s) for x, y in _RUNAS[j % len(_RUNAS)]], w) * k


def _corvo(T, cx, cy, s, ang, k, bate):
    corpo = [(1.0, 0.0), (0.7, -0.15), (0.3, -0.18), (-0.5, -0.12), (-1.0, -0.25), (-0.85, 0.0), (-1.0, 0.25), (-0.5, 0.12), (0.3, 0.18), (0.7, 0.15)]
    g, h = cheio(T, poe(corpo, cx, cy, s, ang), k)
    for lado in (-1, 1):
        g2, h2 = cheio(T, poe(ASA, cx, cy, s * 0.9, ang + lado * (math.pi / 2 + 0.5 * bate) + (math.pi if lado < 0 else 0)), k)
        g, h = g + g2, h + h2
    return g, h


def _lobo(T, cx, cy, s, k, abre=0.0):
    cabeca = [(-0.9, -0.1), (-0.7, -0.6), (-0.55, -1.0), (-0.3, -0.55), (0.1, -0.5), (0.25, -1.0), (0.4, -0.45), (0.95, -0.2 - 0.25 * abre),
              (0.5, -0.05), (0.95, 0.1 + 0.3 * abre), (0.4, 0.3), (-0.3, 0.5), (-0.8, 0.35)]
    g, h = icone(T, poe(cabeca, cx, cy, s), k, 0.4)
    h = h + T.gauss(cx + s * 0.15, cy - s * 0.3, s * 0.06) * k * 2.0
    return g, h


def _mascara_hoquei(T, cx, cy, s, k):
    G, H = icone(T, poe([(0, -1), (0.6, -0.8), (0.72, -0.1), (0.5, 0.65), (0, 0.95), (-0.5, 0.65), (-0.72, -0.1), (-0.6, -0.8)], cx, cy, s), k, 0.45)
    for lado in (-1, 1):
        G = G + T.ring(s * 0.12, s * 0.03, cx + lado * s * 0.3, cy - s * 0.2) * k * 1.2
    for x, y in ((0, -0.6), (-0.2, 0.15), (0.2, 0.15), (0, 0.4), (-0.15, 0.55), (0.15, 0.55)):
        G = G + T.gauss(cx + x * s, cy + y * s, s * 0.04) * k * 1.4
    for lado in (-1, 1):
        G = G + T.polyline([(cx + lado * s * 0.45, cy - s * 0.55), (cx + lado * s * 0.55, cy - s * 0.35), (cx + lado * s * 0.5, cy - s * 0.15)], s * 0.05) * k * 1.0
    return G, H


def _abobora(T, cx, cy, s, k, acesa):
    G, H = icone(T, poe([(math.cos(a), 0.8 * math.sin(a)) for a in np.linspace(0, TAU, 24)], cx, cy, s), k, 0.4)
    G = G + T.lines([(cx, cy - s * 0.8, cx + s * 0.1, cy - s * 1.05, 1.0)], s * 0.08) * k * 1.2
    for lado in (-1, 1):
        G = G + T.polys([([(cx + lado * s * 0.2, cy - s * 0.3), (cx + lado * s * 0.45, cy - s * 0.05), (cx + lado * s * 0.15, cy - s * 0.05)], 1.0)], 0.003) * k * acesa * 1.5
    boca = [(cx - s * 0.5, cy + s * 0.2), (cx - s * 0.3, cy + s * 0.35), (cx - s * 0.15, cy + s * 0.25), (cx, cy + s * 0.4), (cx + s * 0.15, cy + s * 0.25),
            (cx + s * 0.3, cy + s * 0.35), (cx + s * 0.5, cy + s * 0.2), (cx + s * 0.3, cy + s * 0.5), (cx - s * 0.3, cy + s * 0.5)]
    G = G + T.polys([(boca, 1.0)], 0.003) * k * acesa * 1.5
    H = H + T.gauss(cx, cy + s * 0.1, s * 0.3) * k * acesa * 0.8
    return G, H


# ------------------------------------------------------------------ Odin

def gungnir_de_odin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.32), 1.5)
    if 0 < u <= 1:
        x = -0.8 + 1.15 * u
        G += T.lines([(x - 0.55, 0.0, x, 0.0, 1.0)], 0.02) * 1.2
        g, h = icone(T, [(x + 0.16, 0.0), (x, -0.05), (x - 0.02, 0.0), (x, 0.05)], 1.4, 0.6)
        G, H = G + g, H + h
        for j in range(3):
            G += _runa(T, j, x - 0.15 - 0.13 * j, -0.05, 0.03, 1.3, 0.007)
        G += T.tapered([(x - 1.0, 0.0, x - 0.4, 0.0, 0.8)], 0.06) * 0.6
    k = 1 - rel(t, 0.88, 1)
    if t > 0.32 and k > 0:
        G += T.lines([(-0.2, 0.0, 0.35, 0.0, 1.0)], 0.02) * k * 1.2
        for j in range(3):
            G += _runa(T, j, 0.2 - 0.13 * j, -0.05, 0.03, k * (0.8 + 0.5 * math.sin(t * 20 + j)), 0.007)
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.42, 0.0, 1.3, 1.3)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.32, 0.7, 0.05, 0.45, 0.03, 0.0)
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.0) * 1.2
        for j in range(4):
            a = TAU * j / 4 + t
            G += _runa(T, j, 0.45 + 0.28 * m * math.cos(a), 0.28 * m * math.sin(a), 0.035, 1.2, 0.008)
    return G * env, H * env


def corvos_de_odin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(2):
        u = rel(t, 0.05 + 0.1 * j, 0.75 + 0.1 * j)
        if 0 < u < 1:
            e = ease_in(u, 1.2)
            r = 0.25 * (1 - e)
            a = u * TAU * 1.5 + j * math.pi
            x = -0.55 + 1.0 * e + r * math.cos(a)
            y = -0.3 + 0.25 * e + r * 0.6 * math.sin(a)
            ang = math.atan2(0.25, 1.0) + 0.6 * math.sin(a)
            g, h = _corvo(T, x, y, 0.14, ang, 1.2, math.sin(t * 35 + j))
            G, H = G + g, H + h
            H += T.gauss(x + 0.06 * math.cos(ang), y + 0.06 * math.sin(ang), 0.008) * 1.8
    q = np.random.default_rng(95)
    for j in range(8):
        w = rel(t, 0.1 + 0.06 * j, 0.7 + 0.06 * j)
        if 0 < w < 1:
            x0, y0 = -0.55 + q.uniform(-0.2, 0.6), -0.3 + q.uniform(-0.15, 0.15)
            G += T.lines([(x0, y0 + 0.4 * w, x0 + 0.04, y0 + 0.4 * w + 0.02, 1.0)], 0.008) * (1 - w) * 1.2
    m = surge(t, 0.65, 0.85) * (1 - rel(t, 0.9, 1))
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.0) * 1.2
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.13 * m * math.cos(a), 0.13 * m * math.sin(a), 0.45 + 0.26 * m * math.cos(a), 0.26 * m * math.sin(a), 1.0)], 0.01) * 1.3
    return G * env, H * env


def sabedoria_de_asgard(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.8, 0.92)
    if abre > 0 and k > 0:
        cx, cy, s = 0.0, -0.5, 0.15
        G += T.polyline([(cx - s, cy), (cx - s * 0.4, cy - s * 0.45 * abre), (cx + s * 0.4, cy - s * 0.45 * abre), (cx + s, cy)], 0.012) * k * 1.3
        G += T.polyline([(cx - s, cy), (cx - s * 0.4, cy + s * 0.4 * abre), (cx + s * 0.4, cy + s * 0.4 * abre), (cx + s, cy)], 0.012) * k * 1.3
        G += T.gauss(cx, cy, s * 0.3 * abre + 0.001) * k * 1.4
        H += T.gauss(cx, cy, 0.015) * k * abre * 2.0
        G += T.gauss(cx, cy, 0.22) * k * 0.12
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        for j in range(3):
            a0 = 0.25 + 0.06 * i + 0.08 * j
            w = rel(t, a0, a0 + 0.4)
            if 0 < w < 1:
                y = -0.35 + 0.5 * ease_in(w)
                G += _runa(T, i * 3 + j, cx - 0.1 + 0.1 * j, y, 0.04, (1 - rel(w, 0.8, 1)) * 1.4, 0.01)
        kk = pulso(t, 0.55 + 0.05 * i, 1.0)
        if kk > 0:
            G += T.ring(0.13, 0.012, cx, 0.3, 3.0) * kk * 1.2
            for m in range(2):
                y0 = 0.2 - 0.3 * rel(t, 0.55, 1.0) - 0.08 * m
                G += T.polyline([(cx - 0.06, y0 + 0.06), (cx, y0), (cx + 0.06, y0 + 0.06)], 0.014) * kk * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Fenrir

def _mandibula(T, cx, cy, s, fecha, k, ang=0.0):
    G = 0.0
    for lado in (-1, 1):
        a0 = ang + lado * (0.15 + 0.9 * (1 - fecha))
        c, sn = math.cos(a0), math.sin(a0)
        base = [(cx - c * s * 0.2, cy - sn * s * 0.2), (cx + c * s, cy + sn * s)]
        G = G + T.lines([(base[0][0], base[0][1], base[1][0], base[1][1], 1.0)], s * 0.12) * k * 1.0
        for j in range(5):
            u = 0.2 + 0.16 * j
            px, py = cx + c * s * u, cy + sn * s * u
            nx, ny = -sn * -lado, c * -lado
            G = G + T.polys([([(px - c * s * 0.05, py - sn * s * 0.05), (px + c * s * 0.05, py + sn * s * 0.05),
                               (px + nx * s * 0.12, py + ny * s * 0.12)], 1.0)], 0.002) * k * 1.3
    return G


def mordida_de_fenrir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.05, 0.35), 2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        G += _mandibula(T, 0.15, 0.0, 0.35, fecha, k)
    g, h = clarao(T, t, 0.32, 0.52, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    G += anel(T, t, 0.33, 0.7, 0.05, 0.4, 0.03, 0.0)
    q = np.random.default_rng(96)
    for j in range(12):
        w = rel(t, 0.35 + 0.02 * j, 0.9)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.2, 0.45), q.uniform(-0.45, -0.05)
            g2, h2 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.032), (1 - w) * 1.2)
            G, H = G + g2, H + h2
    return G * env, H * env


def uivo_de_fenrir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        G += T.gauss(-0.75, -0.65, 0.09 * s) * 1.0 + T.ring(0.09 * s, 0.01, -0.75, -0.65) * 1.2
        g, h = _lobo(T, -0.55, -0.15, 0.22 * s, 1.1, 0.6)
        G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.15 + 0.08 * j, 0.62 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.1 * u, 0.04 * (1 - 0.5 * u), -0.6, 0.5, 0.7, 0, -0.42, -0.2, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = surge(t, 0.5 + 0.05 * i, 0.68 + 0.05 * i) * (1 - rel(t, 0.88, 1))
        if m > 0 and i > 0:
            for k2 in range(2):
                y0 = -0.3 + 0.1 * k2 + 0.1 * rel(t, 0.5, 0.95)
                G += T.polyline([(cx - 0.07, y0), (cx, y0 + 0.07 * m), (cx + 0.07, y0)], 0.014) * m * 1.2
            G += particulas(T, t, 0.5, 1.0, 8, 97 + i, cx, 0.0, 0.12, -0.3, 0.01)
    return G * env, H * env


def fenrir_preparo(T, t, rng):
    G, H = vazio(T)
    estica = 0.5 + 0.5 * math.sin(t * TAU * 2)
    quebra = (t % 1) > 0.75
    for j in range(7):
        x = -0.45 + 0.15 * j + (0.02 * estica if j > 3 else -0.02 * estica)
        if quebra and j == 3:
            continue
        G += T.ring(0.06, 0.016, x, 0.0, 1.8 if j % 2 == 0 else 0.6) * 1.2
    if quebra:
        G += estouro(T, (t % 1 - 0.75) / 0.25, 0.0, 1.0, 10, 98, 0.0, 0.0, 0.2, 0.01)
        H += T.gauss(0.0, 0.0, 0.03) * 1.5
    g, h = _lobo(T, 0.0, -0.3, 0.19, 0.8, 0.4 * estica)
    return G + g, H + h


def ragnarok(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.38)
    if 0 < u < 1:
        x = -0.65 + 1.05 * ease_in(u, 1.3)
        y = -0.35 * math.sin(math.pi * u)
        g, h = _lobo(T, x, y, 0.35, 1.2, ease_out(u, 2))
        G, H = G + g, H + h
        G += T.tapered([(x - 0.7, y + 0.1, x - 0.2, y, 0.8)], 0.12) * 0.6
    k = 1 - rel(t, 0.55, 0.68)
    fecha = ease_in(rel(t, 0.32, 0.45), 2)
    if fecha > 0 and k > 0:
        G += _mandibula(T, 0.25, 0.0, 0.42, fecha, k)
    g2, h2 = clarao(T, t, 0.4, 0.68, 0.45, 0.0, 1.9, 1.7)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.42, 0.85, 0.05, 0.75, 0.045, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.42, 0.9, 18, 99, 0.45, 0.0, 0.7, 0.014)
    for j in range(6):
        w = rel(t, 0.55 + 0.04 * j, 1.0)
        if 0 < w < 1:
            x = 0.45 - 1.0 * ease_in(w)
            y = -0.05 * (j - 2.5) * (1 - w) - 0.15 * math.sin(math.pi * w)
            G += T.gauss(x, y, 0.02) * (1 - rel(w, 0.8, 1)) * 1.3
            H += T.gauss(x, y, 0.01) * (1 - rel(w, 0.8, 1)) * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Hel

def _mao(T, cx, cy, s, ang, k, osso=False):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.gauss(cx, cy, s * 0.35, s * 0.3) * k * (0.5 if osso else 0.9)
    for j in range(5):
        a = ang + (j - 2) * 0.3
        L = s * (0.9 if 0 < j < 4 else 0.6)
        x0, y0 = cx + s * 0.25 * math.cos(a), cy + s * 0.25 * math.sin(a)
        G = G + T.lines([(x0, y0, x0 + L * math.cos(a), y0 + L * math.sin(a), 1.0)], s * (0.05 if osso else 0.1)) * k * 1.2
        if osso:
            G = G + T.gauss(x0 + L * 0.5 * math.cos(a), y0 + L * 0.5 * math.sin(a), s * 0.05) * k * 1.4
    return G


def toque_da_morte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.6)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        x = -0.3 + 0.55 * u
        G += _mao(T, x, -0.08, 0.25, -0.1, k * 1.0, False)
        G += _mao(T, x, 0.1, 0.25, 0.1, k * 0.9, True)
        G += T.gauss(x - 0.1, 0.0, 0.08, 0.12) * k * 0.5
    g, h = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 0.9, 1.0)
    G, H = G + g, H + h
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.18 * s, 0.014, 0.45, 0.0) * 1.2
        caveira = [(-0.6, -0.2), (-0.5, -0.75), (0.0, -0.95), (0.5, -0.75), (0.6, -0.2), (0.35, 0.2), (0.3, 0.6), (-0.3, 0.6), (-0.35, 0.2)]
        g2, h2 = icone(T, poe(caveira, 0.45, -0.02, 0.1 * s), 1.1, 0.4)
        G, H = G + g2, H + h2
        for lado in (-1, 1):
            G += T.gauss(0.45 + lado * 0.035 * s, -0.04, 0.02 * s) * 1.5
    G += particulas(T, t, 0.35, 1.0, 12, 100, 0.45, 0.0, 0.15, 0.4, 0.012)
    return G * env, H * env


def exercito_dos_mortos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    p = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.85, 0.97))
    if p > 0:
        G += T.ring(0.5 * p, 0.03, -0.1, 0.36, 4.0) * 1.3
        G += T.ring(0.35 * p, 0.012, -0.1, 0.36, 4.0) * 1.0
        G += T.gauss(-0.1, 0.33, 0.45 * p, 0.06) * 0.6
    q = np.random.default_rng(101)
    for j in range(7):
        x = -0.5 + 0.14 * j + q.uniform(-0.04, 0.04)
        a0 = 0.15 + 0.05 * j
        u = ease_out(rel(t, a0, a0 + 0.3), 2)
        kk = 1 - rel(t, 0.85, 0.97)
        if u > 0 and kk > 0:
            G += _mao(T, x, 0.36 - 0.22 * u, 0.09, -math.pi / 2 + q.uniform(-0.3, 0.3), kk * 1.0, j % 2 == 0)
            G += T.lines([(x, 0.36, x, 0.36 - 0.22 * u + 0.05, 1.0)], 0.02) * kk * 0.8
    G += particulas(T, t, 0.2, 1.0, 20, 102, -0.1, 0.3, 0.5, 0.4, 0.012)
    return G * env, H * env


def hel_preparo(T, t, rng):
    G, H = vazio(T)
    coroa = [(-0.5, 0.3), (-0.55, -0.3), (-0.3, 0.0), (-0.15, -0.6), (0.0, -0.1), (0.15, -0.6), (0.3, 0.0), (0.55, -0.3), (0.5, 0.3)]
    g, h = icone(T, poe(coroa, 0.0, -0.15, 0.2), 1.1, 0.45)
    G, H = G + g, H + h
    for m in range(5):
        a = t * TAU + TAU * m / 5
        G += T.gauss(0.35 * math.cos(a), 0.15 + 0.12 * math.sin(a), 0.1, 0.05) * 0.35
    for j in range(6):
        a = -t * TAU * 0.5 + TAU * j / 6
        x, y = 0.3 * math.cos(a), 0.15 + 0.1 * math.sin(a)
        G += T.lines([(x - 0.025, y, x + 0.025, y, 1.0), (x, y - 0.025, x, y + 0.025, 1.0)], 0.006) * 1.3
    return G, H


def _cristal(T, cx, cy, s, k):
    pts = [(cx - s * 0.5, cy), (cx - s * 0.25, cy - s * 1.0), (cx, cy - s * 0.3), (cx + s * 0.15, cy - s * 1.2), (cx + s * 0.35, cy - s * 0.4),
           (cx + s * 0.6, cy - s * 0.8), (cx + s * 0.55, cy)]
    return icone(T, pts, k, 0.4)


def frio_de_helheim(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for m in range(6):
        u = rel(t, 0.03 * m, 0.55 + 0.03 * m)
        if 0 < u < 1:
            x = -1.0 + 2.0 * ease_out(u, 1.3)
            G += T.gauss(x, 0.1 + 0.05 * (m % 3 - 1), 0.3, 0.1) * (1 - rel(u, 0.7, 1)) * 0.2
    kk = 1 - rel(t, 0.88, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        cresce = ease_out(rel(t, 0.35 + 0.07 * i, 0.6 + 0.07 * i), 2)
        if cresce > 0 and kk > 0:
            g, h = _cristal(T, cx, 0.3, 0.3 * cresce, kk * 1.1)
            G, H = G + g, H + h
            G += T.gauss(cx, 0.1, 0.13, 0.2) * cresce * kk * 0.35
        g2, h2 = clarao(T, t, 0.55 + 0.07 * i, 0.72 + 0.07 * i, cx, 0.05, 0.4, 0.8)
        G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.35, 0.95, 1.0, 0.35, 1.3)
    G += particulas(T, t, 0.3, 1.0, 22, 103, 0.0, 0.0, 0.8, -0.3, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Jason

_FACAO = [(0, -1), (0.2, -0.85), (0.22, 0.35), (0.12, 0.4), (0.1, 0.95), (-0.1, 0.95), (-0.12, 0.4), (-0.12, -0.8)]


def facao_de_jason(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2.2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.3 + 2.2 * u
        cx, cy = 0.1 + 0.3 * math.cos(ang), 0.1 + 0.3 * math.sin(ang)
        g, h = icone(T, poe(_FACAO, cx, cy, 0.3, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = corte(T, t, 0.3, 0.52, 0.75, 1.2, 0.09, 0.45, 0.0, 0.08)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.32, 0.52, 0.45, 0.0, 1.0)
    G, H = G + g3, H + h3
    q = np.random.default_rng(104)
    for j in range(12):
        w = rel(t, 0.33 + 0.02 * j, 0.9)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.45), q.uniform(-0.45, -0.1)
            g4, h4 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.033), (1 - w) * 1.2)
            G, H = G + g4, H + h4
    return G * env, H * env


def volta_do_lago(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    G += T.lines([(-0.7, 0.3, 0.7, 0.3, 1.0)], 0.01) * k * 1.0
    for m in range(3):
        G += T.ring(0.15 + 0.15 * m + 0.1 * ((t * 1.5) % 1), 0.008, 0.0, 0.3, 4.0) * k * (1 - 0.3 * m) * 0.9
    sobe = ease_out(rel(t, 0.1, 0.55), 1.8)
    if sobe > 0 and k > 0:
        y = 0.35 - 0.45 * sobe
        g, h = _mascara_hoquei(T, 0.0, y, 0.18, k * 1.1)
        G, H = G + g, H + h
        for j in range(8):
            a = math.pi + math.pi * j / 7
            w = rel(t, 0.15, 0.6)
            if 0 < w < 1:
                G += T.gauss(0.2 * math.cos(a) * (0.5 + w), 0.3 - 0.25 * math.sin(math.pi * w) * abs(math.sin(a)), 0.012) * (1 - w) * 1.4
    kk = pulso(t, 0.5, 1.0)
    if kk > 0:
        G += T.gauss(0.0, -0.1, 0.25, 0.3) * kk * 0.4
        G += T.ring(0.3, 0.015, 0.0, -0.1) * kk * 1.0
    return G * env, H * env


def jason_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _mascara_hoquei(T, 0.0, 0.0, 0.2, 1.0)
    G, H = G + g, H + h
    for j in range(3):
        u = (t * 1.5 + j / 3) % 1
        G += T.arc_band(0.25 + 0.3 * u, 0.012, -0.5, 0.5, 1.0, 0, 0.0, 0.0, 0.0) * (1 - u) * 1.1
        G += T.arc_band(0.25 + 0.3 * u, 0.012, math.pi - 0.5, math.pi + 0.5, 1.0, 0, 0.0, 0.0, 0.0) * (1 - u) * 1.1
    return G, H


def sexta_feira_13(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        G += T.gauss(-0.4, -0.6, 0.12 * s) * 1.0 + T.ring(0.12 * s, 0.012, -0.4, -0.6) * 1.2
        H += T.gauss(-0.4, -0.6, 0.05 * s) * 0.6
    for j, ang in enumerate((0.8, -0.7, 0.2, 1.3)):
        a0 = 0.2 + 0.1 * j
        g, h = corte(T, t, a0, a0 + 0.18, ang, 1.0, 0.07, 0.45, 0.0, 0.08)
        G, H = G + g * 1.2, H + h
        g2, h2 = clarao(T, t, a0 + 0.05, a0 + 0.2, 0.45, 0.0, 0.8, 1.0)
        G, H = G + g2, H + h2
    q = np.random.default_rng(105)
    for j in range(16):
        w = rel(t, 0.3 + 0.025 * j, 0.95)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.4, 0.45), q.uniform(-0.5, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.032), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Freddy

def _luva(T, cx, cy, s, ang, k):
    G = T.gauss(cx, cy, s * 0.3, s * 0.25) * k * 0.9
    for j in range(4):
        a = ang + (j - 1.5) * 0.18
        x0, y0 = cx + s * 0.25 * math.cos(a), cy + s * 0.25 * math.sin(a)
        G = G + T.tapered([(x0, y0, x0 + s * math.cos(a), y0 + s * math.sin(a), 1.0)], s * 0.06) * k * 1.4
    return G


def cancao_de_ninar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(6):
        u = rel(t, 0.06 * j, 0.5 + 0.06 * j)
        if 0 < u < 1:
            x = -0.55 + 1.0 * ease_out(u, 1.3)
            y = -0.2 - 0.15 * math.sin(u * TAU + j)
            g, h = icone(T, poe(NOTA, x, y, 0.075, 0.3 * math.sin(u * 8)), (1 - rel(u, 0.8, 1)) * 1.2, 0.7)
            G, H = G + g, H + h
    for j in range(3):
        u = ((t - 0.45) * 1.2 + j / 3) % 1 if t > 0.45 else -1
        if 0 < u < 1:
            x, y = 0.5 + 0.12 * u, -0.2 - 0.35 * u
            z = 0.03 + 0.02 * u
            G += T.lines([(x - z, y - z, x + z, y - z, 1.0), (x + z, y - z, x - z, y + z, 1.0), (x - z, y + z, x + z, y + z, 1.0)], 0.01) * (1 - u) * 1.4
    k = pulso(t, 0.45, 1.0)
    G += T.gauss(0.45, 0.0, 0.15) * k * 0.35
    return G * env, H * env


def garra_de_laminas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 1.8)
    k = 1 - rel(t, 0.4, 0.5)
    if k > 0:
        G += _luva(T, -0.25 + 0.4 * u, -0.3 + 0.2 * u, 0.36, 0.6, k)
    for m in range(4):
        dx, dy = -math.sin(0.7) * 0.07 * (m - 1.5), math.cos(0.7) * 0.07 * (m - 1.5)
        g, h = corte(T, t, 0.22 + 0.012 * m, 0.45 + 0.012 * m, 0.7, 0.75, 0.04, 0.45 + dx, dy, 0.06)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.25, 0.45, 0.45, 0.0, 1.0)
    G, H = G + g2, H + h2
    for j in range(5):
        H += T.gauss(0.2 + 0.08 * j, -0.2 + 0.05 * j, 0.008) * pulso(t, 0.2 + 0.03 * j, 0.4 + 0.03 * j) * 2.0
    q = np.random.default_rng(106)
    for j in range(10):
        w = rel(t, 0.3 + 0.02 * j, 0.85)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.45), q.uniform(-0.45, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.03), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


def freddy_preparo(T, t, rng):
    G, H = vazio(T)
    chapeu = [(-0.7, 0.2), (-0.4, 0.15), (-0.35, -0.5), (0.35, -0.5), (0.4, 0.15), (0.7, 0.2), (0.7, 0.32), (-0.7, 0.32)]
    g, h = icone(T, poe(chapeu, 0.0, -0.3, 0.28), 1.0, 0.4)
    G, H = G + g, H + h
    raspa = (t * 2) % 1
    G += _luva(T, 0.1, 0.15, 0.32, -0.3 + 0.6 * raspa, 1.0)
    q = np.random.default_rng(int(t * 10))
    for _ in range(4):
        x, y = 0.35 + q.uniform(-0.05, 0.1), 0.1 + q.uniform(-0.1, 0.15)
        H += T.gauss(x, y, 0.008) * 1.8
    return G, H


def pesadelo_de_freddy(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for m in range(5):
        y = -0.6 + 0.12 * m
        G += T.lines([(-0.9, y, 0.9, y, 1.0)], 0.03) * pulso(t, 0.0, 0.5) * (0.35 if m % 2 else 0.15)
    u = ease_in(rel(t, 0.2, 0.45), 1.8)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        G += _luva(T, -0.25 + 0.5 * u, -0.45 + 0.35 * u, 0.5, 0.6, k)
    for m in range(4):
        dx, dy = -math.sin(0.7) * 0.1 * (m - 1.5), math.cos(0.7) * 0.1 * (m - 1.5)
        g, h = corte(T, t, 0.42 + 0.012 * m, 0.65 + 0.012 * m, 0.7, 1.2, 0.06, 0.45 + dx, dy, 0.08)
        G, H = G + g * 1.3, H + h
    g2, h2 = clarao(T, t, 0.45, 0.7, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g2, H + h2
    s = surge(t, 0.6, 0.8) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.18 * s, 0.014, 0.45, 0.0) * 1.2
        G += T.lines([(0.45 - 0.12 * s, -0.12 * s, 0.45 + 0.12 * s, 0.12 * s, 1.0), (0.45 + 0.12 * s, -0.12 * s, 0.45 - 0.12 * s, 0.12 * s, 1.0)], 0.014) * 1.3
    G += particulas(T, t, 0.5, 1.0, 12, 107, 0.45, 0.0, 0.15, -0.3, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Michael Myers

_FACA = [(0, -1), (0.16, -0.7), (0.16, 0.2), (0.1, 0.25), (0.1, 0.95), (-0.1, 0.95), (-0.1, 0.25), (-0.02, 0.2), (-0.02, -0.7)]


def faca_de_cozinha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.25), 2)
    desce = ease_in(rel(t, 0.3, 0.45), 2.5)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        y = 0.0 - 0.45 * sobe + 0.45 * desce
        g, h = icone(T, poe(_FACA, 0.35, y, 0.28, math.pi * (1 if desce > 0.5 else 0)), k * 1.2, 0.5)
        G, H = G + g, H + h
        brilho = rel(t, 0.15, 0.3)
        if 0 < brilho < 1:
            H += T.flare(0.36, y - 0.1, 0.12 * math.sin(math.pi * brilho), 0.3, 0.006) * 1.5
    g2, h2 = corte(T, t, 0.38, 0.55, 1.4, 0.9, 0.08, 0.45, 0.0)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.4, 0.6, 0.45, 0.05, 1.2, 1.3)
    G, H = G + g3, H + h3
    q = np.random.default_rng(108)
    for j in range(8):
        w = rel(t, 0.42 + 0.02 * j, 0.95)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.3, 0.35), q.uniform(-0.4, -0.1)
            g4, h4 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.03), (1 - w) * 1.1)
            G, H = G + g4, H + h4
    return G * env, H * env


_MASCARA_BRANCA = [(0, -1), (0.55, -0.85), (0.7, -0.3), (0.6, 0.4), (0.3, 0.85), (0, 0.95), (-0.3, 0.85), (-0.6, 0.4), (-0.7, -0.3), (-0.55, -0.85)]


def respiracao_na_mascara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = icone(T, poe(_MASCARA_BRANCA, -0.5, -0.2, 0.18), s * 1.1, 0.55)
        G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.15 + 0.12 * j, 0.6 + 0.12 * j)
        if 0 < u < 1:
            G += T.arc_band(0.1 + 0.9 * u, 0.02, -0.4, 0.4, 0.7, 0, -0.45, -0.1, 0.0) * (1 - u) * 1.0
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.0) * 1.2
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.13 * m * math.cos(a), 0.13 * m * math.sin(a), 0.45 + 0.26 * m * math.cos(a), 0.26 * m * math.sin(a), 1.0)], 0.01) * 1.3
        for k2 in range(2):
            y0 = -0.32 + 0.08 * k2 + 0.1 * rel(t, 0.5, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.06 * m), (0.52, y0)], 0.013) * m * 1.2
    return G * env, H * env


def myers_preparo(T, t, rng):
    G, H = vazio(T)
    sombra = [(-0.2, 0.4), (-0.25, -0.05), (-0.15, -0.3), (-0.07, -0.38), (0.07, -0.38), (0.15, -0.3), (0.25, -0.05), (0.2, 0.4)]
    g, h = icone(T, sombra, 0.4, 0.2)
    G, H = G + g, H + h
    g2, h2 = icone(T, poe(_MASCARA_BRANCA, 0.0, -0.28, 0.07), 1.2, 0.6)
    G, H = G + g2, H + h2
    pisca = 0.7 + 0.3 * math.sin(t * TAU * 3) * math.sin(t * TAU * 1.3)
    g3, h3 = _abobora(T, 0.32, 0.28, 0.13, 1.0, pisca)
    return G + g3, H + h3


def noite_de_halloween(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for i, (x, y) in enumerate(((-0.75, 0.3), (-0.45, 0.33), (0.75, 0.3))):
        s = surge(t, 0.05 * i, 0.2 + 0.05 * i)
        if s > 0 and kk > 0:
            g, h = _abobora(T, x, y - 0.02, 0.1 * s, kk, 0.6 + 0.4 * math.sin(t * 20 + i))
            G, H = G + g, H + h
    u = ease_in(rel(t, 0.2, 0.4), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if u > 0 and k > 0:
        g2, h2 = icone(T, poe(_FACA, 0.45, -0.45 + 0.4 * u, 0.22, math.pi), k * 1.3, 0.5)
        G, H = G + g2, H + h2
        G += T.gauss(0.45, -0.6, 0.2, 0.15) * k * 0.4 * (1 - u)
    g3, h3 = corte(T, t, 0.36, 0.55, 1.45, 1.1, 0.1, 0.45, 0.0)
    G, H = G + g3 * 1.3, H + h3
    g4, h4 = clarao(T, t, 0.38, 0.65, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g4, H + h4
    G += anel(T, t, 0.4, 0.8, 0.05, 0.6, 0.04, 0.0, 1.0, 1.3)
    G += estouro(T, t, 0.4, 0.85, 14, 109, 0.45, 0.0, 0.55, 0.013)
    return G * env, H * env


REGISTRO = [
    ("gungnir_de_odin", gungnir_de_odin, GRANDE, "Odin · a Gungnir com as runas", False),
    ("corvos_de_odin", corvos_de_odin, GRANDE, "Odin · Hugin e Munin", False),
    ("sabedoria_de_asgard", sabedoria_de_asgard, GRANDE, "Odin · o olho e as runas no trio", False),
    ("mordida_de_fenrir", mordida_de_fenrir, GRANDE, "Fenrir · as mandíbulas fechando", False),
    ("uivo_de_fenrir", uivo_de_fenrir, GRANDE, "Fenrir · o uivo para a lua", False),
    ("fenrir_preparo", fenrir_preparo, MEDIA, "Fenrir · a corrente Gleipnir arrebentando (Preparo, laço)", True),
    ("ragnarok", ragnarok, GRANDE, "Fenrir · o lobo gigante saltando", False),
    ("toque_da_morte", toque_da_morte, GRANDE, "Hel · a mão e a caveira", False),
    ("exercito_dos_mortos", exercito_dos_mortos, GRANDE, "Hel · as mãos subindo do chão", False),
    ("hel_preparo", hel_preparo, MEDIA, "Hel · a coroa e a névoa fria (Preparo, laço)", True),
    ("frio_de_helheim", frio_de_helheim, GRANDE, "Hel · o gelo crescendo nos rivais", False),
    ("facao_de_jason", facao_de_jason, GRANDE, "Jason · o facão e o sangue", False),
    ("volta_do_lago", volta_do_lago, GRANDE, "Jason · a máscara emergindo do lago", False),
    ("jason_preparo", jason_preparo, MEDIA, "Jason · a máscara e o \"ki-ki-ki\" (Preparo, laço)", True),
    ("sexta_feira_13", sexta_feira_13, GRANDE, "Jason · os golpes sob a lua", False),
    ("cancao_de_ninar", cancao_de_ninar, GRANDE, "Freddy · as notas e o sono", False),
    ("garra_de_laminas", garra_de_laminas, GRANDE, "Freddy · a luva de lâminas", False),
    ("freddy_preparo", freddy_preparo, MEDIA, "Freddy · o chapéu e a luva raspando (Preparo, laço)", True),
    ("pesadelo_de_freddy", pesadelo_de_freddy, GRANDE, "Freddy · a garra gigante do pesadelo", False),
    ("faca_de_cozinha", faca_de_cozinha, GRANDE, "Michael Myers · a faca descendo", False),
    ("respiracao_na_mascara", respiracao_na_mascara, GRANDE, "Michael Myers · a máscara e a respiração", False),
    ("myers_preparo", myers_preparo, MEDIA, "Michael Myers · a abóbora e a silhueta (Preparo, laço)", True),
    ("noite_de_halloween", noite_de_halloween, GRANDE, "Michael Myers · as abóboras e o golpe final", False),
]
