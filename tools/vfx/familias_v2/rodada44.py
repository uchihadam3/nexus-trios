"""Rodada 44 das habilidades próprias: Byakuya, Kitana, Shao Kahn, Snorlax, Patrick e Flecha.

Byakuya Kuchiki
- senbonzakura: a lâmina virando mil pétalas cortantes que varrem todos os rivais.
- danku: a parede de luz translúcida subindo na frente do trio (Escudo e Protegido).
- byakuya_preparo: o Preparo do Senkei — a espada solta se desfazendo em pétalas em volta (laço).
- senkei: as fileiras de espadas formando o círculo em volta dos rivais e cortando juntas (Dissipar).

Kitana
- leque_cortante: os leques de aço abrindo e cortando em arco.
- rajada_de_leque: o abano do leque soltando o redemoinho de vento no rival (Preso).
- kitana_preparo: o Preparo da Fatality — os dois leques abertos e cruzados (laço).
- fatality_do_leque: o leque girando como serra, voando e cortando o rival.

Shao Kahn
- martelo_de_guerra: o martelo de guerra enorme descendo no rival (Enfraquecido).
- provocacao_de_kahn: o elmo de caveira, a risada em ondas vermelhas (Provocado e Fortalecido).
- kahn_preparo: o Preparo da Lança de Kahn — a lança erguida brilhando (laço).
- lanca_de_kahn: a lança lançada atravessando o rival.

Snorlax
- pancada_snorlax: a barrigona balançando e a pancada (Lento).
- descansar: o Snorlax dormindo, o "Zzz" e as bolhas de cura (Vida, Regeneração e Provocado).
- snorlax_preparo: o Preparo do Giga Impacto — o corpo enrolando e quicando (laço).
- giga_impacto: o corpanzil caindo com a aura e a onda gigante em todos.

Patrick Estrela
- abraco_esmagador: os braços de estrela apertando o rival e os corações (Preso).
- debaixo_da_pedra: a pedra levantando e baixando por cima dele como escudo (Protegido e Provocado).
- patrick_preparo: o Preparo do Isso é burrice — o balão de pensamento vazio e o ventinho (laço).
- isso_e_burrice: as besteiras voando para todo lado, as interrogações em todos (Confuso).

Flecha
- soco_veloz: os socos supersônicos em riscos vermelhos (Adianta o ataque).
- corrida_na_agua: correndo por cima da água, os respingos atrás (Esquiva e Acelerado).
- furacao_flecha: correndo em círculo até virar um furacão em volta de todos (Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CORACAO, ESPADA, GOTA, anel, aura, cheio, circulo, clarao, converge, corte, estouro, estrela_pts, flor, icone,
                         onda_no_chao, particulas, poe, surge)


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


_PETALA = [(0, -1)] + [(0.45 * math.sin(math.pi * u), -1 + 1.8 * u) for u in np.linspace(0.05, 0.95, 8)] + [(0.1, 0.85), (0, 0.7), (-0.1, 0.85)] + \
          [(-0.45 * math.sin(math.pi * u), -1 + 1.8 * u) for u in np.linspace(0.95, 0.05, 8)]


def _leque(T, cx, cy, s, ang, abre, k):
    G, H = 0.0, 0.0
    pts = [(cx, cy)]
    for a in np.linspace(-abre / 2, abre / 2, 14):
        pts.append((cx + s * math.cos(ang + a), cy + s * math.sin(ang + a)))
    g, h = icone(T, pts, k * 1.1, 0.45)
    G, H = G + g, H + h
    for a in np.linspace(-abre / 2, abre / 2, 7):
        G = G + T.lines([(cx, cy, cx + s * math.cos(ang + a), cy + s * math.sin(ang + a), 1.0)], s * 0.03) * k * 0.9
    return G, H


# ------------------------------------------------------------------ Byakuya

def senbonzakura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(5)
    for j in range(40):
        a0 = q.uniform(0, 0.3)
        u = rel(t, a0, a0 + 0.6)
        if 0 < u < 1:
            y0 = q.uniform(-0.5, 0.3)
            x = -0.9 + 1.9 * ease_out(u, 1.3) + 0.05 * math.sin(u * 10 + j)
            y = y0 + 0.12 * math.sin(u * 6 + j)
            g, h = icone(T, poe(_PETALA, x, y, 0.035, u * 8 + j), (1 - rel(u, 0.8, 1)) * 1.1, 0.6)
            G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.35 + 0.2 * (x + 0.55), 0.5 + 0.2 * (x + 0.55), x, 0.0, 0.45)
        G, H = G + g2, H + h2
    return G * env, H * env


def danku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2.5)
    k = 1 - rel(t, 0.88, 1)
    if sobe > 0 and k > 0:
        alto = 0.85 * sobe
        parede = [(0.6, 0.35), (0.75, 0.35), (0.75, 0.35 - alto), (0.6, 0.35 - alto)]
        G += T.polys([(parede, 1.0)], 0.02) * k * 0.35
        G += T.polyline(parede + [parede[0]], 0.012) * k * 1.3
        brilho = (t * 1.5) % 1
        G += T.lines([(0.6, 0.35 - alto * brilho, 0.75, 0.35 - alto * brilho, 1.0)], 0.02) * k * 1.0
    for x in (-0.55, 0.0, 0.55):
        m = surge(t, 0.35, 0.55) * k
        if m > 0:
            G += T.arc_band(0.2 * m, 0.025, -2.6, -0.5, 1.0, 0, x - 0.1, 0.3, 0.0) * 1.0
    return G * env, H * env


def byakuya_preparo(T, t, rng):
    G, H = vazio(T)
    some = (t * 1.2) % 1
    g, h = icone(T, poe(ESPADA, 0, 0.05, 0.38, 0), (1 - 0.6 * some), 0.5)
    G, H = G + g, H + h
    for j in range(12):
        a = t * TAU * 0.8 + TAU * j / 12
        r = 0.18 + 0.15 * ((t + j / 12) % 1)
        g2, h2 = icone(T, poe(_PETALA, r * math.cos(a), r * math.sin(a) * 0.8, 0.028, a), 1.1, 0.6)
        G, H = G + g2, H + h2
    return G, H


def senkei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    forma = ease_out(rel(t, 0.0, 0.45), 2)
    k = 1 - rel(t, 0.6, 0.7)
    if forma > 0 and k > 0:
        n = int(24 * forma) + 1
        for j in range(n):
            a = TAU * j / 24
            r = 0.75
            g, h = icone(T, poe(ESPADA, r * math.cos(a), 0.0 + r * 0.55 * math.sin(a), 0.12, a + math.pi / 2), k * 1.0, 0.5)
            G, H = G + g, H + h
    for j in range(5):
        g2, h2 = corte(T, t, 0.6 + 0.03 * j, 0.8 + 0.03 * j, -1.0 + 0.5 * j, 1.6, 0.06, 0.0, 0.0)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.62, 0.82, 0.0, 0.0, 1.6, 1.5)
    G, H = G + g3, H + h3
    q = np.random.default_rng(9)
    for j in range(16):
        w = rel(t, 0.65, 1.0)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            r = 0.1 + 0.6 * w
            g4, h4 = icone(T, poe(_PETALA, r * math.cos(a), r * 0.6 * math.sin(a), 0.03, a + w * 5), (1 - w) * 1.1, 0.6)
            G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Kitana

def leque_cortante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 3)
    u = ease_in(rel(t, 0.15, 0.4), 1.8)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.2 + 2.0 * u
        g, h = _leque(T, -0.1, 0.1, 0.45, ang, 1.6 * abre + 0.1, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.45, 0.06, ang - 0.9, ang, 1.0, 0, -0.1, 0.1, 1.0) * k * 0.7
    g2, h2 = corte(T, t, 0.3, 0.55, -0.5, 1.3, 0.08, 0.4, 0.0, 0.1)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.35, 0.55, 0.4, 0.0, 1.0)
    return (G + g3) * env, (H + h3) * env


def rajada_de_leque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abana = math.sin(rel(t, 0.0, 0.3) * math.pi)
    k = 1 - rel(t, 0.4, 0.5)
    if k > 0:
        g, h = _leque(T, -0.6, 0.05, 0.22, -0.3 * abana, 1.8, k)
        G, H = G + g, H + h
    u = rel(t, 0.2, 0.75)
    if 0 < u < 1:
        x = -0.4 + 0.95 * u
        for m in range(3):
            a = t * 18 + m * 2.1
            G += T.arc_band(0.08 + 0.1 * u, 0.025, a, a + 3.2, 0.6, 0, x, 0.0, 1.0) * (1 - rel(u, 0.85, 1)) * 1.2
        for m in range(4):
            G += T.lines([(x - 0.3 - 0.05 * m, -0.12 + 0.08 * m, x - 0.1, -0.1 + 0.07 * m, 1.0)], 0.006) * 1.0
    m = surge(t, 0.65, 0.85) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.18 * m, 0.02, 0.55, 0.0, 0.6) * 1.2
    return G * env, H * env


def kitana_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        g, h = _leque(T, lado * 0.08, 0.1, 0.25, -math.pi / 2 + lado * 0.5, 1.7, 1.0)
        G, H = G + g, H + h
    H += T.gauss(0, -0.1, 0.02) * (1.3 + 0.7 * math.sin(t * 9))
    return G, H


def fatality_do_leque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.4), 1.5)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        x = -0.65 + 1.1 * u
        a = t * 40
        for m in range(3):
            g, h = _leque(T, x, 0.0, 0.16, a + TAU * m / 3, 1.2, k)
            G, H = G + g, H + h
        G += T.ring(0.17, 0.012, x, 0.0) * k * 1.0
    g2, h2 = clarao(T, t, 0.38, 0.62, 0.45, 0.0, 1.4, 1.4)
    G, H = G + g2, H + h2
    for j in range(4):
        g3, h3 = corte(T, t, 0.4 + 0.04 * j, 0.6 + 0.04 * j, -1.2 + 0.8 * j, 1.0, 0.06, 0.45, 0.0)
        G, H = G + g3, H + h3
    G += estouro(T, t, 0.42, 0.95, 16, 5, 0.45, 0.0, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Shao Kahn

def _martelo(T, px, py, a, s, k):
    hx, hy = px + s * math.cos(a), py + s * math.sin(a)
    G = T.lines([(px, py, hx, hy, 1.0)], 0.03) * k * 1.2
    pe = a + math.pi / 2
    cab = [(hx + 0.2 * math.cos(pe) + 0.1 * math.cos(a), hy + 0.2 * math.sin(pe) + 0.1 * math.sin(a)),
           (hx - 0.2 * math.cos(pe) + 0.1 * math.cos(a), hy - 0.2 * math.sin(pe) + 0.1 * math.sin(a)),
           (hx - 0.2 * math.cos(pe) - 0.12 * math.cos(a), hy - 0.2 * math.sin(pe) - 0.12 * math.sin(a)),
           (hx + 0.2 * math.cos(pe) - 0.12 * math.cos(a), hy + 0.2 * math.sin(pe) - 0.12 * math.sin(a))]
    g, h = icone(T, cab, k * 1.2, 0.5)
    return G + g, h


def martelo_de_guerra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.3)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        g, h = _martelo(T, -0.1, 0.35, -2.1 + 1.75 * u, 0.6, k)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.45, 0.1, 1.4, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.33, 0.9, 0.9, 0.35, 1.7)
    G += estouro(T, t, 0.35, 0.9, 16, 5, 0.45, 0.1, 0.6, 0.015)
    return G * env, H * env


_ELMO = [(-0.7, -0.6), (0.0, -1.0), (0.7, -0.6), (0.75, 0.3), (0.35, 0.7), (0.0, 0.55), (-0.35, 0.7), (-0.75, 0.3)]


def provocacao_de_kahn(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = icone(T, poe(_ELMO, -0.5, -0.15, 0.2 * s), 1.2, 0.45)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(-0.5 + lado * 0.07, -0.18, 0.02) * s * 2.2
            G += T.gauss(-0.5 + lado * 0.07, -0.18, 0.035) * s * 1.2
    for j in range(4):
        u = rel(t, 0.15 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            G += T.arc_band(0.2 + 0.9 * u, 0.04 * (1 - 0.5 * u), -0.6, 0.6, 0.7, 0, -0.5, -0.1, 0.0) * (1 - u) * 1.3
    g2, h2 = aura(T, t, 0.45, 1.0, 0.3, -0.1, 0.6)
    return (G + g2 * 0.5) * env, (H + h2 * 0.5) * env


def kahn_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(0.0, 0.4, 0.0, -0.3, 1.0)], 0.025) * 1.1
    g, h = icone(T, [(0.0, -0.55), (0.07, -0.3), (-0.07, -0.3)], 1.2, 0.6)
    G, H = G + g, H + h
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    H += T.gauss(0, -0.45, 0.025) * (1.4 + b)
    G += T.gauss(0, -0.4, 0.15) * (0.3 + 0.2 * b)
    return G, H


def lanca_de_kahn(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        x = -0.7 + 1.5 * u
        G += T.lines([(x - 0.5, 0.0, x, 0.0, 1.0)], 0.022) * k * 1.2
        g, h = icone(T, [(x + 0.16, 0.0), (x - 0.02, -0.06), (x - 0.02, 0.06)], k * 1.3, 0.6)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.9, 0.0, x - 0.5, 0.0, 1.0)], 0.04) * k * 0.6
    g2, h2 = clarao(T, t, 0.25, 0.45, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.27, 0.7, 0.05, 0.5, 0.035, 0.0)
    G += estouro(T, t, 0.27, 0.8, 14, 4, 0.45, 0.0, 0.5, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Snorlax

def pancada_snorlax(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    bal = math.sin(t * 20) * pulso(t, 0.0, 0.35) * 0.04
    G += T.gauss(-0.45 + bal, 0.05, 0.22, 0.2) * pulso(t, 0.0, 0.6) * 0.7
    u = ease_in(rel(t, 0.2, 0.4), 2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0 and u > 0:
        P, nos = _punho(T, -0.3 + 0.7 * u, 0.0, 2.6, 0)
        G += P * 0.95 * k
        H += nos * 0.4 * k
    g, h = clarao(T, t, 0.38, 0.58, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.38, 0.85, 0.6, 0.35, 1.3)
    return G * env, H * env


def descansar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    resp = 0.03 * math.sin(t * TAU * 1.5)
    G += T.gauss(0, 0.1, 0.28 + resp, 0.2 + resp) * 0.6
    for j in range(3):
        u = ((t * 1.2) + j / 3) % 1
        x, y = 0.15 + 0.15 * u, -0.2 - 0.35 * u
        z = 0.03 + 0.02 * u
        G += T.lines([(x - z, y - z, x + z, y - z, 1.0), (x + z, y - z, x - z, y + z, 1.0), (x - z, y + z, x + z, y + z, 1.0)], 0.01) * (1 - u) * 1.4
    q = np.random.default_rng(4)
    for j in range(10):
        u = ((t * 0.8) + j / 10) % 1
        x = q.uniform(-0.35, 0.35)
        G += T.ring(0.02 + 0.01 * (j % 3), 0.006, x, 0.3 - 0.5 * u) * pulso(t, 0.1, 1.0) * (1 - u) * 1.2
    g, h = aura(T, t, 0.2, 1.0, 0.35, 0.1, 0.7)
    return (G + g) * env, (H + h) * env


def snorlax_preparo(T, t, rng):
    G, H = vazio(T)
    pula = abs(math.sin(t * TAU * 1.5))
    G += T.gauss(0, 0.15 - 0.1 * pula, 0.2, 0.17) * 0.8
    G += T.ring(0.22, 0.02, 0, 0.15 - 0.1 * pula, 1.2) * 1.0
    G += onda_no_chao(T, (t * 1.5) % 1, 0.0, 1.0, 0.4, 0.35, 0.8)
    return G, H


def giga_impacto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        y = -0.8 + 0.9 * u
        G += T.gauss(0.0, y, 0.35, 0.28) * k * 0.9
        G += T.ring(0.38, 0.04, 0.0, y, 1.25) * k * 1.2
        q = np.random.default_rng(int(t * 20))
        for _ in range(8):
            a = q.uniform(0, TAU)
            G += T.lines([(0.42 * math.cos(a), y + 0.34 * math.sin(a), 0.55 * math.cos(a), y + 0.45 * math.sin(a), 1.0)], 0.01) * k * 1.2
    g, h = clarao(T, t, 0.38, 0.62, 0.0, 0.2, 1.8, 1.6)
    G, H = G + g, H + h
    for j in range(2):
        G += anel(T, t, 0.4 + 0.08 * j, 0.95, 0.1, 1.1, 0.05, 0.2, 2.0)
    G += onda_no_chao(T, t, 0.4, 0.95, 1.0, 0.35, 1.8)
    G += estouro(T, t, 0.42, 0.95, 20, 6, 0.0, 0.2, 0.9, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Patrick

def abraco_esmagador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_out(rel(t, 0.0, 0.35), 2)
    aperta = 0.03 * math.sin(t * 25) * pulso(t, 0.35, 0.8)
    k = 1 - rel(t, 0.8, 0.9)
    for lado in (-1, 1):
        a0 = math.pi if lado < 0 else 0.0
        r = 0.28 - 0.06 * fecha + aperta
        G += T.arc_band(r, 0.07, a0 - lado * 1.5 * fecha, a0 + lado * 0.0 + 0.01, 0.8, 0, 0.45, 0.0, 0.0) * k * 1.1
    G += T.gauss(0.45, 0.0, 0.1) * pulso(t, 0.3, 0.8) * 0.6
    for j in range(4):
        u = rel(t, 0.4 + 0.08 * j, 0.9)
        if 0 < u < 1:
            g, h = cheio(T, poe(CORACAO, 0.3 + 0.1 * j, -0.2 - 0.3 * u, 0.04), (1 - u) * 1.3)
            G, H = G + g, H + h
    return G * env, H * env


_PEDRA_GRANDE = [(-1.0, 0.4), (-0.8, -0.3), (-0.3, -0.6), (0.4, -0.55), (0.9, -0.2), (1.0, 0.4)]


def debaixo_da_pedra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = math.sin(math.pi * rel(t, 0.0, 0.6))
    k = 1 - rel(t, 0.88, 1)
    y = 0.15 - 0.25 * sobe
    g, h = icone(T, poe(_PEDRA_GRANDE, 0.0, y, 0.3), k * 1.1, 0.45)
    G, H = G + g, H + h
    for m in range(3):
        G += T.lines([(-0.15 + 0.12 * m, y - 0.05, -0.05 + 0.12 * m, y + 0.03, 1.0)], 0.008) * k * 0.9
    if sobe > 0.2:
        G += T.gauss(0.0, 0.3, 0.12, 0.05) * sobe * 0.9
    G += onda_no_chao(T, t, 0.55, 0.9, 0.6, 0.35, 1.3)
    q = np.random.default_rng(3)
    for j in range(6):
        w = rel(t, 0.55, 0.9)
        if 0 < w < 1:
            a = q.uniform(math.pi, TAU)
            G += T.gauss(0.35 * w * math.cos(a) * 2, 0.35 + 0.2 * w * math.sin(a), 0.015) * (1 - w) * 1.2
    return G * env, H * env


def patrick_preparo(T, t, rng):
    G, H = vazio(T)
    for j, (x, y, r) in enumerate(((-0.1, 0.25, 0.035), (0.02, 0.08, 0.05), (0.2, -0.18, 0.22))):
        G += T.ring(r, 0.02, x, y, 1.0 if j < 2 else 1.4) * 1.2
    u = (t * 1.5) % 1
    G += T.lines([(0.08 + 0.2 * u, -0.18, 0.14 + 0.2 * u, -0.18, 1.0)], 0.01) * (1 - u) * 1.2
    return G, H


def isso_e_burrice(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(8)
    for j in range(10):
        a = q.uniform(-math.pi, 0)
        u = rel(t, 0.03 * j, 0.6 + 0.03 * j)
        if 0 < u < 1:
            r = 0.2 + 0.8 * ease_out(u)
            x, y = -0.5 + r * math.cos(a), r * 0.6 * math.sin(a) + 0.5 * u * u
            forma = estrela_pts(5, 0.45) if j % 2 else [(-1, -1), (1, -1), (1, 1), (-1, 1)]
            g, h = icone(T, poe(forma, x, y, 0.04, u * 10), (1 - rel(u, 0.8, 1)) * 1.1, 0.5)
            G, H = G + g, H + h
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.45 + 0.06 * j, 0.65 + 0.06 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            pts = [(x + px * 0.6 * s, -0.15 + (py + 0.45) * 0.6 * s) for px, py in
                   [(-0.12, -0.5), (-0.06, -0.62), (0.06, -0.64), (0.14, -0.56), (0.13, -0.46), (0.03, -0.38), (0.02, -0.28)]]
            G += T.polyline(pts, 0.018) * 1.3
            G += T.gauss(x, -0.15 + 0.17 * 0.6 * s + 0.0, 0.018) * s * 1.4
        g2, h2 = _tontas(T, t, 0.55, 1.0, x, 0.0, 3, 0.1, 0.03)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Flecha

def soco_veloz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(8):
        a0 = 0.02 + 0.04 * j
        k = pulso(t, a0, a0 + 0.1)
        if k > 0:
            dy = -0.2 + 0.06 * (j % 7)
            G += T.tapered([(-0.6, dy, 0.4, dy * 0.3, 1.0)], 0.04) * k * 1.2
            P, _ = _punho(T, 0.38, dy * 0.3, 1.3, 0)
            G += P * 0.8 * k
    g, h = clarao(T, t, 0.15, 0.45, 0.45, 0.0, 1.0)
    G, H = G + g, H + h
    G += estouro(T, t, 0.2, 0.7, 12, 4, 0.45, 0.0, 0.45, 0.012)
    return G * env, H * env


def corrida_na_agua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.75)
    G += T.lines([(-0.95, 0.32, 0.95, 0.32, 1.0)], 0.008) * pulso(t, 0.0, 0.95) * 0.8
    if 0 < u < 1:
        x = -0.85 + 1.7 * u
        G += T.gauss(x, 0.15, 0.05, 0.12) * 1.0
        G += T.tapered([(x - 0.5, 0.15, x - 0.05, 0.15, 1.0)], 0.06) * 0.8
    for j in range(10):
        xj = -0.85 + 0.17 * j
        tj = (xj + 0.85) / 1.7 * 0.75
        w = rel(t, tj, tj + 0.3)
        if 0 < w < 1:
            for m in range(3):
                a = -math.pi / 2 + (m - 1) * 0.6
                g, h = cheio(T, poe(GOTA, xj + 0.12 * w * math.cos(a), 0.3 - 0.15 * math.sin(math.pi * w) + 0.12 * w * math.sin(a) * 0.3, 0.025),
                             (1 - w) * 1.3)
                G, H = G + g, H + h
    return G * env, H * env


def furacao_flecha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    for m in range(5):
        a = t * 30 - m * 0.3
        x, y = 0.75 * math.cos(a), 0.05 + 0.3 * math.sin(a)
        G += T.gauss(x, y, 0.04, 0.07) * k * (1 - m / 5) * 1.3
    cresce = ease_out(rel(t, 0.1, 0.5), 2)
    for m in range(8):
        v = m / 7
        a = t * 25 + m * 0.6
        G += T.arc_band(0.3 + 0.5 * v * cresce, 0.02, a, a + 2.5, 0.35, 0, 0.0, 0.35 - 0.6 * v * cresce, 1.0) * k * 1.0
    for x in (-0.55, 0.0, 0.55):
        g, h = clarao(T, t, 0.4, 0.6, x, 0.05, 0.4)
        G, H = G + g, H + h
    G += particulas(T, t, 0.2, 0.9, 20, 4, 0, 0.1, 0.8, 0.6, 0.011)
    return G * env, H * env


REGISTRO = [
    ("senbonzakura", senbonzakura, GRANDE, "Byakuya · as mil pétalas cortantes", False),
    ("danku", danku, GRANDE, "Byakuya · a parede de luz", False),
    ("byakuya_preparo", byakuya_preparo, MEDIA, "Byakuya · a espada virando pétalas (Preparo, laço)", True),
    ("senkei", senkei, GRANDE, "Byakuya · o círculo de espadas", False),
    ("leque_cortante", leque_cortante, GRANDE, "Kitana · o leque de aço em arco", False),
    ("rajada_de_leque", rajada_de_leque, GRANDE, "Kitana · o redemoinho do leque", False),
    ("kitana_preparo", kitana_preparo, MEDIA, "Kitana · os dois leques cruzados (Preparo, laço)", True),
    ("fatality_do_leque", fatality_do_leque, GRANDE, "Kitana · o leque girando como serra", False),
    ("martelo_de_guerra", martelo_de_guerra, GRANDE, "Shao Kahn · o martelo de guerra descendo", False),
    ("provocacao_de_kahn", provocacao_de_kahn, GRANDE, "Shao Kahn · o elmo de caveira e as ondas", False),
    ("kahn_preparo", kahn_preparo, MEDIA, "Shao Kahn · a lança erguida (Preparo, laço)", True),
    ("lanca_de_kahn", lanca_de_kahn, GRANDE, "Shao Kahn · a lança atravessando", False),
    ("pancada_snorlax", pancada_snorlax, GRANDE, "Snorlax · a barriga e a pancada", False),
    ("descansar", descansar, GRANDE, "Snorlax · o sono e as bolhas de cura", False),
    ("snorlax_preparo", snorlax_preparo, MEDIA, "Snorlax · o corpo quicando (Preparo, laço)", True),
    ("giga_impacto", giga_impacto, GRANDE, "Snorlax · o corpanzil caindo", False),
    ("abraco_esmagador", abraco_esmagador, GRANDE, "Patrick · os braços apertando", False),
    ("debaixo_da_pedra", debaixo_da_pedra, GRANDE, "Patrick · a pedra levantando", False),
    ("patrick_preparo", patrick_preparo, MEDIA, "Patrick · o balão de pensamento vazio (Preparo, laço)", True),
    ("isso_e_burrice", isso_e_burrice, GRANDE, "Patrick · as besteiras e as interrogações", False),
    ("soco_veloz", soco_veloz, GRANDE, "Flecha · os socos supersônicos", False),
    ("corrida_na_agua", corrida_na_agua, GRANDE, "Flecha · correndo sobre a água", False),
    ("furacao_flecha", furacao_flecha, GRANDE, "Flecha · o furacão em volta de todos", False),
]
